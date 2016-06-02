#plot_WRFmaps.py

"""plot gridded WRF output on a Basemap; 
    NOTE: we assume variables to have dimension [time,y,x] or [time,z,y,x]
    If this is not the case, adapt the dimensions where variable is read

Author: Ingrid Super
Last revisions: 2-6-2016"""

import netCDF4 as nc 
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from maptools import *
from numpy import ma
from matplotlib.colors import LogNorm

##############################################################################################
"""specify the following:"""
"""directory of the WRF output and grid resolution [m] for each domain:"""
wrfout_path='/Storage/WRF/super004/WRF/run_paper2/output'
dx=[48000,12000,4000,1000]
"""year, month, day and hour you want to plot, the WRF domain, WRF vertical level and variable of interest"""
yr=2014
mnt=10
dy=4
hr=15       #in UTC
domain=3    #1 being outer domain
lev=0       #0 being surface level
var='U10'
##############################################################################################

"""read in other grid characteristics"""
wrfout_file=[os.path.join(wrfout_path,filename) for filename in os.listdir(wrfout_path) if filename.startswith('wrfout_d%02d_%04d-%02d-%02d'%(domain,yr,mnt,dy))]
mf=nc.Dataset(wrfout_file[0])
we=mf.variables['XLAT'][:].shape[2]
sn=mf.variables['XLAT'][:].shape[1]
if we%2==0 and sn%2==0:
    lon_0=(mf.variables['XLONG_U'][0,sn/2,we/2]+mf.variables['XLONG_U'][0,sn/2-1,we/2])/2.
    lat_0=(mf.variables['XLAT_V'][0,sn/2,we/2]+mf.variables['XLAT_V'][0,sn/2,we/2-1])/2.
elif we%2!=0 and sn%2!=0:
    lat_0=mf.variables['XLAT'][0,(sn-1)/2,(we-1)/2]
    lon_0=mf.variables['XLONG'][0,(sn-1)/2,(we-1)/2]
elif we%2==0 and sn%2!=0:
    lat_0=(mf.variables['XLAT'][0,(sn-1)/2,we/2]+mf.variables['XLAT'][0,(sn-1)/2,we/2-1])/2.
    lon_0=mf.variables['XLONG_U'][0,(sn-1)/2,we/2]
elif we%2!=0 and sn%2==0:
    lat_0=mf.variables['XLAT_V'][0,sn/2,(we-1)/2]
    lon_0=(mf.variables['XLONG'][0,sn/2,(we-1)/2]+mf.variables['XLONG'][0,sn/2-1,(we-1)/2])/2.
    
"""read in variable of interest"""
dum=mf.variables[var][:]
if len(dum.shape)==3:
    vars=dum[hr,:]
elif len(dum.shape)==4:
    vars=dum[hr,lev,:]

"""create Basemap instance"""
if (dx[domain]*we) < 250000:
    res='i'
    thres=100.
else:
    res='l'
    thres=1000.
m=Basemap(width=(dx[domain-1]*we)-1,height=(dx[domain-1]*sn)-1,resolution=res,area_thresh=thres,projection='lcc',\
            lat_0=lat_0,lon_0=lon_0)

"""plot map and draw rivers, boundaries etc."""
im=m.imshow(vars)
m.drawcoastlines()
m.drawcountries()
m.drawrivers()
#m.drawparallels(np.arange(np.floor(m.latmin/2.)*2, np.ceil(m.latmax),2),linewidth=0,labels=[1,0,0,0], zorder=500)
#m.drawmeridians(np.arange(np.floor(m.lonmin/2.)*2, np.ceil(m.lonmax),2),linewidth=0,labels=[0,0,0,1], zorder=500)
c=colorbar()
#c.set_label('unit') #please specify a unit
#plt.title('Title')  #please specify a title

"""OPTIONAL: plot locations of measurement sites (or other)"""
# lat=[51.97,53.40,51.786666,51.964381]
# lon=[4.93,6.35,4.450536,4.394650]
# for i in range(len(lat)):
    # xCEN, yCEN = m(lon[i],lat[i])
    # m.plot(xCEN,yCEN,'r*',markersize=10, zorder=600)    

plt.show()


