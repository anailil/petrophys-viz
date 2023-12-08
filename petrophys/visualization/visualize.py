import matplotlib.pyplot as plt
import matplotlib as mpl

def remove_last(ax, which='upper'):
    """Remove <which> from x-axis of <ax>.

       This function makes cleaner axis plotting
    
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

def petro_measure_curve(lasfile, depth, density, porosity, cores):
    """ Plots the GR, RHOB and NPHI graphs of the given lasio file
        It adds a scattered graph of depth vs density and depth vs porosity
        with the given depth, density and porosity in seperate lists
        It also plots the position of the cores given in cores
    
    Parameters
    ----------
    lasfile: lasio dataset
    depth: list
    density: list
    porosity: list
    cores: csv table

    """

    # We are making an array of top and bottom depths to plot the core intervals (m)
    # (x1, x2), (bottom, top), 'color'
    c = [(0, 0), (cores['Bottom'][0], cores['Top'][0]), 'b',
         (0, 0), (cores['Bottom'][1], cores['Top'][1]), 'r', 
         (0, 0), (cores['Bottom'][2], cores['Top'][2]), 'g']

    f1, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(8,7))
    f1.subplots_adjust(wspace=0.1)
    plt.gca().invert_yaxis()
    plt.ylim(depth.max()+15,depth.min()-10)
    
    # So that y-tick labels appear on left and right
    plt.tick_params(labelright=True)
    
    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6
    
    #track1: Gamma Ray
    subplot_curve(plot=ax1, curve_type=lasfile['GR'], curve_depth=lasfile['DEPT'], color='k', x_label='GR (API)', y_label='DEPTH (m)',linewidth=1.0,hide_tick=2, cores=c)
    
    # Track 2: RHOB
    subplot_curve(plot=ax2, curve_type=lasfile['RHOB'], curve_depth=lasfile['DEPT'], color='b', x_label='Density (g/cm3)', scatter=True, scatter_x=density, scatter_y=depth, linewidth=1.0, hide_tick=2, xlim_low=2.3, xlim_high=3.0)
    
    # Track 5: NPHI
    subplot_curve(plot=ax3, curve_type=lasfile['NPHI']*100, curve_depth=lasfile['DEPT'], color='c', x_label='Porosity (%)', linewidth=1.0, scatter=True, scatter_x=porosity, scatter_y=depth, scatter_alpha=0.6, scatter_color='b', xlim_high=20)
    
    plt.show()

def depth_intervals_cores(xdata, ydata, xlabel='', ylabel='', xscale='linear', yscale='linear', xsize=9, ysize=5, color='b'):
    """Plot a scattered graph for xdata and ydata

    Parameters
    ----------
    xdata: list of floats or integers
        xdata represents the x axes of the graph
    ydata: list of floats or integers
        ydata represents the y axes of the graph
    xlabel: str
        label printed on the x axes
    ylabel: str
        label printed on the y axes
    xscale: str
        scale of the x axes, can take "linear' or 'log'
        default is linear
    yscale: str
        scale of the y axes, can take "linear' or 'log'
        default is linear
    xsize: float or integer
        size of the figure in the horizontal direction
    ysize: float or integer
        size of the figure in the vertical direction
    color: str
        color of the dots
        see https://matplotlib.org/stable/gallery/color/named_colors.html or 
            https://matplotlib.org/stable/users/explain/colors/colors.html for color options
    """

    f1, (ax1) = plt.subplots(1, 1, figsize=(xsize,ysize))

    plt.gca().invert_yaxis()
    
    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6
    
    #track
    subplot_curve(plot=ax1, plot_curve=False, x_label=xlabel, y_label=ylabel, scatter=True, scatter_x=xdata, scatter_y=ydata, scatter_alpha=0.5, scatter_color=color, x_scale=xscale, y_scale=yscale, xtick='bottom', removelast=False)
    
    plt.show()

def depth_intervals_porosity(xdata, ydata, cdata, xlabel='', ylabel='', clabel='', graphlabel='', xscale='linear', yscale='linear', colormap='jet', orientation=270, aspect=0.45):
    """Plot a scattered graph for the xdata, ydata and cdata

    Parameters
    ----------
    xdata: list of floats or integers
        xdata represents the x axes of the graph
    ydata: list of floats or integers
        ydata represents the y axes of the graph
    cdata: list of floats or integers
        cdata represents the color of the dots in the graph
    xlabel: str
        label printed on the x axes
    ylabel: str
        label printed on the y axes
    clabel: str
        label printed on the colormap
    graphlabel: str
        label printed on top of the graph
    xscale: str
        scale of the x axes, can take "linear' or 'log'
        default is linear
    yscale: str
        scale of the y axes, can take "linear' or 'log'
        default is linear
    colormap: str
        colormap to use for the dots
        see https://matplotlib.org/stable/users/explain/colors/colormaps.html for options
        default is jet
    orientation: int or float
        orientation of the clabel in degrees
        default is 270
    aspect: float
        Set the aspect ratio of the axes scaling, i.e. y/x-scale.
        default is 0.45

    """

    f1 = plt.figure(figsize=plt.figaspect(aspect))
    plt.scatter(
        x=xdata,
        y=ydata,
        c=cdata,
        cmap=colormap)
    plt.title(graphlabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xscale(xscale)
    plt.yscale(yscale)
    cbar = plt.colorbar()
    cbar.set_label(clabel,rotation=orientation)

    plt.show()
