#!/usr/bin/env python
# coding: utf-8

# ## Well Log Data Exploration 
# 
# Among the 41 wells discussed before, there are a couple of them with cores in the intervals of interest. Moreover, some have petrophysical measurements of those cores. We will work with the _CAPELLE-01_ well. 
# 
# Well logs in LAS format (and other formats) can be downloaded from [NLOG data center](https://www.nlog.nl/datacenter/brh-overview). Search by CAPELLE-01, go to tab _LogsLIS/LAS_ and download the _2571_cap01_1985_comp.las_ file. This file is a composite log of all available wireline logs.
# 
# 
# In this notebook we will:
# - Load and read LAS files using lasio 
# - Load and read CSV files with pandas 
# - Plot geophysical well logs using matplotlib 

# ## Set up
# Make sure you have installed [lasio](https://lasio.readthedocs.io/en/latest/) and pandas packages to be able to read well logs in standard LAS file format. 

# In[1]:


import lasio , os  
import numpy as np    
import pandas as pd   

import matplotlib as mpl  
import matplotlib.pyplot as plt

#< Use this for static figures
get_ipython().run_line_magic('matplotlib', 'inline')
# < Use this for interactive figures (zoom in/out, save, etc.)
#%matplotlib widget  


# Well logs contain values that indicate that there is no measurement taken at those depths. The _valtonan_ function let us prepare data before processing and visualizing by converting null values to NaN. Whereas _remove_last_ function helps to make clean graphs of the curves.

# In[2]:


# This function converts absent values to NaN
# E.g. null = -999.25 > Type <print(lasfile.well)> to find out this value

def valtonan(inp, val=-999.25):
    """Convert all 'val' to NaN's."""
    inp[inp==val] = np.nan
    return inp

#This function makes for cleaner axis plotting
def remove_last(ax, which='upper'):
    """Remove <which> from x-axis of <ax>.
    which: 'upper', 'lower', 'both'
    """
    nbins = len(ax.get_xticklabels())
    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=nbins, prune=which))


# ## Loading LAS files
# One simple way of reading a LAS file is by using _lasio_ library. 
# 
# To look at the header call the _.well_ function. Note that measurements start at the bottom of the well. 

# In[3]:


# Read a single file  
lasfile = lasio.read(os.path.join("../data/raw/logs/2571_cap01_1985_comp.las"))


# In[4]:


print(lasfile.well)


# Drilling parameters can be also displayed. They are useful to integrate well log data with seismic and geologic models.

# In[5]:


print(lasfile.params)


# ## Well Log Curves
# Let's display a list of the curves in this LAS file. Note that curve mnemonics do not have a description. If you are unfamiliar with those mnemonic, check [CurveNam.es](http://curvenam.es/), which is a useful fuzzy lookup of wireline log mnemonics. Or check directly on [SLB website](https://www.apps.slb.com/cmd/index.aspx) and 
# [Halliburton website](https://www.halliburton.com/en/resources/lwd-curve-mnemonics).
# 
# PS. Here, the curve mnemonic _DRHO_ stands for for Density Correction, which may be useful for log quality control but not neccesarily for log interpretation. The DRHO curve is the difference between the short- and long-spaced density measurements. It is used as a quality indicator of the bulk density data. DRHO values larger than 0.1 g/cm3 suggest unreliable density data. This can be correlated with high caliper readings due to probable poor contact with the wall borehole.
# 

# In[6]:


print(lasfile.curves)


# In[7]:


for curve in lasfile.curves:
    print(curve.mnemonic + ": " + str(curve.data))


# ## Well log visualization
# 
# This is a simple way of inspecting the curves we just read from that LAS file. You can identify the intervals where the tool did not measure or where there are anomalous measurements to filter before rpocessing.
# 
# Note that to plot the sonic transit time (DT) we have converted its units from _us/ft_ to _m/s_.
# 
# This is an interactive plot. Use the controls on the upper left corner to zoom in and out.

# In[8]:


# These are the variable names, i.e. curve mnemonic
lasfile.keys() 


# In[9]:


# --> To-DO
# Looking for invalid values
# valtonan(lasfile, val=-999.25)


# In[10]:


# Plotting curves along well total depth

f1, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, sharey=True, figsize=(18,16))
f1.subplots_adjust(wspace=0.02)
plt.gca().invert_yaxis()

# So that y-tick labels appear on left and right
plt.tick_params(labelright=True)

# Change tick-label globally
mpl.rcParams['xtick.labelsize'] = 6

