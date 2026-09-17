"""Reproduce historical SMARTS overlaps and corrected precedence on simple molecules."""
from pathlib import Path
import csv
from rdkit import Chem,rdBase
FG=(('CarboxylicAcid','[CX3](=O)[OX2H1]'),('Ester','[CX3](=O)[OX2][#6]'),('Amide','[NX3][CX3](=O)[#6]'),('Anhydride','[CX3](=O)O[CX3](=O)'),('AcylHalide','[CX3](=O)[Cl,Br,I,F]'),('Aldehyde','[CX3H1](=O)[#6]'),('Ketone','[#6][CX3](=O)[#6]'),('Alcohol','[#6;!a][OX2H]'),('Phenol','c[OX2H]'),('Ether','[OX2]([#6])[#6]'),('Nitrile','[CX2]#N'),('Nitro','[$([NX3](=O)=O),$([NX3+](=O)[O-])]'),('Amine_Primary','[NX3;H2][#6]'),('Amine_Secondary','[NX3;H1]([#6])[#6]'),('Amine_Tertiary','[NX3]([#6])([#6])[#6]'),('Thiol','[#16X2H]'),('Thioether','[#16X2]([#6])[#6]'),('Sulfoxide','[#16X3](=O)([#6])[#6]'),('Sulfone','[#16X4](=O)(=O)([#6])[#6]'),('Aryl','c1ccccc1'))
N=[x[0] for x in FG];P=[Chem.MolFromSmarts(x[1]) for x in FG]
def atomsets(m):
 d={n:set() for n in N}
 for n,p in zip(N,P):
  for match in m.GetSubstructMatches(p):d[n].update(match)
 return d
def active(s,clean=False):
 s={k:set(v) for k,v in s.items()}
 if clean:
  for sp,br in [('CarboxylicAcid','Alcohol'),('Ester','Ether'),('Phenol','Alcohol')]:s[br]-=s[sp]
 return [n for n in N if s[n]]
examples={'acetic_acid':'CC(=O)O','aspirin':'CC(=O)Oc1ccccc1C(=O)O','ethyl_acetate':'CCOC(=O)C'};rows=[]
for name,smi in examples.items():
 s=atomsets(Chem.MolFromSmiles(smi));rows += [[name,smi,'historical','; '.join(active(s))],[name,smi,'corrected','; '.join(active(s,True))]]
out=Path(__file__).resolve().parent
with (out/'example_matches.csv').open('w',newline='',encoding='utf-8') as f:w=csv.writer(f);w.writerow(['Molecule','SMILES','Policy','ActiveGroups']);w.writerows(rows)
print('RDKit',rdBase.rdkitVersion);[print(r) for r in rows]
