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
        c_label='',
        graph_label='',
        graph_position='top',
        linewidth=0.5,
        label_position='top',
        grid=True,
        grid_color='g',
        grid_alpha=0.3,
        hide_tick=0,
        xlim_low=None,
        xlim_high=None,
        ylim_low=None,
        ylim_high=None,
        cores=[],
        core_linewidth=5.0,
        core_alpha=0.7,
        x_scale='linear',
        y_scale='linear',
        xtick='top',
        color_bar=False, 
        color_bar_label='', 
        color_bar_rotation=270,
        removelast=True,
        legend_scattered=False,
        legend_list=[],
        legend_curve=False,
        xtick_size=6,
        ytick_size=10,
        invert_x=False,
        invert_y=False,
        ):

    """Function to plot a graph based on the given parameters

    Parameters
    ----------
    plot: axes of a figure
    fig: figure
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
        Default is empty
    scatter_y: list of floats or integers
        Represents the y axes of the graph
        Default is empty
    scatter_alpha: float 
        Alpha adds transparency to a color, the range is from 0.0-1.0.
        Default is 0.3
    scatter_color: str
        color of the dots when using a single color
        see https://matplotlib.org/stable/gallery/color/named_colors.html or
            https://matplotlib.org/stable/users/explain/colors/colors.html for color options
        Default is g (green)
    scatter_cmap: str
        colormap of the dots when the color of the dots represents a value. 
        see https://matplotlib.org/stable/gallery/color/colormap_reference.html for options
        Default is empty
    x_label: str
        label printed on the x axes
        Default is empty
    y_label: str
        label printed on the y axes
        Default is empty
    c_label: str
        label printed on the legend of the colors of the dots.
        Default is empty
    graph_label: str
        Title of the graph.
        Default is empty
    graph_position: str
        Defines the position of the grapg label
        Default is top
    linewidth: float
        Defines the linewidth of the graph
        Default is 0.5
    label_position: str
       Defines the position of the x-axes label.
       Default is top
    grid: Boolean
        Defines wether or not to show a grid.
        Default = True
    grid_color: str
        color of the grid
        see https://matplotlib.org/stable/gallery/color/named_colors.html or
            https://matplotlib.org/stable/users/explain/colors/colors.html for color options
        Default is g (green)
    grid_alpha=: float
        Alpha adds transparency to a color, the range is from 0.0-1.0.
        Default is 0.3
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
        Default is empty
    core_linewidth: float
        Defines the thickness of the cores line
        Default is 5.0
    core_alpha: float
        Alpha adds transparency to a color, the range is from 0.0-1.0.
        Default is 0.3
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
    color_bar: Boolean
        Defines wether or not to show a colorbar next to the graph
        Default is False
    color_bar_label: str
        Defines the label of the colorbar
        Default is empty
    color_bar_rotation: float
        Defines the angle in whoch to show the colorbar label
        Default: 270
    removelast: Boolean
        Wether or not to call the removelast function for cleaner graphs.
        default is True
    legend_scattered : Boolean
        Defines wether or not to display a legend
        Default is False
    legend_curve : Boolean
        Defines wether or not to plot a legend with a curve
        Default is False,
    legend_list: list
        Defines the values to show on the legend 
        Default is empty
    xtick_size: float or str
        Defines the size of the xtick labels
        Default is 6
    ytick_size: float or str
        Defines the size of the ytick labels
        Default is 10
    invert_x: Boolean
        Defines wether or not to invert the x-axes
        Default is False,
    invert_y: Boolean
        Defines wether or not to invert the y-axes
        Default is False,
    """

    if cores != []:
        plot.plot(*cores, linewidth=core_linewidth, alpha=core_alpha)

    if plot_curve:
        plot.plot(xdata, ydata, color, label=x_label, linewidth=linewidth)

    if scatter and not color_bar:
        if scatter_cmap == '':
            scattered = plot.scatter(scatter_x, scatter_y, alpha=scatter_alpha, c=scatter_color)
        else:
            scattered = plot.scatter(scatter_x, scatter_y, alpha=scatter_alpha, c=scatter_color, cmap=scatter_cmap)

    if scatter and color_bar:
        scattered = plot.scatter(scatter_x,scatter_y,alpha=scatter_alpha,c=scatter_color, cmap=scatter_cmap)
        cbar = fig.colorbar(scattered, ax=plot, cmap=scatter_cmap)
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
    plot.tick_params(axis='x', labelsize=xtick_size)
    plot.tick_params(axis='y', labelsize=ytick_size)

    if grid:
        plot.grid(grid, c=grid_color, alpha=grid_alpha)

    if invert_x:
        plot.set_xlim(xlim_high, xlim_low)
    else:
        plot.set_xlim(xlim_low, xlim_high)

    if invert_y:
        plot.set_ylim(ylim_high, ylim_low)
    else:
        plot.set_ylim(ylim_low, ylim_high)

    if hide_tick != 0:
        # Hide ticks defined by every hide_tick
        plt.setp(plot.get_xticklabels()[1::hide_tick], visible=False)

    if legend_scattered:
        plot.legend(handles=scattered.legend_elements()[0],
                   labels=legend_list,
                   title=c_label)

    if legend_curve:
        plot.legend()

    if removelast:
        remove_last(plot)

    return fig

