import matplotlib.pyplot as plt
import matplotlib as mpl

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

def subplot_curve(plot, plot_curve=True, curve_type='', curve_depth='', scatter=False, scatter_x='', scatter_y='', scatter_alpha=0.3, scatter_color='g', scatter_cmap='', color='r', x_label='', y_label='', graph_label='', graph_position='top', linewidth=0.5, label_position='top', grid=True, grid_color='g', grid_alpha=0.3, hide_tick=0, xlim_low=0.0, xlim_high=0.0, cores=[], core_linewidth=5.0, core_alpha=0.7, color_bar=False, color_bar_label='', color_bar_rotation=270, y_scale='linear', x_scale='linear', xtick='top', removelast=True):

    if cores != []:
        plot.plot(*cores, linewidth=core_linewidth,alpha=core_alpha)

    if plot_curve:
        plot.plot(curve_type, curve_depth, color, label=graph_label, linewidth=linewidth)

    if scatter:
        plot.scatter(scatter_x,scatter_y,alpha=scatter_alpha,c=scatter_color)

    plot.set_xlabel(x_label,va = label_position)
    plot.set_xscale(x_scale)
    plot.set_ylabel(y_label)
    plot.set_yscale(y_scale)
    plot.set_title(graph_label)

    if xtick == 'top':
        plot.xaxis.tick_top()
    else:
        plot.xaxis.tick_bottom()

    plot.xaxis.set_label_position(label_position)
    plot.grid(grid, c=grid_color, alpha=grid_alpha)


    if xlim_low != 0.0 or xlim_high != 0.0:
        plot.set_xlim(xlim_low, xlim_high)
    if hide_tick != 0:
        plt.setp(plot.get_xticklabels()[1::hide_tick], visible=False)  # Hide every second tick-label

    if removelast:
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
    subplot_curve(plot=ax1, curve_type=lasfile['GR'], curve_depth=lasfile['DEPT'], color='c', x_label='GR (API)', y_label='DEPTH (m)',hide_tick=2)
    
    # Track 2: Sonic (velocities)
    subplot_curve(plot=ax2, curve_type=lasfile['DT']/0.3048, curve_depth=lasfile['DEPT'], color='r', x_label='DT (m/s)', y_label='DEPTH (m)', graph_label='DTCO')
    
    # Track 3: RHOB (Bulk Density)
    subplot_curve(plot=ax3, curve_type=lasfile['RHOB'], curve_depth=lasfile['DEPT'], color='b', x_label='RHOB (g/cm3', y_label='DEPTH (m)')
    
    # Track 4: DRHO
    subplot_curve(plot=ax4, curve_type=lasfile['DRHO'], curve_depth=lasfile['DEPT'], color='g', x_label='DRHO (g/cm3)', y_label='DEPTH (m)')
    
    # Track 5: NPHI
    subplot_curve(plot=ax5, curve_type=lasfile['NPHI'], curve_depth=lasfile['DEPT'], color='k', x_label='NPHI (v/v)', y_label='DEPTH (m)')
    
    plt.show()

def petro_measure_curve(lasfile, km, dd2, c):

    f1, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(8,7))
    f1.subplots_adjust(wspace=0.1)
    plt.gca().invert_yaxis()
    plt.ylim(km['deipte (m)'].max()+15,km['deipte (m)'].min()-10)
    
    # So that y-tick labels appear on left and right
    plt.tick_params(labelright=True)
    
    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6
    
    #track1: Gamma Ray
    subplot_curve(plot=ax1, curve_type=lasfile['GR'], curve_depth=lasfile['DEPT'], color='k', x_label='GR (API)', y_label='DEPTH (m)',linewidth=1.0,hide_tick=2, cores=c)
    
    # Track 2: RHOB
    subplot_curve(plot=ax2, curve_type=lasfile['RHOB'], curve_depth=lasfile['DEPT'], color='b', x_label='Density (g/cm3)', scatter=True, scatter_x=dd2, scatter_y=km['deipte (m)'], linewidth=1.0, hide_tick=2, xlim_low=2.3, xlim_high=3.0)
    
    # Track 5: NPHI
    subplot_curve(plot=ax3, curve_type=lasfile['NPHI']*100, curve_depth=lasfile['DEPT'], color='c', x_label='Porosity (%)', linewidth=1.0, scatter=True, scatter_x=km['Porositeit (%)'], scatter_y=km['deipte (m)'], scatter_alpha=0.6, scatter_color='b', xlim_high=20)
    
    plt.show()

def depth_intervals_cores(km, dd2, p2, p3):

    f1, (ax1, ax2, ax3) = plt.subplots(3, 1, sharey=True, figsize=(9,14))

    plt.gca().invert_yaxis()
    
    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6
    
    #track1: RHOB
    subplot_curve(plot=ax1, plot_curve=False, x_label='Density (g/cm3)', scatter=True, scatter_x=dd2, scatter_y=km['deipte (m)'], scatter_alpha=0.5, scatter_color='b', xtick='bottom', removelast=False)
    
    # Track 2: RHOB
    subplot_curve(plot=ax2, plot_curve=False, x_label='Porosity (%)', scatter=True, scatter_x=p2, scatter_y=km['deipte (m)'], scatter_alpha=0.5, grid_alpha=0.5, scatter_color='b', xtick='bottom', removelast=False)
    
    # Track 5: NPHI
    subplot_curve(plot=ax3, plot_curve=False, x_label='Permeability (mD)', scatter=True, scatter_x=p3, scatter_y=km['deipte (m)'], scatter_alpha=0.5, grid_alpha=0.5, scatter_color='b', x_scale='log', xtick='bottom', removelast=False)
    
    plt.show()

def depth_intervals_porosity(km, x, y, xlabel, ylabel, clabel, graphlabel, yscale='linear', colormap='jet', orientation=270, aspect=0.45):

    f1 = plt.figure(figsize=plt.figaspect(aspect))
    plt.scatter(
        x=x,
        y=y,
        c=km,
        cmap=colormap)
    plt.title(graphlabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.yscale(yscale)
    cbar = plt.colorbar()
    cbar.set_label(clabel,rotation=orientation)
