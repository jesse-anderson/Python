# -*- coding: utf-8 -*-
# Jesse Anderson

""" This program takes as input an XY matrix file and outputs 
either a simple plot of the original data, a Ripley’s K/L graph 
with the domain size in title, a DBSCAN based clustering of the XY 
points, or an OPTICS based clustering of the XY points."""

from tkinter import filedialog #openMatrix fun
from tkinter import ttk
import tkinter 
from tkinter.messagebox import showinfo
import numpy as np
from matplotlib import pyplot as plt #plotting

import os #checkFolder
#RipleysK
from astropy.stats import RipleysKEstimator as RipK #RipleysK fun
#DBSCAN
from sklearn.cluster import DBSCAN as DB
from tkinter import Text
from numpy import nan
from sklearn.neighbors import kneighbors_graph as KNN
#OPTICS
from sklearn.cluster import OPTICS, cluster_optics_dbscan #OPTICS fun
global root
root= tkinter.Tk()
root.title('Cluster Analysis Toolbox')


def openMatrix():
    """Program that opens up an xyz matrix and saves it to a variable to be used later for any number
    of purposes. Additionally updates a variable Box with the filepath of the file in question."""
    global nameMe, numCol
    global openCheck, file_size
    pathMe = os.getcwd()
    filetypes = ( ('text files', '*.txt'), ('All files','*.*') ) #specifies file types for file dialog box
    fileName = filedialog.askopenfilename(title = 'Open Matrix file to x y z',
                                          initialdir =pathMe,
                                          filetype = filetypes) #creates dialog box allowing user to select file to be opened
    #Try to load a standard space delimiter type file, failing that try a comma
    file_size = os.path.getsize(fileName) #get the size of the file
    openCheck = True
    if int(file_size) <= 1000000: #file size less than 1.0 mb
        openCheck = True
        try:
            file = np.loadtxt(fileName)#delimiter =' change based on input txt', not needed for project
        except:
            print('Trying , delimiter')
            try:
                file =np.loadtxt(fileName,delimiter = ',') #try opening txt file with comma delimiter
            except:
                print('Please use a .txt file with either a space or comma delimiter.')

    else:
        openCheck = False
        print('File you chose is too big. Please choose another file.') #to console error message
        tkinter.messagebox.showerror(title = "Error", message = "Please open an XY matrix file less than 1.0 mb in size") #to tkinter error message box
        #Alt call R using Rpy2 and use scaling to decrease numbers greater than 65,535 by factor to accomodate 32 bit calc
        return
    
    nameMe = file #save opened file data to nameMe variable
    Box.config(state = 'enabled') #inaccessible text box is now writeable
    NameBox.set(fileName)#write file name to nameBox in tkinter GUI
    Box.config(state = 'disabled')#accessible text box is no longer writeable
    numRows = np.shape(nameMe)[0] #find number of rows of opened matrix
    numCol = np.shape(nameMe)[1]#num columns of opened matrix, used to check if XY type
    return nameMe


def checkMatrix():
    """ Program that checks that the matrix file opened up by openMatrix() and 
    assigned to the nameMe variable is an XY matrix. If it is not an error box appears
    and every single other function call in this program will keep raising the error message
    until a satisfactory matrix file is opened up."""
    global check
    check = True
    if ('numCol' in globals() ) and (numCol==2): #if we have an opened file that is a matrix with some number of columns and that value is equal to 2...
        check = True #check, lets program run and is used repeatedly to check our matrix file is good to go for analysis
    else:
        check = False
        tkinter.messagebox.showerror(title = "Error", message = "Please open an XY matrix file") #error message, will stop program at many points if a bad file is used
        return check
     
     

def checkFolder():
    """Program checks if the figure folder and file folders exist.
    if they do not then they are created."""

    figures = 'Figures'#folder name
    figureCheck = os.path.isdir(figures) #check if this folder is in the current directory
    Data = 'Data'
    DataCheck = os.path.isdir(Data)
    if figureCheck == False:
        os.mkdir(figures) #creates folder if Figures is not a folder in current directory
    if DataCheck == False:
        os.mkdir(Data) #creates folder if Data not folder in cd
        

