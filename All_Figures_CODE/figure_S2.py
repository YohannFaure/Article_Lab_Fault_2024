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

###
# Location
with open("E:/Article/parameters.py", 'r') as f:
        exec(f.read())



reload = False

try:
    loaded_data = np.load("E:/Article/Figure_S2/figure_S2.npy",allow_pickle= True).all()
    locals().update(loaded_data)
except:
    reload = True


###



def sliding_plot(x,disp,ax,vlines = None,labels=True,suptitle=False,color="blue",alpha=1):

    if not vlines is None:
        for v in vlines:
            #ax.axvline(v,color="black",linestyle=dash_line_style ,linewidth=0.4,alpha= secondary_plot_alpha)
            ax.plot([v,v],[0,disp[np.abs(x - v).argmin()]],
                    color=dashed_color,linestyle=dash_line_style,
                    linewidth=0.1,alpha= 0.2)

    ax.grid(True,which="both")

    ax.plot(x,disp,color=color,alpha=alpha)


    if labels:
        ax.set_ylabel(tot_sliding_short )

    if suptitle:
        ax.set_title(suptitle)


def creep_plot(x,creep,ax,labels=True,suptitle=False,color="blue",alpha=1,marker=scatter_marker,s=scatter_size,vlines=False ):
    if vlines:
        for i in range(len(x)):
            ax.plot([x[i],x[i]],[creep[i],100],
                    color=dashed_color,linestyle=dash_line_style,
                    linewidth=0.1,alpha=0.2)

    ax.plot(x,creep,color=color,alpha=alpha)
    ax.scatter(x,creep,marker=marker ,s=s ,c=color,alpha = 1 ,zorder=10,edgecolors="k",linewidth=0.01)

    ax.grid(True,which="both")

    if labels:
        ax.set_ylabel(sliding_perc_name_short )

    if suptitle:
        ax.set_title(suptitle)




def mu_plot(t,mu,ax,timings=None,linecolor=main_plot_color):
    a=next((i for i, b in enumerate(mu[7000:]>0.05) if b), None)+7000
    start = max(a-5200,0)
    ax.plot(t[start:]-t[start],mu[start:],color=linecolor )






def ramp(l,v,f=100):
    return(v*np.arange(0,l,1)/f)


### [[ RAMP ]]

i = [0,1,8,11]

if reload or force_reload:
    print("reloading data for Figure S2")


    loc = "E:/2023-2024/2024-02-27-tracking-resolution-zaber-deplacement-profilo/"

    data_prof_10 = np.genfromtxt(loc + '10micromsec.CSV', delimiter=';')[2:,0]/1000
    data_prof_100 = np.genfromtxt(loc + '100micromsec.CSV', delimiter=';')[2:,0]/1000
    data_prof_script = np.genfromtxt(loc + 'script2.CSV', delimiter=';')[12000:,0]/1000

    data_prof_10 -= data_prof_10[0]
    data_prof_100 -= data_prof_100[0]
    data_prof_script -= data_prof_script[0]



    matdata=scio.loadmat("E:/2023-2024/2024-02-27-tracking-resolution-zaber-deplacement-profilo/10micromsec.mat")
    data_sub=matdata["subx"][:,1:]
    data_pixel=matdata["pixx"][:,1:].astype(np.float32)


    # camera
    data_cam_ramp=np.mean(data_sub[i,:],axis=0)
    data_cam_ramp=data_cam_ramp-data_cam_ramp[0]
    data_cam_ramp=-data_cam_ramp/8.8-0.0025

    data_cam_ramp_pix = data_pixel[i[0]]
    data_cam_ramp_pix=data_cam_ramp_pix-data_cam_ramp_pix[0]
    data_cam_ramp_pix=-data_cam_ramp_pix/8.8

    time_cam_ramp = np.arange(0,len(data_cam_ramp))/100-1.5

    # profilo
    data_prof_10=data_prof_10-data_prof_10[0]-0.0025

    time_prof_10 = np.arange(0,len(data_prof_10))/100-15.66

    # simul
    time_simul_ramp=np.arange(0,60,1/100)

    data_simul_ramp = -ramp(len(time_simul_ramp),0.01)

### [[ script ]]

#for j in range(20,matdata["subx"].shape[0]):
i=[0,1,17,18]

