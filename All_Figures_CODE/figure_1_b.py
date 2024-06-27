## Imports
# Science
from matplotlib.colors import LinearSegmentedColormap

# custom file
try :
    import sys
    sys.path.insert(0, "D:/Users/Manips/Documents/Python/DAQ_Python")
    from Python_DAQ import *
except :
    from DAQ_Python.Python_DAQ import *
# this also imports E and nu
with open("E:/Article/parameters.py", 'r') as f:
        exec(f.read())




### load data : set up the loading


reload = False
try:
    loaded_data = np.load("E:/Article/Figure_1/figure_1_b.npy",allow_pickle=True).all()
    locals().update(loaded_data)
except:
    reload = True


if force_reload or reload :
    print("reloading data for Figure 1b")
    datagran=np.load("E:/2023-2024/2023-12-01-low_FN_measurement/python_plots/summary_data.npy",allow_pickle=True).all()
    datasolid=np.load("E:/2023-2024/2023-07-11-manips-10-voies/python_plots/summary_data.npy",allow_pickle=True).all()

    with open("E:/2023-2024/2024-03-13-manip-vrai-solide-solide/timings_and_forces.txt", 'r') as f:
            exec(f.read())

    ss_times_mean = 1.1*np.array( [ np.mean(np.diff(times[i])) for i in range(len(times))] )
    ss_times_std = 1.1*np.array( [ np.std(np.diff(times[i])) for i in range(len(times))] )
    ss_sig=np.array(fns)/(0.01 * 0.15)




in_solid=np.isin(datasolid["manip_num"],solids)




###


def nice_plot(xpos,ypos,ax=None,xerr=None,yerr=None,xlabel="",ylabel="",
              annotate=None,old_data=False,
              color="b",error_bar_color="k",marker_size=3,capsize=3,
              marker="d",in_solid=None,solid_color=solid_solid_color,cmap=None,label=None):

    # all data
    if not cmap is None:
        ax.errorbar(xpos,ypos, xerr=xerr,yerr=yerr,
                fmt=" ",capsize=capsize,color="k",
                ecolor=error_bar_color,elinewidth=.5,
                alpha=error_bar_alpha,markeredgewidth=markeredgewidth)
        aaaa=ax.scatter(xpos[np.logical_not(in_solid)],ypos[np.logical_not(in_solid)],c=color[np.logical_not(in_solid)],s=marker_size,marker=marker,zorder=5,edgecolors="k",linewidth=0.01,cmap=cmap,vmin=min(color), vmax=1.01*max(color),label=label)


    else:
        ax.errorbar(xpos,ypos, xerr=xerr,yerr=yerr,
                fmt=" ",capsize=capsize,color="k",
                ecolor=error_bar_color,
                elinewidth=.5,alpha=error_bar_alpha,markeredgewidth=markeredgewidth)
        ax.scatter(xpos,ypos,color=color,s=marker_size,marker=marker,zorder=5,edgecolors="k",linewidth=0.01,label=label)
    # solids
    if not in_solid is None:
        ax.errorbar(xpos[in_solid],ypos[in_solid], xerr=xerr[...,in_solid],yerr=yerr[...,in_solid],
                    fmt=" ",capsize=capsize,color=solid_color,ecolor=error_bar_color,elinewidth=.5,alpha=error_bar_alpha ,markeredgewidth=markeredgewidth)
        ax.scatter(xpos[in_solid],ypos[in_solid],color=solid_color,s=marker_size*2/3,marker=solid_marker,zorder=5,edgecolors="k",linewidth=0.01)

    ax.set_xlabel(xlabel,size=MEDIUM_SIZE,labelpad=2)
    ax.set_ylabel(ylabel,size=MEDIUM_SIZE,labelpad=2)
    if not cmap is None:
        return(aaaa)

###
fig,ax=plt.subplots(1,1)
fig.set_size_inches(size_fig_1d)



nice_plot(datagran['mean_eps_yy_ss']/1e6,datagran['mean_dt'],ax=ax,
        xerr=datagran['std_eps_yy_ss']*0,yerr=datagran['sigma_dt'],
        xlabel=r"$\left<\sigma_{yy}^{solid}\right>$ (MPa)",ylabel=r"$\left<\Delta T\right>$ (s)",
        in_solid=[0,1,2,3],
        color=solid_solid_color, error_bar_color=error_bar_color,
        marker_size=scatter_size*2, capsize=error_bar_width, marker=solid_marker,label="empty-hole" )


nice_plot(ss_sig/1e6,ss_times_mean,ax=ax,
        xerr=ss_sig*0,yerr=ss_times_std,
        xlabel=r"$\left<\sigma_{yy}^{solid}\right>$ (MPa)",ylabel=r"$\left<\Delta T\right>$ (s)",
        in_solid=[0,1,2,3,4],
        color='k', error_bar_color=error_bar_color,
        marker_size=scatter_size*2, capsize=error_bar_width, marker='s',
        solid_color="k",label="flat solids" )



color_a = solid_in_granular_color  # RGB values for color a
color_b = granular_color  # RGB values for color b

cm = LinearSegmentedColormap.from_list("aaaa",[color_a,color_b],N=256)
cm=mpl.colormaps["rainbow"]


aaaa=nice_plot(datasolid['mean_eps_yy_ss'][:-5]/1e6,datasolid['mean_dt'][:-5],ax=ax,
        xerr=datasolid['std_eps_yy_ss'][:-5]*0,yerr=datasolid['sigma_dt'][:-5],
        xlabel=r"$\left<\sigma_{yy}^{solid}\right>$ (MPa)",ylabel=r"$\left<\Delta T\right>$ (s)",
        in_solid=in_solid[:-5],
        color=datasolid['mean_lc'][:-5], error_bar_color=error_bar_color,
        marker_size=scatter_size*3, capsize=error_bar_width, marker="d",
        cmap=cm,label="granular (filled hole)" )



#get handles and labels
handles, labels = plt.gca().get_legend_handles_labels()
order = [1,0,2]
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],prop={'size': INSET_MEDIUM_SIZE},framealpha = 1, facecolor = (1,1,1,1))




cbar=plt.colorbar(aaaa)

#cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel(r"${}$".format(LC_name_short), rotation=270,size=MEDIUM_SIZE)
cbar.ax.tick_params(labelsize=INSET_SMALL_SIZE)

ax.xaxis.set_minor_locator(MultipleLocator(.5))
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_minor_locator(MultipleLocator(10))
ax.yaxis.set_major_locator(MultipleLocator(20))
plt.grid(which="both")

#ax.tick_params(labelsize=SMALL_SIZE)

#plt.plot([1,3.2],[14,62],color="k",linewidth=.5,linestyle=":")

ax.set_xlim([0,3.8])
ax.set_ylim([0,65])

set_grid(ax)

fig.subplots_adjust(left=0.1, right=1.02, bottom=0.11, top=0.98)
fig.text(0.01,0.948,"d",size=LETTER_SIZE, weight='bold')



###



plt.savefig("E:/Article/Figure_1/figure_1_b.svg",dpi=dpi_global)
plt.savefig("E:/Article/Figure_1/figure_1_b.pdf",dpi=dpi_global)
plt.savefig("E:/Article/Figure_1/figure_1_b.png",dpi=dpi_global)
#plt.show()
plt.close('all')




###



to_save={}

to_save["datagran"]=datagran
to_save["datasolid"]=datasolid
to_save["solids"]=solids
to_save["in_solid"]=in_solid
to_save["to_remove"]=[39,40,42,43,44]
to_save["ss_sig"]=ss_sig
to_save["ss_times_mean"]=ss_times_mean
to_save["ss_times_std"]=ss_times_std

np.save("E:/Article/Figure_1/figure_1_b.npy",to_save)
scio.savemat("E:/Article/Figure_1/figure_1_b.mat",to_save)



