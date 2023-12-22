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
    ax.xaxis.set_major_locator(
            mpl.ticker.MaxNLocator(nbins=nbins, prune=which)
            )

def subplot_curve(
        plot='',
        fig='',
        plot_curve=True,
        xdata='',
        ydata='',
        color='r',
        scatter=False,
        scatter_x='',
        scatter_y='',
        scatter_alpha=0.3,
        scatter_color='g',
        scatter_cmap='',
        x_label='',
        y_label='',
        graph_label='',
        graph_position='top',
        linewidth=0.5,
        label_position='top',
        grid=True,
        grid_color='g',
        grid_alpha=0.3,
        hide_tick=0,
        xlim_low=0.0,
        xlim_high=0.0,
        cores=[],
        core_linewidth=5.0,
        core_alpha=0.7,
        x_scale='linear',
        y_scale='linear',
        xtick='top',
        color_bar=False, 
        color_bar_label='', 
        color_bar_rotation=270,
        removelast=True
        ):
    """Function to plot a graph based on the given parameters

    Parameters
    ----------
    plot: figure
    plot_curve: Boolean
        Defines wether or not to plot a curve
        Default is True
    xdata=: list of floats or integers
        Represents the x axes of the graph
    ydata=: list of floats or integers
        Represents the y axes of the graph
    color: str
        color of the graph line
        see https://matplotlib.org/stable/gallery/color/named_colors.html or
            https://matplotlib.org/stable/users/explain/colors/colors.html for color options
        Default is red.
    scatter: Boolean
        Defines wether or not to plot a scatter graph
        Default is False
    scatter_x: list of floats or integers
        Represents the x axes of the graph
    scatter_y: list of floats or integers
        Represents the y axes of the graph
    scatter_alpha: float, default is 0.3
        Alpha adds transparency to a color, the range is from 0.0-1.0.
    scatter_color: str
        color of the dots
        see https://matplotlib.org/stable/gallery/color/named_colors.html or
            https://matplotlib.org/stable/users/explain/colors/colors.html for color options
    x_label: str
        label printed on the x axes
        Default is empty
    y_label: str
        label printed on the y axes
        Default is empty
    graph_label: str
        Title of the graph.
        Default is empty
    graph_position='top',
    linewidth: float
        Defines the linewidth of the graph
        Default is 0.5
    label_position='top',
    grid: Boolean
        Defines wether or not to show a grid.
        Default = True
    grid_color: str
        color of the grid
        see https://matplotlib.org/stable/gallery/color/named_colors.html or
            https://matplotlib.org/stable/users/explain/colors/colors.html for color options
    grid_alpha=: float, default is 0.3
        Alpha adds transparency to a color, the range is from 0.0-1.0.
    hide_tick: integer
        Defines ticks to skip in the x axes. .
        default is 0
    xlim_low: float
        sets the low limit of the x axes
        default is 0.0
    xlim_high: float
        sets the high limit of the x axes
        default is 0.0
    cores: list
        definition of the cores to plot.
    core_linewidth: float
        Defines the thickness of the cores line
    core_alpha: float
        Alpha adds transparency to a color, the range is from 0.0-1.0.
    x_scale: str
        scale of the x axes, can take "linear' or 'log'
        default is linear
    y_scale: str
        scale of the y axes, can take "linear' or 'log'
        default is linear
    xtick: str
        Defines the place of the ticks on the x axes.
        Takes 'top' for top or any other for bottom.
        default is top.
    removelast: Boolean
        Wether or not to call the removelast function for cleaner graphs.
        default is True
    """

    if cores != []:
        plot.plot(*cores, linewidth=core_linewidth, alpha=core_alpha)

    if plot_curve:
        plot.plot(xdata, ydata, color, label=graph_label, linewidth=linewidth)

    if scatter and not color_bar:
        plot.scatter(scatter_x, scatter_y, alpha=scatter_alpha, c=scatter_color)

    if scatter and color_bar:
        scattered = plot.scatter(scatter_x,scatter_y,alpha=scatter_alpha,c=scatter_color, cmap=scatter_cmap)
        cbar = fig.colorbar(scattered, ax=plot, cmap="jet")
        cbar.set_label(color_bar_label, rotation=color_bar_rotation)

    plot.set_xlabel(x_label, va=label_position)
    plot.set_xscale(x_scale)
    plot.set_ylabel(y_label)
    plot.set_yscale(y_scale)
    plot.set_title(graph_label)

    if xtick == 'top':
        plot.xaxis.tick_top()
    else:
        plot.xaxis.tick_bottom()

    plot.xaxis.set_label_position(label_position)

    if grid:
        plot.grid(grid, c=grid_color, alpha=grid_alpha)

    if xlim_low != 0.0 or xlim_high != 0.0:
        plot.set_xlim(xlim_low, xlim_high)
    if hide_tick != 0:
        # Hide ticks defined by every hide_tick
        plt.setp(plot.get_xticklabels()[1::hide_tick], visible=False)

    if removelast:
        remove_last(plot)

    return fig

