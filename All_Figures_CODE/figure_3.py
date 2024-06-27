
with open("E:/Article/parameters.py", 'r') as f:
        exec(f.read())



loc_old_data = "D:/Users/Manips/Documents/DATA/FRICS/2023/2023-01-05-manip-grains/summary2.npy"
loc_new_data = loc_general+"python_plots/summary_data.npy"


reload = False
try:
    loaded_data = np.load("E:/Article/Figure_3/figure_3.npy",allow_pickle=True).all()
    locals().update(loaded_data)
except:
    reload = True


if force_reload or reload :
    print("reloading data for Figure 3")
    old_data=np.load(loc_old_data,allow_pickle=True).all()

    new_data=np.load(loc_new_data,allow_pickle=True).all()



###

def nice_plot(xpos,ypos,ax=None,xerr=None,yerr=None,xlabel="",ylabel="",
              annotate=None,old_data=False,
              color="b",error_bar_color="k",marker_size=3,capsize=3,
              marker="d",solid_marker=solid_marker,in_solid=None,
              solid_color=solid_solid_color,
              label = None,
              label_solid = None):
    if ax is None:
        fig, ax = plt.subplots()
    if old_data:
        ax.errorbar(old_data[0],old_data[1],xerr=old_data[2],yerr=old_data[3],
                    fmt=" ",capsize=capsize,color=color,ecolor=error_bar_color,elinewidth=.5, alpha=error_bar_alpha,markeredgewidth=markeredgewidth)
        ax.scatter(old_data[0],old_data[1],color=color,s=marker_size,marker=marker,zorder=5,edgecolors="k",linewidth=0.01)

    # all data
    ax.errorbar(xpos,ypos, xerr=xerr,yerr=yerr,
                fmt=" ",capsize=capsize,color=color,ecolor=error_bar_color,elinewidth=.5,alpha=error_bar_alpha,markeredgewidth=markeredgewidth)
    ax.scatter(xpos,ypos,color=color,s=marker_size,marker=marker,zorder=5,edgecolors="k",linewidth=0.01,label = label)

    # solids
    ax.errorbar(xpos[in_solid],ypos[in_solid], xerr=xerr[...,in_solid],yerr=yerr[...,in_solid],
                fmt=" ",capsize=capsize,color=solid_color,ecolor=error_bar_color,elinewidth=.5,alpha=error_bar_alpha ,markeredgewidth=markeredgewidth)
    ax.scatter(xpos[in_solid],ypos[in_solid],color=solid_color,s=marker_size,marker=solid_marker,zorder=5,edgecolors="k",linewidth=0.01,label = label_solid)
    if not annotate is None:
        for i in range(len(annotate)):
            ax.annotate(annotate[i], (xpos[i], ypos[i]))

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)



substract_sides = False
plot_sides = True
plot_old = True





##


fig = plt.figure(layout=None)
fig.set_size_inches(size_fig_3)

gs = fig.add_gridspec(nrows=8, ncols=11, left=0.11, right=0.99,
                      hspace=0, wspace=0.65)
ax0 = fig.add_subplot(gs[0:4, 0:4])
ax1 = fig.add_subplot(gs[4:, 0:4], sharex=ax0,sharey=ax0)
ax2 = fig.add_subplot(gs[0:8,5: ], sharex=ax0,sharey=ax0)


ax3 = fig.add_axes([0.605, 0.75,   0.22,  0.22],facecolor="w")

axes=np.array([ax0,ax1,ax2,ax3])




if plot_old:
    old_data0=[old_data["lc"],old_data["ie_slip_grains"]/100,
            old_data["lc_err"],old_data["ie_slip_err"]/100]
    old_data1=[old_data["lc"],old_data["ie_slip_solid"]/100,
            old_data["lc_err"],old_data["ie_slip_err"]/100]
    old_data2=[old_data["lc"],old_data["ie_slip_grains"]/100-old_data["ie_slip_solid"]/100,
            old_data["lc_err"],old_data["ie_slip_err"]/100]
    old_data3=[old_data["ie_slip_grains"]/100-old_data["ie_slip_solid"]/100,old_data["freq"],
                old_data["ie_slip_err"]/100,old_data["freq_err"]]

else:
    old_data0=None
    old_data1=None
    old_data2=None
    old_data3=None


if differentiate_solids_fig_3:
    in_solid=np.isin(new_data["manip_num"],solids)
else:
    in_solid=None


nice_plot(new_data["mean_lc"],new_data["creep_center"]/100,ax=ax0,
        xerr=new_data["wide_lc"],yerr=new_data["sigma_creep_center"]/100,
        xlabel=None,ylabel="$S^{patch}_f$",
        old_data=old_data0,in_solid=in_solid,
        color=granular_color, error_bar_color=error_bar_color,
        marker_size=scatter_size, capsize=error_bar_width, marker=scatter_marker,
        solid_color = hole_in_solid_color,
        label = "granular",
        label_solid = "empty-hole")


nice_plot(new_data["mean_lc"],new_data["creep_sides"]/100,ax=ax1,
        xerr=new_data["wide_lc"],yerr=new_data["sigma_creep_center"]/100,
        xlabel=r"${}$".format(LC_name_short),ylabel="$S^{solid}_f$",
        old_data=old_data1,in_solid=in_solid,
        color=solid_in_granular_color, error_bar_color=error_bar_color,
        marker_size=scatter_size, capsize=error_bar_width, marker=scatter_marker,
        solid_color=solid_in_granular_color,
        label = "granular",
        label_solid = "empty-hole")


nice_plot(new_data["mean_lc"],new_data["creep_center"]/100-new_data["creep_sides"]/100,ax=ax2,
        xerr=new_data["wide_lc"],yerr=new_data["sigma_creep_center"]/100,
        xlabel=r"${}$".format(LC_name_short),ylabel=r"$S^{patch}_f-S^{solid}_f$",
        old_data=old_data2,in_solid=in_solid,
        color=main_plot_color, error_bar_color=error_bar_color,
        marker_size=scatter_size, capsize=error_bar_width, marker=scatter_marker,
        label = "granular",
        label_solid = "empty-hole")


nice_plot(new_data["creep_center"]/100-new_data["creep_sides"]/100,new_data["mean_freq"],ax=ax3,
            xerr=new_data["sigma_creep_center"]/100,yerr=new_data["wide_freq"],
            xlabel=r"$S^{patch}_f-S^{solid}_f$" ,ylabel=freq_name_short ,
            old_data=old_data3,in_solid=in_solid,
            color=main_plot_color, error_bar_color=error_bar_color,
            marker_size=scatter_size/4, capsize=error_bar_width/2, marker="d")

legends = [["patch (empty)" , "solid-solid"],
           ["patch (filled)", "solid-solid"]]

#get handles and labels
#handles, labels = ax1.get_legend_handles_labels()
#order = [0]
#ax1.legend([handles[idx] for idx in order],[labels[idx] for idx in order],prop={'size': INSET_SMALL_SIZE},framealpha = 0, facecolor = (1,1,1,0),loc = "upper left",bbox_to_anchor=(-.07,1.),handletextpad=0.1)

handles, labels = ax0.get_legend_handles_labels()
order = [1,0]
ax0.legend([handles[idx] for idx in order],[labels[idx] for idx in order],prop={'size': INSET_SMALL_SIZE},framealpha = 0, facecolor = (1,1,1,0),loc = "upper left",bbox_to_anchor=(-.07,1.045),handletextpad=0.1)

handles, labels = ax1.get_legend_handles_labels()
order = [1,0]
ax1.legend([handles[idx] for idx in order],[labels[idx] for idx in order],prop={'size': INSET_SMALL_SIZE},framealpha = 0, facecolor = (1,1,1,0),loc = "upper left",bbox_to_anchor=(-.07,1.0),handletextpad=0.1)


handles, labels = ax2.get_legend_handles_labels()
order = [1,0]
ax2.legend([handles[idx] for idx in order],[labels[idx] for idx in order],prop={'size': INSET_SMALL_SIZE},framealpha = 0, facecolor = (1,1,1,0),loc = "lower right",bbox_to_anchor=(1.01,0),handletextpad=0.1)



ax0.get_yaxis().labelpad=1
ax1.get_yaxis().labelpad=1
ax2.get_yaxis().labelpad=0
ax1.get_xaxis().labelpad=2
ax2.get_xaxis().labelpad=2







# adjust ticks
# Top Left
ax0.set_xlim([-1.1,2.8])
ax0.set_xticks([-1,0,1,2])
ax0.set_xticklabels(["-1","0","1","2"])
ax0.set_ylim([-4/100,28/100])
ax0.set_yticks([0,10/100,20/100])
ax0.set_yticklabels(["0",0.1,0.2])
ax0.xaxis.set_minor_locator(MultipleLocator(1))
ax0.yaxis.set_minor_locator(MultipleLocator(0.05))


plt.setp(ax0.get_xticklabels(), visible=False)


# right
ax3.set_xlim([-2/100,18/100])
ax3.set_xticks([0,10/100])#ax3.set_ylim([0,0.25])
ax3.set_xticklabels(["0",0.1])
ax3.xaxis.set_minor_locator(MultipleLocator(0.05))

ax3.set_ylim([-0.01,0.6])
ax3.set_yticks([0,0.5])
ax3.set_yticklabels(["0",0.5])
ax3.yaxis.set_minor_locator(MultipleLocator(0.25))
set_up_inset(ax3)

ax3.get_yaxis().labelpad=inset_label_pad-2
ax3.get_xaxis().labelpad=inset_label_pad


set_grid(axes[-1])
set_grid(axes[:-1])

axes[-1].grid(False,which="both")




y=(size_fig_1[1]-3.5*mm)/size_fig_1[1]
fig.text(0.01,y,"a",size=LETTER_SIZE, weight='bold')
#fig.text(0.01,y/1.9,"b",size=LETTER_SIZE, weight='bold')
fig.text(.43,y,"b",size=LETTER_SIZE, weight='bold')
# save


fig.subplots_adjust( top=0.99, bottom=0.12)

plt.savefig("E:/Article/Figure_3/figure_3.png",dpi=dpi_global)
plt.savefig("E:/Article/Figure_3/figure_3.jpg",dpi=dpi_global)
plt.savefig("E:/Article/Figure_3/figure_3.pdf")
plt.savefig("E:/Article/Figure_3/figure_3.svg")



plt.close('all')



###


to_save={}

to_save["old_data"]=old_data
to_save["new_data"]=new_data
to_save["solids"]=solids

np.save("E:/Article/Figure_3/figure_3.npy",to_save)
scio.savemat("E:/Article/Figure_3/figure_3.mat",to_save)






























