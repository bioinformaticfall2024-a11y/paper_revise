"""Reference loss for graph-only + ligand/protein InfoNCE reviewer control. This defines a control; it is not an observed result."""
import torch
import torch.nn.functional as F
def symmetric_info_nce(a,b,tau=0.07):
 a=F.normalize(a,dim=-1);b=F.normalize(b,dim=-1);logits=(a@b.T)/tau;labels=torch.arange(a.size(0),device=a.device)
 return F.cross_entropy(logits,labels)+F.cross_entropy(logits.T,labels)
def total_loss(pred,y,z_ligand,z_protein,alpha=0.5,tau=0.07):
 mse=F.mse_loss(pred.view_as(y),y);nce=symmetric_info_nce(z_ligand,z_protein,tau);return mse+alpha*nce,mse.detach(),nce.detach()