if reload or force_reload:
    matdata=scio.loadmat("E:/2023-2024/2024-02-27-tracking-resolution-zaber-deplacement-profilo/script2.mat")
    data_sub=matdata["subx"][:,1:]
    data_pixel=matdata["pixx"][:,1:].astype(np.float32)



    # camera

    data_cam_script=np.mean(data_sub[i,10:],axis=0)
    data_cam_script=data_cam_script-data_cam_script[0]
    data_cam_script=-data_cam_script/8.8-0.005

    data_cam_script_pix = data_pixel[i[0],10:]
    data_cam_script_pix=data_cam_script_pix-data_cam_script_pix[0]
    data_cam_script_pix=-data_cam_script_pix/8.8

    time_cam_script = np.arange(0,len(data_cam_script))/100-0.21-5

    # profilo
    data_prof_script=data_prof_script-data_prof_script[0]-0.005

    time_prof_script = np.arange(0,len(data_prof_script))/100 - 10.666-0.0948-5

    # simul

    time_simul_script=np.arange(0,70,1/100)-5
    data_simul_script = np.zeros_like(time_simul_script)

    sle = 5 #s
    t=sle*100
    for i in range(7):
        data_simul_script[t:t+sle*100]-=ramp(sle*100,0.02)
        t=t+sle*100
        data_simul_script[t:]-= sle*0.02 + 0.1
        t=t+sle*100




### Matlab

##
def findevents(signal, sensit):
    typical_wait_time = 60
    # signal = np.convolve(signal, np.ones(5)/5, mode='valid')  # Smoothing signal, if needed
    diff = np.abs(signal[2:] - signal[:-2])
    m = np.mean(diff)
    diff -= m
    index = np.where(diff > sensit)[0]
    index = np.append(index, index[-1] + 2 * typical_wait_time)
    diffindex = np.abs(-index[1:] + index[:-1])
    found_events = [index[0]]
    found_events.extend(index[np.where(diffindex > typical_wait_time)[0] + 1])
    found_events.pop()  # Remove the last element
    return np.array(found_events)

# Assuming the variables such as avgtop, avgbot, xyresolution, tInit, tEnd, detection_grain,
# listAllCircles, sensit, space_after_event_temp, space_before_event, removelast,
# avgtopleft, avgbotleft, avgtopright, avgbotright, avgtopcenter, avgbotcenter, realtime
# are already defined and initialized in your Python environment


i=[0,1,17,18]

if reload or force_reload:
    matdata=scio.loadmat("E:/2023-2024/2024-02-27-tracking-resolution-zaber-deplacement-profilo/script2.mat")
    data_sub=matdata["subx"][:,1:]
    data_pixel=matdata["pixx"][:,1:].astype(np.float32)




    data_cam=np.mean(data_sub[i,10:],axis=0)
    data_cam=data_cam-data_cam[0]
    data_cam=-data_cam/8.8




    data_cam_cut=data_cam[:]


totslip = -data_cam_cut
realtime= np.arange(0,len(data_cam_cut))/100-0.21-5

found_events = findevents(data_cam_cut, 0.01)


if len(found_events) > 1:
    space_after_event_temp = min(np.fix(np.diff(found_events) / 10))
else:
    space_after_event_temp = 50

space_after_event = max(min(50, space_after_event_temp), 15)
space_before_event = 5


##



delta = np.sum(totslip[found_events + space_after_event] - totslip[found_events - space_before_event])

delta_tot = totslip[-1] - totslip[0]

creeped_distance = delta_tot - delta


###


# Compute creep proportion to seek convergence
creep = totslip

delta = []
delta_tot = []
totslip_partial = []

for i in range(len(found_events)):
    delta.append(np.sum(creep[found_events[0:i+1] + space_after_event] - creep[found_events[0:i+1] - space_before_event]))
    delta_tot.append(creep[found_events[i] + space_after_event] - creep[0])

    totslip_partial.append(abs(np.mean(creep[found_events[i] + int(space_after_event/2):found_events[i] + space_after_event]) ) )

creeped_distance_frac = (np.array(delta_tot) - np.array(delta)) / np.array(totslip_partial)
creeped_distance = np.array(delta_tot) - np.array(delta)




















## FIGURE

