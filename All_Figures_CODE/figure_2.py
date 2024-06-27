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





loc_folder_main=loc_general+"Full_Daq_{}_figures/"

loc_folders=[loc_folder_main.format(i) for i in chosen_manips_fig2]



roll_smooth=25
start=0



reload = False

try :
    loaded_data = np.load("E:/Article/Figure_2/figure_2.npy",allow_pickle=True).all()
    locals().update(loaded_data)
except:
    reload=True


if reload or force_reload:
    print("reloading data for Figure 2")
    t0s=[90,24.5]

    x1s=[]
    x2s=[]

    creep_percents=[]

    creep_percent_lefts=[]
    creep_percent_rights=[]
    creep_percent_centers=[]

    creep_dist_lefts=[]
    creep_dist_rights=[]
    creep_dist_centers=[]

    disp_lefts=[]
    disp_rights=[]
    disp_centers=[]



    for i in range(2):
        matdata1=scio.loadmat(loc_folders[i]+"creep/creep1_data.mat")
        matdata2=scio.loadmat(loc_folders[i]+"creep/creep2_data.mat")

        x1=matdata1["creep_1_x_axis"].flatten()
        x2=matdata2["creep_2_x_axis"].flatten()

        disp_center=matdata1["displacement_center"].flatten()
        disp_left=matdata1["displacement_left"].flatten()
        disp_right=matdata1["displacement_right"].flatten()

        creep_percent_center=matdata2["pourcent_center"].flatten()
        creep_percent_right=matdata2["pourcent_right"].flatten()
        creep_percent_left=matdata2["pourcent_left"].flatten()

        creep_dist_center=matdata2["distance_center"].flatten()
        creep_dist_right=matdata2["distance_right"].flatten()
        creep_dist_left=matdata2["distance_left"].flatten()

        creep_percent=creep_percent_center-0.5*(creep_percent_right+creep_percent_left)
        creep_percent_left=np.insert(creep_percent_left,0,0)
        creep_percent_right=np.insert(creep_percent_right,0,0)
        creep_percent_center=np.insert(creep_percent_center,0,0)

        creep_dist_center=np.insert(creep_dist_center,0,0)
        creep_dist_right=np.insert(creep_dist_right,0,0)
        creep_dist_left=np.insert(creep_dist_left,0,0)

        creep_percent=np.insert(creep_percent,0,0)
        x2=x2+t0s[i]
        x2=np.insert(x2,0,0)
        x1=x1+t0s[i]
        x1s.append(x1)
        x2s.append(x2)

        creep_percents.append(creep_percent)
        creep_percent_lefts.append(creep_percent_left)
        creep_percent_rights.append(creep_percent_right)
        creep_percent_centers.append(creep_percent_center)

        creep_dist_centers.append(creep_dist_center)
        creep_dist_rights.append(creep_dist_right)
        creep_dist_lefts.append(creep_dist_left)

        disp_lefts.append(disp_left)
        disp_rights.append(disp_right)
        disp_centers.append(disp_center)



    creep_percent_sides=[(c[0]+c[1])/2 for c in zip(creep_percent_rights,creep_percent_lefts)]
    creep_dist_sides=[(c[0]+c[1])/2 for c in zip(creep_dist_rights,creep_dist_lefts)]
    disp_sides=[(c[0]+c[1])/2 for c in zip(disp_rights,disp_lefts)]





    # load inset data


    try :
        dicto = np.load("E:/Article/Figure_1/figure_1_c_d.npy",allow_pickle=True).all()

        timings=dicto["timings"]
        times=dicto["times"]
        mus=dicto["mus"]
        mean_fns=dicto["mean_fns"]

    except ValueError:
        print("try reloading fig 1.")


    timings=[timings[0],timings[-1]]
    times=[times[0],times[-1]]
    mus=[mus[0],mus[-1]]
    mean_fns=[mean_fns[0],mean_fns[-1]]




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


def creep_plot(x,creep,ax,labels=True,suptitle=False,color="blue",alpha=1,marker=scatter_marker,s=scatter_size,vlines=False,label=None ):
    if vlines:
        for i in range(len(x)):
            ax.plot([x[i],x[i]],[creep[i],100],
                    color=dashed_color,linestyle=dash_line_style,
                    linewidth=0.1,alpha=0.2)

    ax.plot(x,creep,color=color,alpha=alpha,label=label)
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



##

time_lim_1=[0,220]
time_lim_2=[0,180]



fig, axes = plt.subplots(nrows=2,ncols=2,sharex="col",sharey="none")
fig.set_size_inches(size_fig_2)


colors_here=[solid_solid_color,main_plot_color]