def well_curve(lasfile, xsize=18, ysize=16):
    """ Plots the GR, DT, RHOB, DRHO and NPHI vs Depth graphs of the given lasio file

    Parameters
    ----------
    lasfile: lasio dataset
    xsize: float or integer
        size of the figure in the horizontal direction
    ysize: float or integer
        size of the figure in the vertical direction

    """
    f1, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, sharey=True, figsize=(xsize, ysize))
    f1.subplots_adjust(wspace=0.02)
    plt.gca().invert_yaxis()

    # So that y-tick labels appear on left and right
    plt.tick_params(labelright=True)

    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6

    # track 1: Gamma Ray
    subplot_curve(
            plot=ax1,
            xdata=lasfile['GR'],
            ydata=lasfile['DEPT'],
            color='c',
            x_label='GR (API)',
            y_label='DEPTH (m)',
            hide_tick=2
            )

    # Track 2: Sonic (velocities)
    subplot_curve(
            plot=ax2,
            xdata=lasfile['DT']/0.3048,
            ydata=lasfile['DEPT'],
            color='r',
            x_label='DT (m/s)',
            y_label='DEPTH (m)',
            graph_label='DTCO'
            )

    # Track 3: RHOB (Bulk Density)
    subplot_curve(
            plot=ax3,
            xdata=lasfile['RHOB'],
            ydata=lasfile['DEPT'],
            color='b',
            x_label='RHOB (g/cm3',
            y_label='DEPTH (m)'
            )

    # Track 4: DRHO
    subplot_curve(
            plot=ax4,
            xdata=lasfile['DRHO'],
            ydata=lasfile['DEPT'],
            color='g',
            x_label='DRHO (g/cm3)',
            y_label='DEPTH (m)'
            )

    # Track 5: NPHI
    subplot_curve(
            plot=ax5,
            xdata=lasfile['NPHI'],
            ydata=lasfile['DEPT'],
            color='k',
            x_label='NPHI (v/v)',
            y_label='DEPTH (m)'
            )

    plt.show()


