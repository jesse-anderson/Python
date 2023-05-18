

# Dependencies: 
#### Tkinter
#### Numpy
#### Matplotlib
#### Astropy
#### sklearn.cluster/sklearn.neighbors

### Clustering Data sets taken from: http://cs.joensuu.fi/sipu/datasets/ 

## TESTING

#### Click ‘Open File’ Button
#### Open Matrix file ‘20clusters.txt’.
#### Plot Matrix file using ‘Plot Matrix Button
#### -=-=-
#### Click ‘Run Ripley’s K’ button
#### -=-=-
#### Click ‘Run DBSCAN’ button
#### -=-=-
#### Click ‘Run OPTICS’ button
#### -=-=-
#### Click ‘Close Program’ button

## PROGRAM OVERVIEW
#### This python program creates a Tkinter GUI with several options to choose from.

#### Initially data is loaded into the program via a .txt file called ‘20clusters.txt’ by clicking Open File and selecting the location of this file in your computer. The text box next to the Open File button is populated by the path and name of the file selected. Upon loading in this file one clicks Plot Matrix which generates an XY plot of the data. If the data is not an XY matrix with two columns an error box will be created.

#### Next a Ripley’s K analysis is performed by first specifying the search radius to use for Ripley’s K. Conveniently the Search Radius is set to the maximum value of ‘20clusters.txt’ opened previously but can be changed by the user.

#### DBSCAN analysis is performed by specifying the minimum number of points to search for in a given search radius to define a cluster. The default values of 15 for minimum points and 950 for search radius give the correct number of clusters. The plots will be appropriately labeled with the number of clusters found, k = “ “, and the input parameters. There will be data plotted for the clusters with and without data so the user can see how well the noise was filtered.

#### OPTICS analysis is performed by specifying the minimum number of points to create a reachability plot then defining the epsilon ceiling to find the clusters. Note that it is useful to first specify the minimum number of points by looking at the plot in “Plot Matrix” and zooming in and then specifying the minimum number of points on that basis. From there one will repeatedly find reachability plots with different degrees of peaks and valleys. In general, the greater the degree of peaks/valleys, the better defined the clustering is. From there define an epsilon ceiling and a horizontal line will be drawn and point below that horizontal line will be clustered on the basis of if the points are continuous indexed(1,2,3,....) and if a break occurs then a new cluster is formed. From there a plot is created using a DBSCAN-like coloring scheme.

#### All Figures will be saved in the same folder as the original .py file in a new ‘Figures’ folder as high resolution .jpg files and Data will be saved similarly in its own folder as text files. Data includes the Ripley’s K X/Y/Ripley’s Data, DBSCAN X/Y/Cluster# Data, and OPTICS X/Y/Cluster# Data. All of these are .txt files and use a space delimiter.

#### The close button will close all figures and all tkinter windows once yes is selected, if no is selected then you will be returned back to the program.

#### Personal notes: Astropy’s documentation is INSUFFICIENT and its examples use a randomly generated set of data that they meticulously complicated. They should have compared one subject against a Complete Spatial Randomness and progressively stepped up the complexity. This algorithm is slower than R’s implementation and somewhat faster than my own in MATLAB, so it is likely there are no optimizations occurring. Also the implementations of these clustering protocols are better done in MATLAB for DBSCAN and R for OPTICS/Ripley’s K due to RAM limitations in the way the matrices for calculation are created. It is possible to call MATLAB from Python and R from Python however that is beyond the scope of this project. If this project in Python is pursued further it would be done in such a way that for files exceeding 1 mb R and MATLAB will be called with rpy2 and matlab.engine respectively in the Try arguments in the code. Additionally another implementation will be to automatically transpose matrices that are 2 row, many column upon opening so more data types can be fitted. Another implementation will be 3 dimensional clustering using the same algorithms but using a sphere as a base as opposed to a circle.
