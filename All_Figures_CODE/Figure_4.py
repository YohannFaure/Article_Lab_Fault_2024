## Imports
# Science
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

# custom file
try :
    import sys
    sys.path.insert(0, "D:/Users/Manips/Documents/Python/DAQ_Python")
    from Python_DAQ import *
except :
    from DAQ_Python.Python_DAQ import *

with open("E:/Article/parameters.py", 'r') as f:
        exec(f.read())





reload = False

try:
    loaded_data = np.load("E:/Article/Figure_4/figure_4.npy",allow_pickle=True).all()
    locals().update(loaded_data)
except:
    reload = True


########################## create figure



# nested gridspecs, yeaaaaah...
fig = plt.figure()
fig.set_size_inches(size_fig_4)

gs0 = gridspec.GridSpec(2, 1, figure=fig, height_ratios = [9,3],
                      left=0.06, right=0.97,
                      top=0.98,bottom=0.06,
                      hspace=0.2, wspace=0)

#nrows=nrows, ncols=11, left=0.06, right=0.97,
#                      top=0.98,bottom=0.06,
#                      hspace=0, wspace=0

gs00 = gridspec.GridSpecFromSubplotSpec(10, 3, subplot_spec=gs0[0],
                      width_ratios = [5,0.8,5],
                      hspace=0, wspace=0)

axes_1=[]
axes_3=[]

for i in range(10):
    axes_1.append( fig.add_subplot(gs00[i,0]) )
    axes_1[-1].sharex(axes_1[0])
    axes_1[-1].sharey(axes_1[0])

    axes_3.append( fig.add_subplot(gs00[i, -1]) )
    axes_3[-1].sharex(axes_3[0])
    axes_3[-1].sharey(axes_1[0])




gs01 = gridspec.GridSpecFromSubplotSpec(1, 7, subplot_spec = gs0[1],
                      width_ratios = [1,1,1,1,1,0.6,2],
                      hspace=0, wspace=0)
axes_2=[]
for i in range(5):
    axes_2.append( fig.add_subplot(gs01[0, i]) )
    axes_2[-1].sharex(axes_2[0])
    axes_2[-1].sharey(axes_2[0])


gs02 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec = gs01[-1],
                      height_ratios = [0.5,1],
                      hspace=0, wspace=0)

ax_4 = fig.add_subplot(gs02[-1])
ax_drawing = fig.add_subplot(gs02[0])








########################## Data for propagation


# main folder
loc_folder=loc_general+"/manip_{}/".format(chosen_manip_fig41)
# name of the file / event
loc_file="event-00{}.npy".format(chosen_event_fig41)
# name of the reference file, containing unloaded signal, usually event-001
loc_file_zero = "event-001.npy"
# parameters file
loc_params="parameters.txt"

# control smoothing of the data (rolling average) and starting point
roll_smooth=5
start=0
n_plot=10

## Location of the data inside the file
# channels containing the actual strain gages
gages_channels = np.concatenate([np.arange(0,15),np.arange(16,31)])
# channels containing the normal and tangetial force
forces_channels = [32,33]
# channel containing the trigger
trigger_channel = 34

## Parameters
# default x, just in case there's nothing in the saved params
x=np.array([1,2,3,4,5,8,11,12,13,14])*1e-2 -0.005
# Load the params file, and extract frequency of acquisition







