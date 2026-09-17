from pathlib import Path
import json
vals={'graph_only':(0.2018,0.9034),'graph_plus_resnet':(0.2216,0.8648),'plus_ae':(0.2148,0.8704),'full_infonce':(0.2070,0.8750)}
base=vals['graph_only'][0]
summary={k:{'MSE':m,'CI':ci,'MSE_change_vs_graph_only_pct':(m/base-1)*100,'CI_change_vs_graph_only':ci-vals['graph_only'][1]} for k,(m,ci) in vals.items()}
Path(__file__).with_name('ablation_arithmetic.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
