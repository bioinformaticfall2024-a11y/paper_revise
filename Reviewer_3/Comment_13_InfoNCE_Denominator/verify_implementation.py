"""Static verifier for recovered PVgraphDTA InfoNCE code. Usage: python verify_implementation.py path/to/pvgraphdta.py"""
import argparse,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('source');a=ap.parse_args();s=Path(a.source).read_text(encoding='utf-8')
checks={'cross_modal_logits':'logits = (a @ b.T) / self.temperature' in s,'diagonal_positive':'labels = torch.arange(a.size(0), device=a.device)' in s,'symmetric':'F.cross_entropy(logits, labels) + F.cross_entropy(logits.T, labels)' in s,'three_pairs':all(x in s for x in ['self._pair(ligand, protein)','self._pair(ligand, image)','self._pair(protein, image)'])}
print(json.dumps(checks,indent=2))
