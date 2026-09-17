from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np
from rdkit import Chem, rdBase

# Exact 20 SMARTS patterns reported for FGgraphDTA / FG20.
FG_SMARTS = (
    ("CarboxylicAcid", "[CX3](=O)[OX2H1]"),
    ("Ester", "[CX3](=O)[OX2][#6]"),
    ("Amide", "[NX3][CX3](=O)[#6]"),
    ("Anhydride", "[CX3](=O)O[CX3](=O)"),
    ("AcylHalide", "[CX3](=O)[Cl,Br,I,F]"),
    ("Aldehyde", "[CX3H1](=O)[#6]"),
    ("Ketone", "[#6][CX3](=O)[#6]"),
    ("Alcohol", "[#6;!a][OX2H]"),
    ("Phenol", "c[OX2H]"),
    ("Ether", "[OX2]([#6])[#6]"),
    ("Nitrile", "[CX2]#N"),
    ("Nitro", "[$([NX3](=O)=O),$([NX3+](=O)[O-])]"),
    ("Amine_Primary", "[NX3;H2][#6]"),
    ("Amine_Secondary", "[NX3;H1]([#6])[#6]"),
    ("Amine_Tertiary", "[NX3]([#6])([#6])[#6]"),
    ("Thiol", "[#16X2H]"),
    ("Thioether", "[#16X2]([#6])[#6]"),
    ("Sulfoxide", "[#16X3](=O)([#6])[#6]"),
    ("Sulfone", "[#16X4](=O)(=O)([#6])[#6]"),
    ("Aryl", "c1ccccc1"),
)

# Additional motifs mentioned by Reviewer 3 Comment 8.
# These are diagnostic only; they are NOT added to FG20.
DIAGNOSTIC_SMARTS = (
    ("Aromatic_N_heteroatom", "[n;R]"),
    ("Pyridine_like_N", "[nH0;R]"),
    ("Sulfonamide", "[SX4](=O)(=O)[NX3]"),
    ("Aryl_F", "[c][F]"),
    ("Aryl_Cl", "[c][Cl]"),
    ("Trifluoromethyl", "[CX4](F)(F)F"),
    ("Urea", "[NX3][CX3](=O)[NX3]"),
    ("Morpholine_ring", "[O;R]1[C;R][C;R][N;R][C;R][C;R]1"),
    ("Acrylamide_like_warhead", "[CX3]=[CX3][CX3](=O)[NX3]"),
    ("Hydroxamate_like", "[CX3](=O)[NX3][OX2H,OX1-]"),
)

SIX_DAVIS = {
    "5291": "Imatinib",
    "123631": "Gefitinib",
    "176870": "Erlotinib",
    "216239": "Sorafenib",
    "3062316": "Dasatinib",
    "5329102": "Sunitinib",
}


def compile_patterns(spec):
    compiled = []
    for name, smarts in spec:
        query = Chem.MolFromSmarts(smarts)
        if query is None:
            raise RuntimeError(f"Failed to compile SMARTS: {name}: {smarts}")
        compiled.append((name, smarts, query))
    return compiled


FG = compile_patterns(FG_SMARTS)
DIAG = compile_patterns(DIAGNOSTIC_SMARTS)


def load_ligands(path: Path):
    """Load either a JSON {id: SMILES} dictionary or whitespace-delimited id SMILES text."""
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Empty ligand file: {path}")

    if text[0] in "{[":
        obj = json.loads(text)
        if isinstance(obj, dict):
            return [(str(k), str(v)) for k, v in obj.items()]
        if isinstance(obj, list):
            rows = []
            for i, item in enumerate(obj):
                if isinstance(item, dict):
                    entity_id = item.get("id", item.get("drug_id", item.get("name", i)))
                    smiles = item.get("smiles", item.get("SMILES"))
                    if smiles is None:
                        raise ValueError("JSON list entries must contain a smiles/SMILES field")
                    rows.append((str(entity_id), str(smiles)))
                else:
                    rows.append((str(i), str(item)))
            return rows
        raise ValueError("Unsupported JSON ligand format")

    rows = []
    for line_no, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Expected 'id SMILES' on line {line_no}: {line}")
        rows.append((parts[0], parts[1]))
    return rows


def bits_for_mol(mol, compiled):
    return [int(mol.HasSubstructMatch(query)) for _, _, query in compiled]