time_lim_1=[-1,51]
time_lim_2=[-0.5,55]



fig = plt.figure(layout=None)
fig.set_size_inches(size_fig_S2)

nrows=12


gs = fig.add_gridspec(nrows=5, ncols=2,
                      hspace=0, height_ratios=[1,0.1,0.5,0.05,0.5],
                      left=0.08)

axes=np.array([[None,None],[None,None]])

axes[0,0]=fig.add_subplot(gs[0,0])
axes[0,1]=fig.add_subplot(gs[0,1], sharex = axes[0,0])
axes[1,0]=fig.add_subplot(gs[2:,0], sharex = axes[0,0])
ax_br = [fig.add_subplot(gs[2,1], sharex = axes[0,0]),fig.add_subplot(gs[4,1], sharex = axes[0,0])]

##




#fig, axes = plt.subplots(nrows=2,ncols=2,sharex="col",sharey="none")
#fig.set_size_inches(size_fig_6)




# TOP LEFT

axes[0,0].plot(time_simul_ramp,-data_simul_ramp,label="instructions",zorder=3)
axes[0,0].plot(time_prof_10,-data_prof_10,label="profilometer")
axes[0,0].plot(time_cam_ramp,-data_cam_ramp_pix,label="pixel tracking",linestyle="solid",alpha=.5,c=u'#d62728')
axes[0,0].plot(time_cam_ramp,-data_cam_ramp,label="subpixel tracking",c=u'#2ca02c')


axes[0,0].plot(time_simul_ramp,-data_simul_ramp+0.008,linewidth=.5,c="k",linestyle=':')
axes[0,0].plot(time_simul_ramp,-data_simul_ramp-0.008,linewidth=.5,c="k",linestyle=':')

rect = mpl.patches.Rectangle((20,0.200),5,0.050,facecolor='None',edgecolor="r",linewidth=2,zorder=4)
axes[0,0].add_artist(rect)
axes[0,0].xaxis.set_minor_locator(MultipleLocator(10))
axes[0,0].xaxis.set_major_locator(MultipleLocator(20))
axes[0,0].yaxis.set_minor_locator(MultipleLocator(0.1))
axes[0,0].yaxis.set_major_locator(MultipleLocator(0.2))

axes[0,0].set_xlim([0,58])
axes[0,0].set_ylim([0,0.580])
axes[0,0].legend(facecolor='white', framealpha=1)
set_grid(axes[0,0])
axes[0,0].set_ylabel('displacement (mm)')

coords = [0.33,   0.6,    0.15,  0.15] #left, bottom, width, height
axin00=fig.add_axes(coords)



axin00.plot(time_simul_ramp,-data_simul_ramp,label="simul",zorder=4)
axin00.plot(time_prof_10,-data_prof_10,label="profilo")
axin00.plot(time_cam_ramp,-data_cam_ramp,label="camera")

axin00.plot(time_simul_ramp, -data_simul_ramp+0.008, linewidth=.5, c="k",linestyle=':')
axin00.plot(time_simul_ramp, -data_simul_ramp-0.008, linewidth=.5, c="k",linestyle=':')

axin00.set_xlim([20,25])
axin00.set_ylim([0.200,0.250])
axin00.xaxis.set_minor_locator(MultipleLocator(1))
axin00.xaxis.set_major_locator(MultipleLocator(2))
axin00.yaxis.set_minor_locator(MultipleLocator(0.010))
axin00.yaxis.set_major_locator(MultipleLocator(0.020))


axin00.grid(False)
axin00.set_facecolor("w")
set_up_inset(axin00)


# TOP RIGHT



axes[0,1].plot(time_simul_script,-data_simul_script,label="instructions",zorder=3)
axes[0,1].plot(time_prof_script,-data_prof_script,label="profilometer")
axes[0,1].plot(time_cam_script,-data_cam_script_pix,label="pixel tracking",linestyle="solid",alpha=.5,c=u'#d62728')
axes[0,1].plot(time_cam_script,-data_cam_script,label="subpixel tracking",c=u"#2ca02c")

axes[0,1].plot(time_simul_script,-data_simul_script+0.008,linewidth=.5,c="k",linestyle=':')
axes[0,1].plot(time_simul_script,-data_simul_script-0.008,linewidth=.5,c="k",linestyle=':')

