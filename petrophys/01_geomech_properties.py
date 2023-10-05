#!/usr/bin/env python
# coding: utf-8

# # Geomechanical Parameters from Well Logs
# 
# ## Introduction
# 
# Dynamic geomechanical parameters were derived from well logs of 41 wells at relevant geothermal intervals. TNO has published the following documents describing the well logs and the selected files for the computations:
# 
# https://www.nlog.nl/sites/default/files/2021-12/data_selection_and_methods.pdf
# 
# The main selection criteria is the availability of compressional (DTCO, DTC, DT4C or DT) and shear (DTSM, DTS or DT4S) sonic logs for intervals that contain main geothermal targets in the Netherlands.
# 
# https://www.nlog.nl/sites/default/files/2021-12/appendix_a_list_of_wells_and_data_files_used.xlsx
# 
# Spreadsheet about wells which have sonic logs.
# 
# https://www.nlog.nl/sites/default/files/2021-12/appendix_b_summary_data_sheet.xlsx
# 
# Spreadsheet with average geomechanical parameter values per lithostratigraphic interval. 

# ## Loading Data
# 
# Let's take a look at the geomechanical parameters and make a crossplot.  
# 
# First, we will import both pandas and matplotlib python libraries. 

# In[1]:


import os
import pandas as pd

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# The geomechanical parameters are in Appendix B, which is in the folder called references. 

# In[3]:


geomech_par = pd.read_excel('../references/appendix_b_summary_data_sheet.xlsx', sheet_name=1)


# Data has been converted into a dataframe. Let's view the first 5 rows by callling upon the .head() function. We can see all the columns contained in this file. Note that there are NaN (_Not a Number_) data, which in the spreadsheet appear as empty cells. 

# In[4]:


geomech_par.head()


# ## Inspecting Data
# 
# By calling the .info() function we know the number of rows and columns, the column names, and the data types of each of these columns. 
# 
# There 4 columns with depth information about each stratigraphic interval: _Top (MD)_ and _Bottom (MD)_ refer to the start and end depths of the interval as measured along the well path. MD = Measured Depth. Whereas _TVDSS_Top_ and _TVDSS_Bottom_ refer to the start and end depths of the interval measured vertically from the surface. TVDSS = True Vertical Depth SubSea.
# 
# Note: The key _TVCSS_Top_ appears to be a typo error and C corresponds to D.  
# 

# In[5]:


geomech_par.info()


# ## Checking Numerical Values
# Calling upon the .describe() function, we get some statistical measurements of the numerical values only. This statistical summary is helpful to spot anomalous values.

# In[6]:


geomech_par.describe()


# ## Crossploting Data
# 
# The following image corresponds to Figure 5 in ([Hunfeld et al., 2021](https://www.nlog.nl/sites/default/files/2021-12/data_selection_and_methods.pdf)). 
# ![Young's Modulus vs Depth graph|100x100](../references/EvsTVCSS_Top.jpg)
# 
# Let's reproduce this _Young’s Modulus E (GPa) vs TVCSS_Top_ graph using the computed geomechanical properties.
# 
# The legend indicates _Lithology Type_, for which we have to collect the unique names to be able to plot them. 

# In[7]:


lith_list = [(k) for k in geomech_par['Lithology_type'].unique()]


# In[8]:


plt.figure(figsize=(15,9))
scatter = plt.scatter(geomech_par['TVCSS_Top'],
            geomech_par['Young’s Modulus E (GPa)'],
            c=geomech_par['Lithology_type'].astype('category').cat.codes)
#            cmap="tab10",
plt.xlabel('Depth (TVCSS_Top) [m]')
plt.ylabel('Young’s Modulus E (GPa)')
plt.title('Young’s Modulus vs Depth')
plt.ylim(0, 100)
plt.xlim(0, 6000)
plt.legend(handles=scatter.legend_elements()[0], 
           labels=lith_list,
           
           title="Lithology type")
plt.show()



# In[ ]:




