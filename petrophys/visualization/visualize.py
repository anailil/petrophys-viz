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

def well_curve()

    f1, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, sharey=True, figsize=(18,16))
    f1.subplots_adjust(wspace=0.02)
    plt.gca().invert_yaxis()
    
    # So that y-tick labels appear on left and right
    plt.tick_params(labelright=True)
    
    # Change tick-label globally
    mpl.rcParams['xtick.labelsize'] = 6
    
    #track1: Gamma Ray
    plot_well_curve(ax1, lasfile['GR'], lasfile['DEPT'], 'c', 'GR (API)', 'DEPTH (m)',hide_tick=2)
    
    # Track 2: Sonic (velocities)
    plot_well_curve(ax2, lasfile['DT']/0.3048, lasfile['DEPT'], 'r', 'DT (m/s)', 'DEPTH (m)', 'DTCO')
    
    # Track 3: RHOB (Bulk Density)
    plot_well_curve(ax3, lasfile['RHOB'], lasfile['DEPT'], 'b', 'RHOB (g/cm3', 'DEPTH (m)')
    
    # Track 4: DRHO
    plot_well_curve(ax4, lasfile['DRHO'], lasfile['DEPT'], 'g', 'DRHO (g/cm3)', 'DEPTH (m)')
    
    # Track 5: NPHI
    plot_well_curve(ax5, lasfile['NPHI'], lasfile['DEPT'], 'k', 'NPHI (v/v)', 'DEPTH (m)')
    
    plt.show()
