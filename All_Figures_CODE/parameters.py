import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np
import scipy.io as scio
from scipy import interpolate
import os



#mpl.rcParams['text.usetex'] = True
#mpl.rcParams['text.latex.preview'] = True
#plt.rc('font', family='serif')

loc_general="E:/2023-2024/2023-07-11-manips-10-voies/"
#"D:/Users/Manips/Documents/DATA/FRICS/2023/2023-07-11-manips-10-voies/"

# chose experiments
chosen_manips_fig1=[38,13,26,30]#34 ou 36, fréquent cool, ou 4, profil plat

chosen_manips_fig2=np.array(chosen_manips_fig1)[[0,-1]]

chosen_manip_fig41=44
chosen_event_fig41=2

chosen_manip_fig41_sec=33
chosen_event_fig41_sec=14

chosen_manip_fig42=29
chosen_manip_fig42_sec=16


chosen_manip_fig5=34

force_reload=True

bins=np.array([-1,-0.5,0,1,2])

pad_title_hists=-7

solids = [14,15,16,17,18,37,38]


differentiate_solids_fig_3 = True

x_plot=(np.array([1,2,3,4,5,8,11,12,13,14])-0.5)*10

# chose colors
solid_solid_color = "navy"
granular_color = "peru"
solid_in_granular_color="royalblue"
hole_in_solid_color="navy"
main_plot_color = "dodgerblue"
secondary_plot_color = "lightsteelblue"
error_bar_color="grey"
error_bar_alpha=1
dashed_color="k"
secondary_plot_alpha = 0.5


# chose sizes and shapes
scatter_size = 15
scatter_marker = "d"
solid_marker = "o"
error_bar_width=1.5
markeredgewidth=.5
dash_line_style = ":"

SMALL_SIZE = 7
MEDIUM_SIZE = 8
LARGE_SIZE = 9

LETTER_SIZE=7.5

INSET_SMALL_SIZE = 5
INSET_MEDIUM_SIZE = 6
INSET_LARGE_SIZE = 7
inset_label_pad = 1



# chose line width
main_linewidth=.5

# chose names
sliding_perc_name_full = r"Inter-event slip"
sliding_perc_name_short = r"$S=\delta_{IE}/\delta_{tot}$"

sliding_ie_name_full = r"Inter-event slip (mm)"
sliding_ie_name_short = r"$\delta_{IE}$ (mm)"

hists_y_label = r"$N_{event}~/~N_{tot}$"
hists_y_label_2 = r"$N_{SL}~/~N_{event}$"

freq_name_full = "Average stick-slip frequency (Hz)"
#freq_name_short = r"$\left< f_{ss} \right>$ (Hz)"
freq_name_short = r"$\left< 1/\Delta T \right>$ (Hz)"

tot_sliding_full = "Total sliding (mm)"
tot_sliding_short = "$\delta_{tot}$ (mm)"

LC_name_long = "Loading contrast"
LC_name_short = r"C_{\sigma}"


dpi_global = 1200


# set up grid
grid_major_color="darkgray"
grid_major_width=.5
grid_major_lines="-"
grid_major_alpha=.5
grid_minor_color="lightgray"
grid_minor_width=.1
grid_minor_lines="-"
grid_minor_alpha=.3

mm=1/25.4


# Sizes (w,h)
size_fig_1 = (186*mm, 90*mm)
size_fig_1d = (90*mm, 70*mm)
size_fig_2 = (90*mm, 76*mm)
size_fig_3 = (90*mm, 60*mm)
size_fig_4= (180*mm, 130*mm)
size_fig_5= (180*mm, 130*mm)
size_fig_S2 = ((180)*mm, 140*mm)

size_fig_6 = (90*mm, 45*mm)







# # # # # #







# ggplot_styles = {
#     'axes.edgecolor': 'white',
#     'axes.facecolor': 'EBEBEB',
#     'axes.grid': True,
#     'xtick.major.bottom': True,
#     'xtick.minor.bottom': False,
#     'ytick.major.left': True,
#     'ytick.minor.left': False
# }

#plt.rcParams.update(ggplot_styles)


def set_grid(axes):
    if type(axes)==list:
        axes=np.array(axes)
    if type(axes)==np.ndarray:
        for ax in axes.flatten():
            ax.grid(True,which='major', color=grid_major_color, linestyle=grid_major_lines, linewidth=grid_major_width,alpha=grid_major_alpha)
            ax.grid(True,which='minor', color=grid_minor_color, linestyle=grid_minor_lines, linewidth=grid_minor_width,alpha=grid_minor_alpha)
            ax.set_facecolor('none')
            ax.set_axisbelow(True)
    else:
        axes.grid(True,which='major', color=grid_major_color, linestyle=grid_major_lines, linewidth=grid_major_width,alpha=grid_major_alpha)
        axes.grid(True,which='minor', color=grid_minor_color, linestyle=grid_minor_lines, linewidth=grid_minor_width,alpha=grid_minor_alpha)
        axes.set_facecolor('white')





mpl.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
mpl.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
mpl.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
mpl.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
mpl.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
mpl.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
mpl.rc('figure', titlesize=LARGE_SIZE)  # fontsize of the figure title
mpl.rcParams['lines.linewidth'] = main_linewidth
mpl.rcParams['axes.facecolor'] = 'none'
mpl.rcParams['axes.linewidth'] = .5
mpl.rcParams['xtick.major.width'] = .5
mpl.rcParams['xtick.minor.width'] = .3
mpl.rcParams['ytick.major.width'] = .5
mpl.rcParams['ytick.minor.width'] = .3
mpl.rcParams['xtick.major.size'] = 2.5
mpl.rcParams['xtick.minor.size'] = 1
mpl.rcParams['ytick.major.size'] = 2.5
mpl.rcParams['ytick.minor.size'] = 1
mpl.rcParams['xtick.major.pad']='1'
mpl.rcParams['ytick.major.pad']='1'


def real_tight_layout(fig):
    fig.tight_layout()
    fig.align_labels()
    left, right, bottom, top, wspace, hspace = fig.subplotpars.left, fig.subplotpars.right, fig.subplotpars.bottom, fig.subplotpars.top, fig.subplotpars.wspace, fig.subplotpars.hspace
    fig.subplots_adjust(left=left, right=right, bottom=bottom, top=top)
    return(left, right, bottom, top, wspace, hspace)







def set_up_inset(axin):
    axin.tick_params(labelsize=INSET_SMALL_SIZE)
    axin.set_xlabel(axin.get_xlabel(),fontsize=INSET_MEDIUM_SIZE)
    axin.set_ylabel(axin.get_ylabel(),fontsize=INSET_MEDIUM_SIZE)
    for line in axin.lines:
        line.set_linewidth(.5)
    axin.tick_params(axis='y', pad=1)
    axin.tick_params(axis='x', pad=1)