def well_curve2(GRAPHS, invert_x=False, invert_y=False, xlim_high=None, xlim_low=None, ylim_high=None, ylim_low=None, xsize=18, ysize=16):
    """ Plots the  graphs given in the GRAPHS variable

    Parameters
    ----------
    GRAPHS: list
        List of Lists of graph data
        One graph list has the following data:

        [   line width: float, 
            color:str, 
            hide ticks:int, 
            graph label:str, 
            x label:str, 
            x data:list, 
            y label:str, 
            y data:list, 
            low limit x-axes: float, 
            high limit x-axes: float, 
            print a legend: boolean
        ]

    invert_x: Boolean
        Defines wether or not to invert the x-axes
        Default is False, 
    invert_y: Boolean
        Defines wether or not to invert the y-axes
        Default is False, 
    xlim_high: Float
        Defines the high limit of the X-axes
        Default is None 
    xlim_low: Float
        Defines the low limit of the X-axes
        Default is None 
    ylim_high: Float
        Defines the high limit of the y-axes
        Default is None 
    ylim_low: Float
        Defines the low limit of the y-axes
        Default is None 
    xsize: float or integer
        size of the figure in the horizontal direction
        Default is 18
    ysize: float or integer
        size of the figure in the vertical direction
        Default is 16
    """
    f1, (axs) = plt.subplots(ncols=len(GRAPHS), nrows=1, sharey=True, figsize=(xsize, ysize))

    f1.subplots_adjust(wspace=0.02)

    # So that y-tick labels appear on left and right
    plt.tick_params(labelright=True)

    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6

    number_of_graphs = len(GRAPHS)

    for i in range(number_of_graphs):
        graphlabel = ''
        for j in range(len(GRAPHS[i])):
            if len(GRAPHS[i]) > 1:
                graphlabel = graphlabel + GRAPHS[i][j][3]
            else:
                graphlabel = GRAPHS[i][j][3]

            if number_of_graphs == 1:
                plot_graph=axs
            else:
                plot_graph=axs[i]

            subplot_curve(
                plot=plot_graph,
                xdata=GRAPHS[i][j][5],
                ydata=GRAPHS[i][j][7],
                color=GRAPHS[i][j][1],
                x_label=GRAPHS[i][j][4],
                y_label=GRAPHS[i][j][6],
                graph_label=graphlabel,
                hide_tick=GRAPHS[i][j][2],
                ylim_low=ylim_low,
                ylim_high=ylim_high,
                xlim_low=GRAPHS[i][j][8],
                xlim_high=GRAPHS[i][j][9],
                invert_x=invert_x,
                invert_y=invert_y,
                linewidth=GRAPHS[i][j][0],
                legend_curve=GRAPHS[i][j][10]
                )

    plt.show()

def well_curve(lasfile, xsize=18, ysize=16):
    """ Plots the GR, DT, RHOB, DRHO and NPHI vs Depth graphs of the given lasio file

    Parameters
    ----------
    lasfile: lasio dataset
    xsize: float or integer
        size of the figure in the horizontal direction
        Default is 18
    ysize: float or integer
        size of the figure in the vertical direction
        Default is 16
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
        Default is 8
    ysize: float or integer
        size of the figure in the vertical direction
        Default is 7

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
        Default is empty
    ylabel: str
        label printed on the y axes
        Default is empty
    xscale: str
        scale of the x axes, can take "linear' or 'log'
        default is linear
    yscale: str
        scale of the y axes, can take "linear' or 'log'
        default is linear
    xsize: float or integer
        size of the figure in the horizontal direction
        Default is 9
    ysize: float or integer
        size of the figure in the vertical direction
        Default is 5
    color: str
        color of the dots
        see https://matplotlib.org/stable/gallery/color/named_colors.html or
            https://matplotlib.org/stable/users/explain/colors/colors.html for color options
        default is b (blue)
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

    """Plot a scattered graph for xdata, ydata and cdata width a colorbar

    Parameters
    ----------
    xdata: list of floats or integers
        xdata represents the x axes of the graph
    ydata: list of floats or integers
        ydata represents the y axes of the graph
    cdata: list of floats or integers
        cdata represents the y axes of the graph
    xlabel: str
        label printed on the x axes
        Default is empty
    ylabel: str
        label printed on the y axes
        Default is empty
    clabel: str
        label printed on the colorbar
        Default is empty
    graphlabel: str
        label of the graph
        Default is empty
    yscale: str
        scale of the y axes, can take "linear' or 'log'
        default is linear
    """

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

def youngs_modulus_vs_depth(xdata, ydata, cdata, xlabel, ylabel, clabel, graphlabel, legend_list=[]):

    """Plot a scattered graph for xdata, ydata and cdata with a legend

    Parameters
    ----------
    xdata: list of floats or integers
        xdata represents the x axes of the graph
    ydata: list of floats or integers
        ydata represents the y axes of the graph
    cdata: list of floats or integers
        cdata represents the y axes of the graph
    xlabel: str
        label printed on the x axes
        Default is empty
    ylabel: str
        label printed on the y axes
        Default is empty
    clabel: str
        label printed on the colorbar
        Default is empty
    graphlabel: str
        label of the graph
        Default is empty
    legend_list: list
        Defines the values displayed on the legend
        default is empty
    """

    f1, (ax1) = plt.subplots(1, 1, figsize=(15, 9))

    subplot_curve(
            plot=ax1,
            fig=f1, 
            plot_curve=False, 
            x_label=xlabel, 
            label_position='bottom',
            y_label=ylabel, 
            c_label=clabel, 
            graph_label = graphlabel, 
            scatter=True, 
            scatter_x=xdata, 
            scatter_y=ydata, 
            scatter_color=cdata,
            scatter_alpha = 1,
            scatter_cmap="tab10", 
            xlim_high=6000,
            ylim_high=100,
            xtick='bottom',
            legend_scattered=True,
            legend_list=legend_list,
            grid=False,
            removelast=False,
            )

    plt.show()