def petro_measure_curve(
        lasfile,
        depth,
        density,
        porosity,
        cores,
        xsize=8,
        ysize=7
        ):
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
    xsize: float or integer
        size of the figure in the horizontal direction
    ysize: float or integer
        size of the figure in the vertical direction

    """

    # We are making an array of top and bottom depths to plot the core intervals (m)
    # (x1, x2), (bottom, top), 'color'
    c = [(0, 0), (cores['Bottom'][0], cores['Top'][0]), 'b',
         (0, 0), (cores['Bottom'][1], cores['Top'][1]), 'r',
         (0, 0), (cores['Bottom'][2], cores['Top'][2]), 'g']

    f1, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(xsize, ysize))
    f1.subplots_adjust(wspace=0.1)
    plt.gca().invert_yaxis()
    plt.ylim(depth.max()+15, depth.min()-10)

    # So that y-tick labels appear on left and right
    plt.tick_params(labelright=True)

    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6

    # track 1: Gamma Ray
    subplot_curve(
            plot=ax1,
            xdata=lasfile['GR'],
            ydata=lasfile['DEPT'],
            color='k',
            x_label='GR (API)',
            y_label='DEPTH (m)',
            linewidth=1.0,
            hide_tick=2, cores=c
            )

    # Track 2: RHOB
    subplot_curve(
            plot=ax2,
            xdata=lasfile['RHOB'],
            ydata=lasfile['DEPT'],
            color='b',
            x_label='Density (g/cm3)',
            scatter=True,
            scatter_x=density,
            scatter_y=depth,
            linewidth=1.0,
            hide_tick=2,
            xlim_low=2.3,
            xlim_high=3.0
            )

    # Track 3: NPHI
    subplot_curve(
            plot=ax3,
            xdata=lasfile['NPHI']*100,
            ydata=lasfile['DEPT'],
            color='c',
            x_label='Porosity (%)',
            linewidth=1.0,
            scatter=True,
            scatter_x=porosity,
            scatter_y=depth,
            scatter_alpha=0.6,
            scatter_color='b',
            xlim_high=20
            )

    plt.show()


def depth_intervals_cores(
        xdata,
        ydata,
        xlabel='',
        ylabel='',
        xscale='linear',
        yscale='linear',
        xsize=9,
        ysize=5,
        color='b'
        ):
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

    f1, (ax1) = plt.subplots(1, 1, figsize=(xsize, ysize))

    plt.gca().invert_yaxis()

    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6

    # track
    subplot_curve(
            plot=ax1,
            plot_curve=False,
            x_label=xlabel,
            y_label=ylabel,
            scatter=True,
            scatter_x=xdata,
            scatter_y=ydata,
            scatter_alpha=0.5,
            scatter_color=color,
            x_scale=xscale,
            y_scale=yscale,
            xtick='bottom',
            removelast=False
            )

    plt.show()


def depth_intervals_porosity(xdata, ydata, cdata, xlabel, ylabel, clabel, graphlabel, yscale='linear'):

    f1, (ax1) = plt.subplots(figsize=plt.figaspect(0.45))

    subplot_curve(
            plot=ax1,
            fig=f1, 
            plot_curve=False, 
            x_label=xlabel, 
            y_label=ylabel, 
            graph_label = graphlabel, 
            scatter=True, 
            scatter_x=xdata, 
            scatter_y=ydata, 
            scatter_color=cdata,
            scatter_alpha = 1,
            scatter_cmap="jet", 
            color_bar=True, 
            color_bar_label=clabel,
            label_position='bottom', 
            grid=False,
            y_scale=yscale,
            removelast=False,
            )

    plt.show()

def depth_intervals_porosity(xdata, ydata, cdata, xlabel, ylabel, clabel, graphlabel, yscale='linear'):

    f1, (ax1) = plt.subplots(figsize=plt.figaspect(0.45))

    subplot_curve(
            plot=ax1,
            fig=f1, 
            plot_curve=False, 
            x_label=xlabel, 
            y_label=ylabel, 
            graph_label = graphlabel, 
            scatter=True, 
            scatter_x=xdata, 
            scatter_y=ydata, 
            scatter_color=cdata,
            scatter_alpha = 1,
            scatter_cmap="jet", 
            color_bar=True, 
            color_bar_label=clabel,
            label_position='bottom', 
            grid=False,
            y_scale=yscale,
            removelast=False,
            )

    plt.show()

def scattered_graph(
        xdata,
        ydata,
        cdata=[],
        xlabel='',
        ylabel='',
        clabel='',
        graphlabel='',
        xscale='linear',
        yscale='linear',
        colormap='jet',
        colorbar=False,
        legend=False,
        legend_list=[],
        orientation=270,
        xsize=15,
        ysize=9,
        xlim=0,
        ylim=0,
        y_reverse=False,
        grid=False,
        grid_color='g',
        grid_alpha=0.3,
        scatter_alpha=1
        ):
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
        label printed on the colormap or legend
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
    colorbar: boolean
        defines wether or not to print a colorbar
        default is False
    legend: boolean
        defines wether or not to print a legend
        default is False
    legend_list: list
        list of labels for the legend
        default is an empty list
    orientation: int or float
        orientation of the clabel in degrees
        default is 270
    xsize: integer
        defines the size of the graph in the x direction
        default is 15
    ysize: integer
        defines the size of the graph in the y direction
        default is 9
    xlim: integer or float
        custom limit of the x axes
        default is 0 (limit based on the data)
    ylim: integer or float
        custom limit of the y axes
        default is 0 (limit based on the data)

    """
    plt.figure(figsize=(xsize, ysize))

    plt.rcParams.update({'image.cmap': colormap})

    if y_reverse:
        plt.gca().invert_yaxis()

    if type(cdata) == list:
        scatter = plt.scatter(
                               x=xdata,
                               y=ydata,
                               c=cdata,
                               cmap=colormap,
                               alpha=scatter_alpha
                             )
    else:
        scatter = plt.scatter(
                               x=xdata,
                               y=ydata,
                               c=cdata,
                               alpha=scatter_alpha
                             )
    plt.title(graphlabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xscale(xscale)
    plt.yscale(yscale)
    if xlim != 0:
        plt.xlim(0, xlim)
    if ylim != 0:
        plt.ylim(0, ylim)
    if colorbar:
        cbar = plt.colorbar()
        cbar.set_label(clabel, rotation=orientation)
    if legend:
        plt.legend(handles=scatter.legend_elements()[0],
                   labels=legend_list,
                   title=clabel)
    if grid:
        plt.grid(grid, c=grid_color, alpha=grid_alpha)
    plt.show()