if force_reload or reload :
    print("reloading data for Figure 4")

    exec(load_params(loc_folder+loc_params))
    sampling_freq_in = clock/10
    # Create the location strings
    loc=loc_folder+loc_file
    loc_zero=loc_folder+loc_file_zero
    # Number of channels
    nchannels = len(gages_channels)

    # Fast acquicition
    # Load data


    data=np.load(loc,allow_pickle=True)
    data_zero=np.load(loc_zero,allow_pickle=True)

    # smooth data
    data=smooth(data,roll_smooth)
    data=np.transpose(np.transpose(data)-np.mean(data_zero,axis=1))

    # assign specific channels to specific variables
    forces=data[forces_channels,:]
    mu = data[forces_channels[1],:].mean() / data[forces_channels[0],:].mean()
    gages = data[gages_channels]
    gages_zero = data_zero[gages_channels]
    gages=np.transpose(np.transpose(gages)-np.mean(gages_zero,axis=-1))
    fast_time=np.arange(len(gages[0]))/sampling_freq_in

    for i in range(nchannels//3):
        ch_1=gages[3*i]
        ch_2=gages[3*i+1]
        ch_3=gages[3*i+2]
        ch_1,ch_2,ch_3=voltage_to_strains(ch_1,ch_2,ch_3)
        ch_1,ch_2,ch_3=rosette_to_tensor(ch_1,ch_2,ch_3)
        #ch_1,ch_2,ch_3=eps_to_sigma(ch_1,ch_2,ch_3,E=E,nu=nu)
        gages[3*i]=ch_1
        gages[3*i+1]=ch_2
        gages[3*i+2]=ch_3


    # axes 1

    indexes=np.load(loc+"_times_hand_picked.npy")+0.007/1000
    indexes[0]-=0.013/1000
    indexes[2]-=0.003/1000
    indexes[5]=0
    indexes[-1]-=0.01/1000


## plot data
# lines propag
xs=[0.17,0.155,0.215]
ys=[0.7,0.775,0.97]
line = mpl.lines.Line2D(xs, ys, lw=1, color='r', alpha=1)
fig.add_artist(line)

xs=[0.31,0.35]
ys=[0.6,0.4]
line = mpl.lines.Line2D(xs, ys, lw=1, color='r', alpha=1)
fig.add_artist(line)



color=[solid_in_granular_color]*5+[granular_color]+[solid_in_granular_color]*4

for i in range(10):
    axes_1[i].plot(1000*fast_time[start:]-1000*fast_time.mean(),1000*(gages[3*(i+1)-1][start:]-gages[3*(i+1)-1][0:10000].mean()),color=color[i])
    axes_1[i].ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    axes_1[i].grid("both")
    # dashes
    axes_1[i].axvline(x=indexes[i]*1000-1000*fast_time.mean(),c="k",linestyle="--")

axes_1[3].scatter(indexes[3]*1000-1000*fast_time.mean(), 0, s=50, marker='*', color='r', zorder=3)
fig.text(0.12, 0.88, r"$c_f\sim 800$ m/s", size = INSET_SMALL_SIZE, rotation =0, c="r")
fig.text(0.34, 0.51, r"$c_f\sim 1000$ m/s", size = INSET_SMALL_SIZE, rotation = 0,c="r")
#txt1.set_bbox(dict(facecolor='white', alpha=0.5, linewidth=0))



axes_1[-1].set_xlabel('time (ms)')
axes_1[4].set_ylabel(r'$\varepsilon_{xy}-\varepsilon_{xy}^0$ (mStrain)',size=MEDIUM_SIZE)


# adjust ticks
axes_1[-1].set_xlim([-0.16,0.06])
axes_1[-1].set_xticks([-0.15,-0.1,-0.05,0,0.05])
axes_1[-1].set_xticklabels(["-$0.15$","-$0.1$","-$0.05$","$0$","$0.05$"])
axes_1[-1].set_ylim([-0.19,0.06])
axes_1[-1].set_yticks([-0.1,0])
axes_1[-1].set_yticklabels(["$-0.1$","$0$"])



for i in range(9):
    plt.setp(axes_1[i].get_yticklabels(), visible=False)
    plt.setp(axes_1[i].get_xticklabels(), visible=False)




labels = [r"$x=5 \pm 0.25$ mm"]+[r"$x={}$".format(i) for i in [int(x_plot[i]) for i in range(1,len(x_plot))]]

# Iterate through each subplot and add data
for i, ax in enumerate(axes_1):
    ax.annotate(labels[i], xy=(0.025, 0.1), xycoords='axes fraction',
                xytext=(10, 0), textcoords='offset points',
                va="center",size=5)





# LC :
loc_folder=loc_general

if reload or force_reload:
    data_loaded=np.load(loc_folder+"python_plots/summary_data.npy",allow_pickle=True).all()


mean_lc=data_loaded["mean_lc"]
manip_num=np.array(data_loaded["manip_num"])
LC_here = mean_lc[manip_num==chosen_manip_fig41][0]


axes_1[0].annotate("${}=${:.2f}".format(LC_name_short,LC_here), xy=(0.8, 0.85), xycoords='axes fraction',
                xytext=(10, 0), textcoords='offset points',
                va="center",size=5)



set_grid(axes_1)



for i in range(1,5):
    plt.setp(axes_2[i].get_yticklabels(), visible=False)
    plt.setp(axes_2[i].get_yticklabels(), visible=False)



########################## Data for starting point

## Nice plot
def temp_nice_plot(y_min,x, ax = None ,ylim=None) :
    """
    plots a nice representation of the bloc in an histogram
    Useful way later
    """
    if ax is None:
        ax=plt.gca()
    if ylim is None:
        ylim=ax.get_ylim()
    else:
        ylim=ylim
    dilat = (ylim[1]-ylim[0])*0.7
    ax.set_ylim((y_min-0.1*dilat,ylim[1]))
    import matplotlib.patches as patches
    arc_radius = 0.05*dilat
    arc_center_x = 75
    arc_center_y = y_min
    start_angle = 0
    end_angle = 180
    arc_patch = patches.Arc((arc_center_x, arc_center_y), width=30, height=2*arc_radius, angle=0,
                            theta1=start_angle, theta2=end_angle, edgecolor=secondary_plot_color, linewidth=1)
    ax.add_patch(arc_patch)

    # lines of the block
    line1 = patches.ConnectionPatch((0, y_min), (60, y_min), "data", "data", edgecolor=secondary_plot_color, linewidth=1, arrowstyle="-")
    ax.add_patch(line1)
    line2 = patches.ConnectionPatch((90, y_min), (150, y_min), "data", "data", edgecolor=secondary_plot_color, linewidth=1, arrowstyle="-")
    ax.add_patch(line2)
    line3 = patches.ConnectionPatch((0, y_min), (0, y_min+0.25*dilat), "data", "data", edgecolor=secondary_plot_color, linewidth=1, arrowstyle="-")
    ax.add_patch(line3)
    line4 = patches.ConnectionPatch((150, y_min), (150, y_min+0.25*dilat), "data", "data", edgecolor=secondary_plot_color, linewidth=1, arrowstyle="-")
    ax.add_patch(line4)

    # gages, used and unused
    width_patch=(x[1]-x[0])/50
    for xi in x:
        if xi != 75.:
            square_patch = patches.Rectangle((xi-width_patch, y_min+0.07*dilat), 2*width_patch, 0.01*dilat, color=solid_in_granular_color,alpha=1)
        else:
            square_patch = patches.Rectangle((xi-width_patch, y_min+0.07*dilat), 2*width_patch, 0.01*dilat, color=granular_color,alpha=1)
        ax.add_patch(square_patch)




def temp_nice_plot_large(y_min,x, ax = None ,ylim=None) :
    """
    plots a nice representation of the bloc in an histogram
    Useful way later
    """
    if ax is None:
        ax=plt.gca()
    if ylim is None:
        ylim=ax.get_ylim()
    else:
        ylim=ylim
    dilat = (ylim[1]-ylim[0])*0.7
    ax.set_ylim((y_min-0.1*dilat,ylim[1]))
    import matplotlib.patches as patches
    arc_radius = 0.05*dilat
    arc_center_x = 75
    arc_center_y = y_min
    start_angle = 0
    end_angle = 180
    arc_patch = patches.Arc((arc_center_x, arc_center_y), width=30, height=3*arc_radius, angle=0,
                            theta1=start_angle, theta2=end_angle, edgecolor=secondary_plot_color, linewidth=1)
    ax.add_patch(arc_patch)

    # lines of the block
    line1 = patches.ConnectionPatch((0, y_min), (60, y_min), "data", "data", edgecolor=secondary_plot_color, linewidth=1, arrowstyle="-")
    ax.add_patch(line1)
    line2 = patches.ConnectionPatch((90, y_min), (150, y_min), "data", "data", edgecolor=secondary_plot_color, linewidth=1, arrowstyle="-")
    ax.add_patch(line2)
    line3 = patches.ConnectionPatch((0, y_min), (0, y_min+0.25*dilat), "data", "data", edgecolor=secondary_plot_color, linewidth=1, arrowstyle="-")
    ax.add_patch(line3)
    line4 = patches.ConnectionPatch((150, y_min), (150, y_min+0.25*dilat), "data", "data", edgecolor=secondary_plot_color, linewidth=1, arrowstyle="-")
    ax.add_patch(line4)

    # gages, used and unused
    width_patch=(x[1]-x[0])/10
    for xi in x:
        if xi != 75.:
            square_patch = patches.Rectangle((xi-width_patch, y_min+0.15*dilat), 2*width_patch, 0.03*dilat, color=solid_in_granular_color,alpha=1)
        else:
            square_patch = patches.Rectangle((xi-width_patch, y_min+0.15*dilat), 2*width_patch, 0.03*dilat, color=granular_color,alpha=1)
        ax.add_patch(square_patch)



## Data location
# location of the main folder containing all the "manip_..." subfolders

loc_folder=loc_general
loc_figures = loc_folder + "histograms/"
loc_manip = "manip_{}/"
loc_params="parameters.txt"



## Load all data


if reload or force_reload:
    data_loaded_3=np.load(loc_folder+"python_plots/summary_data_2.npy",
                    allow_pickle=True).all()



index_start= np.array(data_loaded_3["start_per_event"])
loading_contrast = np.array(data_loaded_3["lc_per_event"])
from_solid=np.array(data_loaded_3["solid_per_event"])




## Define histograms

n_bin=len(bins)-1

def make_hists(bins, bin_variable, to_count):
    hists = []
    for i in range(n_bin):
        hists.append([([to_count[k]
                            for k in range(len(to_count))
                            if  bin_variable[k]<bins[i+1]
                            and bin_variable[k]>=bins[i]
                        ]).count(j) for j in range(10)])
    hists=np.array(hists)
    return(hists)


histogram_start_solid = np.array([list(index_start[from_solid]).count(i) for i in range(10)])
histograms_start=make_hists(bins, loading_contrast[np.logical_not(from_solid)], index_start[np.logical_not(from_solid)])





## Plot data axis 2

hist_y_lim=[-0.08,1]

y_min=-0.05
pad_title = pad_title_hists
y_title = 1+1e-50
width=0.8*min(np.diff(x_plot))


meanstarts_left  =[]
meanstarts_right =[]

for i in range(5):
    ax=axes_2[i]
    if i==0:
        ax.bar(x_plot, histogram_start_solid/histogram_start_solid.sum(),
                width=width,
                color = solid_solid_color,
                linewidth=.1,edgecolor='k')
        ax.set_title("Empty-hole", pad=pad_title,y=y_title,size=6)
        temp_nice_plot(y_min,x_plot,ax=ax,ylim=None)
        ax.grid(True,which="both")
        meanstart = (x_plot*histogram_start_solid).sum()/histogram_start_solid.sum()
        meanstarts_left.append(meanstart)
        meanstarts_right.append(meanstart)
        ax.axvline(x=meanstart, ymax=0.8,linestyle='--',c='k')

    else:
        ax.bar(x_plot, histograms_start[i-1]/histograms_start[i-1].sum(),
                width=width,
                color = main_plot_color,linewidth=.1,edgecolor='k')
        ax.set_title(r"{}$\leq${}<{}".format(bins[i-1],r"${}$".format(LC_name_short),bins[i]), pad=pad_title, y=y_title,size=6)
        temp_nice_plot(y_min,x_plot,ax=ax,ylim=None)
        ax.grid(True,which="both")
        meanstart_left = (x_plot*histograms_start[i-1])[x_plot>75.].sum()/histograms_start[i-1][x_plot>75.].sum()
        meanstart_right= (x_plot*histograms_start[i-1])[x_plot<75.].sum()/histograms_start[i-1][x_plot<75].sum()
        ax.axvline(x=meanstart_left, ymax=0.8,linestyle='--',c='k')
        ax.axvline(x=meanstart_right, ymax=0.8,linestyle='--',c='k')
        meanstarts_left.append(meanstart_left)
        meanstarts_right.append(meanstart_right)


# adjust ticks

axes_2[0].set_xlim([-5,155])
axes_2[0].set_ylim(hist_y_lim)
axes_2[0].set_yticks([0,0.5,1])
axes_2[0].set_yticklabels([0,0.5,1])
axes_2[0].yaxis.set_minor_locator(MultipleLocator(0.25))
axes_2[0].yaxis.set_major_locator(MultipleLocator(0.5))
axes_2[0].xaxis.set_major_locator(MultipleLocator(100))
axes_2[0].xaxis.set_minor_locator(MultipleLocator(50))

axes_2[0].set_ylabel(hists_y_label,size=MEDIUM_SIZE)
axes_2[2].set_xlabel("$x$ (mm)",size=MEDIUM_SIZE)

set_grid(axes_2)


# plt.scatter(loading_contrast, x_plot[index_start])
# plt.xlabel("LC")
# plt.ylabel("nucleation point")
# plt.show()


#### drawing










temp_nice_plot_large(y_min,x_plot,ax=ax_drawing,ylim=None)

ax_drawing.set_xlim([0,150])
ax_drawing.set_ylim([-0.3,0.12])

ax_drawing.scatter(125, -0.05, s=20, marker='*', color='r', zorder=3)
ax_drawing.plot([75,75],[-0.2,0.12],linestyle='--',c='k')
ax_drawing.plot([125,125],[-0.2,0.12],linestyle='--',c='k')

ax_drawing.plot([75,125],[-0.2,-0.2],c='k',linewidth=.5)

ax_drawing.arrow(122,-0.2,1,0,length_includes_head = True, head_width=0.02, head_length = 3,edgecolor = None, color = "k", width = 0.001, shape = "full")
ax_drawing.arrow(78,-0.2,-1,0,length_includes_head = True, head_width=0.02, head_length = 3,edgecolor = None, color = "k", width = 0.001, shape = "full")

ax_drawing.text(100,-0.17,"$d_{nuc}$",size=SMALL_SIZE,horizontalalignment='center')
ax_drawing.axis("off")













########################## Data for propagation
# main folder
loc_folder=loc_general+"manip_{}/".format(chosen_manip_fig41_sec)
# name of the file / event
loc_file="event-{i:03d}.npy".format(i=chosen_event_fig41_sec)
# name of the reference file, containing unloaded signal, usually event-001
loc_file_zero = "event-001.npy"
# parameters file
loc_params="parameters.txt"

# control smoothing of the data (rolling average) and starting point
roll_smooth=5
start=0
n_plot=10

## Location of the data inside the file
# channels containing the actual strain gages
gages_channels = np.concatenate([np.arange(0,15),np.arange(16,31)])
# channels containing the normal and tangetial force
forces_channels = [32,33]
# channel containing the trigger
trigger_channel = 34

## Parameters
# default x, just in case there's nothing in the saved params
x=np.array([1,2,3,4,5,8,11,12,13,14])*1e-2 -0.005
# Load the params file, and extract frequency of acquisition


if reload or force_reload:
    exec(load_params(loc_folder+loc_params))
    sampling_freq_in = clock/10
    # Create the location strings
    loc=loc_folder+loc_file
    loc_zero=loc_folder+loc_file_zero
    # Number of channels
    nchannels = len(gages_channels)

    # Fast acquicition
    # Load data
    data_2=np.load(loc,allow_pickle=True)
    data_zero_2=np.load(loc_zero,allow_pickle=True)

    # smooth data
    data_2=smooth(data_2,roll_smooth)
    data_2=np.transpose(np.transpose(data_2)-np.mean(data_zero_2,axis=1))

    # assign specific channels to specific variables
    forces=data_2[forces_channels,:]
    mu = data_2[forces_channels[1],:].mean() / data_2[forces_channels[0],:].mean()
    gages_2 = data_2[gages_channels]
    gages_zero = data_zero_2[gages_channels]
    gages_2=np.transpose(np.transpose(gages_2)-np.mean(gages_zero,axis=-1))
    fast_time_2=np.arange(len(gages_2[0]))/sampling_freq_in



    for i in range(nchannels//3):
        ch_1_2=gages_2[3*i]
        ch_2_2=gages_2[3*i+1]
        ch_3_2=gages_2[3*i+2]
        ch_1_2,ch_2_2,ch_3_2=voltage_to_strains(ch_1_2,ch_2_2,ch_3_2)
        ch_1_2,ch_2_2,ch_3_2=rosette_to_tensor(ch_1_2,ch_2_2,ch_3_2)
        #ch_1,ch_2,ch_3=eps_to_sigma(ch_1,ch_2,ch_3,E=E,nu=nu)
        gages_2[3*i]=ch_1_2
        gages_2[3*i+1]=ch_2_2
        gages_2[3*i+2]=ch_3_2

    indexes_2=np.load(loc+"_times_hand_picked.npy")+0.007/1000

## Plot data
## axes 3


#indexes_2[5]*=0
#indexes_2[6]+=0.00001
#indexes_2[7]+=0.000019

#indexes_2[4]*=0

# lines propag
xs=[0.7,0.68,0.7]
ys=[0.96,0.9,0.84]
line = mpl.lines.Line2D(xs, ys, lw=1, color='r', alpha=1)
fig.add_artist(line)

xs=[0.89,0.92]
ys=[0.53,0.4]
line = mpl.lines.Line2D(xs, ys, lw=1, color='r', alpha=1)
fig.add_artist(line)



color=[solid_in_granular_color]*5+[granular_color]+[solid_in_granular_color]*4

delta = -0.3

for i in range(10):
    axes_3[i].plot(1000*fast_time_2[start:]-1000*fast_time_2.mean()-delta,1000*(gages_2[3*(i+1)-1][start:]-gages_2[3*(i+1)-1][0:10000].mean()),color=color[i])
    #axes_3[i].ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    axes_3[i].grid("both")
    # dashes
    axes_3[i].axvline(x=indexes_2[i]*1000-1000*fast_time_2.mean()-delta,c="k",linestyle="--")

axes_3[1].scatter(indexes_2[1]*1000-1000*fast_time_2.mean()-delta, 0, s=50, marker='*', color='r', zorder=3)


fig.text(0.7, 0.86, r"$c_f\sim 500$ m/s", size = INSET_SMALL_SIZE, rotation =0, c="r")
fig.text(0.83, 0.44, r"$c_f\sim 600$ m/s", size = INSET_SMALL_SIZE, rotation = 0,c="r")
#txt1.set_bbox(dict(facecolor='white', alpha=0.5, linewidth=0))



axes_3[-1].set_xlabel('time (ms)')
axes_3[4].set_ylabel(r'$\varepsilon_{xy}-\varepsilon_{xy}^0$ (mStrain)',size=MEDIUM_SIZE)


# adjust ticks
axes_3[-1].set_xlim([-0.24,0.24])
axes_3[-1].set_xticks([-0.2,-0.1,0,0.1,0.2])
axes_3[-1].set_xticklabels(["-$0.2$","-$0.1$","$0$","$0.1$","$0.2$"])
axes_3[-1].set_ylim([-0.15,0.06])
axes_3[-1].set_yticks([-0.1,0])
axes_3[-1].set_yticklabels(["-$0.1$","$0$"])



for i in range(9):
    plt.setp(axes_3[i].get_yticklabels(), visible=False)
    plt.setp(axes_3[i].get_xticklabels(), visible=False)




labels = [r"$x=5 \pm 0.25$ mm"]+[r"$x={}$".format(i) for i in [int(x_plot[i]) for i in range(1,len(x_plot))]]

# Iterate through each subplot and add data
for i, ax in enumerate(axes_3):
    ax.annotate(labels[i], xy=(0.025, 0.1), xycoords='axes fraction',
                xytext=(10, 0), textcoords='offset points',
                va="center",size=5)




# LC :
loc_folder=loc_general

if reload or force_reload:
    data_loaded_2=np.load(loc_folder+"python_plots/summary_data.npy",allow_pickle=True).all()

mean_lc=data_loaded_2["mean_lc"]
manip_num=np.array(data_loaded_2["manip_num"])
LC_there = mean_lc[manip_num==chosen_manip_fig41_sec][0]


axes_3[0].annotate("${}={:.2f}$".format(LC_name_short,LC_there), xy=(0.8, 0.85), xycoords='axes fraction',
                xytext=(10, 0), textcoords='offset points',
                va="center",size=5)



set_grid(axes_3)























##


def my_mean(x):
    m = 0
    c = 0
    for xi in x:
        if xi!= 0:
            m+=xi
            c+=1
    if m==0:
        return(np.nan)
    return(m/c)

nuc_pt = x[index_start]
ell_nuc = 1000*(np.abs(nuc_pt-0.075))

ell_nuc_2 = nuc_pt*(nuc_pt>0.075)
ell_nuc_3 = nuc_pt*(nuc_pt<0.075)

xxs = np.arange(0,15,1)*10

lc_per_ell_nuc = [np.mean(loading_contrast[ell_nuc == xxs[i]]) if len(loading_contrast[ell_nuc == xxs[i]])!=0 else np.nan for i in range(15)]

#lc_list_nuc = np.linspace(-1,2,4)
#lc_list_nuc = np.linspace(-1,2,8)
#lc_list_nuc = np.linspace(-1,2,15)
lc_list_nuc = np.array([-1,-0.5,0,1,2])


ell_per_lc_nuc = np.array(
        [np.mean(
            ell_nuc[np.logical_and(
                loading_contrast<lc_list_nuc[i+1] ,
                loading_contrast>lc_list_nuc[i])
                ]
            )/1000
        if len(
            ell_nuc[np.logical_and(
                loading_contrast<lc_list_nuc[i+1],
                loading_contrast>lc_list_nuc[i] ,
                np.logical_not(from_solid)
                )
                ]
            )!=0
        else np.nan
        for i in range(len(lc_list_nuc)-1)]
        )


ell_per_lc_nuc_width = np.array(
        [np.std(
            ell_nuc[np.logical_and(
                loading_contrast<lc_list_nuc[i+1] ,
                loading_contrast>lc_list_nuc[i] ,
                np.logical_not(from_solid)
                )
            ])/1000
        if len(
            ell_nuc[np.logical_and(
                loading_contrast<lc_list_nuc[i+1],
                loading_contrast>lc_list_nuc[i])
                ]
            )!=0
        else np.nan
        for i in range(len(lc_list_nuc)-1)]
        )







ell_per_lc_nuc_solid = np.mean(ell_nuc[from_solid])/1000


ell_per_lc_nuc_width_solid = np.std(ell_nuc[from_solid])/1000

lc_solid_mean = np.mean(loading_contrast[from_solid])










ax_4.scatter((lc_list_nuc[:-1]+lc_list_nuc[1:])/2,ell_per_lc_nuc*1000/15,
        c=main_plot_color,s=scatter_size*2,
        marker="d",zorder=3,
        edgecolors="k",linewidth=0.01)


ax_4.errorbar((lc_list_nuc[:-1]+lc_list_nuc[1:])/2,ell_per_lc_nuc*1000/15,yerr = ell_per_lc_nuc_width*1000/15,
                 fmt=" ",capsize=error_bar_width,color="k",
               ecolor=error_bar_color,
               elinewidth=.5,alpha=error_bar_alpha,markeredgewidth=markeredgewidth)




ax_4.scatter(lc_solid_mean,ell_per_lc_nuc_solid*1000/15,
        c=solid_solid_color,s=scatter_size*4/3,
        marker="o",zorder=3,
        edgecolors="k",linewidth=0.01)


ax_4.errorbar(lc_solid_mean,ell_per_lc_nuc_solid*1000/15,yerr = ell_per_lc_nuc_width_solid*1000/15,
               fmt=" ",capsize=error_bar_width,color="k",
               ecolor=error_bar_color,
               elinewidth=.5,alpha=error_bar_alpha,markeredgewidth=markeredgewidth)










#ax_4.legend()
ax_4.set_xlim(-1.1,2)
ax_4.set_ylim(1.7,4.3)
ax_4.set_xlabel("${}$".format(LC_name_short),labelpad = 1.5)
ax_4.set_ylabel(r"$\frac{\left\langled_{nuc}\right\rangle}{\ell_{hole}\,/\,2}$")

ax_4.set_xticks([-1,0,1,2])
ax_4.set_xticklabels(["-1","0","1","2"])
ax_4.yaxis.set_minor_locator(MultipleLocator(0.5))
ax_4.yaxis.set_major_locator(MultipleLocator(1))


set_grid(ax_4)



"""
##
ell = np.array(ell)

xxs = np.arange(0,15,1)*10

lc_per_ell_round = [np.mean(lc_event[ell == xxs[i]]) if len(lc_event[ell == xxs[i]])!=0 else np.nan for i in range(15)]

lc_list_round = np.linspace(-1,2,15)



ell_per_lc_round = np.array(
        [np.mean(
            ell[np.logical_and(lc_event<lc_list_round[i+1],lc_event>lc_list_round[i])])/1000
        if len(
            ell[np.logical_and(lc_event<lc_list_round[i+1],lc_event>lc_list_round[i])]
            )!=0
        else np.nan
        for i in range(len(lc_list_round)-1)]
        )

plt.scatter(lc_per_ell_round,xxs/1000,label=r"$\left\langle C_{\sigma}\right\rangle$ per bin of $\ell$")
plt.scatter(lc_list_round[:-1],ell_per_lc_round,label = r"$\left\langle\ell\right\rangle$ per bin of $C_{\sigma}$")
plt.legend()

plt.show()



"""


################### Plot adjustment


axes_1[-1].xaxis.labelpad=1
axes_2[2].xaxis.labelpad=1

axes_1[4].yaxis.set_label_coords(-0.058, 0)
axes_2[0].yaxis.set_label_coords(-0.225, 0.5)
ax_4.yaxis.set_label_coords(-0.09, 0.5)



axes_3[-1].xaxis.labelpad=1
#axes_4[2].xaxis.labelpad=1

axes_3[4].yaxis.set_label_coords(-0.058, 0)
#axes_4[0].yaxis.set_label_coords(-0.065*5, 0.5)


#real_tight_layout(fig)
y=(size_fig_1[1]-2.5*mm)/size_fig_1[1]
fig.text(0.005,0.98,"a",size=LETTER_SIZE, weight='bold')
fig.text(.5,0.98,"b",size=LETTER_SIZE, weight='bold')
fig.text(0.005,0.27,"c",size=LETTER_SIZE, weight='bold')
fig.text(.68,0.27,"d",size=LETTER_SIZE, weight='bold')

fig.savefig("E:/Article/Figure_4/figure_4.png",dpi=dpi_global)
fig.savefig("E:/Article/Figure_4/figure_4.pdf")
fig.savefig("E:/Article/Figure_4/figure_4.svg")
plt.close('all')


###


to_save={}

#to_save["time_sm"]=time_sm
#to_save["eps_xy_sm"]=eps_xy_sm
to_save["labels"]=labels
to_save["x_plot"]=x_plot
#to_save["histogram_round_solid"]=histogram_round_solid
to_save["histogram_start_solid"]=histogram_start_solid
#to_save["histograms_round"]=histograms_round
to_save["histograms_start"]=histograms_start
to_save["chosen_manip_fig41"]=chosen_manip_fig41
to_save["chosen_event_fig41"]=chosen_event_fig41
to_save["chosen_manip_fig41_sec"]=chosen_manip_fig41_sec
to_save["chosen_event_fig41_sec"]=chosen_event_fig41_sec
#to_save["chosen_manip_fig42"]=chosen_manip_fig42

to_save["lc_list_nuc"]=lc_list_nuc
to_save["ell_per_lc_nuc"]=ell_per_lc_nuc
to_save["ell_per_lc_nuc_solid"]=ell_per_lc_nuc_solid
to_save["lc_solid_mean"]=lc_solid_mean
to_save["ell_per_lc_nuc_width"]=ell_per_lc_nuc_width
to_save["ell_per_lc_nuc_width_solid"]=ell_per_lc_nuc_width_solid

to_save["ell_nuc"]=ell_nuc
to_save["loading_contrast"]=loading_contrast


#to_save["lc_per_ell_round"]=lc_per_ell_round
#to_save["possible_ells"]=xxs
#to_save["lc_list_round"]=lc_list_round[-1]
#to_save["ell_per_lc_round"]=ell_per_lc_round

to_save["fast_time"]=fast_time
to_save["gages"]=gages
to_save["indexes"]=indexes
to_save["fast_time_2"]=fast_time_2
to_save["gages_2"]=gages_2
to_save["indexes_2"]=indexes_2

to_save["data_loaded"]=data_loaded
to_save["data_loaded_2"]=data_loaded_2
to_save["data_loaded_3"]=data_loaded_3


np.save("E:/Article/Figure_4/figure_4.npy",to_save)
scio.savemat("E:/Article/Figure_4/figure_4.mat",to_save)