rect = mpl.patches.Rectangle((14,0.300),12,0.300,facecolor='None',
                edgecolor="r",linewidth=2,zorder=4)
axes[0,1].add_artist(rect)
axes[0,1].xaxis.set_minor_locator(MultipleLocator(10))
axes[0,1].xaxis.set_major_locator(MultipleLocator(20))
axes[0,1].yaxis.set_minor_locator(MultipleLocator(0.1))
axes[0,1].yaxis.set_major_locator(MultipleLocator(0.2))

axes[0,1].set_ylim([0,1.30])
axes[0,1].legend(facecolor='white', framealpha=1)
set_grid(axes[0,1])
axes[0,1].set_ylabel('displacement (mm)')


for i in range(len(found_events)):
    axes[0,1].axvline(time_simul_script[found_events[i]], linestyle=':', color='k',linewidth=.5)



coords = [0.83,   0.6,    0.15,  0.15] #left, bottom, width, height
axin01=fig.add_axes(coords)



axin01.plot(time_simul_script,-data_simul_script,label="simul",zorder=3)
axin01.plot(time_prof_script,-data_prof_script,label="profilo")
axin01.plot(time_cam_script,-data_cam_script,label="camera")
#axin01.plot(time_cam_script,-data_cam_script_pix,label="camera pix")

axin01.plot(time_simul_script,-data_simul_script+0.008,linewidth=.5,c="k",linestyle=':')
axin01.plot(time_simul_script,-data_simul_script-0.008,linewidth=.5,c="k",linestyle=':')

axin01.set_xlim([14,26])
axin01.set_ylim([0.300,0.60])
axin01.xaxis.set_minor_locator(MultipleLocator(1))
axin01.xaxis.set_major_locator(MultipleLocator(2))
axin01.yaxis.set_minor_locator(MultipleLocator(0.050))
axin01.yaxis.set_major_locator(MultipleLocator(0.10))


axin01.grid(False)
axin01.set_facecolor("w")
set_up_inset(axin01)












# bottom left



ramp_or_script = "ramp"


if ramp_or_script=="ramp":
    print("ramp")
    # for ramp
    min_of_max = min([max(time_simul_ramp),max(time_prof_10),max(time_cam_ramp)])
    max_of_min = max([min(time_simul_ramp),min(time_prof_10),min(time_cam_ramp)])

    mask_simul = np.logical_and(time_simul_ramp>max_of_min,time_simul_ramp<min_of_max)
    mask_prof = np.logical_and(time_prof_10>max_of_min,time_prof_10<min_of_max)
    mask_cam = np.logical_and(time_cam_ramp>max_of_min,time_cam_ramp<min_of_max)


    time_shared= time_simul_ramp[mask_simul]
    compar_simul = -data_simul_ramp[mask_simul]+data_cam_ramp[mask_cam]
    compar_simul -= np.mean(compar_simul)
    compar_prof = -data_prof_10[mask_prof]+data_cam_ramp[mask_cam]
    compar_prof -= np.mean(compar_prof)

    axes[1,0].plot(time_shared,1000*compar_simul,label="$x_{ref}$ from instructions",zorder=3)
    axes[1,0].plot(time_shared,1000*compar_prof,label="$x_{ref}$ from profilometer")


elif ramp_or_script == "script":
    # for script
    min_of_max = min([max(time_simul_script),max(time_prof_script),max(time_cam_script)])
    max_of_min = max([min(time_simul_script),min(time_prof_script),min(time_cam_script)])

    mask_simul = np.logical_and(time_simul_script>max_of_min,time_simul_script<min_of_max)
    mask_prof = np.logical_and(time_prof_script>max_of_min,time_prof_script<min_of_max)
    mask_cam = np.logical_and(time_cam_script>max_of_min,time_cam_script<min_of_max)

    mask_prof[1076]=False
    mask_prof[1077]=False

    time_shared= time_simul_script[mask_simul]
    compar_simul = -data_simul_script[mask_simul]+data_cam_script[mask_cam]
    compar_simul -= np.mean(compar_simul)
    compar_prof = -data_prof_script[mask_prof]+data_cam_script[mask_cam]
    compar_prof -= np.mean(compar_prof)

    axes[1,0].plot(time_shared,1000*compar_simul,label="$x_{ref}$ from instructions",zorder=3)
    axes[1,0].plot(time_shared,1000*compar_prof,label="$x_{ref}$ from profilometer")