def plotData():
    """Plotting program to verify matrix opened up is correct. Function will plot
    the X/Y coordinates after checking that the previously opened matrix is an XY
    matrix."""
    checkMatrix() #run checkMatrix to make sure we have a good matrix
    checkFolder() #run checkFolder to make sure we have a writeable folder
    if check == True:
        x,y = nameMe[:, 0], nameMe[:, 1] #assign x/y values from nameMe
        #
        plot0 = plt.figure(1) #named figure, (1) allows repeated button presses that update current fig, will plot over figure otherwise. Saving to variable allows variable to be updated with new value
        plt.plot(x,y,'.k', markersize=3)#plot x/y in black with marker sizes of 3
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Unprocessed Data')
        plt.savefig('Figures\RawData.jpg', dpi=600) #saves high resolution image to Figures folder for publication
        plt.show()
    else:
        return


##Open file button and displayed filename

label1 = tkinter.ttk.Label(root,text = 'File I/O') #txt label
label1.grid(row=0,column=1) #[0,1] is location of label referenced
NameBox = tkinter.StringVar() #init string var of NameBox holding path to opened file
Box = tkinter.ttk.Entry(root, textvariable= NameBox) #assign NameBox var to entry box
NameBox.set('File Name Here') #initial NameBox txt value
Box.grid(row = 1, column =1)#split properties or else Python will throw NoneType errors
Box.config(state = 'disabled') #grays out box initially so unwriteable
open_button = tkinter.ttk.Button(root, text = 'Open File', command = openMatrix) #open matrix button
open_button.grid(column=0,row=1)
plot_button = tkinter.ttk.Button(root,text ='Plot Matrix', command = plotData ) #plot button
plot_button.grid(row = 1,column =2,padx = 5)

##Ripleys K


def RipleysK():
    """RipleysK based clustering analysis checked against a Complete Spatial Randomness
    distribution. Gives an overview of the degree of clustering between points at various
    radii. """
    global Kest,Lest
    global kRip
    checkMatrix()#check if good matrix
    checkFolder()#check existence of data and figures folder
    if check == True:
        maxX = max(nameMe[:,0])
        minX = min(nameMe[:,0])
        maxY =max(nameMe[:,1])
        minY = min(nameMe[:,1])
        areaRip = (maxX-minX)*(maxY-minY) #find area under consideration for ripley's k
        if RadBox.get() == '': #if the max distance we are looking at in ripley's k is undefined
            RadBox.set(np.amax(nameMe)) #get max of the X/Y values of the matrix
            radMax = float(RadBox.get())#set radius to that value
        else:
            radMax = float(RadBox.get())#else use supplied value in GUI
        radiiRip = np.linspace(0,radMax,513)#Between 0 and the radmax defined create 513 linearly spaced values
        pipi = 3.14159265358979 #NASA only uses 15 digits
        CSR = pipi * radiiRip*radiiRip #complete spatial randomness formula, easier to use than astropy implementation
        Kest = RipK(area = areaRip,x_max = maxX, y_max = maxY, 
                    x_min =minX, y_min = minY) # within an area defined by area and the min/max of X/Y initialize a Ripley's K analysis
        RipleyKVar = Kest(data = nameMe, radii=radiiRip, mode='none') #conduct Ripley's K analysis using nameMe matrix, distances defined by radiiRip, and no edge correction.
        #
        w = open("Data\RipleysK.txt","w") #open Ripley's K txt file for writing, if it doesn't exist create it
        for x in range(0,len(radiiRip)):
            i = nameMe[x,0]
            j = nameMe[x,0]
            k = RipleyKVar[x] #Ripley's K value calculated, THIS IS NOT CSR ONLY RIPLEY'S K
            w.write(str(i))
            w.write(' ')
            w.write(str(j))
            w.write(' ')
            w.write(str(k))
            w.write(' ')
            w.write('\n') #write values separated by a space, then new line, should be X/Y/Calculated ripley's K
        w.close()
        #Ripley's L, find domain size
        Lest = np.sqrt(RipleyKVar/pipi)-radiiRip #calculation of Ripley's L value
        LestMax = max(Lest) #find the maximum of Ripley's L
        LSpace = np.linspace(0,LestMax,50) #generate the straight line up to clearly indicate max
        LIndex = np.where(Lest==LestMax) #find index in Lest matrix where we have our max value
        holdRadius = radiiRip[LIndex] #max Radius
        LIndexValue = Lest[LIndex] #max L value, possibly useful to analysts
        radiiRepeat = np.full(50,holdRadius) #repeat that max Radius value 50 times.
        CSR_L = np.sqrt(CSR/pipi)-radiiRip#Complete Spatial Randomness calculation
        #K Plot
        fig1 = plt.figure(2)
        plt.xlabel('Distance Between Points')
        plt.ylabel('K Value')
        plt.title("Ripley's K")
        plt.plot(radiiRip,RipleyKVar,'r', markersize=3)
        plt.plot(radiiRip, CSR,'k')
        plt.savefig('Figures\RipleysK.jpg', dpi=600)
        plt.show()
        #L Plot with maximum plotted in third plt.plot() call
        fig2 = plt.figure(3)
        plt.xlabel('Distance Between Points')
        plt.ylabel('L Value')
        plt.title("Ripley's L\n Domain Size= %.3f units" %holdRadius) #pretty label
        plt.plot(radiiRip,Lest,'r')
        plt.plot(radiiRip,CSR_L,'k')
        plt.plot(radiiRepeat,LSpace,'k', markersize=3)
        plt.savefig('Figures\RipleysL.jpg', dpi=600)
        plt.show()
        #
        showMeInfo = showinfo(title='COMPLETE',message = "Ripley's K Finished!",parent=root) #audio/visual cue analysis is done.
    else:
        return
