"""Standalone audit of the protein-side FG20 encoding. Requires rdkit and numpy."""
from collections import defaultdict, Counter
from math import log2
from pathlib import Path
import csv,json
import numpy as np
from rdkit import Chem,rdBase
FG=(('CarboxylicAcid','[CX3](=O)[OX2H1]'),('Ester','[CX3](=O)[OX2][#6]'),('Amide','[NX3][CX3](=O)[#6]'),('Anhydride','[CX3](=O)O[CX3](=O)'),('AcylHalide','[CX3](=O)[Cl,Br,I,F]'),('Aldehyde','[CX3H1](=O)[#6]'),('Ketone','[#6][CX3](=O)[#6]'),('Alcohol','[#6;!a][OX2H]'),('Phenol','c[OX2H]'),('Ether','[OX2]([#6])[#6]'),('Nitrile','[CX2]#N'),('Nitro','[$([NX3](=O)=O),$([NX3+](=O)[O-])]'),('Amine_Primary','[NX3;H2][#6]'),('Amine_Secondary','[NX3;H1]([#6])[#6]'),('Amine_Tertiary','[NX3]([#6])([#6])[#6]'),('Thiol','[#16X2H]'),('Thioether','[#16X2]([#6])[#6]'),('Sulfoxide','[#16X3](=O)([#6])[#6]'),('Sulfone','[#16X4](=O)(=O)([#6])[#6]'),('Aryl','c1ccccc1'))
N=tuple(x[0] for x in FG); P=[(n,Chem.MolFromSmarts(s)) for n,s in FG]
AA={'A':'NCC(C)C(=O)O','R':'NCC(CCCNC(N)=N)C(=O)O','N':'NCC(C(=O)N)C(=O)O','D':'NCC(C(=O)O)C(=O)O','C':'NCC(S)C(=O)O','E':'NCC(CCC(=O)O)C(=O)O','Q':'NCC(CCC(=O)N)C(=O)O','G':'NCC(=O)O','H':'NCC(Cc1c[nH]cn1)C(=O)O','I':'NCC(C(C)CC)C(=O)O','L':'NCC(CC(C)C)C(=O)O','K':'NCC(CCCCN)C(=O)O','M':'NCC(CCSC)C(=O)O','F':'NCC(Cc1ccccc1)C(=O)O','P':'N1CCC(C(=O)O)C1','S':'NCC(CO)C(=O)O','T':'NCC(C(O)C)C(=O)O','W':'NCC(Cc1c2ccccc2[nH]c1)C(=O)O','Y':'NCC(Cc1ccc(O)cc1)C(=O)O','V':'NCC(C(C)C)C(=O)O'}
def groups(m):
 g={n for n,p in P if m.HasSubstructMatch(p)}
 if 'Ester' in g:g.discard('Ether')
 if 'CarboxylicAcid' in g:g.discard('Alcohol')
 if 'Phenol' in g:g.discard('Alcohol')
 return g
rows=[]
for aa,smi in AA.items():
 g=groups(Chem.MolFromSmiles(smi));v=np.array([int(n in g) for n in N]);rows.append((aa,smi,v))
mat=np.stack([v for _,_,v in rows]);zero=[N[i] for i in range(20) if mat[:,i].sum()==0];clusters=defaultdict(list)
for aa,_,v in rows:clusters[tuple(v.tolist())].append(aa)
counts=Counter(tuple(v.tolist()) for _,_,v in rows);ent=-sum((c/20)*log2(c/20) for c in counts.values());out=Path(__file__).resolve().parent
with (out/'protein_fg_vectors.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['Residue','SMILES',*N,'ActiveCount']);[w.writerow([aa,smi,*v.tolist(),int(v.sum())]) for aa,smi,v in rows]
with (out/'collision_groups.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['Residues','GroupSize','ActiveFGs']);[w.writerow([''.join(aas),len(aas),'; '.join(N[i] for i,x in enumerate(sig) if x)]) for sig,aas in sorted(clusters.items(),key=lambda x:(-len(x[1]),x[1]))]
summary={'rdkit_version':rdBase.rdkitVersion,'zero_columns_count':len(zero),'zero_columns':zero,'distinct_vectors':len(clusters),'max_categorical_capacity_bits_log2_distinct':log2(len(clusters)),'empirical_shannon_entropy_uniform_residues_bits':ent,'collision_groups':[x for x in clusters.values() if len(x)>1]}
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))
