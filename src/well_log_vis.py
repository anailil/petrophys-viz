#!/usr/bin/env python
# coding: utf-8

# # Well Log Data Exploration 
# 
# ### Borehole CAPELLE-01
# 
# __Find the files used in this notebook in this location__:
# 
# /geomechanical_properties/data/raw/
# - appendix_b_summary_data_sheet.xlsx 
# - appendix_a_list_of_wells_and_data_files_used.xlsx
# - 2571_cap01_1985_comp.las
# - CAP-01_cores.csv
# - CAP-01_kernmetingen.csv
# 
# In this notebook we will:
# - Load and read LAS files using lasio 
# - Load and read CSV files with pandas 
# - Plot geophysical well logs using matplotlib 
# - Plot petrophysical properties from cores with matplotlib 

# ## Set up
# Install [lasio](https://lasio.readthedocs.io/en/latest/) and pandas packages to be able to read well logs in standard LAS file format. 

# In[33]:


import lasio , os  
import numpy as np    
import pandas as pd   

import matplotlib as mpl  
import matplotlib.pyplot as plt

# Uncomment to produce static figures
get_ipython().run_line_magic('matplotlib', 'inline')

# Uncomment to produce interactive figures (zoom in/out, save, etc.)
#%matplotlib widget


# In[34]:


# functions to prepare data before processing and visualizing

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


# ## Exploring contents of LAS files
# Load the LAS file and look at the its header. Note that the borehole tools started measuring from the bottom of the well. Also note that the value -999.25 should be considered as null. Such values must be converted to NaN before analysing the data with the function _valtonan_. Other drilling parameters can also be displayed. They may be useful to integrate well logs with seismic and geologic data and other numerical models.

# In[35]:


# Read a single file 
# ----> To-Do: Batch reading example in a directory 
lasfile = lasio.read(os.path.join("../data/raw/logs/2571_cap01_1985_comp.las"))


# In[36]:


print(lasfile.well)


# In[37]:


print(lasfile.params)


# ## Well Log Curves
# Let's display a list of the curves in this LAS file. Note that curve mnemonics do not have a description. If you are unfamiliar with those mnemonic, check [CurveNam.es](http://curvenam.es/), which is a useful fuzzy lookup of wireline log mnemonics. Or check directly on [SLB website](https://www.apps.slb.com/cmd/index.aspx) and 
# [Halliburton website](https://www.halliburton.com/en/resources/lwd-curve-mnemonics).
# 
# PS. Here, the curve mnemonic _DRHO_ stands for for Density Correction, which may be useful for log quality control but not neccesarily for log interpretation. The DRHO curve is the difference between the short- and long-spaced density measurements. It is used as a quality indicator of the bulk density data. DRHO values larger than 0.1 g/cm3 suggest unreliable density data. This can be correlated with high caliper readings due to probable poor contact with the wall borehole.
# 

# In[38]:


print(lasfile.curves)


# In[39]:


for curve in lasfile.curves:
    print(curve.mnemonic + ": " + str(curve.data))


# ## Well log visualization
# 
# This is a simple way of inspecting the curves we just read from that LAS file. You can identify the intervals where the tool did not measure or where there are anomalous measurements to filter before rpocessing.
# 
# Note that to plot the sonic transit time (DT) we have converted its units from _us/ft_ to _m/s_.
# 
# This is an interactive plot. Use the controls on the upper left corner to zoom in and out.

# In[40]:


# These are the variable names, i.e. curve mnemonic
lasfile.keys() 


# In[41]:


# --> To-DO
# Looking for invalid values
# valtonan(lasfile, val=-999.25)


# In[42]:


# Plotting curves along well's total depth

f1, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, sharey=True, figsize=(16,12))
plt.gca().invert_yaxis()
f1.subplots_adjust(wspace=0.02)


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

# Track 6: Cores and Properties
#ax6.plot(*c, linewidth=5)
#ax6.scatter(km['Porositeit (%)'],km['deipte (m)'],alpha=0.5)
#ax6.set_xlabel('Cores')
#ax6.xaxis.tick_top()
#ax6.xaxis.set_label_position('top')
#ax6.grid(False) 
#remove_last(ax6)  

plt.show()


# ## Petrophysical properties from cores
# 
# These experimental measurements are available in a variety of file formats. In this case we have two files in .csv format, which are handled with the _pandas package_. We are interested in plotting together well logs and core measurements. Therefore, columns two and three, which correspond to core top and bottom depths, are relevant. These are the vertical lines (blue, red, green) in track 1 (Figure 2).

