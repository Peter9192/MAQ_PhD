#plot_WRFtimeseries.py

"""plot time series of WRF output; 
    NOTE: we assume variables to have dimension [time,y,x] or [time,z,y,x]
    If this is not the case, adapt the dimensions where variable is read

Author: Ingrid Super
Last revisions: 2-6-2016"""

import netCDF4 as nc 
import numpy as np
import matplotlib.pyplot as plt
from maptools import *
from numpy import ma
import datetime as dtm
from matplotlib.colors import LogNorm

##############################################################################################
"""specify the following:"""
"""directory of the WRF output and grid resolution [m] for each domain:"""
wrfout_path='/Storage/WRF/super004/WRF/run_paper2/output'
"""x- and y-location of the location you want to plot, the WRF domain, WRF vertical level and variable of interest"""
xloc=22
yloc=28
domain=3    #1 being outer domain
lev=0       #0 being surface level
var='U10'
##############################################################################################

"""read in variable of interest"""
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

"""make plot and lay-out"""
xvar=np.arange(1,len(timers)+1)
plot(xvar,vars,label='time series',color='k',linestyle='-',linewidth=2)
legend(loc='upper right')
xlabel('label')     #please specify
ylabel('label')     #please specify
title('title')      #please specify
skp=len(timers)/4
ticks=[xvar[0],xvar[skp],xvar[2*skp],xvar[3*skp],xvar[4*skp]]
"""the following statement allows you to change the labels on the x-axis and can be adapted to your specific needs (e.g. including year)"""
labels=[timers[0].strftime("%d. %B"),timers[skp].strftime("%d. %B"),timers[2*skp].strftime("%d. %B"),timers[3*skp].strftime("%d. %B"),timers[4*skp].strftime("%d. %B")]
plt.xticks(ticks,labels)
plt.show()
