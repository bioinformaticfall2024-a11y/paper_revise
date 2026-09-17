import math
for kd in [0.1,1,10,100,1000,10000]:print(kd,-math.log10(kd/1e9))
print('pKd = -log10(Kd_nM / 1e9) = 9 - log10(Kd_nM)')