axes[1,0].yaxis.set_minor_locator(MultipleLocator(2.5))
axes[1,0].yaxis.set_major_locator(MultipleLocator(5))

axes[1,0].set_ylim([-13,13])
axes[1,0].axhline(8,linestyle = ":", c="k")
axes[1,0].axhline(-8,linestyle = ":", c="k")

axes[1,0].legend(facecolor='white', framealpha=1)
set_grid(axes[1,0])

axes[1,0].set_xlabel("time (s)")
axes[1,0].set_ylabel("$x-x_{ref}$ (µm)")




# bottom right

ax_br[0].plot(realtime[found_events], creeped_distance, '-', color='red', label='Left',marker="x")
#ax_br[0].plot([0,60], [0,0.6], ':', color='k')
ax_br[0].set_ylabel('$\delta_{IE}$ (mm)')
ax_br[0].set_ylim([0,0.65])
ax_br[0].yaxis.set_minor_locator(MultipleLocator(0.1))
ax_br[0].yaxis.set_major_locator(MultipleLocator(0.2))
plt.setp(ax_br[0].get_xticklabels(), visible=False)

for i in range(len(found_events)):
    ax_br[0].axvline(time_simul_script[found_events[i]], linestyle=':', color='k',linewidth=.5)
    ax_br[1].axvline(time_simul_script[found_events[i]], linestyle=':', color='k',linewidth=.5)



ax_br[1].plot(realtime[found_events], creeped_distance_frac, '-', color='red', label='Left',marker="x")
ax_br[1].set_ylabel('$S=\delta_{IE}/\delta_{tot}$')
ax_br[1].set_ylim([0.41,0.59])
#ax_br[1].axhline(50,c="k",linestyle=":")
ax_br[1].set_xlabel('time (s)')
ax_br[1].yaxis.set_minor_locator(MultipleLocator(0.025))
ax_br[1].yaxis.set_major_locator(MultipleLocator(0.05))

axes[0,1].get_yaxis().labelpad=6
set_grid(ax_br)


# adjust spacing
real_tight_layout(fig)
plt.subplots_adjust(wspace=0.22,hspace=0)
"""
axes[1,1].get_xaxis().labelpad=2
"""
#axes[1,0].get_xaxis().labelpad=2

axes[0,0].yaxis.set_label_coords(-0.08, 0.5)
axes[1,0].yaxis.set_label_coords(-0.07, 0.5)












fig.subplots_adjust(left=0.11, right=0.99, top=0.98, bottom=0.1)


y=(size_fig_1[1]-3*mm)/size_fig_1[1]
fig.text(0.01,y,"a",size=LETTER_SIZE, weight="bold")
fig.text(.505,y,"c",size=LETTER_SIZE, weight="bold")
fig.text(0.01,y/1.88,"b",size=LETTER_SIZE, weight="bold")
fig.text(.505,y/1.88,"d",size=LETTER_SIZE, weight="bold")


plt.savefig("E:/Article/Figure_S2/figure_S2.png",dpi=dpi_global)
plt.savefig("E:/Article/Figure_S2/figure_S2.pdf")
plt.savefig("E:/Article/Figure_S2/figure_S2.svg")

#plt.show()
plt.close('all')






to_save = {}
var_to_save = ["creeped_distance_frac",
        "creeped_distance",
        "compar_prof",
        "found_events",
        "compar_simul",
        "time_cam_ramp",
        "time_shared",
        "data_cam_ramp_pix",
        "time_simul_ramp",
        "time_cam_ramp",
        "data_simul_ramp",
        "data_cam_ramp",
        "time_prof_10",
        "time_simul_script",
        "data_simul_ramp",
        "time_simul_ramp",
        "data_simul_script",
        "data_prof_10",
        "data_prof_script",
        "time_cam_script",
        "time_prof_script",
        "data_cam_script_pix",
        "data_cam_cut",
        "data_cam_script"]



for v in var_to_save:
    to_save[v]=eval(v)


np.save("E:/Article/Figure_S2/figure_S2.npy",to_save)
scio.savemat("E:/Article/Figure_S2/figure_S2.mat",to_save)





