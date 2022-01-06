#Jesse Anderson movegui MATLAB clone
##Basically got annoyed with matplotlibs lack of automatic resizing of graphs so developed this
#developed on 1920x1080 so results may vary, but they vary FOR YOU. My native workflow will be unchanged until I acquire better monitors.
def movegui(direction):
    import matplotlib.pyplot as plt 
    #
    #
    import tkinter as tk #used to get screen dimensions and bring figure to front
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    moveMe= plt.get_current_fig_manager()
    root.lift()
    root.destroy()
    #
    if direction == "northwest" or direction == "Northwest" or direction =="NorthWest":#good
        moveMe= plt.get_current_fig_manager()
        moveMeX=screen_width*0
        moveMeY =screen_height*0+25
        moveMe.window.setGeometry(moveMeX,moveMeY,640, 545)#upper right, northwest
        
    elif direction == "northeast" or direction == "Northeast" or direction == "NorthEast":
        moveMeX=screen_width-640
        moveMeY =(screen_height*0)+25
        moveMe.window.setGeometry(moveMeX,moveMeY,640,545)#upper left,northeast
        
    elif direction =="southwest" or direction =="Southwest" or direction =="SouthWest":#good
        moveMeX=screen_width*0
        moveMeY =screen_height-545
        moveMe.window.setGeometry(moveMeX,moveMeY,640,545)#Lower left,Southwest
        
    elif direction =="southeast" or direction =="Southeast" or direction =="SouthEast":
        moveMeX=screen_width-640
        moveMeY =screen_height-545
        moveMe.window.setGeometry(moveMeX,moveMeY,640,545)#Lower right,Southeast
        
    elif direction =="north" or direction =="North": #ok enough
        moveMeX=screen_width/2-640/2
        moveMeY =(screen_height*0)+25
        moveMe.window.setGeometry(moveMeX,moveMeY,640,545)#Center up,North
        
    elif direction == "south" or direction =="South":#ok enough
        moveMeX=screen_width/2-640/2
        moveMeY =(screen_height)-545
        moveMe.window.setGeometry(moveMeX,moveMeY,640,545)#center down,South
        
    elif direction =="east" or direction == "East":
        moveMeX=screen_width-640
        moveMeY = screen_height/5
        moveMe.window.setGeometry(moveMeX,moveMeY,640,545)#upper right,East
        
    elif direction =="west" or direction == "West":
        moveMeX=screen_width*0
        moveMeY = screen_height/5
        moveMe.window.setGeometry(moveMeX,moveMeY,640,545)#center Left,west
        
    else:
        print('You did not enter a direction such as N/S/E/W/NE/NW/SW/SE or center')
        
