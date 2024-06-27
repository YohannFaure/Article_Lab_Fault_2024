import numpy as np
import scipy.io as scio
import xlsxwriter

with open("E:/Article/parameters.py", 'r') as f:
        exec(f.read())



def retime(t,mu):
    # Create new time and new starting point, to keep only loading
    a=next((i for i, b in enumerate(mu[7000:]>0.05) if b), None)+7000
    start = max(a-5200,0)
    new_t = t[start:]-t[start]
    new_mu = mu[start:]
    return(new_t,new_mu)



# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook("E:/Article/Source_Data.xlsx")


## Fig1 b
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig1b")

locals().update(np.load("E:/Article/Figure_1/figure_1_c_d.npy",allow_pickle = True).all())

labels = ["x",
            "sig_yy empty-hole",
            "sig_yy granular 1",
            "sig_yy granular 2",
            "sig_yy granular 3"]

cols_labels = [0]+[1]+[load_profiles[i].shape[0] for i in range(4)]
cols_labels = np.cumsum(cols_labels)

data = [list(x_plot)]+list(load_profiles[0]/1e6)+list(load_profiles[1]/1e6)+list(load_profiles[2]/1e6)+list(load_profiles[3]/1e6)


for i in range(5):
    worksheet.write(0, cols_labels[i],     labels[i])

for col in range(len(data)):
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])





# Create a new chart object. In this case an embedded chart.
chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

# Configure the first series.

for x in ["B","C","D"]:
    chart1.add_series(
        {
            "name": "=Fig1b!${}$1".format(x),
            "categories": "=Fig1b!$A$2:$A$11",
            "values": "=Fig1b!${}$2:${}$11".format(x,x),
            "line": {"width": 1}
        }
    )


chart1.set_title({"name": "empty hole"})
chart1.set_x_axis({"name": "x (mm)"})
chart1.set_y_axis({"name": "\sig_yy"})
chart1.set_style(10)
worksheet.insert_chart("A12", chart1, {"x_offset": 25, "y_offset": 10})

# Create a new chart object. In this case an embedded chart.
chart2 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

# Configure the first series.

for x in ["E","F","G"]:
    chart2.add_series(
        {
            "name": "=Fig1b!${}$1".format(x),
            "categories": "=Fig1b!$A$2:$A$11",
            "values": "=Fig1b!${}$2:${}$11".format(x,x),
            "line": {"width": 1}
        }
    )


chart2.set_title({"name": "granular 1"})
chart2.set_x_axis({"name": "x (mm)"})
chart2.set_y_axis({"name": "\sig_yy"})
chart2.set_style(10)
worksheet.insert_chart("I12", chart2, {"x_offset": 25, "y_offset": 10})

chart3 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

for x in ["H","I","J","K","L","M"]:
    chart3.add_series(
        {
            "name": "=Fig1b!${}$1".format(x),
            "categories": "=Fig1b!$A$2:$A$11",
            "values": "=Fig1b!${}$2:${}$11".format(x,x),
            "line": {"width": 1}
        }
    )


chart3.set_title({"name": "granular 2"})
chart3.set_x_axis({"name": "x (mm)"})
chart3.set_y_axis({"name": "\sig_yy"})
chart3.set_style(10)
worksheet.insert_chart("Q12", chart3, {"x_offset": 25, "y_offset": 10})


chart4 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

for x in ([*"NOPQRSTUVWXYZ"]+["AA","AB","AC","AD"]):
    chart4.add_series(
        {
            "name": "=Fig1b!${}$1".format(x),
            "categories": "=Fig1b!$A$2:$A$11",
            "values": "=Fig1b!${}$2:${}$11".format(x,x),
            "line": {"width": 1}
        }
    )

chart4.set_title({"name": "granular 3"})
chart4.set_x_axis({"name": "x (mm)"})
chart4.set_y_axis({"name": "\sig_yy"})
chart4.set_style(10)
worksheet.insert_chart("Y12", chart4, {"x_offset": 25, "y_offset": 10})







## Fig1 c
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig1c")

labels=["time empty-hole", "mu empty-hole",
        "time granular 1", "mu granular 1",
        "time granular 2", "mu granular 2",
        "time granular 3", "mu granular 3"]



for i in range(4):
    times[i],mus[i] = retime(times[i],mus[i])

data = [times[0] , mus[0],
        times[1] , mus[1],
        times[2] , mus[2],
        times[3] , mus[3]]


for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])





# Create a new chart object. In this case an embedded chart.
chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

# Configure the first series.
chart1.add_series(
    {
        "name": "=Fig1c!$B$1",
        "categories": "=Fig1c!$A$2:$A$77731",
        "values": "=Fig1c!$B$2:$B$77731",
        "line": {"width": 1}
    }
)
chart2 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart2.add_series(
    {
        "name": "=Fig1c!$D$1",
        "categories": "=Fig1c!$C$2:$C$77731",
        "values": "=Fig1c!$D$2:$D$77731",
        "line": {"width": 1}
    }
)
chart3 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart3.add_series(
    {
        "name": "=Fig1c!$F$1",
        "categories": "=Fig1c!$E$2:$E$77731",
        "values": "=Fig1c!$F$2:$F$77731",
        "line": {"width": 1}
    }
)
chart4 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart4.add_series(
    {
        "name": "=Fig1c!$H$1",
        "categories": "=Fig1c!$G$2:$G$77731",
        "values": "=Fig1c!$H$2:$H$77731",
        "line": {"width": 1}
    }
)


# Add a chart title and some axis labels.
#chart1.set_title({"name": ""})
chart1.set_x_axis({"name": "t (s)"})
chart1.set_y_axis({"name": "\mu"})
chart1.set_style(10)

chart2.set_x_axis({"name": "t (s)"})
chart2.set_y_axis({"name": "\mu"})
chart2.set_style(10)

chart3.set_x_axis({"name": "t (s)"})
chart3.set_y_axis({"name": "\mu"})
chart3.set_style(10)

chart4.set_x_axis({"name": "t (s)"})
chart4.set_y_axis({"name": "\mu"})
chart4.set_style(10)


# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart("J1", chart1, {"x_offset": 25, "y_offset": 10})
worksheet.insert_chart("J15", chart2, {"x_offset": 25, "y_offset": 10})
worksheet.insert_chart("J30", chart3, {"x_offset": 25, "y_offset": 10})
worksheet.insert_chart("J45", chart4, {"x_offset": 25, "y_offset": 10})








## Fig1 d
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig1d")

locals().update(np.load("E:/Article/Figure_1/figure_1_b.npy",allow_pickle = True).all())

labels = ["x flat solids",
            "y flat solids",
            "y err flat solid",
            "x empty-hole",
            "y empty-hole",
            "y err empty-hole",
            "x granular",
            "y granular",
            "y err granular",
            "loading contrast granular",
            "is empty-hole"]

data = [ss_sig/1e6,
        ss_times_mean,
        ss_times_std,
        datagran['mean_eps_yy_ss']/1e6,
        datagran['mean_dt'],
        datagran['sigma_dt'],
        datasolid['mean_eps_yy_ss'][:-5]/1e6,
        datasolid['mean_dt'][:-5],
        datasolid['sigma_dt'][:-5],
        datasolid['mean_lc'][:-5],
        in_solid]


for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])






# Create a new chart object. In this case an embedded chart.
chart1 = workbook.add_chart({"type": "scatter"})

# Configure the first series.
chart1.add_series(
    {
        "name": "=Fig1d!$B$1",
        "categories": "=Fig1d!$A$2:$A$100000",
        "values": "=Fig1d!$B$2:$B$100000",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig1d!$C$2:$C$100000',
            'minus_values': '=Fig1d!$C$2:$C$100000'
            }
    }
)

chart1.add_series(
    {
        "name": "=Fig1d!$E$1",
        "categories": "=Fig1d!$D$2:$D$100000",
        "values": "=Fig1d!$E$2:$E$100000",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig1d!$F$2:$F$100000',
            'minus_values': '=Fig1d!$F$2:$F$100000'
            }
    }
)


chart1.add_series(
    {
        "name": "=Fig1d!$H$1",
        "categories": "=Fig1d!$G$2:$G$100000",
        "values": "=Fig1d!$H$2:$H$100000",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig1d!$I$2:$I$100000',
            'minus_values': '=Fig1d!$I$2:$I$100000'
            }
    }
)



# Add a chart title and some axis labels.
#chart1.set_title({"name": ""})
chart1.set_x_axis({"name": "\sig_yy^solid"})
chart1.set_y_axis({"name": "\Delta T"})


# Set an Excel chart style. Colors with white outline and shadow.
chart1.set_style(10)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart("L2", chart1, {"x_offset": 25, "y_offset": 10})



## Fig2a
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig2a")

locals().update(np.load("E:/Article/Figure_2/figure_2.npy",allow_pickle = True).all())


times[0],mus[0] = retime(times[0],mus[0])

labels=["time delta tot","delta tot","time mu","mu"]
data = [x1s[0],disp_sides[0],times[0],mus[0]]


for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])



# Create a new chart object. In this case an embedded chart.
chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart1.add_series(
    {
        "name": "=Fig2a!$B$1",
        "categories": "=Fig2a!$A$2:$A$11690",
        "values": "=Fig2a!$B$2:$B$11690",
        "line": {"width": 1}
    }
)

chart1.set_x_axis({"name": "time (s)"})
chart1.set_y_axis({"name": "delta tot (s)"})
chart1.set_style(10)
worksheet.insert_chart("E1", chart1, {"x_offset": 25, "y_offset": 10})



chart2 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart2.add_series(
    {
        "name": "=Fig2a!$D$1",
        "categories": "=Fig2a!$C$2:$C$77731",
        "values": "=Fig2a!$D$2:$D$77731",
        "line": {"width": 1}
    }
)

chart2.set_x_axis({"name": "time (s)"})
chart2.set_y_axis({"name": "\mu"})
chart2.set_style(10)
worksheet.insert_chart("E16", chart2, {"x_offset": 25, "y_offset": 10})


## Fig2b
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig2b")


times[1],mus[1] = retime(times[1],mus[1])

labels=["time delta tot","delta tot","time mu","mu"]
data = [x1s[1],disp_sides[1],times[1],mus[1]]


for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])


# Create a new chart object. In this case an embedded chart.
chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart1.add_series(
    {
        "name": "=Fig2b!$B$1",
        "categories": "=Fig2b!$A$2:$A$14756",
        "values": "=Fig2b!$B$2:$B$14756",
        "line": {"width": 1}
    }
)

chart1.set_x_axis({"name": "time (s)"})
chart1.set_y_axis({"name": "delta tot (s)"})
chart1.set_style(10)
worksheet.insert_chart("E1", chart1, {"x_offset": 25, "y_offset": 10})



chart2 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart2.add_series(
    {
        "name": "=Fig2b!$D$1",
        "categories": "=Fig2b!$C$2:$C$52690",
        "values": "=Fig2b!$D$2:$D$52690",
        "line": {"width": 1}
    }
)

chart2.set_x_axis({"name": "time (s)"})
chart2.set_y_axis({"name": "\mu"})
chart2.set_style(10)
worksheet.insert_chart("E16", chart2, {"x_offset": 25, "y_offset": 10})







## Fig2c
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig2c")




labels=["time","S hole","S solid-solid","delta IE hole","delta IE solid-solid"]
data = [x2s[0],
        creep_percent_centers[0]/100,
        creep_percent_sides[0]/100,
        creep_dist_centers[0],
        (creep_dist_lefts[0]+creep_dist_rights[0])/2]


for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])


# Create a new chart object. In this case an embedded chart.
chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart1.add_series(
    {
        "name": "=Fig2c!$B$1",
        "categories": "=Fig2c!$A$2:$A$5",
        "values": "=Fig2c!$B$2:$B$5",
        "line": {"width": 1}
    }
)

chart1.add_series(
    {
        "name": "=Fig2c!$C$1",
        "categories": "=Fig2c!$A$2:$A$5",
        "values": "=Fig2c!$C$2:$C$5",
        "line": {"width": 1}
    }
)

chart1.set_x_axis({"name": "time (s)"})
chart1.set_y_axis({"name": "S"})
chart1.set_style(10)
worksheet.insert_chart("G2", chart1, {"x_offset": 25, "y_offset": 10})



chart2 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart2.add_series(
    {
        "name": "=Fig2c!$D$1",
        "categories": "=Fig2c!$A$2:$A$5",
        "values": "=Fig2c!$D$2:$D$5",
        "line": {"width": 1}
    }
)

chart2.add_series(
    {
        "name": "=Fig2c!$E$1",
        "categories": "=Fig2c!$A$2:$A$5",
        "values": "=Fig2c!$E$2:$E$5",
        "line": {"width": 1}
    }
)

chart2.set_x_axis({"name": "time (s)"})
chart2.set_y_axis({"name": "\delta IE"})
chart2.set_style(10)
worksheet.insert_chart("G17", chart2, {"x_offset": 25, "y_offset": 10})



## Fig2d
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig2d")




labels=["time","S hole","S solid-solid","delta IE hole","delta IE solid-solid"]
data = [x2s[1],
        creep_percent_centers[1]/100,
        creep_percent_sides[1]/100,
        creep_dist_centers[1],
        (creep_dist_lefts[1]+creep_dist_rights[1])/2]


for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])


# Create a new chart object. In this case an embedded chart.
chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart1.add_series(
    {
        "name": "=Fig2d!$B$1",
        "categories": "=Fig2d!$A$2:$A$21",
        "values": "=Fig2d!$B$2:$B$21",
        "line": {"width": 1}
    }
)

chart1.add_series(
    {
        "name": "=Fig2d!$C$1",
        "categories": "=Fig2d!$A$2:$A$21",
        "values": "=Fig2d!$C$2:$C$21",
        "line": {"width": 1}
    }
)

chart1.set_x_axis({"name": "time (s)"})
chart1.set_y_axis({"name": "S"})
chart1.set_style(10)
worksheet.insert_chart("F2", chart1, {"x_offset": 25, "y_offset": 10})



chart2 = workbook.add_chart({"type": "scatter", "subtype": "straight"})

chart2.add_series(
    {
        "name": "=Fig2d!$D$1",
        "categories": "=Fig2d!$A$2:$A$21",
        "values": "=Fig2d!$D$2:$D$21",
        "line": {"width": 1}
    }
)

chart2.add_series(
    {
        "name": "=Fig2d!$E$1",
        "categories": "=Fig2d!$A$2:$A$21",
        "values": "=Fig2d!$E$2:$E$21",
        "line": {"width": 1}
    }
)

chart2.set_x_axis({"name": "time (s)"})
chart2.set_y_axis({"name": "\delta IE"})
chart2.set_style(10)
worksheet.insert_chart("F17", chart2, {"x_offset": 25, "y_offset": 10})








## Fig3
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig3")

locals().update(np.load("E:/Article/Figure_3/figure_3.npy",allow_pickle = True).all())

in_solid=np.isin(new_data["manip_num"],solids)



labels = ["loading contrast",
          "loading contrast err -",
          "loading contrast err +",
          "S_f^patch",
          "S_f^solid",
          "S_f^patch err" ,
          "\Delta S_f",
          "mean freq",
          "freq err -",
          "freq err +",
          "is empty hole",
          "old lc",
          "old lc err",
          "old S_f^patch",
          "old S_f^solid",
          "old S_f^solid err",
          "old \Delta S_f",
          "old freq",
          "old freq err"
          ]

data = [new_data["mean_lc"],
        new_data["wide_lc"][0],
        new_data["wide_lc"][1],
        new_data["creep_center"]/100,
        new_data["creep_sides"]/100,
        new_data["sigma_creep_center"]/100,
        new_data["creep_center"]/100 - new_data["creep_sides"]/100,
        new_data["mean_freq"],
        new_data["wide_freq"][0],
        new_data["wide_freq"][1],
        in_solid,
        old_data["lc"],
        old_data["lc_err"],
        old_data["ie_slip_solid"]/100,
        old_data["ie_slip_grains"]/100,
        old_data["ie_slip_err"]/100,
        old_data["ie_slip_grains"]/100 - old_data["ie_slip_solid"]/100,
        old_data["freq"],
        old_data["freq_err"]
        ]



for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])










# Create a new chart object. In this case an embedded chart.
chart1 = workbook.add_chart({"type": "scatter"})

# Configure the first series.
chart1.add_series(
    {
        "name": "=Fig3!$D$1",
        "categories": "=Fig3!$A$2:$A$100000",
        "values": "=Fig3!$D$2:$D$100000",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$F$2:$F$100000',
            'minus_values': '=Fig3!$F$2:$F$100000'
            },
        'x_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$B$2:$B$100000',
            'minus_values': '=Fig3!$C$2:$C$100000'
            }
    }
)
chart1.add_series(
    {
        "name": "=Fig3!$N$1",
        "categories": "=Fig3!$L$2:$L$100000",
        "values": "=Fig3!$N$2:$N$100000",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$P$2:$P$100000',
            'minus_values': '=Fig3!$P$2:$P$100000'
            },
        'x_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$M$2:$M$100000',
            'minus_values': '=Fig3!$M$2:$M$100000'
            }
    }
)



chart2 = workbook.add_chart({"type": "scatter"})
chart2.add_series(
    {
        "name": "=Fig3!$E$1",
        "categories": "=Fig3!$A$2:$A$100000",
        "values": "=Fig3!$E$2:$E$100000",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$F$2:$F$100000',
            'minus_values': '=Fig3!$F$2:$F$100000'
            },
        'x_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$B$2:$B$100000',
            'minus_values': '=Fig3!$C$2:$C$100000'
            }
    }
)

chart2.add_series(
    {
        "name": "=Fig3!$O$1",
        "categories": "=Fig3!$L$2:$L$100000",
        "values": "=Fig3!$O$2:$O$100000",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$P$2:$P$100000',
            'minus_values': '=Fig3!$P$2:$P$100000'
            },
        'x_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$M$2:$M$100000',
            'minus_values': '=Fig3!$M$2:$M$100000'
            }
    }
)




chart3 = workbook.add_chart({"type": "scatter"})
chart3.add_series(
    {
        "name": "\Delta S_f",
        "categories": "=Fig3!$A$2:$A$100000",
        "values": "=Fig3!$G$2:$G$100000",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$F$2:$F$100000',
            'minus_values': '=Fig3!$F$2:$F$100000'
            },
        'x_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$B$2:$B$100000',
            'minus_values': '=Fig3!$C$2:$C$100000'
            }
    }
)

chart3.add_series(
    {
        "name": "old \Delta S_f",
        "categories": "=Fig3!$L$2:$L$100000",
        "values": "=Fig3!$Q$2:$Q$100000",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$P$2:$P$100000',
            'minus_values': '=Fig3!$P$2:$P$100000'
            },
        'x_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$M$2:$M$100000',
            'minus_values': '=Fig3!$M$2:$M$100000'
            }
    }
)




chart4 = workbook.add_chart({"type": "scatter"})
chart4.add_series(
    {
        "name": "freq",
        "categories": "Fig3!$G$2:$G$100000",
        "values": "=Fig3!$H$2:$H$100000",
        'x_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$F$2:$F$100000',
            'minus_values': '=Fig3!$F$2:$F$100000'
            },
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$J$2:$J$100000',
            'minus_values': '=Fig3!$I$2:$I$100000'
            }
    }
)

chart4.add_series(
    {
        "name": "old freq",
        "categories": "=Fig3!$Q$2:$Q$100000",
        "values": "=Fig3!$R$2:$R$100000",
        'x_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$P$2:$P$100000',
            'minus_values': '=Fig3!$P$2:$P$100000'
            },
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig3!$S$2:$S$100000',
            'minus_values': '=Fig3!$S$2:$S$100000'
            }
    }
)





chart1.set_title({"name": "a. top"})
chart1.set_x_axis({"name": "C_\sig"})
chart1.set_y_axis({"name": "S_f"})
chart1.set_style(10)
worksheet.insert_chart("T1", chart1, {"x_offset": 25, "y_offset": 10})


chart2.set_title({"name": "a. bot"})
chart2.set_x_axis({"name": "C_\sig"})
chart2.set_y_axis({"name": "S_f"})
chart2.set_style(10)
worksheet.insert_chart("T16", chart2, {"x_offset": 25, "y_offset": 10})

chart3.set_title({"name": "b."})
chart3.set_x_axis({"name": "C_\sig"})
chart3.set_y_axis({"name": "\Delta S_f"})
chart3.set_style(10)
worksheet.insert_chart("AB16", chart3, {"x_offset": 25, "y_offset": 10})

chart4.set_title({"name": "b. inset"})
chart4.set_x_axis({"name": "\Delta S_f"})
chart4.set_y_axis({"name": "freq"})
chart4.set_style(10)
worksheet.insert_chart("AB1", chart4, {"x_offset": 25, "y_offset": 10})





## Fig4a
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig4a")

locals().update(np.load("E:/Article/Figure_4/figure_4.npy",allow_pickle = True).all())



labels = ["time"] + ["eps_xy^{}".format(i) for i in range(10)]+["x","nuc time"]

data = [1000*fast_time-1000*fast_time.mean()]+ [1000*(gages[3*(i+1)-1]-gages[3*(i+1)-1][0:10000].mean()) for i in range(10)] + [[5,15,25,35,45,75,105,115,125,135],indexes*1000-1000*fast_time.mean()]

data[-1][5]=0


for col in range(len(labels)-1):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])

col = 12
row = 0
worksheet.write(row, col,     labels[col])
for row in range(0,5):
    worksheet.write(row+1, col,     data[col][row])
for row in range(6,10):
    worksheet.write(row+1, col,     data[col][row])




# Create a new chart object. In this case an embedded chart.

# Configure the first series.

kk=1

for x in [*"BCDEFGHIJK"]:
    chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})
    chart1.add_series(
        {
            "name": "=Fig4a!${}$1".format(x),
            "categories": "=Fig4a!$A$2:$A$40000",
            "values": "=Fig4a!${}$2:${}$40000".format(x,x),
            "line": {"width": 1}
        }
    )
    chart1.set_title({"name": ""})
    chart1.set_x_axis({"name": "time (ms)"})
    chart1.set_y_axis({"name": "\eps_xy"})
    chart1.set_style(10)
    worksheet.insert_chart("N{}".format(kk), chart1, {"x_offset": 25, "y_offset": 10})
    kk+=14


chart2 = workbook.add_chart({"type": "scatter", "subtype": "straight"})
chart2.add_series(
    {
        "name": "=Fig4a!$L$1",
        "categories" : "=Fig4a!$M$2:$M$11",
        "values": "=Fig4a!$L$2:$L$11",
        "line": {"width": 1}
    }
)
chart2.set_title({"name": "nucleation gage"})
chart2.set_x_axis({"name": "nucleation gage"})
chart2.set_y_axis({"name": "time (ms)"})
chart2.set_style(10)
worksheet.insert_chart("U1", chart2, {"x_offset": 25, "y_offset": 10})






## Fig4b
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig4b")




labels = ["time"] + ["eps_xy^{}".format(i) for i in range(10)]+["nuc time","x"]

data = [1000*fast_time_2-1000*fast_time_2.mean()]+ [1000*(gages_2[3*(i+1)-1]-gages_2[3*(i+1)-1][0:10000].mean()) for i in range(10)] + [[5,15,25,35,45,75,105,115,125,135],indexes_2*1000-1000*fast_time_2.mean()]

data[-1][5]=0


for col in range(len(labels)-1):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])

col = 12
row = 0
worksheet.write(row, col,     labels[col])
for row in range(0,3):
    worksheet.write(row+1, col,     data[col][row])
for row in range(7,10):
    worksheet.write(row+1, col,     data[col][row])




# Create a new chart object. In this case an embedded chart.

# Configure the first series.

kk=1

for x in [*"BCDEFGHIJK"]:
    chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})
    chart1.add_series(
        {
            "name": "=Fig4b!${}$1".format(x),
            "categories": "=Fig4b!$A$2:$A$40000",
            "values": "=Fig4b!${}$2:${}$40000".format(x,x),
            "line": {"width": 1}
        }
    )
    chart1.set_title({"name": ""})
    chart1.set_x_axis({"name": "time (ms)"})
    chart1.set_y_axis({"name": "\eps_xy"})
    chart1.set_style(10)
    worksheet.insert_chart("N{}".format(kk), chart1, {"x_offset": 25, "y_offset": 10})
    kk+=14


chart2 = workbook.add_chart({"type": "scatter", "subtype": "straight"})
chart2.add_series(
    {
        "name": "=Fig4b!$L$1",
        "categories" : "=Fig4a!$M$2:$M$11",
        "values": "=Fig4a!$L$2:$L$11",
        "line": {"width": 1}
    }
)
chart2.set_title({"name": "nucleation gage"})
chart2.set_x_axis({"name": "nucleation gage"})
chart2.set_y_axis({"name": "time (ms)"})
chart2.set_style(10)
worksheet.insert_chart("U1", chart2, {"x_offset": 25, "y_offset": 10})


## Fig4c
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig4c")


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



index_start= np.array(data_loaded_3["start_per_event"])
loading_contrast = np.array(data_loaded_3["lc_per_event"])
from_solid=np.array(data_loaded_3["solid_per_event"])
histogram_start_solid = np.array([list(index_start[from_solid]).count(i) for i in range(10)])
histograms_start=make_hists(bins, loading_contrast[np.logical_not(from_solid)], index_start[np.logical_not(from_solid)])



x=[5,15,25,35,45,75,105,115,125,135]
labels = ["nucleation gage", "loading contrast", "is empty hole","position","histogram empty hole"] + ["histogram gran {}".format(i) for i in range(1,5)]
data = [index_start, loading_contrast, from_solid, x, histogram_start_solid/np.sum(histogram_start_solid)]+[histograms_start[i]/np.sum(histograms_start[i]) for i in range(4)]


for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])


i=0
letter = [*"DJPV"]+["AB"]
for x in [*"EFGHI"]:
    chart1 = workbook.add_chart({"type": "bar"})
    chart1.add_series(
        {
            "name": "",
            "categories": "=Fig4c!$D$2:$D$11",
            "values": "=Fig4c!${}$2:${}$11".format(x,x)
        }
    )
    chart1.set_title({"name": "=Fig4c!${}$1".format(x)})
    chart1.set_x_axis({"name": "Proportion"})
    chart1.set_y_axis({"name": "Position (mm)"})
    chart1.set_style(10)
    worksheet.insert_chart("{}12".format(letter[i]), chart1, {"x_offset": 25, "y_offset": 10})
    i+=1





## Fig4d
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig4d")





from_solid = data_loaded_3["solid_per_event"]


lc_bins =np.insert( (lc_list_nuc[:-1]+lc_list_nuc[1:]) / 2, 0, lc_solid_mean)
ell_bins =np.insert( ell_per_lc_nuc ,0,ell_per_lc_nuc_solid)*1000/15
ell_bins_err = np.insert( ell_per_lc_nuc_width ,0, ell_per_lc_nuc_width_solid)*1000/15


labels = ["loading contrast",
          "d_nuc",
          "is empty-hole",
          "bin loading contrast",
          "<\ell>",
          "std(\ell)"
          ]


data = [loading_contrast,
        ell_nuc,
        from_solid,
        lc_bins,
        ell_bins,
        ell_bins_err
        ]




for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])


chart1 = workbook.add_chart({"type": "scatter"})
chart1.add_series(
    {
        "name": "",
        "categories": "=Fig4d!$D$2:$D$6",
        "values": "=Fig4d!$E$2:$E$6",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig4d!$F$2:$F$6',
            'minus_values': '=Fig4d!$F$2:$F$6'
            }
    }
)

chart1.set_title({"name": "=Fig4d!$E$1"})
chart1.set_x_axis({"name": "C_\sig"})
chart1.set_y_axis({"name": "<\ell> / \ell_0"})
chart1.set_style(10)
worksheet.insert_chart("G1", chart1, {"x_offset": 25, "y_offset": 10})





## Fig5a
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig5a")

locals().update(np.load("E:/Article/Figure_5/figure_5.npy",allow_pickle = True).all())


labels = ["time"] + ["eps_xy^{}".format(i) for i in range(10)]


def local_mean(data,n=10):
    nn = len(data)//n
    data_2=data[:n * nn]
    data_2=data_2.reshape((nn,n))
    return(np.mean(data_2,axis=-1))


data = [local_mean(time_sm[:-8000])]+ [local_mean(eps_xy_sm[i][8000:])*1e3-eps_xy_sm[i][7999]*1e3 for i in range(10)]




for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])




# Create a new chart object. In this case an embedded chart.

# Configure the first series.

kk=1

for x in [*"BCDEFGHIJK"]:
    chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})
    chart1.add_series(
        {
            "name": "=Fig5a!${}$1".format(x),
            "categories": "=Fig5a!$A$2:$A$5466",
            "values": "=Fig5a!${}$2:${}$5466".format(x,x),
            "line": {"width": 1}
        }
    )
    chart1.set_title({"name": ""})
    chart1.set_x_axis({"name": "time (s)"})
    chart1.set_y_axis({"name": "\eps_xy"})
    chart1.set_style(10)
    worksheet.insert_chart("M{}".format(kk), chart1, {"x_offset": 25, "y_offset": 10})
    kk+=14



## Fig5b
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig5b")



labels = ["time"] + ["eps_xy^{}".format(i) for i in range(10)]


def local_mean(data,n=10):
    nn = len(data)//n
    data_2=data[:n * nn]
    data_2=data_2.reshape((nn,n))
    return(np.mean(data_2,axis=-1))


data = [local_mean(time_sm_2[:-8000])]+ [local_mean(eps_xy_sm_2[i][8000:])*1e3-eps_xy_sm_2[i][7999]*1e3 for i in range(10)]




for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])




# Create a new chart object. In this case an embedded chart.

# Configure the first series.

kk=1

for x in [*"BCDEFGHIJK"]:
    chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})
    chart1.add_series(
        {
            "name": "=Fig5b!${}$1".format(x),
            "categories": "=Fig5b!$A$2:$A$5837",
            "values": "=Fig5b!${}$2:${}$5837".format(x,x),
            "line": {"width": 1}
        }
    )
    chart1.set_title({"name": ""})
    chart1.set_x_axis({"name": "time (s)"})
    chart1.set_y_axis({"name": "\eps_xy"})
    chart1.set_style(10)
    worksheet.insert_chart("M{}".format(kk), chart1, {"x_offset": 25, "y_offset": 10})
    kk+=14



## Fig5c
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig5c")


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





x=[5,15,25,35,45,75,105,115,125,135]
labels = ["loading contrast"] + ["x = {} is Sub linear".format(x[i]) for i in range(10)] + ["is empty hole","position","histogram empty hole"] + ["histogram gran {}".format(i) for i in range(1,5)]


data = [lc_event]+[data_nuc[:,i] for i in range(10)]+ [from_solid, x, histogram_round_solid/np.sum(histogram_round_solid)]+[histograms_round[i] for i in range(4)]


for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])


i=0
letter = [*"MSY"]+["AE","AK"]
for x in [*"NOPQR"]:
    chart1 = workbook.add_chart({"type": "bar"})
    chart1.add_series(
        {
            "name": "",
            "categories": "=Fig5c!$M$2:$M$11",
            "values": "=Fig5c!${}$2:${}$11".format(x,x)
        }
    )
    chart1.set_title({"name": "=Fig5c!${}$1".format(x)})
    chart1.set_x_axis({"name": "proportion"})
    chart1.set_y_axis({"name": "position (m)"})
    chart1.set_style(10)
    worksheet.insert_chart("{}12".format(letter[i]), chart1, {"x_offset": 25, "y_offset": 10})
    i+=1


## Fig5d
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig5d")





lc_bins =np.insert( (lc_list_nuc[:-1]+lc_list_nuc[1:]) / 2, 0, lc_solid_mean)
ell_bins =np.insert( ell_per_lc_nuc ,0,ell_per_lc_nuc_solid)*1000/15
ell_bins_err = np.insert( ell_per_lc_nuc_width ,0, ell_per_lc_nuc_width_solid)*1000/15



x = np.insert(ell_per_lc_nuc,0,ell_per_lc_nuc_solid)
xerr = np.insert(ell_per_lc_nuc_width,0,ell_per_lc_nuc_width_solid)
y = np.insert(ell_per_lc_round,0,ell_per_lc_round_solid)
yerr = np.insert(ell_per_lc_round_width,0,ell_per_lc_round_width_solid)



labels = ["d nuc/(\ell_h/2)",
          "\ell_slip",
          "x_err",
          "y_err",
          ]


data = [x*1000/15,
        y*1000/30,
        xerr*1000/15,
        yerr*1000/30
        ]




for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])


chart1 = workbook.add_chart({"type": "scatter"})
chart1.add_series(
    {
        "name": "",
        "categories": "=Fig5d!$A$2:$A$6",
        "values": "=Fig5d!$B$2:$B$6",
        'x_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig5d!$C$2:$C$6',
            'minus_values': '=Fig5d!$C$2:$C$6'
            },
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig5d!$D$2:$D$6',
            'minus_values': '=Fig5d!$D$2:$D$6'
            }
    }
)

chart1.set_x_axis({"name": "2<d_nuc>/\ell_h"})
chart1.set_y_axis({"name": "\ell_slip/\ell_h"})
chart1.set_style(10)
worksheet.insert_chart("E1", chart1, {"x_offset": 25, "y_offset": 10})





## Fig6
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "Fig6")

locals().update(np.load("E:/Article/Figure_6/figure_6.npy",allow_pickle = True).all())
locals().update(np.load("E:/Article/Figure_5/figure_5.npy",allow_pickle = True).all())






# 6a
#x
lc_bins = np.insert((lc_list_round[:-1]+lc_list_round[1:])/2,0,lc_solid_mean)

#y
ell_round = np.insert(ell_per_lc_round*1000/30,0,ell_per_lc_round_solid*1000/30)
ell_round_err = np.insert(ell_per_lc_round_width*1000/30,0,ell_per_lc_round_width_solid*1000/30)

#x2
lc_event
#y2
ell_round_per_event = ell/30

#6b
#y
sig = np.insert(sig_binned/1e6,0,sig_sol/1e6)
sig_err = np.insert(sig_binned_std/1e6,0,sig_sol_std/1e6)


labels = ["loading contrast",
          "\ell slip",
          "\ell slip err",
          "loading contrast per event",
          "\ell slip per event",
          "\sig tip",
          "\sig tip err",
          "\sig tip per event"]

data = [lc_bins,
        ell_round,
        ell_round_err,
        lc_event,
        ell_round_per_event,
        sig,
        sig_err,
        sigma_yy_0_tip_per_manip_2/1e6]



for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])



chart1 = workbook.add_chart({"type": "scatter"})
chart1.add_series(
    {
        "name": "=Fig6!$E$1",
        "categories": "=Fig6!$D$2:$D$292",
        "values": "=Fig6!$E$2:$E$292"
    }
)

chart1.add_series(
    {
        "name": "=Fig6!$B$1",
        "categories": "=Fig6!$A$2:$A$6",
        "values": "=Fig6!$B$2:$B$6",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig6!$C$2:$C$6',
            'minus_values': '=Fig6!$C$2:$C$6'
            }
    }
)

chart1.set_x_axis({"name": "C_\sig"})
chart1.set_y_axis({"name": "\ell_slip / \ell_h"})
chart1.set_style(10)
worksheet.insert_chart("J1", chart1, {"x_offset": 25, "y_offset": 10})


chart2 = workbook.add_chart({"type": "scatter"})
chart2.add_series(
    {
        "name": "=Fig6!$H$1",
        "categories": "=Fig6!$D$2:$D$226",
        "values": "=Fig6!$H$2:$H$226"
    }
)
chart2.add_series(
    {
        "name": "=Fig6!$F$1",
        "categories": "=Fig6!$A$2:$A$6",
        "values": "=Fig6!$F$2:$F$6",
        'y_error_bars': {
            'type': 'custom',
            'plus_values': '=Fig6!$G$2:$G$6',
            'minus_values': '=Fig6!$G$2:$G$6'
            }
    }
)

chart2.set_x_axis({"name": "C_\sig"})
chart2.set_y_axis({"name": "<\sig_yy^0(x_nuc)> (MPa)"})
chart2.set_style(10)
worksheet.insert_chart("R1", chart2, {"x_offset": 25, "y_offset": 10})






## FigS2a
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "FigS2a")

locals().update(np.load("E:/Article/Figure_S2/figure_S2.npy",allow_pickle = True).all())



labels = ["time instruc",
          "x instruct",
          "time profilo",
          "x profilo",
          "time tracking",
          "x pixel",
          "x subpixel"]

data = [time_simul_ramp,
        -data_simul_ramp,
        time_prof_10,
        -data_prof_10,
        time_cam_ramp,
        -data_cam_ramp_pix,
        -data_cam_ramp]



for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])



chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})
chart1.add_series(
    {
        "name": "=FigS2a!$B$1",
        "categories": "=FigS2a!$A$2:$A$6000",
        "values": "=FigS2a!$B$2:$B$6000",
        "line": {"width": 1}
    }
)

chart1.add_series(
    {
        "name": "=FigS2a!$D$1",
        "categories": "=FigS2a!$C$2:$C$6000",
        "values": "=FigS2a!$D$2:$D$6000",
        "line": {"width": 1}
    }
)

chart1.add_series(
    {
        "name": "=FigS2a!$F$1",
        "categories": "=FigS2a!$E$2:$E$6000",
        "values": "=FigS2a!$F$2:$F$6000",
        "line": {"width": 1}
    }
)

chart1.add_series(
    {
        "name": "=FigS2a!$G$1",
        "categories": "=FigS2a!$E$2:$E$6000",
        "values": "=FigS2a!$G$2:$G$6000",
        "line": {"width": 1}
    }
)

chart1.set_title({"name": "Ramp"})


chart1.set_x_axis({"name": "time (s)"})
chart1.set_y_axis({"name": "displacement (mm)"})
chart1.set_style(10)
worksheet.insert_chart("H2", chart1, {"x_offset": 25, "y_offset": 10})




## FigS2b
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "FigS2b")



labels = ["time instruc",
          "x instruct",
          "time profilo",
          "x profilo",
          "time tracking",
          "x pixel",
          "x subpixel"]

data = [time_simul_script,
        -data_simul_script,
        time_prof_script,
        -data_prof_script,
        time_cam_script,
        -data_cam_script_pix,
        -data_cam_script]



for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])



chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})
chart1.add_series(
    {
        "name": "=FigS2b!$B$1",
        "categories": "=FigS2b!$A$2:$A$6000",
        "values": "=FigS2b!$B$2:$B$6000",
        "line": {"width": 1}
    }
)

chart1.add_series(
    {
        "name": "=FigS2b!$D$1",
        "categories": "=FigS2b!$C$2:$C$6000",
        "values": "=FigS2b!$D$2:$D$6000",
        "line": {"width": 1}
    }
)

chart1.add_series(
    {
        "name": "=FigS2b!$F$1",
        "categories": "=FigS2b!$E$2:$E$6000",
        "values": "=FigS2b!$F$2:$F$6000",
        "line": {"width": 1}
    }
)

chart1.add_series(
    {
        "name": "=FigS2b!$G$1",
        "categories": "=FigS2b!$E$2:$E$6000",
        "values": "=FigS2b!$G$2:$G$6000",
        "line": {"width": 1}
    }
)


chart1.set_title({"name": "Script"})

chart1.set_x_axis({"name": "time (s)"})
chart1.set_y_axis({"name": "displacement (mm)"})
chart1.set_style(10)
worksheet.insert_chart("H2", chart1, {"x_offset": 25, "y_offset": 10})


## FigS2c
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "FigS2c")



labels = ["time",
          "x - xref instructions",
          "x - xref profilo"]

data = [time_shared,
        1000*compar_simul,
        1000*compar_prof]


for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])



chart1 = workbook.add_chart({"type": "scatter", "subtype": "straight"})
chart1.add_series(
    {
        "name": "=FigS2c!$B$1",
        "categories": "=FigS2c!$A$2:$A$6000",
        "values": "=FigS2c!$B$2:$B$6000",
        "line": {"width": 1}
    }
)

chart1.add_series(
    {
        "name": "=FigS2c!$C$1",
        "categories": "=FigS2c!$A$2:$A$6000",
        "values": "=FigS2c!$C$2:$C$6000",
        "line": {"width": 1}
    }
)



chart1.set_x_axis({"name": "time (s)"})
chart1.set_y_axis({"name": "x-x_ref (µm)"})
chart1.set_style(10)
worksheet.insert_chart("J1", chart1, {"x_offset": 25, "y_offset": 10})



## FigS2d
# Add a worksheet.
worksheet = workbook.add_worksheet(name = "FigS2d")

realtime= np.arange(0,len(data_cam_cut))/100-0.21-5


labels = ["time",
          "\delta_IE",
          "S"]

data = [realtime[found_events],
        creeped_distance,
        creeped_distance_frac]


for col in range(len(labels)):
    row = 0
    worksheet.write(row, col,     labels[col])
    for row in range(len(data[col])):
        worksheet.write(row+1, col,     data[col][row])



chart1 = workbook.add_chart({"type": "scatter"})
chart1.add_series(
    {
        "name": "=FigS2d!$B$1",
        "categories": "=FigS2d!$A$2:$A$7",
        "values": "=FigS2d!$B$2:$B$7"
    }
)


chart1.set_x_axis({"name": "time (s)"})
chart1.set_y_axis({"name": "\delta_IE (µm)"})
chart1.set_style(10)
worksheet.insert_chart("J1", chart1, {"x_offset": 25, "y_offset": 10})

chart2 = workbook.add_chart({"type": "scatter"})

chart2.add_series(
    {
        "name": "=FigS2d!$C$1",
        "categories": "=FigS2d!$A$2:$A$7",
        "values": "=FigS2d!$C$2:$C$7"
    }
)



chart2.set_x_axis({"name": "time (s)"})
chart2.set_y_axis({"name": "S"})
chart2.set_style(10)
worksheet.insert_chart("J14", chart2, {"x_offset": 25, "y_offset": 10})


workbook.close()