def write_csv(path: Path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def audit_dataset(label: str, records, outdir: Path):
    fg_names = [name for name, _ in FG_SMARTS]
    diag_names = [name for name, _ in DIAGNOSTIC_SMARTS]

    per_ligand = []
    invalid = []
    fg_rows = []
    diag_rows = []

    for entity_id, smiles in records:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            invalid.append({"id": entity_id, "smiles": smiles})
            continue
        fg_bits = bits_for_mol(mol, FG)
        diag_bits = bits_for_mol(mol, DIAG)
        fg_rows.append(fg_bits)
        diag_rows.append(diag_bits)

        row = {
            "id": entity_id,
            "smiles": smiles,
            "active_fg20_count": int(sum(fg_bits)),
        }
        row.update({name: bit for name, bit in zip(fg_names, fg_bits)})
        row.update({f"diag_{name}": bit for name, bit in zip(diag_names, diag_bits)})
        per_ligand.append(row)

    if not per_ligand:
        raise RuntimeError(f"No valid molecules in {label}")

    fg_matrix = np.asarray(fg_rows, dtype=int)
    diag_matrix = np.asarray(diag_rows, dtype=int)
    n = fg_matrix.shape[0]

    coverage = []
    for j, (name, smarts) in enumerate(FG_SMARTS):
        count = int(fg_matrix[:, j].sum())
        coverage.append({
            "functional_group": name,
            "smarts": smarts,
            "count": count,
            "percent_of_valid_ligands": 100.0 * count / n,
        })

    diagnostics = []
    for j, (name, smarts) in enumerate(DIAGNOSTIC_SMARTS):
        count = int(diag_matrix[:, j].sum())
        diagnostics.append({
            "diagnostic_motif": name,
            "smarts": smarts,
            "count": count,
            "percent_of_valid_ligands": 100.0 * count / n,
        })

    active_counts = fg_matrix.sum(axis=1)
    dist = Counter(map(int, active_counts))
    ever_active = int((fg_matrix.sum(axis=0) > 0).sum())

    summary = {
        "dataset": label,
        "rdkit_version": rdBase.rdkitVersion,
        "n_input": len(records),
        "n_valid": n,
        "n_invalid": len(invalid),
        "ever_active_patterns": ever_active,
        "vocabulary_usage_percent": 100.0 * ever_active / len(FG_SMARTS),
        "never_active_patterns": [
            fg_names[j] for j in range(len(fg_names)) if fg_matrix[:, j].sum() == 0
        ],
        "zero_match_ligands": int((active_counts == 0).sum()),
        "mean_active_patterns_per_ligand": float(active_counts.mean()),
        "median_active_patterns_per_ligand": float(np.median(active_counts)),
        "q1_active_patterns_per_ligand": float(np.quantile(active_counts, 0.25)),
        "q3_active_patterns_per_ligand": float(np.quantile(active_counts, 0.75)),
        "min_active_patterns_per_ligand": int(active_counts.min()),
        "max_active_patterns_per_ligand": int(active_counts.max()),
        "unique_fg20_signatures": int(len({tuple(row) for row in fg_matrix.tolist()})),
        "active_pattern_count_distribution": {str(k): int(v) for k, v in sorted(dist.items())},
    }

    prefix = label.lower().replace(" ", "_")
    write_csv(outdir / f"{prefix}_fg20_coverage.csv", coverage, list(coverage[0].keys()))
    write_csv(outdir / f"{prefix}_diagnostic_motifs.csv", diagnostics, list(diagnostics[0].keys()))
    write_csv(outdir / f"{prefix}_per_ligand.csv", per_ligand, list(per_ligand[0].keys()))
    if invalid:
        write_csv(outdir / f"{prefix}_invalid_smiles.csv", invalid, ["id", "smiles"])

    return summary


def reproduce_six_compound_panel(davis_records, outdir: Path):
    davis = dict(davis_records)
    fg_names = [name for name, _ in FG_SMARTS]
    rows = []
    union = np.zeros(len(FG_SMARTS), dtype=int)

    missing = [cid for cid in SIX_DAVIS if cid not in davis]
    if missing:
        return {"status": "not_run", "reason": f"DAVIS IDs not found: {missing}"}

    for cid, compound in SIX_DAVIS.items():
        mol = Chem.MolFromSmiles(davis[cid])
        if mol is None:
            raise RuntimeError(f"Invalid DAVIS SMILES for {compound} ({cid})")
        bits = np.asarray(bits_for_mol(mol, FG), dtype=int)
        union |= bits
        rows.append({
            "compound": compound,
            "davis_id": cid,
            "active_count": int(bits.sum()),
            "active_groups": "; ".join(name for name, bit in zip(fg_names, bits) if bit),
        })

    write_csv(outdir / "reviewer_six_compound_panel.csv", rows, list(rows[0].keys()))
    return {
        "status": "ok",
        "mean_active_patterns": float(np.mean([row["active_count"] for row in rows])),
        "union_patterns": int(union.sum()),
        "vocabulary_usage_percent": 100.0 * int(union.sum()) / len(FG_SMARTS),
        "never_active_patterns": int((union == 0).sum()),
        "active_union": [name for name, bit in zip(fg_names, union) if bit],
        "compounds": rows,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Dataset-wide audit of the 20 ligand-side FGgraphDTA SMARTS patterns."
    )
    parser.add_argument("--davis", type=Path, required=True, help="DAVIS ligand file")
    parser.add_argument("--kiba", type=Path, required=True, help="KIBA ligand file")
    parser.add_argument("--outdir", type=Path, default=Path("results"))
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    davis_records = load_ligands(args.davis)
    kiba_records = load_ligands(args.kiba)

    report = {
        "rdkit_version": rdBase.rdkitVersion,
        "fg20_pattern_count": len(FG_SMARTS),
        "reviewer_six_compound_panel": reproduce_six_compound_panel(davis_records, args.outdir),
        "datasets": {
            "DAVIS": audit_dataset("DAVIS", davis_records, args.outdir),
            "KIBA": audit_dataset("KIBA", kiba_records, args.outdir),
        },
    }

    (args.outdir / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
