cd /D E:\Article\

mkdir All_Figures_PDF
mkdir All_Figures_SVG
mkdir All_Figures_PNG
mkdir All_Figures_CODE
mkdir All_Figures_DATA

copy parameters.py .\All_Figures_CODE\
copy plot_all_figs.bat .\All_Figures_CODE\



cd Figure_1

"C:/Program Files/Inkscape/bin/inkscape.exe" --actions="select-all" --export-type="pdf" "E:\Article\Figure_1\schema.svg" --export-area-page
"C:/Program Files/Inkscape/bin/inkscape.exe" --actions="select-all" --export-type="png" "E:\Article\Figure_1\schema.svg" --export-area-page -d 1200

python figure_1.py

"C:/Program Files/Inkscape/bin/inkscape.exe" --actions="select-all" --export-type="pdf" "E:\Article\Figure_1\figure_1.svg" --export-area-page --actions="export-background:white"
"C:/Program Files/Inkscape/bin/inkscape.exe" --actions="select-all" --export-type="png" "E:\Article\Figure_1\figure_1.svg" --export-area-page -d 1200 --actions="export-background:white"

del figure_1_unmerged.svg
del figure_1_c_d.pdf
del figure_1_c_d.png
del figure_1_c_d.svg
del figure_1_b.png
del figure_1_b.pdf
del figure_1_b.svg
del schema.pdf
del schema.png

copy figure_1.pdf ..\All_Figures_PDF\figure_1.pdf
copy figure_1.png ..\All_Figures_PNG\figure_1.png
copy figure_1.svg ..\All_Figures_SVG\figure_1.svg

copy figure_1_b.npy ..\All_Figures_DATA\figure_1_b.npy
copy figure_1_b.mat ..\All_Figures_DATA\figure_1_b.mat
copy figure_1_c_d.npy ..\All_Figures_DATA\figure_1_c_d.npy
copy figure_1_c_d.mat ..\All_Figures_DATA\figure_1_c_d.mat

copy *.py ..\All_Figures_CODE\



cd ..\Figure_2
python figure_2.py
copy figure_2.pdf ..\All_Figures_PDF\figure_2.pdf
copy figure_2.png ..\All_Figures_PNG\figure_2.png
copy figure_2.svg ..\All_Figures_SVG\figure_2.svg

copy figure_2.npy ..\All_Figures_DATA\figure_2.npy
copy figure_2.mat ..\All_Figures_DATA\figure_2.mat

copy *.py ..\All_Figures_CODE\



cd ..\Figure_3
python figure_3.py
copy figure_3.pdf ..\All_Figures_PDF\figure_3.pdf
copy figure_3.png ..\All_Figures_PNG\figure_3.png
copy figure_3.svg ..\All_Figures_SVG\figure_3.svg


copy figure_3.npy ..\All_Figures_DATA\figure_3.npy
copy figure_3.mat ..\All_Figures_DATA\figure_3.mat

copy *.py ..\All_Figures_CODE\



cd ..\Figure_4
python figure_4.py
copy figure_4.pdf ..\All_Figures_PDF\figure_4.pdf
copy figure_4.png ..\All_Figures_PNG\figure_4.png
copy figure_4.svg ..\All_Figures_SVG\figure_4.svg

copy figure_4.npy ..\All_Figures_DATA\figure_4.npy
copy figure_4.mat ..\All_Figures_DATA\figure_4.mat

copy *.py ..\All_Figures_CODE\



cd ..\Figure_5
python figure_5.py
copy figure_5.pdf ..\All_Figures_PDF\figure_5.pdf
copy figure_5.png ..\All_Figures_PNG\figure_5.png
copy figure_5.svg ..\All_Figures_SVG\figure_5.svg


copy figure_5.npy ..\All_Figures_DATA\figure_5.npy
copy figure_5.mat ..\All_Figures_DATA\figure_5.mat

copy *.py ..\All_Figures_CODE\


cd ..\Figure_6
python figure_6.py
copy figure_6.pdf ..\All_Figures_PDF\figure_6.pdf
copy figure_6.png ..\All_Figures_PNG\figure_6.png
copy figure_6.svg ..\All_Figures_SVG\figure_6.svg


copy figure_6.npy ..\All_Figures_DATA\figure_6.npy
copy figure_6.mat ..\All_Figures_DATA\figure_6.mat

copy *.py ..\All_Figures_CODE\


cd ..\Figure_S1

"C:/Program Files/Inkscape/bin/inkscape.exe" --actions="select-all" --export-type="pdf" "E:\Article\Figure_S1\figure_S1.svg" --export-area-page --actions="export-background:white"
"C:/Program Files/Inkscape/bin/inkscape.exe" --actions="select-all" --export-type="png" "E:\Article\Figure_S1\figure_S1.svg" --export-area-page -d 1200 --actions="export-background:white"


copy figure_S1.pdf ..\All_Figures_PDF\figure_S1.pdf
copy figure_S1.png ..\All_Figures_PNG\figure_S1.png
copy figure_S1.svg ..\All_Figures_SVG\figure_S1.svg



cd ..\Figure_S2
python figure_S2.py
copy figure_S2.pdf ..\All_Figures_PDF\figure_S2.pdf
copy figure_S2.png ..\All_Figures_PNG\figure_S2.png
copy figure_S2.svg ..\All_Figures_SVG\figure_S2.svg



copy figure_S2.npy ..\All_Figures_DATA\figure_S2.npy
copy figure_S2.mat ..\All_Figures_DATA\figure_S2.mat

copy *.py ..\All_Figures_CODE\


cd ..\Reponse_review
for %%f in (*.py) do (
    echo Running %%f
    python "%%f"
)

copy *.pdf ..\Reponse_review_Figures\
copy *.png ..\Reponse_review_Figures\
copy *.svg ..\Reponse_review_Figures\


cd ..\

python data_availability.py
copy Source_Data.xlsx All_Figures_DATA\
copy explaining_the_data.txt All_Figures_DATA\

tar.exe -acf Figures.zip All_Figures_PDF All_Figures_SVG All_Figures_PNG All_Figures_CODE All_Figures_DATA Reponse_review_Figures


cmd /k


