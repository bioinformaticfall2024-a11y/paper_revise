import json
def ge(d,o=128):
 return (d*d+d)+(d*2*d+2*d)+(2*d*4*d+4*d)+(4*d*1024+1024)+(1024*o+o)
def dense(i,o):return i*o+o
def head(s,e=128):return dense(s*e,1024)+dense(1024,512)+dense(512,1)
base=ge(78)+ge(54)+head(2);fg=ge(98)+ge(74)+head(2);pv=ge(78)+ge(54)+dense(2048,128)+3*dense(128,128)+head(3)
def conv(i,o):return i*o*9+o
ae=conv(3,16)+conv(16,32)+conv(32,64)+conv(64,128)+conv(128,256)+dense(256*16*16,128)+dense(128,256*16*16)+conv(256,128)+conv(128,64)+conv(64,32)+conv(32,16)+conv(16,2)
full=44549160;fc=2048*1000+1000;headless=full-fc
x={'base_graph':base,'FGgraphDTA':fg,'FG_minus_base':fg-base,'PV_predictor':pv,'autoencoder':ae,'ResNet101_full':full,'ResNet101_headless':headless,'PV_plus_AE_plus_headless_ResNet':pv+ae+headless}
print(json.dumps(x,indent=2))