# main figure
colors_sides=[solid_in_granular_color,solid_in_granular_color]
colors_center=[hole_in_solid_color,granular_color]
markers=[solid_marker,scatter_marker]
markers_size=[scatter_size*2/3,scatter_size]
for i in range(2):
    sliding_plot(x1s[i],disp_sides[i],axes[0,i],vlines = None,labels=True,suptitle=False,
                    color=colors_sides[i],alpha=1)
    sliding_plot(x1s[i],disp_centers[i],axes[0,i],
                    vlines = x2s[i][1:],labels=True,suptitle=False,
                    color=colors_center[i])
    creep_plot(x2s[i],creep_percent_sides[i]/100,
               axes[1,i],labels=True,suptitle=False,
               color=colors_sides[i],alpha = 1,#.2
               vlines=True, marker = markers[i],s=markers_size[i])
    creep_plot(x2s[i],creep_percent_centers[i]/100,axes[1,i],labels=True,suptitle=False,
                color=colors_center[i],vlines=False, marker = markers[i],s=markers_size[i])




# adjust ticks
# top left
axes[0,0].set_xlim(time_lim_1)
axes[0,0].set_ylim([0,3.9])
axes[0,0].set_yticks([0,1,2,3])
axes[0,0].xaxis.set_minor_locator(MultipleLocator(50))
axes[0,0].xaxis.set_major_locator(MultipleLocator(100))

# top right
axes[0,1].set_xlim(time_lim_2)
axes[0,1].set_ylim([0,2.60])
axes[0,1].set_yticks([0,1,2])
axes[0,1].set_yticklabels([0,1,2])
axes[0,1].xaxis.set_minor_locator(MultipleLocator(50))
axes[0,1].xaxis.set_major_locator(MultipleLocator(100))

# bottom left
axes[1,0].set_ylim([0,2.9/100])
axes[1,0].set_yticks([0,1/100,2/100])
axes[1,0].set_yticklabels(["0","0.01","0.02"])
# axes[1,0].set_yticks([0,1/100,2/100,3/100])
# axes[1,0].set_yticklabels(["0","0.01","0.02","0.03"])
#axes[1,0].text(3, 3.47/100, r"$\times 10^{-2}$",size=SMALL_SIZE)
axes[1,0].set_xlabel("time (s)")

# bottom right
axes[1,1].set_ylim([0,38/100])
axes[1,1].set_yticks([0,10/100,20/100,30/100])
axes[1,1].set_yticklabels(["0","0.1","0.2","0.3"])
#axes[1,1].text(3, 3.47/10, r"$\times 10^{-2}$",size=SMALL_SIZE)
axes[1,1].set_xlabel("time (s)")



# adjust spacing
real_tight_layout(fig)
plt.subplots_adjust(wspace=0.22,hspace=0)

axes[1,1].get_xaxis().labelpad=2
axes[1,0].get_xaxis().labelpad=2

axes[0,0].yaxis.set_label_coords(-0.23, 0.5)
axes[1,0].yaxis.set_label_coords(-0.24, 0.5)

axes[0,1].yaxis.set_label_coords(-0.18, 0.5)
axes[1,1].yaxis.set_label_coords(-0.19, 0.5)





# adding the insets


# These are in unitless percentages of the figure size. (0,0 is bottom left)
coords = [#left, bottom, width, height
         [0.24,   0.84,    0.14,  0.13],
         [0.727,     0.84,    0.14,  0.13],
         [0.343,    0.375,    0.15,  0.14],
         [0.83,   0.375,    0.15,  0.14],
         ]

# create the axes :
axesin=np.array([fig.add_axes(coords[i]) for i in range(4)])

legends = [["hole (empty)" , "solid-solid"],
           ["hole (filled)", "solid-solid"]]

bbox = [(0.93,0.52),
        (0.84,0.52)]

# Bottom
for i in range(2):
    axin=axesin[2+i]

    creep_plot(x2s[i],
               (creep_dist_lefts[i]+creep_dist_rights[i])/2,
               axin,labels=None,suptitle=False,
               color=colors_sides[i],
               alpha = 1,# secondary_plot_alpha,
               marker="|",
               s=scatter_size/4,
               label = legends[i][1])
    creep_plot(x2s[i],
               creep_dist_centers[i],axin,labels=None,suptitle=False,
               color=colors_center[i],alpha = 1,marker="|",s=scatter_size/4,
               label = legends[i][0])

    if i==0:
        axin.set_xlim(time_lim_1)
    if i==1:
        axin.set_xlim(time_lim_2)
    axin.xaxis.set_minor_locator(MultipleLocator(50))
    axin.xaxis.set_major_locator(MultipleLocator(100))

    axin.get_yaxis().labelpad=inset_label_pad

    axin.set_ylabel(sliding_ie_name_short)
    axin.set_xlabel("time (s)",labelpad=inset_label_pad)
    if i==0:
        axin.set_ylim([0,0.038])
        axin.set_yticks([0,0.02])
        axin.set_yticklabels([0,0.02])
        axin.yaxis.set_minor_locator(MultipleLocator(0.01))


    else:
        axin.set_ylim([0,0.27])
        axin.set_yticks([0,0.2])
        axin.set_yticklabels([0,0.2])
        axin.yaxis.set_minor_locator(MultipleLocator(0.1))
    if i==0:
        axin.xaxis.set_label_coords(0.5, -0.3)
        axin.yaxis.set_label_coords(-0.42, 0.5)
    if i==1:
        axin.xaxis.set_label_coords(0.5, -0.3)
        axin.yaxis.set_label_coords(-0.32, 0.5)

    set_up_inset(axin)
    #get handles and labels
    handles, labels = axin.get_legend_handles_labels()
    order = [1,0]
    axin.legend([handles[idx] for idx in order],[labels[idx] for idx in order],prop={'size': 4},framealpha = 0, facecolor = (1,1,1,0),handlelength =.5, loc='lower right',bbox_to_anchor=bbox[i],handletextpad=0.5)