# In[43]:


# Reading the .csv file containing depths and properties measured on cores 
cores = pd.read_csv('../data/raw/cores/CAP-01_cores.csv')


# In[44]:


cores.head()


# In[45]:


# We are making an array of top and bottom depths to plot the core intervals (m)
# (x1, x2), (bottom, top), 'color'
c = [(0, 0), (cores['Bottom'][0], cores['Top'][0]), 'b',
     (0, 0), (cores['Bottom'][1], cores['Top'][1]), 'r', 
     (0, 0), (cores['Bottom'][2], cores['Top'][2]), 'g']


# A second .csv file contains the actual measurements taken on cores. This file contains the units as part of the key name, which would be removed during the data cleaning phase. In this notebook, we use the keys as they are.

# In[46]:


# Reading the .csv file containinig experimental petrophysical measurements 
km = pd.read_csv('../data/raw/cores/CAP-01_kernmetingen.csv')


# Using head and tail functions, we can explore the data to find invalid values, outliers, etc. Note that lines 1, 9 and 147 have a dash ('-') instead of null (or NaN).  

# In[47]:


km.head(10)


# In[48]:


km.tail(10)


# Indeed, the presence of strings ('-') makes data appear as object, not as an array. For what one can not plot them. The two columns that contain numerical values are "depth" and "porosity". 

# In[49]:


#km.describe()


# In[50]:


# Print how many and which properties 
# Note that the data type is Object, not array
km.columns


# In[51]:


# Depth interval where there are logs
core_int = km['deipte (m)']
core_int [(core_int >= km['deipte (m)'].min()) & (core_int <= km['deipte (m)'].max())]


# In[52]:


km['Korreldichtheid (g/cm³)']


# The following code removes strings (object) and converts data into arrays (float).

# In[53]:


# Converting '-' into Nan and removing outliers
km2= valtonan(km, val='-')
km2= valtonan(km, val='0.66')
den2=km2['Korreldichtheid (g/cm³)']
dd2 = np.array(den2.values, dtype=float)
np.nanmin(dd2), np.nanmax(dd2)


# In[54]:


por2=km2['Porositeit (%)']
p2 = np.array(por2.values, dtype=float)
np.nanmin(p2), np.nanmax(p2)


# In[55]:


perm2=km2['hor. Perm (mD)']
p3 = np.array(perm2.values, dtype=float)
np.nanmin(p3), np.nanmax(p3)


# In[56]:


# Plotting petrophysical measurements and curves

f3, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(16,12))
f3.subplots_adjust(wspace=0.1)
plt.gca().invert_yaxis()
plt.ylim(km['deipte (m)'].max()+15,km['deipte (m)'].min()-10)

# So that y-tick labels appear on left and right
plt.tick_params(labelright=True)

# Change tick-label globally
mpl.rcParams['xtick.labelsize'] = 10

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


# In[57]:


f4 = plt.figure(figsize=(12,6))
plt.scatter(dd2,km['deipte (m)'],alpha=0.8,c="orange")
plt.xlabel('Density (g/cm³)')
plt.ylabel('Depth (m)')
plt.grid(True, alpha=0.3)


# In[58]:


f5 = plt.figure(figsize=(12,6))
plt.scatter(p2,km['deipte (m)'],alpha=0.5, c='b')
plt.xlabel('Porosity (%)')
plt.ylabel('Depth (m)')
plt.grid(True, alpha=0.3)


# In[59]:


f6 = plt.figure(figsize=(12,6))
plt.scatter(p3,km['deipte (m)'],alpha=0.5, c='g')
plt.xlabel('Permeability (mD)')
plt.xscale("log")
plt.ylabel('Depth (m)')
plt.grid(True, alpha=0.3)


# In[60]:


#Plotting the depth intervals with cores
#plt.style.use("seaborn")
f7 = plt.figure(figsize=(12,6))
plt.scatter(p2,dd2,c=km['deipte (m)'])
plt.title("Porosity vs Density")
plt.xlabel("Porosity (%)")
plt.ylabel("Density (g/cm³)")
cbar = plt.colorbar()
cbar.set_label('Depth (m)')


# In[61]:


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


# ## End of the Excercise
# 
# This concludes this excercise, which focused on loading, checking, and plotting well logs and petrophysical measurements using Python libraries. This simple scripts can be adapted to check other files, improved and optimized using other Python libraries and defining functions for repetitive tasks.

# In[ ]:





# In[ ]:





# In[ ]:




