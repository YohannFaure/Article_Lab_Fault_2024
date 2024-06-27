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








### Fig 6 a.
data_fig_5 = np.load("E:/Article/Figure_5/figure_5.npy",allow_pickle=True).all()




lc_solid_mean                   = data_fig_5["lc_solid_mean"]
ell_per_lc_round_solid          = data_fig_5["ell_per_lc_round_solid"]
lc_list_round                   = data_fig_5["lc_list_round"]
ell_per_lc_round                = data_fig_5["ell_per_lc_round"]
ell_per_lc_round_width          = data_fig_5["ell_per_lc_round_width"]
ell_per_lc_round_width_solid    = data_fig_5["ell_per_lc_round_width_solid"]


mean_lc                         = data_fig_5["mean_lc"]
lc_event                        = data_fig_5["lc_event"]
ell                             = data_fig_5["ell"]
is_solid                        = data_fig_5["is_solid"]










### Fig 6 b.

### load data : set up the loading

solids = [14,15,16,17,18,37,38]

# name of the reference file, containing unloaded signal, usually event-001
loc_file_zero = "event-001.npy"

# parameters file
loc_params="parameters.txt"


# control smoothing of the data (rolling average) and starting point
roll_smooth=10
start=0




### Location of the data inside the file
# channels containing the actual strain gages
gages_channels = np.concatenate([np.arange(0,15),np.arange(16,31)])

# channels containing the normal and tangetial force
forces_channels = [32,33]

# channel containing the trigger
trigger_channel = 34



### Load data : load and create usefull variables
## Parameters
# default x, just in case there's nothing in the saved params
x=np.array([1,2,3,4,5,8,11,12,13,14])*1e-2

import os

chosen_manips = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38]#, 39, 40, 42, 43, 44]



reload = False

try:
    loaded_data = np.load("E:/Article/Figure_6/Figure_6.npy",allow_pickle= True).all()
    locals().update(loaded_data)
except:
    reload = True


if reload or force_reload:
    print("reloading data for Figure 6")
    lc_per_manip = []
    lc_per_manip_std = []


    lc_per_manip_2 = []
    lc_per_manip_std_2 = []



    sigma_yy_0_tip_per_manip = []
    sigma_yy_0_tip_per_manip_std = []


    sigma_yy_0_tip_per_manip_2 = []
    sigma_yy_0_tip_per_manip_std_2 = []

    solid_per_manip = []
    solid_per_manip_2 = []


    #for j in range(5,6):

    for j in range(0,len(chosen_manips)):

        print(chosen_manips[j])

        loc_folder="E:/2023-2024/2023-07-11-manips-10-voies/manip_{}/".format(chosen_manips[j])


        directory = loc_folder
        files = [file for file in os.listdir(directory) if file.startswith("event-") and file.endswith("_times_hand_picked.npy")]
        n_events = max(int(file.split('-')[1].split('.')[0]) for file in files)+1

        # Load the params file, and extract frequency of acquisition
        exec(load_params(loc_folder+loc_params))
        sampling_freq_in = clock/10
        # Create the location strings
        loc_zero=loc_folder+loc_file_zero
        # Number of channels
        nchannels = len(gages_channels)


        # Fast acquicition


        def comp_lc(prof,fn=300):
            # osef de fn
            ss = np.mean(prof[[0,1,2,3,4,6,7,8,9]])
            gg = prof[5]
            lc = 15*(gg-ss)/(3*gg+12*ss)
            return(lc)


        # def comp_lc(prof,fn=300):
        #     S=0.01*0.015
        #     ss = np.mean(prof[[0,1,2,3,4,6,7,8,9]])
        #     gg = prof[5]
        #     lc = (gg-ss)/(10*fn/S)
        #     return(lc)


        lc_per_event = []
        sigma_yy_0_tip_per_event = []


        data_zero=np.load(loc_zero,allow_pickle=True)

        if chosen_manips[j]==28:
            start_avoid_2=3
        else:
            start_avoid_2=2

        solid_per_manip.append(chosen_manips[j] in solids)

        for i in range(start_avoid_2,n_events):
            solid_per_manip_2.append(chosen_manips[j] in solids)

            # name of the file / event
            loc_file="event-0{:02d}.npy".format(i)
            print(loc_file)
            loc=loc_folder+loc_file


            # Load data
            data=np.load(loc,allow_pickle=True)

            # smooth data
            data=smooth(data,roll_smooth)
            data=np.transpose(np.transpose(data)-np.mean(data_zero,axis=1))


            # assign specific channels to specific variables
            forces=data[forces_channels,:]
            mu = data[forces_channels[1],:].mean() / data[forces_channels[0],:].mean()
            gages = data[gages_channels]
            gages_zero = data_zero[gages_channels]
            fast_time=np.arange(len(gages[0]))/sampling_freq_in

            # create labels
            ylabels = [
            r"$\varepsilon_{{xx}}^{{{}}}$" ,
            r"$\varepsilon_{{yy}}^{{{}}}$" ,
            r"$\varepsilon_{{xy}}^{{{}}}$"
                    ] * (nchannels//3)

            for i in range(len(ylabels)):
                ylabels[i]=ylabels[i].format((i+3)//3)


            converted = False

            # Convert voltage to strains or forces, and rosette to tensor

            if not converted:
                for i in range(nchannels//3):
                    ch_1=gages[3*i]
                    ch_2=gages[3*i+1]
                    ch_3=gages[3*i+2]
                    ch_1,ch_2,ch_3=voltage_to_strains(ch_1,ch_2,ch_3)
                    ch_1,ch_2,ch_3=rosette_to_tensor(ch_1,ch_2,ch_3)
                    gages[3*i]=ch_1
                    gages[3*i+1]=ch_2
                    gages[3*i+2]=ch_3

                forces = voltage_to_force(forces)

            fn = np.mean(forces[0][:10000])
            converted=True




            indexes=np.load(loc+"_times_hand_picked.npy")

            start = np.argmin(indexes)

            temp = E*np.mean(gages[1::3,:1000],axis = 1)
            lc_per_event.append(comp_lc(temp,fn))
            sigma_yy_0_tip_per_event.append(temp[start])



        sigma_yy_0_tip_per_event = np.array(sigma_yy_0_tip_per_event)
        lc_per_event = np.array(lc_per_event)

        lc_per_manip.append(np.mean(lc_per_event))
        lc_per_manip_std.append(np.std(lc_per_event))

        sigma_yy_0_tip_per_manip.append(np.mean(sigma_yy_0_tip_per_event))
        sigma_yy_0_tip_per_manip_std.append(np.std(sigma_yy_0_tip_per_event))

        lc_per_manip_2 += list(lc_per_event)
        lc_per_manip_std_2 += list(lc_per_event)

        sigma_yy_0_tip_per_manip_2 += list(sigma_yy_0_tip_per_event)
        sigma_yy_0_tip_per_manip_std_2 += list(sigma_yy_0_tip_per_event)



    lc_per_manip=np.array(lc_per_manip)
    lc_per_manip_std=np.array(lc_per_manip_std)
    lc_per_manip_2=np.array(lc_per_manip_2)
    lc_per_manip_std_2 = np.array(lc_per_manip_std_2)
    sigma_yy_0_tip_per_manip = np.array(sigma_yy_0_tip_per_manip)
    sigma_yy_0_tip_per_manip_std = np.array(sigma_yy_0_tip_per_manip_std)
    sigma_yy_0_tip_per_manip_2 = np.array(sigma_yy_0_tip_per_manip_2)
    solid_per_manip = np.array(solid_per_manip)

    data_to_save = {}


    names = ["lc_per_manip",
                "lc_per_manip_std",
                "lc_per_manip_2",
                "lc_per_manip_std_2",
                "sigma_yy_0_tip_per_manip",
                "sigma_yy_0_tip_per_manip_std",
                "sigma_yy_0_tip_per_manip_2",
                "sigma_yy_0_tip_per_manip_std_2",
                "solid_per_manip",
                "solid_per_manip_2"]

    for n in names:
        data_to_save[n]=eval(n)

    np.save("E:/Article/Figure_6/Figure_6.npy",data_to_save)

##






def nice_plot(xpos,ypos,ax=None,xerr=None,yerr=None,xlabel="",ylabel="",
              annotate=None,old_data=False,
              color="b",error_bar_color="k",marker_size=3,capsize=error_bar_width,
              marker="d",solid_marker=solid_marker,in_solid=None,solid_color=solid_solid_color):
    if ax is None:
        fig, ax = plt.subplots()
    if old_data:
        ax.errorbar(old_data[0],old_data[1],xerr=old_data[2],yerr=old_data[3],
                    fmt=" ",capsize=capsize,color=color,ecolor=error_bar_color,elinewidth=.5, alpha=error_bar_alpha,markeredgewidth=markeredgewidth)
        ax.scatter(old_data[0],old_data[1],color=color,s=marker_size,marker=marker,zorder=5,edgecolors="k",linewidth=0.01)

    # all data
    ax.errorbar(xpos,ypos, xerr=xerr,yerr=yerr,
                fmt=" ",capsize=capsize,color=color,ecolor=error_bar_color,elinewidth=.5,alpha=error_bar_alpha,markeredgewidth=markeredgewidth)
    ax.scatter(xpos,ypos,color=color,s=marker_size,marker=marker,zorder=5,edgecolors="k",linewidth=0.01)

    # solids
    if not in_solid is None:
        ax.errorbar(xpos[in_solid],ypos[in_solid],
        xerr=xerr[...,in_solid],yerr=yerr[...,in_solid],
        fmt=" ",capsize=capsize,
        color=solid_color,ecolor=error_bar_color,
        elinewidth=.5,alpha=error_bar_alpha ,
        markeredgewidth=markeredgewidth)

        ax.scatter(xpos[in_solid],ypos[in_solid],
        color=solid_color,s=marker_size,
        marker=solid_marker,zorder=5,
        edgecolors="k",linewidth=0.01)
    if not annotate is None:
        for i in range(len(annotate)):
            ax.annotate(annotate[i], (xpos[i], ypos[i]))

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)





#
bins_2 = np.array([-1.1,-0.5,0,1,2])
bins = np.array([-2,-0.5,0,1,5])

solid = np.array(solid_per_manip_2)
not_solid = np.logical_not(solid)

bins_bool = np.array( [ np.logical_and(
                            np.logical_and( lc_per_manip_2<bins[i+1],
                                            lc_per_manip_2>bins[i]),
                            not_solid)
                        for i in range(len(bins)-1)] )


bins_bool_solid = solid

sig_binned = np.array([np.mean(sigma_yy_0_tip_per_manip_2[b]) for b in bins_bool])
sig_binned_std = np.array([np.std(sigma_yy_0_tip_per_manip_2[b]) for b in bins_bool])

sig_sol = np.mean(sigma_yy_0_tip_per_manip_2[bins_bool_solid])
sig_sol_std = np.std(sigma_yy_0_tip_per_manip_2[bins_bool_solid])


















### plot 6a.

fig,axes = plt.subplots(1,2,sharex=True)
fig.subplots_adjust(left=0.1, bottom=0.2, right=0.99, top=0.98, wspace=0.3)
fig.set_size_inches(size_fig_6)

axes[0].errorbar(lc_solid_mean,ell_per_lc_round_solid*1000/30,yerr = ell_per_lc_round_width_solid*1000/30,
                 fmt=" ",capsize=error_bar_width,color="k",
               ecolor=error_bar_color,
               elinewidth=.5,alpha=error_bar_alpha,markeredgewidth=markeredgewidth)

axes[0].scatter((lc_list_round[:-1]+lc_list_round[1:])/2,ell_per_lc_round*1000/30,
        c=main_plot_color,s=scatter_size*2,
        marker="d",zorder=2,
        edgecolors="k",linewidth=0.01)



axes[0].scatter(lc_solid_mean,ell_per_lc_round_solid*1000/30,
        c=solid_solid_color,s=scatter_size*4/3,
        marker="o",zorder=2,
        edgecolors="k",linewidth=0.01)



axes[0].errorbar((lc_list_round[:-1]+lc_list_round[1:])/2,ell_per_lc_round*1000/30,yerr = ell_per_lc_round_width*1000/30,
                 fmt=" ",capsize=error_bar_width,color="k",
               ecolor=error_bar_color,
               elinewidth=.5,alpha=error_bar_alpha,markeredgewidth=markeredgewidth)



#axes[0].legend()
axes[0].set_xlim(-1.1,2)
#axes[0].set_ylim(23,120)
axes[0].set_xlabel("${}$".format(LC_name_short))
axes[0].set_ylabel(r"$\left\langle\ell_{slip}\right\rangle\,/\,\ell_{hole}$")

axes[0].xaxis.set_minor_locator(MultipleLocator(0.5))
axes[0].xaxis.set_major_locator(MultipleLocator(1))
axes[0].yaxis.set_minor_locator(MultipleLocator(0.5))
axes[0].yaxis.set_major_locator(MultipleLocator(1))





"""
mean_lc                         = data_fig_5["mean_lc"]
lc_event                        = data_fig_5["lc_event"]
ell                             = data_fig_5["ell"]
is_solid                        = data_fig_5["is_solid"]
"""


temp = np.cumsum(np.diff(lc_event)!=0)
temp = np.insert(temp,0,0)
mean_slip = np.array(  [
                            np.mean(
                                    ell[temp == i]
                                    )
                            for i in range(max(temp)+1)
                       ]
                    )

"""
axes[0].scatter(mean_lc,
                mean_slip/30,
                marker = scatter_marker, s = scatter_size/4,
                c=secondary_plot_color,alpha = secondary_plot_alpha ,
                zorder=-1,edgecolors="k",linewidth=0)

axes[0].scatter(mean_lc[is_solid],
                mean_slip[is_solid]/30,
                marker = 'o', s = scatter_size/4*2/3,
                c=secondary_plot_color,alpha = secondary_plot_alpha ,
                zorder=-1,edgecolors="k",linewidth=0)
"""



axes[0].scatter(lc_event,
                ell/30,
                marker = scatter_marker, s = scatter_size/4,
                c=secondary_plot_color,alpha = secondary_plot_alpha ,
                zorder=-1,edgecolors="k",linewidth=0)










### plot 6b.


nice_plot(bins_2[1:]/2+bins_2[:-1]/2,sig_binned/1e6,
              ax=axes[1],xerr=None,yerr=sig_binned_std/1e6,
              color=main_plot_color, marker_size=scatter_size*2,
              marker="d",solid_marker="o",in_solid=None,
              error_bar_color=error_bar_color,
              solid_color=solid_solid_color)



nice_plot(lc_solid_mean,sig_sol/1e6,
              ax=axes[1],xerr=None,yerr=sig_sol_std/1e6,
              color=solid_solid_color, marker_size=scatter_size*4/3,
              marker="o",solid_marker="o",in_solid=None,
              error_bar_color=error_bar_color,
              solid_color=solid_solid_color)





axes[1].set_xlabel("${}$".format(LC_name_short))
axes[1].set_ylabel(r"$\left\langle\sigma_{yy}^{0}(x_{nuc})\right\rangle$ (MPa)")
axes[1].set_xlim([-1.1,2])
axes[1].set_ylim([0,3.8])
axes[1].xaxis.set_minor_locator(MultipleLocator(0.5))
axes[1].xaxis.set_major_locator(MultipleLocator(1))
axes[1].yaxis.set_minor_locator(MultipleLocator(0.5))
axes[1].yaxis.set_major_locator(MultipleLocator(1))
set_grid(axes)








"""
axin = fig.add_axes([0.6447, 0.295,   0.27,  0.23],facecolor="w")



axin.scatter(lc_per_manip_2,
                sigma_yy_0_tip_per_manip_2/1e6,
                marker = scatter_marker, s = scatter_size/4,
                c=main_plot_color,alpha = 1 ,
                zorder=1,edgecolors="k",linewidth=0.01)

axin.scatter(lc_per_manip_2[solid_per_manip_2],
                sigma_yy_0_tip_per_manip_2[solid_per_manip_2]/1e6,
                marker = 'o', s = scatter_size/4*2/3,
                c=solid_solid_color,alpha = 1 ,
                zorder=2,edgecolors="k",linewidth=0.01)



axin.set_xlim([-1.1,2])
axin.set_ylim([0,4])
#axin.set_xlabel("${}$".format(LC_name_short))
#axin.set_ylabel("$\sigma_{yy}^{0}(x_{nuc})$ (MPa)")

axin.xaxis.set_minor_locator(MultipleLocator(1))
axin.xaxis.set_major_locator(MultipleLocator(2))
axin.yaxis.set_minor_locator(MultipleLocator(1))
axin.yaxis.set_major_locator(MultipleLocator(2))


set_up_inset(axin)
"""

axes[-1].scatter(lc_per_manip_2,
                sigma_yy_0_tip_per_manip_2/1e6,
                marker = scatter_marker, s = scatter_size/4,
                c=secondary_plot_color,alpha = secondary_plot_alpha ,
                zorder=-1,edgecolors="k",linewidth=0)

axes[-1].scatter(lc_per_manip_2[solid_per_manip_2],
                sigma_yy_0_tip_per_manip_2[solid_per_manip_2]/1e6,
                marker = 'o', s = scatter_size/4*2/3,
                c=secondary_plot_color,alpha = secondary_plot_alpha ,
                zorder=-1,edgecolors="k",linewidth=0)


fig.savefig("E:/Article/Figure_6/figure_6.png",dpi=dpi_global)
fig.savefig("E:/Article/Figure_6/figure_6.pdf")
fig.savefig("E:/Article/Figure_6/figure_6.svg")
plt.close('all')


plt.show()








##


to_save={}

vars = ["lc_list_round",
    "ell_per_lc_round",
    "lc_solid_mean",
    "ell_per_lc_round_solid",
    "ell_per_lc_round_width",
    "ell_per_lc_round_width_solid",
    "lc_per_manip",
    "lc_per_manip_std",
    "lc_per_manip_2",
    "lc_per_manip_std_2",
    "sigma_yy_0_tip_per_manip",
    "sigma_yy_0_tip_per_manip_std",
    "sigma_yy_0_tip_per_manip_2",
    "solid_per_manip",
    "solid_per_manip_2",
    "sig_binned",
    "sig_binned_std",
    "sig_sol",
    "sig_sol_std"]






for v in vars:
    to_save[v]=eval(v)



np.save("E:/Article/Figure_6/figure_6.npy",to_save)
scio.savemat("E:/Article/Figure_6/figure_6.mat",to_save)