#top
for i in range(2):
    axin=axesin[i]


    mu_plot(times[i],mus[i],axin,timings=timings[i],linecolor=colors_here[i])


    if i==0:
        axin.set_xlim(time_lim_1)
    if i==1:
        axin.set_xlim(time_lim_2)
    axin.xaxis.set_minor_locator(MultipleLocator(50))
    axin.xaxis.set_major_locator(MultipleLocator(100))
    axin.set_ylim([0,0.365])
    axin.set_yticks([0,0.15,0.3])
    axin.set_yticklabels([0,0.15,0.3])




    axin.set_ylabel(r"$\mu$",labelpad=inset_label_pad)
    axin.set_xlabel("time (s)",labelpad=inset_label_pad)



    #axin.yaxis.tick_right()
    #axin.yaxis.set_label_position("right")


    set_up_inset(axin)



# adding the dashed lines indicating the final value of S
x_top = 133
x_bot = 146


x_dash   = x2s[-1][-5:]

y_dash_1 = np.ones_like(x_dash)*np.median(creep_percent_centers[-1][-5:])/100

y_dash_2 = np.ones_like(x_dash)*np.median(creep_percent_sides[-1][-5:])/100

axes[1,1].plot(x_dash,y_dash_1,linestyle = dash_line_style, c=dashed_color,zorder=10)
axes[1,1].plot(x_dash,y_dash_2,linestyle = dash_line_style, c=dashed_color,zorder=10)

axes[1,1].arrow(x_top, 0, 0, y_dash_1[-1],length_includes_head=True,linewidth=.5,head_width=3,head_length=y_dash_1[-1]/10,color=granular_color,zorder=10)
axes[1,1].arrow(x_bot, 0, 0, y_dash_2[-1],length_includes_head=True,linewidth=.5,head_width=3,head_length=y_dash_1[-1]/10,color=solid_in_granular_color,zorder=10)

axes[1,1].text(x_top-39,y_dash_2[-1]*2.4,r"$S^{patch}_f$",c=granular_color,size=MEDIUM_SIZE)
axes[1,1].text(x_bot-9,y_dash_2[-1]*1.6,r"$S^{solid}_f$",c=solid_in_granular_color,size=MEDIUM_SIZE)


from matplotlib.transforms import TransformedBbox, blended_transform_factory
import matplotlib.patches as patches


set_grid(axes)
for axin in axesin:
    set_grid(axin)
for ax in axesin:
    ax.grid(False,which="both")


fig.subplots_adjust(left=0.15, right=0.99, top=0.98, bottom=0.1,wspace=0.38)


y=(size_fig_1[1]-3*mm)/size_fig_1[1]
fig.text(0.01,y,"a",size=LETTER_SIZE, weight="bold")
fig.text(.52,y,"b",size=LETTER_SIZE, weight="bold")
fig.text(0.01,y/1.88,"c",size=LETTER_SIZE, weight="bold")
fig.text(.52,y/1.88,"d",size=LETTER_SIZE, weight="bold")


plt.savefig("E:/Article/Figure_2/figure_2.png",dpi=dpi_global)
plt.savefig("E:/Article/Figure_2/figure_2.pdf")
plt.savefig("E:/Article/Figure_2/figure_2.svg")

plt.close('all')

###


##

to_save={}

to_save["times"]=times
to_save["mus"]=mus
to_save["x1s"]=x1s
to_save["disp_sides"]=disp_sides
to_save["disp_centers"]=disp_centers
to_save["x2s"]=x2s
to_save["creep_percent_sides"]=creep_percent_sides
to_save["creep_percent_centers"]=creep_percent_centers
to_save["creep_dist_lefts"]=creep_dist_lefts
to_save["creep_dist_rights"]=creep_dist_rights
to_save["chosen_manips_fig2"]=chosen_manips_fig2
to_save["creep_dist_centers"]=creep_dist_centers
to_save["timings"]=timings


timings

np.save("E:/Article/Figure_2/figure_2.npy",to_save)
scio.savemat("E:/Article/Figure_2/figure_2.mat",to_save)






















