import sys
import numpy as np
from scipy import stats
from scipy.stats import norm
import matplotlib.pyplot as plt


# http://web.mit.edu/neboat/Public/6.042/randomwalks.pdf
# https://www.youtube.com/watch?v=9FVlkg2bLlI

x = 5
y = -5
H = 1
T = 0
rounds = 100000
flips = {}
total_tries = 0
data = []


if(len(sys.argv) >= 3):
  x = int(sys.argv[1])
  y = int(sys.argv[2])

if(len(sys.argv) >= 4):
  rounds = int(sys.argv[3])


print("[Calculus] Expected number of steps before hitting boundary (x*y): " + str(abs(x)* abs(y)))
print("[Calculus] Expected path with highest probability (x*y)/3: " + str(np.ceil(float(abs(x)* abs(y))/3)) + " +/-2")
print("#######")

for i in range(0,rounds):
  marker = 0
  tries = 0
  s = ""
  while True:
    toss = np.random.randint(2,size=1)[0]
    tries += 1
    if(toss == H):
      s += "H"
      marker += 1
    else:
      s += "T"
      marker -= 1


    if(marker == x) or (marker == y):
      #if(tries == 12):
      #  print(s)
      data.append(tries)
      if(tries in flips.keys()):
        flips[tries] += 1
      else:
        flips[tries] = 1
      break
  
  total_tries += tries

bv = 0
bk = 0
exp_value = 0
print("flips  success_times  probability")
 
for k in sorted(flips):
  v = flips[k]
  if(v >= bv):
    bv = v
    bk = k
  per = round(((float(v) / rounds)),5)
  exp_value += k*per
  print(str(k)+" "+str(v)+" "+str(per)) 

print("########")
print("[Simulation] Expected number of steps before hitting boundary (x*y): " + str(exp_value))
print("[Simulation] Expected path with highest probability (x*y)/3: " + str(bk))


bins = len(flips.keys())
param= stats.lognorm.fit(data,loc=0)

print("[Simulation] Fitting log-normal distribution parameters: ")
print(param)

x=np.linspace(0,max(flips.keys()),200)
pdf_fitted = stats.lognorm.pdf(x, param[0], loc=param[1], scale=param[2]) # fitted distribution
plt.plot(x,pdf_fitted,'r-')
plt.hist(data,bins=bins/2,normed=True,alpha=.3)
plt.show()