# Track 1: Gamma Ray
ax1.plot(lasfile['GR'], lasfile['DEPT'],'c', linewidth=0.5)
ax1.xaxis.tick_top()
ax1.xaxis.set_label_position('top') 
ax1.set_xlabel('GR (API)')
ax1.set_ylabel('DEPTH (m)')
ax1.grid(True, c="g", alpha=0.3)

plt.setp(ax1.get_xticklabels()[1::2], visible=False)  # Hide every second tick-label
remove_last(ax1)  # remove last value of x-ticks, see function defined in first cell

# Track 2: Sonic (velocities)
ax2.plot((lasfile['DT']/0.3048), lasfile['DEPT'], 'r',label='DTCO',linewidth=0.5)
ax2.xaxis.tick_top()
ax2.xaxis.set_label_position('top') 
ax2.set_xlabel('DT (m/s)')
ax2.grid(True, c="g", alpha=0.3)
remove_last(ax2)  

# Track 3: RHOB (Bulk Density)
ax3.plot(lasfile['RHOB'], lasfile['DEPT'], linewidth=0.5)
ax3.set_xlabel('RHOB (g/cm3)',va = 'top')
ax3.xaxis.tick_top()
ax3.xaxis.set_label_position('top')
ax3.grid(True, c="g", alpha=0.3)
remove_last(ax3)  

# Track 4: DRHO
ax4.plot(lasfile['DRHO'], lasfile['DEPT'], 'g',linewidth=0.5)
ax4.set_xlabel('DRHO (g/cm3)')
ax4.xaxis.tick_top()
ax4.xaxis.set_label_position('top')
ax4.grid(True, c="g", alpha=0.3) 
remove_last(ax4)  

# Track 5: NPHI
ax5.plot(lasfile['NPHI'], lasfile['DEPT'], 'k', linewidth=0.5)
ax5.set_xlabel('NPHI (v/v)',va = 'top')
ax5.xaxis.tick_top()
ax5.xaxis.set_label_position('top')
ax5.grid(True, c="g", alpha=0.3) 
remove_last(ax5)  

plt.show()


# ## Plotting petrophysical properties from cores
# 
# These experimental measurements are available in a variety of file formats. In this case we have two files in .csv format, which are handled with the _pandas package_. We are interested in plotting together well logs and core measurements. Therefore, columns two and three, which correspond to core top and bottom depths, are relevant. These are the vertical lines (blue, red, green) in track 1 (Figure 2).

# In[11]:


# Reading the .csv file containing depths and properties measured on cores 
cores = pd.read_csv('../data/raw/cores/CAP-01_cores.csv')


# In[12]:


cores.head()


# In[13]:


# We are making an array of top and bottom depths to plot the core intervals (m)
# (x1, x2), (bottom, top), 'color'
c = [(0, 0), (cores['Bottom'][0], cores['Top'][0]), 'b',
     (0, 0), (cores['Bottom'][1], cores['Top'][1]), 'r', 
     (0, 0), (cores['Bottom'][2], cores['Top'][2]), 'g']


# A second .csv file contains the actual measurements taken on cores. This file contains the units as part of the key name, which would be removed during the data cleaning phase. In this notebook, we use the keys as they are.

# In[14]:


# Reading the .csv file containinig experimental petrophysical measurements 
km = pd.read_csv('../data/raw/cores/CAP-01_kernmetingen.csv')


# Using .head() and .tail() functions, we can explore the data to find invalid values, outliers, etc. Note that lines 1, 9 and 147 have a dash ('-') instead of null (or NaN).  

# In[15]:


km.head(10)


# In[16]:


km.tail(10)


# Indeed, the presence of strings ('-') makes data appear as object, not as an array. For what one can not plot them. The two columns that contain numerical values are "depth" and "porosity". 

# In[17]:


#km.describe()


# In[18]:


# Print how many and which properties 
# Note that the data type is Object, not array
km.columns


# In[19]:


# Depth interval where there are logs
core_int = km['deipte (m)']
core_int [(core_int >= km['deipte (m)'].min()) & (core_int <= km['deipte (m)'].max())]


# In[20]:


km['Korreldichtheid (g/cm³)']


# The following code removes strings (object) and converts data into arrays (float).

# In[21]:


# Converting '-' into Nan and removing outliers
km2= valtonan(km, val='-')
km2= valtonan(km, val='0.66')
den2=km2['Korreldichtheid (g/cm³)']
dd2 = np.array(den2.values, dtype=float)
np.nanmin(dd2), np.nanmax(dd2)


# In[22]:


por2=km2['Porositeit (%)']
p2 = np.array(por2.values, dtype=float)
np.nanmin(p2), np.nanmax(p2)


# In[23]:


perm2=km2['hor. Perm (mD)']
p3 = np.array(perm2.values, dtype=float)
np.nanmin(p3), np.nanmax(p3)


