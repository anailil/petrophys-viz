import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def valtonan(inp, val=-999.25):
    """Convert all 'val' to NaN's."""
    inp[inp==val] = np.nan
    return inp

#This function makes for cleaner axis plotting
def remove_last(ax, which='upper'):
    """Remove <which> from x-axis of <ax>.
    
    Parameters
    ----------
    which: str
        which can take 'upper', 'lower', 'both'
    """
    nbins = len(ax.get_xticklabels())
    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=nbins, prune=which))

def plot_well_curve(plot, curve_type, curve_depth, color, x_label, y_label, graphlabel='', linewidth=0.5, label_position='top', grid=True, grid_color='g', alpha=0.3, hide_tick=0):
    plot.plot(curve_type, curve_depth, color, label=graphlabel, linewidth=linewidth)
    plot.xaxis.tick_top()
    plot.xaxis.set_label_position(label_position) 
    plot.set_xlabel(x_label)
    plot.set_ylabel(y_label)
    plot.grid(grid, c=grid_color, alpha=alpha)
    
    if hide_tick != 0:
        plt.setp(plot.get_xticklabels()[1::hide_tick], visible=False)  # Hide every second tick-label
    remove_last(plot)  # remove last value of x-ticks, see function defined in first cell

def plot_petro_measure_curve(plot, curve_type, curve_depth, scatter_x='', scatter_y='', scatter_alpha=0.3, scatter_color='g', color='r', x_label='', y_label='', graphlabel='', linewidth=0.5, label_position='top', grid=True, grid_color='g', grid_alpha=0.3, hide_tick=0, xlim_low=0.0, xlim_high=0.0):

    plot.plot(curve_type, curve_depth, color, label=graphlabel, linewidth=linewidth)
    if scatter_x != '' and scatter_y != '':
        plot.scatter(scatter_x,scatter_y,alpha=scatter_alpha,c=scatter_color)
    plot.set_xlabel(x_label,va = label_position)
    plot.set_ylabel(y_label)
    plot.xaxis.tick_top()
    plot.xaxis.set_label_position(label_position)
    plot.grid(grid, c=grid_color, alpha=grid_alpha)
    if xlim_low != 0.0 or xlim_high != 0.0:
        plot.set_xlim(xlim_low, xlim_high)
    if hide_tick != 0:
        plt.setp(plot.get_xticklabels()[1::hide_tick], visible=False)  # Hide every second tick-label
    remove_last(plot) 


def well_curve(lasfile):

    f1, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, sharey=True, figsize=(18,16))
    f1.subplots_adjust(wspace=0.02)
    plt.gca().invert_yaxis()
    
    # So that y-tick labels appear on left and right
    plt.tick_params(labelright=True)
    
    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6
    
    #track1: Gamma Ray
    plot_petro_measure_curve(ax1, lasfile['GR'], lasfile['DEPT'], color='c', x_label='GR (API)', y_label='DEPTH (m)',hide_tick=2)
    
    # Track 2: Sonic (velocities)
    plot_petro_measure_curve(ax2, lasfile['DT']/0.3048, lasfile['DEPT'], color='r', x_label='DT (m/s)', y_label='DEPTH (m)', graphlabel='DTCO')
    
    # Track 3: RHOB (Bulk Density)
    plot_petro_measure_curve(ax3, lasfile['RHOB'], lasfile['DEPT'], color='b', x_label='RHOB (g/cm3', y_label='DEPTH (m)')
    
    # Track 4: DRHO
    plot_petro_measure_curve(ax4, lasfile['DRHO'], lasfile['DEPT'], color='g', x_label='DRHO (g/cm3)', y_label='DEPTH (m)')
    
    # Track 5: NPHI
    plot_petro_measure_curve(ax5, lasfile['NPHI'], lasfile['DEPT'], color='k', x_label='NPHI (v/v)', y_label='DEPTH (m)')
    
    plt.show()

def petro_measure_curve(lasfile, km):

    # Converting '-' into Nan and removing outliers
    km2= valtonan(km, val='-')
    km2= valtonan(km, val='0.66')
    den2=km2['Korreldichtheid (g/cm³)']
    dd2 = np.array(den2.values, dtype=float)
    np.nanmin(dd2), np.nanmax(dd2)

    f1, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(8,7))
    f1.subplots_adjust(wspace=0.1)
    plt.gca().invert_yaxis()
    plt.ylim(km['deipte (m)'].max()+15,km['deipte (m)'].min()-10)
    
    # So that y-tick labels appear on left and right
    plt.tick_params(labelright=True)
    
    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6
    
    #track1: Gamma Ray
    plot_petro_measure_curve(ax1, lasfile['GR'], lasfile['DEPT'], color='k', x_label='GR (API)', y_label='DEPTH (m)',linewidth=1.0,hide_tick=2)
    
    # Track 2: RHOB
    plot_petro_measure_curve(ax2, lasfile['RHOB'], lasfile['DEPT'], color='b', x_label='Density (g/cm3)', y_label='DEPTH (m)', scatter_x=dd2, scatter_y=km['deipte (m)'], linewidth=1.0, hide_tick=2, xlim_low=2.3, xlim_high=3.0)
    
    # Track 5: NPHI
    plot_petro_measure_curve(ax5, lasfile['NPHI']*100, lasfile['DEPT'], color='k', x_label='Porosity (%)', y_label='DEPTH (m)', linewidth=1.0, scatter_x=km['Porositeit (%)'], scatter_y=km['deipte (m)'], scatter_alpha=0.6, scatter_color='b', xlim_high=20)
    
    plt.show()
