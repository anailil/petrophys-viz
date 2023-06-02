#!/usr/bin/env python
# coding: utf-8

# ## Well Log and Core Data Visualization 
# 
# Depth intervals of core in the  _CAPELLE-01_ well have been manually compiled in the _CAP-01_cores.csv_ file.
# 
# Petrophysical measurements taken on those cores are available at [NLOG data center](https://www.nlog.nl/datacenter/brh-overview), under tab _kernmetingen_. We have created _CAP-01_kernmetingen.cvs_ file.
# 
# In this notebook we will:
# - Load and read LAS files using lasio 
# - Load and read CSV files with pandas 
# - Plot geophysical well logs using matplotlib 
# - Plot petrophysical properties from cores with matplotlib 

# In[1]:


import lasio , os  
import numpy as np    
import pandas as pd   

import matplotlib as mpl  
import matplotlib.pyplot as plt

# get_ipython().run_line_magic('matplotlib', 'inline')


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


# In[3]:


# Read a single file 
lasfile = lasio.read(os.path.join("../data/raw/logs/2571_cap01_1985_comp.las"))


# ## Plotting Cored Depth Intervals
# 
# Loading the file _CAP-01_cores.csv_ with _pandas_ and inspecting its contents, we see that there are three cores only. These are indicated in column _Kernmetingen_ with a _YES_.

# In[4]:


# Reading the .csv file containing depths and properties measured on cores 
cores = pd.read_csv('../data/raw/cores/CAP-01_cores.csv')


# In[5]:


cores.head(10)


# Columns two and three correspond with top and bottom depths of each interval. To plot them as a vertical line next to the well logs, we need to make an array as follows. These are the vertical lines (blue, red, green) in track 1.

# In[6]:


# (x1, x2), (bottom, top), 'color'
c = [(0, 0), (cores['Bottom'][0], cores['Top'][0]), 'b',
     (0, 0), (cores['Bottom'][1], cores['Top'][1]), 'r', 
     (0, 0), (cores['Bottom'][2], cores['Top'][2]), 'g']


# In[7]:


# Reading the .csv file containinig experimental petrophysical measurements 
km = pd.read_csv('../data/raw/cores/CAP-01_kernmetingen.csv')


# In[8]:


# Depth interval where there are logs
core_int = km['deipte (m)']
core_int [(core_int >= km['deipte (m)'].min()) & (core_int <= km['deipte (m)'].max())]


# In[9]:


# Plotting core intervals along well logs

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
ax2.set_xlabel('Density (g/cm3)',va = 'top')
ax2.xaxis.tick_top()
ax2.xaxis.set_label_position('top')
ax2.grid(True, c="g", alpha=0.3)
ax2.set_xlim(2.3, 3.0)
plt.setp(ax2.get_xticklabels()[1::2], visible=False)  # Hide every second tick-label
remove_last(ax2)  

# Track 5: NPHI
ax3.plot(lasfile['NPHI']*100, lasfile['DEPT'], 'c', linewidth=1)
ax3.set_xlabel('Porosity (%)',va = 'top')
ax3.set_xlim(0,20)
ax3.xaxis.tick_top()
ax3.xaxis.set_label_position('top')
ax3.grid(True, c="g", alpha=0.3) 
remove_last(ax3)  

plt.show()


# ## Checking Measurements from Cores
# 
# The _CAP-01_kernmetingen.csv_ file contains the actual petrophysical measurements taken on those cores. This file contains the units as part of the key name, which would be removed during the data cleaning phase. However, in this notebook, we use the keys as they are.

# In[10]:


# Reading the .csv file containinig experimental petrophysical measurements 
km = pd.read_csv('../data/raw/cores/CAP-01_kernmetingen.csv')


# Using _.head()_ and _.tail()_ functions, we check the data to find invalid values, outliers, etc. For example, lines 1, 9 and 147 have a dash ('-') instead of null (or NaN), which must be corrected for plotting. 

# In[11]:


km.head(10)


# In[12]:


km.tail(10)


# Indeed, the presence of strings ('-') makes data appear as _object_, not as an array. For what one can not plot them. The two columns that contain numerical values are _diepte_ and _Porositeit_. 

# In[13]:


#km.describe()


# In[14]:


# Print how many and which properties 
# Note that the data type is Object, not array
km.columns


# In[15]:


# Depth interval where there are logs
core_int = km['deipte (m)']
core_int [(core_int >= km['deipte (m)'].min()) & (core_int <= km['deipte (m)'].max())]


# In[16]:


km['Korreldichtheid (g/cm³)']


# ### Converting Objects into Data Arrays  
# The following code removes strings (object) and converts data into arrays (float).

# In[17]:


# Converting '-' into Nan and removing outliers
km2= valtonan(km, val='-')
km2= valtonan(km, val='0.66')
den2=km2['Korreldichtheid (g/cm³)']
dd2 = np.array(den2.values, dtype=float)
np.nanmin(dd2), np.nanmax(dd2)


# In[18]:


por2=km2['Porositeit (%)']
p2 = np.array(por2.values, dtype=float)
np.nanmin(p2), np.nanmax(p2)


# In[19]:


perm2=km2['hor. Perm (mD)']
p3 = np.array(perm2.values, dtype=float)
np.nanmin(p3), np.nanmax(p3)


# ## Plotting Petrophysical Measurements
# 
# Let's plot together the curves and measurements for both the density and porosity. Note that both sources of petrophysical information have a good correlation. 

# In[20]:


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


# Next, we will plot the petrophysical measurements alone to inspect their trends.

# In[ ]:




