## Imports
# Science



# custom file
try :
    import sys
    sys.path.insert(0, "D:/Users/Manips/Documents/Python/DAQ_Python")
    from Python_DAQ import *
except :
    from DAQ_Python.Python_DAQ import *
# this also imports E and nu



### load data : set up the loading

# Location
with open("E:/Article/parameters.py", 'r') as f:
        exec(f.read())

loc_folder_main=loc_general+"manip_{}/"


loc_folders=[loc_folder_main.format(i) for i in chosen_manips_fig1]

roll_smooth=25
start=0

# parameters file
loc_params="parameters.txt"
loc_file_zero = "event-001.npy"

# Location of the data inside the file
# channels containing the actual strain gages
gages_channels = np.concatenate([np.arange(0,15),np.arange(16,31)])
# channels containing the normal and tangetial force
forces_channels = [32,33]
# channel containing the trigger
trigger_channel = 34

# Number of channels
nchannels = len(gages_channels)





def trig_to_time(sm_trig):
    sm_trig=sm_trig>3
    sm_trig[4:-1]+=sm_trig[0:-5]
    sm_trig=sm_trig>0.5
    stop = len(sm_trig)
    j=10000
    timings=[]
    while j < stop:
        if sm_trig[j] :
            k=0
            while j+k<stop and sm_trig[j+k]:
                k+=1
            if k>25:
                timings.append(j)
            j=j+k
        else :
            j+=1
    return(timings)




## quick-load data if already generated

try :
    dicto = np.load("E:/Article/Figure_1/figure_1_c_d.npy",allow_pickle=True).all()
    reload = dicto["chosen_manips"]!=chosen_manips_fig1

    if chosen_manips_fig1!=dicto["chosen_manips"]:
        raise

    timings=dicto["timings"]
    times=dicto["times"]
    mus=dicto["mus"]
    mean_fns=dicto["mean_fns"]
    load_profiles=dicto["load_profiles"]
    LCs=dicto["LCs"]

except :
    reload=True


## regenerate all data if necessary

if reload or force_reload :
    print("Reloading data for Figure 1 c d")
    load_profiles=[]
    LCs=[]


    for i in range(4):
        # load each manip
        loc_folder=loc_folders[i]

        # load zero
        # Load the params file, and extract frequency of acquisition
        # default x, just in case there's nothing in the saved params
        exec(load_params(loc_folder+loc_params))
        loc_zero=loc_folder+loc_file_zero
        data_zero=np.load(loc_zero,allow_pickle=True)
        data_zero_mean=np.mean(data_zero,axis=1)

        # load each event for the profile
        events = list_files_with_pattern(loc_folder, "event")
        events = [e for e in events if len(e)==13][1:]
        events = events[-30:]
        sigma_before=[]
        for e in events:
            data=np.transpose(np.transpose(np.load(loc_folder+e,allow_pickle=True))-data_zero_mean)
            gages = data[gages_channels]
            gages = np.mean(gages[:,:1000],axis=-1)
            # convert to stress
            for i in range(nchannels//3):
                ch_1=gages[3*i]
                ch_2=gages[3*i+1]
                ch_3=gages[3*i+2]
                # xx,yy,xy
                ch_1,ch_2,ch_3=voltage_to_strains(ch_1,ch_2,ch_3)
                ch_1,ch_2,ch_3=rosette_to_tensor(ch_1,ch_2,ch_3)
                gages[3*i]=ch_1
                gages[3*i+1]=ch_2
                gages[3*i+2]=ch_3
            sigma_before.append(E*gages)

        sigma_before=np.array(sigma_before)
        load_profile=sigma_before[:,[3*i+1 for i in range(10)]]

        load_profiles.append(load_profile)
        load_profile_mean=np.mean(load_profile,axis=0)
        med=np.median(load_profile_mean[[i for i in range(10) if i!=5]] )

        def comp_lc(prof):
            ss = np.mean(prof[[0,1,2,3,4,6,7,8,9]])
            gg = prof[5]
            lc = 15*(gg-ss)/(3*gg+12*ss)
            return(lc)
        LCs.append(comp_lc( load_profile_mean ))



    timings=[]
    times=[]
    mus=[]
    mean_fns=[]
    fns=[]
    fss=[]
    for i in range(4):
        print(100*i/4,r"%")
        # load slow monitoring
        loc_folder=loc_folders[i]

        sm = np.load(loc_folder+"slowmon.npy",allow_pickle=True)
        sm = np.transpose(np.transpose(sm)-data_zero_mean)
        time_sm = np.load(loc_folder+"slowmon_time.npy")
        sm = smooth(sm,roll_smooth)
        time_sm = smooth(time_sm,roll_smooth)

        # extract observables
        #gages_sm = sm[gages_channels]
        forces_sm=sm[forces_channels,:]
        fn_sm=forces_sm[0]
        fs_sm=forces_sm[1]
        trig_sm = 100*sm[trigger_channel]
        timing=trig_to_time(trig_sm)
        converted = False

        forces_sm=voltage_to_force(forces_sm)
        fn_sm = voltage_to_force(fn_sm)
        fs_sm = voltage_to_force(fs_sm)

        fn_sm = fn_sm*np.sign(np.mean(fn_sm))
        fs_sm = fs_sm*np.sign(np.mean(fs_sm))
        fn_sm[fn_sm < 0]=0

        mu=(fs_sm/fn_sm)
        fns.append(fn_sm)
        fss.append(fs_sm)
        timings.append(timing)
        times.append(time_sm)
        mus.append(mu)
        mean_fns.append(np.mean(fn_sm[len(fn_sm)//10:]))

    print(r"100%")

    dicto={}
    dicto["fns"]=fns
    dicto["fss"]=fss
    dicto["timings"]=timings
    dicto["times"]=times
    dicto["mus"]=mus
    dicto["mean_fns"]=mean_fns
    dicto["chosen_manips"]=chosen_manips_fig1
    dicto["load_profiles"]=load_profiles
    dicto["LCs"]=LCs

    scio.savemat("E:/Article/Figure_1/figure_1_c_d.mat",dicto)
    np.save("E:/Article/Figure_1/figure_1_c_d.npy",dicto)







###

with open("E:/Article/parameters.py", 'r') as f:
        exec(f.read())

def load_profile_plot(x_plot,load_profile,ax,labels=True,suptitle=False,legend=False,
                      linecolor=main_plot_color,c_solid=solid_in_granular_color,c_hole=granular_color, marker=scatter_marker,marker_size=3 ):
    """
    To plot the loading profile (bottom)
    """
    #load
    load_profile_mean=np.mean(load_profile,axis=0)

    # Les lignes transparentes
    for event in load_profile:
        ax.plot(x_plot,event*1e-6,c=secondary_plot_color ,alpha=secondary_plot_alpha ,zorder=1)
        ax.plot(x_plot,load_profile_mean*1e-6,color=linecolor ,zorder=2)

    # Le plot en lui même
    # Points bords
    ax.scatter(x_plot,load_profile_mean*1e-6,
               marker=marker ,s=scatter_size*marker_size ,c=c_solid,zorder=3,edgecolors="k",linewidth=0.01 )
    # Point central

    ax.scatter(x_plot[5],load_profile_mean[5]*1e-6,
               marker=marker,s=scatter_size*marker_size,
               c=c_hole ,label=legend,zorder=3,edgecolors="k",linewidth=0.01)
    if legend:
        ax.legend()

    if labels:
        ax.set_ylabel("$\sigma_{yy}$ (MPa)",size=MEDIUM_SIZE)

    if suptitle:
        ax.set_title(suptitle)


def mu_plot(t,mu,ax,fn,labels=True,suptitle=False,timings=None,
                      linecolor=main_plot_color):
    """
    Plots Mu(t) (top)
    """
    # Create new time and new starting point, to keep only loading
    a=next((i for i, b in enumerate(mu[7000:]>0.05) if b), None)+7000
    start = max(a-5200,0)
    new_t = t[start:]-t[start]
    new_mu = mu[start:]

    # plot
    ax.plot(new_t,new_mu,color=linecolor )

    if labels:
        ax.set_ylabel("$\mu=F_S\,/\,F_N$",size=MEDIUM_SIZE)

    if suptitle:
        ax.set_title(suptitle)

    # Les petits pointillés

    if timings:
        for ti in timings:
            ax.axvline(ti,linestyle=dash_line_style )
            ax.plot([ti,ti],[0,disp[np.abs(t - ti).argmin()]],
                    color=dashed_color,linestyle=dash_line_style ,
                    linewidth=0.4,alpha= secondary_plot_alpha)

##


#fig, axes = plt.subplots(nrows=2,ncols=4,sharex=False,sharey="row")
#fig.set_size_inches(size_fig_1)
fig = plt.figure(layout=None)
fig.set_size_inches(size_fig_1)


heights = [1,1]
widths = [1,0.25,1,1,1]


gs = fig.add_gridspec(nrows=2, ncols=5, left=0.065, right=0.99,
                      top=0.96,bottom=0.1,
                      hspace=.23, wspace=0,width_ratios=widths,
                      height_ratios=heights)


#top
axes_top=[]
for i in range(5):
    if i!=1:
        axes_top.append( fig.add_subplot(gs[0, i]) )
        axes_top[-1].sharex(axes_top[0])
        axes_top[-1].sharey(axes_top[0])

axes_bot=[]
for i in range(5):
    if i!=1:
        axes_bot.append( fig.add_subplot(gs[1, i]) )
        axes_bot[-1].sharex(axes_bot[0])
        axes_bot[-1].sharey(axes_bot[0])

axes=np.array([axes_bot,axes_top])


# plot solid solid
i=0
load_profile_plot(x_plot, load_profiles[i], axes[1,i],
                      labels=i<1, legend=False,
                      linecolor=solid_solid_color,
                      c_solid=solid_in_granular_color,
                      c_hole=hole_in_solid_color,
                      marker=solid_marker,marker_size=2)
mu_plot(times[i],mus[i],axes[0,i],mean_fns[i],labels=i<1,suptitle=False,
                      linecolor=solid_solid_color )

# plot granular
for i in range(1,4):
    load_profile_plot(x_plot, load_profiles[i], axes[1,i], labels=i<1, legend=False,c_hole=granular_color,linecolor=main_plot_color)
    mu_plot(times[i],mus[i],axes[0,i],mean_fns[i],labels=i<1,suptitle=False,linecolor=main_plot_color)




# top
for i in range(4):
    axes[0,i].set_xlim([0,230])
    if i==0:
        axes[0,i].set_xticks([0,100,200])
    else:
        axes[0,i].set_xticks([100,200])
    axes[0,i].xaxis.set_minor_locator(MultipleLocator(50))
    axes[1,i].set_xlim([0,150])
    axes[1,i].set_xticks([0,50,100])
axes[0,0].set_ylim([0,0.4])
axes[0,0].set_yticks([0,0.1,0.2,0.3])
axes[0,0].set_yticklabels([0,0.1,0.2,0.3])
axes[0,2].set_xlabel("time (s)",size=MEDIUM_SIZE,labelpad=2)
axes[0,0].set_xlabel("time (s)",size=MEDIUM_SIZE,labelpad=2)
axes[0,1].set_ylabel("$\mu=F_S\,/\,F_N$",size=MEDIUM_SIZE,labelpad=7)

# bottom

axes[1,0].set_ylim([0,5.5])
axes[1,0].set_yticks([0,2,4])

# adjust spacings and limits
#real_tight_layout(fig)
set_grid(axes)
plt.subplots_adjust(wspace=0)
plt.subplots_adjust(hspace=0.35)



for i in range(1,4):
    plt.setp(axes[0,i].get_yticklabels(), visible=False)
    plt.setp(axes[1,i].get_yticklabels(), visible=False)


#fig.subplots_adjust(left=0.14,right=0.99, top=0.99, bottom=0.11)


axes[1,2].set_xlabel("$x$ (mm)",size=MEDIUM_SIZE,labelpad=2)
axes[1,0].set_xlabel("$x$ (mm)",size=MEDIUM_SIZE,labelpad=2)
axes[1,1].set_ylabel("$\sigma_{yy}$ (MPa)",size=MEDIUM_SIZE,labelpad=5.5)

axes[0,0].yaxis.labelpad=5
axes[1,0].yaxis.labelpad=9
axes[0,1].xaxis.set_label_coords(1.45, -0.18)
axes[1,1].xaxis.set_label_coords(1, -0.18)

for i in range(4):
    axes[1,i].text(5,5.05,r"$\left<F_N\right>={:.0f}$ N".format(round(dicto["mean_fns"][i])*10),size=6)
    axes[1,i].text(145,5.05,r"${}=${:.2f}".format(LC_name_short,(dicto["LCs"][i])),size=6,horizontalalignment='right')

axes[1,0].set_title("Empty-hole",size=MEDIUM_SIZE,pad=3)
axes[1,2].set_title("Granular (filled hole)",size=MEDIUM_SIZE,pad=3)


fig.text(0.007,0.95,"b",size=LETTER_SIZE, weight='bold')
fig.text(0.007,0.47,"c",size=LETTER_SIZE, weight='bold')
# save

plt.savefig("E:/Article/Figure_1/figure_1_c_d.svg")
plt.savefig("E:/Article/Figure_1/figure_1_c_d.pdf")
plt.savefig("E:/Article/Figure_1/figure_1_c_d.png",dpi=dpi_global)
#plt.show()
plt.close('all')
















