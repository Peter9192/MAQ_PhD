#plot_daily_cycle.py

"""plot the average daily cycle of your WRF output 
    NOTE: we assume variables to have dimension [time,y,x] or [time,z,y,x]
    If this is not the case, adapt the dimensions where variable is read

Author: Ingrid Super
Last revisions: 3-6-2016"""

import netCDF4 as nc 
import numpy as np
import matplotlib.pyplot as plt
from maptools import *
from numpy import ma
import datetime as dtm
from scipy import stats

##############################################################################################
"""specify the following:"""
"""directory of the WRF output:"""
wrfout_path='/Storage/WRF/super004/WRF/run_paper2/output'
"""x- and y-location of the location you want to plot, the WRF domain, WRF vertical level and variable of interest"""
xloc=22
yloc=28
domain=3    #1 being outer domain
lev=0       #0 being surface level
var='U10'
##############################################################################################

"""read in variable of interest, in this case from WRF (could also be observations or both)"""
vars=[]
timers=[]
wrfout_files=[os.path.join(wrfout_path,filename) for filename in os.listdir(wrfout_path) if filename.startswith('wrfout_d%02d'%domain)]
for each_file in wrfout_files:
    mf=nc.Dataset(each_file)
    dum=mf.variables[var][:]
    wrftime=mf.variables['Times'][:]
    for j in range(len(wrftime)):
        year=int(''.join(wrftime[j][0:4]))
        month=int(''.join(wrftime[j][5:7]))
        day=int(''.join(wrftime[j][8:10]))
        hour=int(''.join(wrftime[j][11:13]))
        dat=dtm.datetime(year,month,day,hour,0)
        timers.append(dat)
    if len(dum.shape)==3:
        dum2=dum[:,yloc,xloc]
    elif len(dum.shape)==4:
        dum2=dum[:,lev,yloc,xloc]
    vars.extend(dum2)

"""cluster the data based on hour of the day; you can add additional selection criteria in the if-statement below:
E.g. the example shows how to show differences between winter and summer; this can also be used to compare simulations or model vs. observations"""
dcy1=[]
dcy2=[]
for i in range(24):
   dum1=[]
   dum2=[]
   for j in range(len(timers)):
      if timers[j].hour==i and timers[j].month>4 and timers[j].month<10:
        dum1.append(vars[j])
      elif timers[j].hour==i and timers[j].month>=10 and timers[j].month<=4:
        dum2.append(vars[j])
   dcy1.append(dum1)
   dcy2.append(dum2)
dcy1=np.array(dcy1)
dcy2=np.array(dcy2)

"""the following routines give you a confidence interval for your daily cycles"""
def effectiveSampleSize(data, stepSize = 1) :
   """ Effective sample size, as computed by BEAST Tracer."""
   a = 1.0*np.array(data)
   n = len(a)
   assert len(a) > 1,"no stats for short sequences"
   maxLag = min(n//3, 1000)
   gammaStat = [0,]*maxLag
   varStat = 0.0;
   if type(a) != np.ndarray:
      a = np.array(a)
   normalizedData = a - a[~np.isnan(a)].mean()
   for lag in range(maxLag):
      v1 = normalizedData[:n-lag]
      v2 = normalizedData[lag:]
      v = v1 * v2
      gammaStat[lag] = np.nansum(v) / len(v)
      if lag == 0 :
         varStat = gammaStat[0]
      elif lag % 2 == 0 :
         s = gammaStat[lag-1] + gammaStat[lag]
         if s > 0 :
            varStat += 2.0*s
         else :
            break  
   # auto correlation time
   act = stepSize * varStat / gammaStat[0]
   # effective sample size
   ess = (stepSize * n) / act
   
   return act

def mean_confidence_interval(data, confidence=0.95, act=0):
    """calculate mean and 95% confidence interval"""
    if data.ndim == 1:
        mask=~np.isnan(data)
        b=data[mask]
        a = 1.0*np.array(b)
        n = len(a)/act
        m, se = np.nanmean(a), stats.sem(a)
        h = se * stats.t._ppf((1+confidence)/2., n-1)
        return m, m-h, m+h
    if data.ndim == 2:
        a = 1.0*np.array(data)
        n = len(a)
        m, se = np.nanmean(a,axis=0), stats.sem(a,axis=0)
        h = se * stats.t._ppf((1+confidence)/2., n-1)
        return m, h  

mn1=24*[None]
lowb1=24*[None]
upb1=24*[None]
mn2=24*[None]
lowb2=24*[None]
upb2=24*[None]
for i in range(24):
    act=effectiveSampleSize(data=np.array(dcy1[i]),stepSize=1)
    output=mean_confidence_interval(data=np.array(dcy1[i]),confidence=0.95,act=1)
    mn1[i]=output[0]
    lowb1[i]=output[1]
    upb1[i]=output[2]
    act=effectiveSampleSize(data=np.array(dcy2[i]),stepSize=1)
    output=mean_confidence_interval(data=np.array(dcy2[i]),confidence=0.95,act=1)
    mn2[i]=output[0]
    lowb2[i]=output[1]
    upb2[i]=output[2]

"""make plot and lay-out"""
fig=plt.figure(1,figsize=(12,8))
x=arange(24)
fill_between(x,lowb1,upb1,color='silver')
fill_between(x,lowb2,upb2,color='silver')
plot(x,mn1,color='k',label='summer')
plot(x,mn2,color='k',linestyle='--',label='winter')
legend(loc='upper right')
xlabel('label')     #please specify
ylabel('label')     #please specify
title('title')      #please specify
ticks=[x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16],x[17],x[18],x[19],x[20],x[21],x[22]]
labels=['','','3','','','6','','','9','','','12','','','15','','','18','','','21','','']
plt.xticks(ticks,labels)
plt.grid(True)
plt.show()