# In[24]:


# Plotting petrophysical measurements and curves

f3, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(8,7))
f3.subplots_adjust(wspace=0.1)
plt.gca().invert_yaxis()
plt.ylim(km['deipte (m)'].max()+15,km['deipte (m)'].min()-10)

# So that y-tick labels appear on left and right
plt.tick_params(labelright=True)

# Change tick-label globally
mpl.rcParams['xtick.labelsize'] = 6

# Track 1: GR
ax1.plot(*c, linewidth=5,alpha=0.7)
ax1.plot(lasfile['GR'], lasfile['DEPT'],'k', linewidth=1)
ax1.xaxis.tick_top()
ax1.xaxis.set_label_position('top') 
ax1.set_xlabel('GR (API)')
ax1.set_ylabel('DEPTH (m)')
ax1.grid(True, c="g", alpha=0.3)

plt.setp(ax1.get_xticklabels()[1::2], visible=False)  # Hide every second tick-label
remove_last(ax1)  # remove last value of x-ticks, see function defined in first cell

# Track 2: RHOB
ax2.plot(lasfile['RHOB'], lasfile['DEPT'], 'b', linewidth=1)
#ax2.scatter(km['Korreldichtheid (g/cm³)'],km['deipte (m)'],alpha=0.8,c='g')
ax2.scatter(dd2,km['deipte (m)'],alpha=0.7,c='g')
ax2.set_xlabel('Density (g/cm3)',va = 'top')
ax2.xaxis.tick_top()
ax2.xaxis.set_label_position('top')
ax2.grid(True, c="g", alpha=0.3)
ax2.set_xlim(2.3, 3.0)
plt.setp(ax2.get_xticklabels()[1::2], visible=False)  # Hide every second tick-label
remove_last(ax2)  

# Track 5: NPHI
ax3.plot(lasfile['NPHI']*100, lasfile['DEPT'], 'c', linewidth=1)
ax3.scatter(km['Porositeit (%)'],km['deipte (m)'],alpha=0.6,c='b')
ax3.set_xlabel('Porosity (%)',va = 'top')
ax3.set_xlim(0,20)
ax3.xaxis.tick_top()
ax3.xaxis.set_label_position('top')
ax3.grid(True, c="g", alpha=0.3) 
remove_last(ax3)  

plt.show()


# In[25]:


#Plotting the depth intervals with cores

f4, (ax1, ax2, ax3) = plt.subplots(3, 1, sharey=True, figsize=(9,14))
plt.gca().invert_yaxis()

# Change tick-label globally
mpl.rcParams['xtick.labelsize'] = 6

# Track 1: RHOB
#ax1.plot(*c1, linewidth=5,alpha=0.7)
ax1.scatter(dd2,km['deipte (m)'],alpha=0.5)
ax1.set_xlabel('Density (g/cm³)',va = 'top')
ax1.xaxis.set_label_position('top')
ax1.grid(True, c="g", alpha=0.3) 

#ax2.plot(*c2, linewidth=5,alpha=0.7)
ax2.scatter(p2,km['deipte (m)'],alpha=0.5)
ax2.set_xlabel('Porosity (%)',va = 'top')
ax2.xaxis.set_label_position('top')
ax2.grid(True, c="g", alpha=0.5) 

#ax3.plot(*c3, linewidth=5,alpha=0.7)
ax3.scatter(p3,km['deipte (m)'],alpha=0.5)
ax3.set_xlabel('Permeability (mD)',va = 'top')
ax3.set_xscale('log')
ax3.xaxis.set_label_position('top')
ax3.grid(True, c="g", alpha=0.5)

plt.show()


# In[26]:


#Plotting the depth intervals with cores
#plt.style.use("seaborn")
f4 = plt.figure(figsize=plt.figaspect(0.45))
plt.scatter(
    x=p2,
    y=dd2,
    c=km['deipte (m)'],
    cmap="jet")
plt.title("Porosity vs Density")
plt.xlabel("Porosity")
plt.ylabel("Density")
cbar = plt.colorbar()
cbar.set_label('Depth (m)',rotation=270)


# In[27]:


#Plotting the depth intervals with cores
#plt.style.use("seaborn")
f5 = plt.figure(figsize=plt.figaspect(0.45))
plt.scatter(
    x=p2,
    y=p3,
    c=km['deipte (m)'],
    cmap="jet")
plt.title("Porosity vs Permeability")
plt.xlabel("Porosity")
plt.ylabel("Permeability")
plt.yscale('log')
cbar = plt.colorbar()
cbar.set_label('Depth (m)',rotation=270)


# In[ ]:





# In[ ]:





# In[ ]:




