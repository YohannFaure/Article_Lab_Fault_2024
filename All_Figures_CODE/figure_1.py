with open("E:/Article/Figure_1/figure_1_b.py", 'r') as f:
        exec(f.read())
with open("E:/Article/Figure_1/figure_1_c_d.py", 'r') as f:
        exec(f.read())


import svg_stack as ss

doc = ss.Document()

layout1 = ss.HBoxLayout()
layout1.addSVG("E:/Article/Figure_1/schema.svg",alignment=ss.AlignCenter|ss.AlignLeft)
layout1.addSVG("E:/Article/Figure_1/figure_1_b.svg",alignment=ss.AlignCenter|ss.AlignLeft)
doc.setLayout(layout1)
doc.save("E:/Article/Figure_1/figure_1.svg")

doc = ss.Document()

layout2 = ss.VBoxLayout()
layout2.addSVG("E:/Article/Figure_1/figure_1.svg",alignment=ss.AlignTop|ss.AlignCenter)
layout2.addSVG("E:/Article/Figure_1/figure_1_c_d.svg",alignment=ss.AlignTop|ss.AlignLeft)

doc.setLayout(layout2)
doc.save("E:/Article/Figure_1/figure_1.svg")