#Ripley's K Text
label2 = tkinter.ttk.Label(root,text = "Ripleys K")
label2 = label2.grid(row=2,column=1)
#Run Ripley's K button
RipKButton = tkinter.ttk.Button(root, text = 'Run RipleysK', command = RipleysK)
RipKButton.grid(column=2,row = 3,padx = 10)
##Search Radius label and search radius text box
label3 = tkinter.ttk.Label(root,text = "Search Radius: ")
label3 = label3.grid(row=3,column=0,padx = 5)
RadBox = tkinter.StringVar()
Box2 = tkinter.ttk.Entry(root, textvariable= RadBox)
Box2.grid(row = 3, column =1)
#Begin DBSCAN

def DBSCAN():
    """DBSCAN or, Density-Based Spatial Clustering of Applications with Noise, is a
    function call that will cluster XY points on the basis of a search radius where the program
    searches for the nearest points within said radius and defines a cluster as any radius
    holding as many points or more as minimum points. The resulting clusters are color coded
    according to the jet colormap. And the number of noise points and number of clusters
    is given in a pop up tkinter info box."""
    
    global clusterMe, labels, clusteringSet,ReportMe
    global KNearest, A
    checkMatrix() #check matrix for dimensionality
    checkFolder()#check folders exist
    
    if check == True:
        
        searchRad = float(SearchRadBox.get()) #get search radius from GUI
        minPts = float(MinptsBox.get()) #Get min pts
        clusterMe = DB(eps = searchRad, min_samples = minPts).fit(nameMe) #perform DBSCAN, eps=search distance, min_samples= minimum number of points to define a cluster
        labels = clusterMe.labels_ #get cluster labels, tells you how many clusters exist numerically.
        #Find our noise values and save to clusteringSet
        clusteringSet=[]
        for i in range(0, len(labels)): #loop through labels looking for noise
            if labels[i] == -1:
                clusteringSet.append(nan) #-1 is noise, so we set those values to NaN to ignore them when plotting
            else:
                clusteringSet.append(labels[i]) #keep those values
        x = nameMe[:,0]
        y = nameMe[:,1]
        j=min(labels)+1 #Python starts at 0, if 1 cluster and 1 noise, then 0 clusters doesn't make sense.
        #Find our Clusters and save them to clusterLegend
        clusterLegend = []
        for i in range(min(labels), max(labels)):
            clusterLegend.append('Cluster '+str(j)) #clustering labels, from 1-...max
            j= j+1
        for i in range(0, len(clusterLegend)):
            if clusterLegend[i] == 'Cluster 0': #where we have Cluster 0 var
                clusterLegend[i] = 'Noise' #actual label should be Noise
        #Create cluster figure with Noise, use jet colormap for color gradations, and s(size marker) of 3
        fig3 = plt.figure(4)
        plt.scatter(x,y,c = labels, cmap = "jet",s=3)
        plt.xlabel('X coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('DBSCAN Clustering with Noise[k= %d]\n'%(max(labels)+1)+'Search Radius = %.3f units   '%searchRad + 'Min Pts = %d units' %minPts)
        plt.savefig('Figures\DBSCANwithNoise.jpg', dpi=600)# Nature submissions == 600dpi
        ##Plot clusters without noise
        fig4 = plt.figure(5)
        plt.scatter(x,y,c = clusteringSet, cmap = "jet",s=3)
        plt.xlabel('X coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('DBSCAN Clustering without Noise[k= %d]\n' %(max(labels)+1)+'Search Radius = %.3f units   '%searchRad + 'Min Pts = %d units' %minPts)
        plt.savefig('Figures\DBSCANwithoutNoise.jpg', dpi=600)
        #
        showinfo(title='COMPLETE',message = "DBSCAN Finished!") #audio/visual cue job is complete
        
        plt.show()#calling twice = errors with showinfo
        ReportMe = tkinter.Tk()
        ReportMe.title('DBSCAN Report') #generate tkinter report of number of clusters and noise points, a lot of noise may call into question original data acquisition
        NumClusters = ['Number of Clusters is: '+str(len(set(labels)) - (1 if -1 in labels else 0))]
        Noise = ['Number of Noise points is: '+str(list(labels).count(-1))]
        #
        w = open("Data\DBSCAN.txt","w") #open DBSCAN for writing, create it if it doesn't exist
        for x in range(0,len(labels)):
            i = nameMe[x,0]
            j = nameMe[x,0]
            k = labels[x]
            w.write(str(i))
            w.write(' ')
            w.write(str(j))
            w.write(' ')
            w.write(str(k))
            w.write(' ')
            w.write('\n')#write X/Y values and cluster index number separated by spaces then new line
        w.close()
        #
        Report = tkinter.ttk.Label(ReportMe, text = NumClusters) #first line is number of clusters data
        Report.grid(row=0,column =0)
        Report2 = tkinter.ttk.Label(ReportMe, text = Noise) #second line is amount of noise in data
        Report2.grid(row=1,column =0)
        ReportMe.mainloop()
    else:
        return
#DBSCAN label
label3 = tkinter.ttk.Label(root,text = "DBSCAN")
label3 = label3.grid(row=4,column=1)
##Min pts: label and minpts box prepopulated with value of 15
label4 = tkinter.ttk.Label(root,text = "Min Pts: ")
label4 = label4.grid(row=5,column=0,padx = 5)
MinptsBox = tkinter.StringVar()
MinptsBox.set('15')
Box3 = tkinter.ttk.Entry(root, textvariable= MinptsBox)
Box3.grid(row = 5, column =1)
#Search radius: label and search radius box prepopulated with value of 950
label5 = tkinter.ttk.Label(root,text = "Search Radius: ")
label5 = label5.grid(row=6,column=0,padx = 5)
SearchRadBox = tkinter.StringVar()
SearchRadBox.set('950')
Box4 = tkinter.ttk.Entry(root, textvariable= SearchRadBox)
Box4.grid(row = 6, column =1)
#Run DBSCAN button
DBSCANButton = tkinter.ttk.Button(root, text = ' Run DBSCAN', command = DBSCAN)
DBSCANButton.grid(column=2,row = 6,padx = 10)

#OPTICS


def sklOPTICS():
    """OPTICS or, Ordering Points To Identify the Clustering Structure, is a clustering
    function call that is similar to DBSCAN but uses a reachability plot to find how far
    points are from each other using a minimum number of samples within a cluster
    and from there a minimum distance is defined that creates a horizontal line on the 
    reachability plot. Any points below this line that are connected by index(1,2,3...) 
    are clustered and any points broken up by at least one index are clustered separately.
    For example [1,2,3,5,6,7] would form two clusters are the 4th index was above the
    horizontal line."""
    global ReachMe, clust,clusterDBSCAN, space, fillEpsilon,X, labels,reachability
        
    checkMatrix() #check matrix is XY and works with analysis
    checkFolder()#check folders exist to write to
    
    if check == True:
        minSample = int(MinSampleBox.get()) #get values of minimum samples to define a cluster, used for reachability plot
        clust = OPTICS(min_samples = minSample) #perform low level reachability analysis
        epsilon =float(EpsBox.get())#grab epsilon ceiling values
        X = np.vstack(nameMe)#stack
        ReachMe = clust.fit(X) #create clust fit so we can plot
        reachability = clust.reachability_[clust.ordering_]#get reachability values
        labels = clust.labels_[clust.ordering_] #get our clust labels
        space = np.arange(len(X)) #grab index values
        fillEpsilon= np.full((len(X)),epsilon)#get our flat epsilon ceilign line
        #perform our actual cluster analysis using previous low level reachability values and new epsilon value from GUI
        clusterDBSCAN = cluster_optics_dbscan(reachability = clust.reachability_,
                                              core_distances = clust.core_distances_,
                                              ordering = clust.ordering_,
                                              eps = epsilon) 
        x = nameMe[:,0]
        y = nameMe[:,1]
        #
        fig5 = plt.figure(6)
        plt.plot(space, reachability,'k.', markersize=3) #Real world data isn't drawn from rng, plot all in black then decide
        plt.plot(space,fillEpsilon,'r',markersize=1) #epsilon ceiling value
        plt.xlabel('Point Index')
        plt.ylabel('Reachability Distance[Epsilon]')
        plt.title("Reachability Plot\n Min Samples = %d units" %minSample) #display epsilon value in title
        plt.savefig('Figures\OPTICSReachabilityPlot.jpg', dpi=600)
        plt.show()
        #
        fig6 = plt.figure(7)
        reachabilitySort = sorted(reachability)
        plt.plot(space, reachabilitySort,'k.', markersize=3) #Real world data isn't drawn from rng, plot all in black then decide
        plt.plot(space,fillEpsilon,'r',markersize=1) #epsilon ceiling value
        plt.xlabel('Point Index')
        plt.ylabel('Reachability Distance[Epsilon]')
        plt.title("SortedReachability Plot\n Min Samples = %d units" %minSample) #display epsilon value in title
        plt.savefig('Figures\OPTICSReachabilityPlot.jpg', dpi=600)
        plt.show()
        #
        fig7 = plt.figure(8)
        plt.scatter(x,y,c=clusterDBSCAN, cmap = "jet", s = 3)
        plt.xlabel('X coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('OPTICS Clustering[k=%d]\n'%(max(clusterDBSCAN)+1)+ 'Min Samples =  %d units   ' %minSample +"Minimum Points = %.3f units" %epsilon  )
        plt.savefig('Figures\OPTICSwithNoise.jpg', dpi=600)
        plt.show()
        #
        w = open("Data\OPTICS.txt","w")
        for x in range(0,len(clusterDBSCAN)):
            i = nameMe[x,0]
            j = nameMe[x,0]
            k = clusterDBSCAN[x]
            w.write(str(i))
            w.write(' ')
            w.write(str(j))
            w.write(' ')
            w.write(str(k))
            w.write(' ')
            w.write('\n')
        w.close()
        #
        showinfo(title='COMPLETE',message = "OPTICS Finished!")
    else:
        return
    
label6 = tkinter.ttk.Label(root,text = "OPTICS")
label6 = label6.grid(row=7,column=1)
#
label7 = tkinter.ttk.Label(root,text = "Min Points: ")
label7 = label7.grid(row=8,column=0,padx = 5)
MinSampleBox = tkinter.StringVar()
MinSampleBox.set('15')
Box5 = tkinter.ttk.Entry(root, textvariable= MinSampleBox)
Box5.grid(row = 8, column =1)
#
label10 = tkinter.ttk.Label(root,text = "Epsilon Ceiling: ")
label10 = label10.grid(row=9,column=0,padx = 5)
EpsBox = tkinter.StringVar()
EpsBox.set('1000')
Box8 = tkinter.ttk.Entry(root, textvariable= EpsBox)
Box8.grid(row = 9, column =1)
#
OPTICSButton = tkinter.ttk.Button(root, text = ' Run OPTICS', command = sklOPTICS)
OPTICSButton.grid(column=2,row = 9,padx = 10)

def closeEVERYTHING():
    """Program that will close all figures and any existing tkinter windows. Useful
    if one has every window open after manically swapping variables to achieve suitable
    clustering."""
    closeMe = tkinter.messagebox.askquestion('Exit Program','Are you sure you want to exit the Program?')
    if closeMe == 'yes':
        plt.close('all')
        if 'root' in globals():
            root.destroy()
        if 'ReportMe' in globals():
            ReportMe.destroy()
    else:
        tkinter.messagebox.showinfo('Return','Returning to the Program')
        
closeButton = tkinter.ttk.Button(root,text='Close Program', command = closeEVERYTHING)
closeButton.grid(column =1,row = 11,padx = 10, pady=20)
root.mainloop()
