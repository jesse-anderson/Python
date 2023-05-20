import sys
import json #json file i/o
import urllib3 #connection html
from bs4 import BeautifulSoup #parse html
import re #to robustly parse out the reg ex
from flask import * #render webpages
from os.path import exists #check file if exist later on then delete
import os #general helper, for file i/o

os.chdir(os.path.dirname(sys.argv[0])) # change wd to script directory.

global ijk #global var to help extract catch errors in emails, debugging tool
global iijjkk #global car to help extract catch errors in schedules, debugging tool
global read
ijk = 0

def extractData(site):
    """Function which, given a uic faculty profile url, will extract relevant data"""
    init = urllib3.PoolManager()#need capital P and M
    get = init.request('Get',site) #grab site name
    #BS = BeautifulSoup(get.data.decode("utf-8"),"html.parser") #html.parser is super ugly but works but makes work harder
    BS = BeautifulSoup(get.data.decode("utf-8"),"html5lib") #html5lib is just as ugly, easy swap with comments to see what works eventually.
    #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser

    email = BS.find_all('p',attrs={'class':'_content'}) # what we need to match to find the emails.
    #get name first, to identify who throws error.
    searchName = BS.find_all('div',attrs={'class':'_colB'})
    teacher = searchName[0].find('h1').text #find actual text within tag. Later on this method isn't as robust and may need to use regex to get it working.,
    print(teacher)
    #try except pass block, find emails
    try:
        emailscrape = email[2].text #sometimes email doesn't grab correctly. Try/catch here to allow for that.
    except:
        printIt = ['Trying another scraping method for ', teacher] #lets you know of error in grab.
        printIt = ''.join(printIt) #pretty print
        print(printIt) #actual print statement
    try:
        emailscrape = email[1].text #alt way of grabbing email.
    except:
        ijk = ijk +1 #count if something screws up. haven't had this happen, but useful counter.
        printMe = ['Code failed to find ',str(ijk),' emails']
        printMe = ''.join(printMe)
        print("Code failed to find") #never prints!
    #try except block, find schedules
    sched = [] #need list, since some professors teach a lot.
    searchMe = BS.find_all('div',attrs={'class':'u-rich-text'})
    try:
        schedStore = searchMe[1].find_all('li') #find all the list tags.
        for i in schedStore: #loop through them all
            sched.append(i.get_text('',strip=True)) #grab the schedules and put them into a list for each professor
    except:
        printMe = [teacher,' has no schedule posted!'] #in case there are no schedules it prints. Needs to be more robust, but no time.

    #uic = '@uic.edu'
    email = str(email) #needs to be string for re to work
    emailEdit = re.findall('\S+uic.edu',email) #will leave end email just in case they don't use @uic for some terrible reason
    #some emails are math.uic.edu and had to change re. This method is robust to anything within the uic domain.
    #makes scraping take forever. Had a faster implementation, but it wouldn't catch every single email if something changes.
    emailEdit = str(emailEdit) #back to string
    email = emailEdit[emailEdit.find('>'):] #delete everything to the left of >
    email = email[1:-2:] #remove '>' and also last two characters to get clean emails.

    print(email)
    return(teacher, email,sched)

#print(extract('https://mscs.uic.edu/profiles/jbergen/')) #test, works! Also grabs phone number, office#.

def writetoJSON(writeList):
    """Creates dictionary and writes scrape output to JSON."""
    file_exists = os.path.exists('list.json') #check if this file exists
    pathMe = os.getcwd() #get our current working directory..
    pathT = [pathMe,'\list.json'] #get the long path
    pathT = ''.join(pathT) #join the string to get the long path
    print(pathT)
    if file_exists == True:
        print("File exists. Deleting....") #print
        os.remove(pathT) #works
    writeIt = {"Teacher":writeList[0],"Email":writeList[1],"Teaching Schedule":writeList[2], "Link":writeList[3]}
    #what we are writing for each professor.
    print(writeIt)
    with open("list.json","w") as f:
        json.dump(writeIt,f,indent = 1) #one indent looks fine in VSCODE
#write(["1","2","3","4"]) #works

def scrapeUICMCS():
    """Function that will extract data from University of Illinois at Chicago MCS
     Teacher site for name, email, and teaching schedule and saves it to a json file."""

    site = "https://mscs.uic.edu/people/faculty/" #what site we are scraping
    init = urllib3.PoolManager() #urllib3 init
    get = init.request('Get',site) #urllib3 grabs site
    BS = BeautifulSoup(get.data.decode("utf-8"),"html5lib") #html5lib works well. If it throws an error then pip isntall html5lib per above comment.


    findMe = BS.find_all('div',attrs={'class','_colB'}) #what we're grabbing
    #init lists
    teacher = []
    schedule =[]
    link = []
    email = []

    for i in findMe:
        link1 = i.find_all('a')[0] #grab links a href....
        link2 = link1['href'] #grab links href....
        info = extractData(link2) #actually grab link with extract fun
        link.append(link2) #append 

        teacher.append(info[0]) #grab from return function.
        email.append(info[1]) #parsing error in [1], fix or json failure to write because p class included.
        #fixed with regular expression.
        schedule.append(info[2])
    listMe = (teacher,email,schedule,link) #make list of each var.
    #print(str(teacher)) #doesn't work, OOP memory address type thing
    writetoJSON(listMe)



scrapeUICMCS()






def DetailsJSON(text):
    """Grabs details from json file we wrote. Entirely dependent on search query."""
    file = open('list.json')
    #open and read the json file from the scraping.
    openMe = json.load(file)

    teacherList = openMe["Teacher"]
    emailList = openMe["Email"]
    schedList = openMe["Teaching Schedule"]
    linkList = openMe["Link"]
    #separate out each part of the json into vars
    findMe = emailList.index(text)
    #find that match from fun input
    teacher = teacherList[findMe]
    email = emailList[findMe]
    sched = schedList[findMe]
    link = linkList[findMe]
    #match the values to the input
    return (teacher,email,sched,link)

def partialTeacher(text):
    """Find entire teacher name from partial letters given."""
    file = open('list.json')
    #open and read the json file from the scraping.
    openMe = json.load(file)
    list = openMe["Email"]
    hold = [i for i in list if text == i[:len(text)]]
    return hold
def searchTeacher(text):
    """find the teacher name from search query. Will find matches with partial names. Also returns all relevant information."""
    list = partialTeacher(text)
    holdMe = [DetailsJSON(i)[0] for i in list],[DetailsJSON(i)[1] for i in list],[DetailsJSON(i)[2] for i in list],[DetailsJSON(i)[3] for i in list] #email + name +sched + link to their profile page
    return holdMe
app = Flask(__name__)

def scheduleSplit(text):
    """Returns teacher name, email, schedule, and profile link given a class time such as 09:00"""
    teacher =[]
    email = []
    sched = []
    link = []
    file = open('list.json')
    #open and read the json file from the scraping.
    openMe = json.load(file)
    findMe = openMe["Teaching Schedule"] #init to find correlations in time.
    for i,j in enumerate(findMe):
        for k in j:
            if text in k.split("-")[0]: #all this woprk to get to - split correctly
                teacher.append(openMe["Teacher"][i]) #other implementation was faulty
                email.append(openMe["Email"][i])
                sched.append(k)
                link.append(openMe["Link"][i])
                
            elif type(k) == list: #for errors, loop back.
                scheduleSplit(text,k)
    return(teacher,email,sched,link)
#print(schedSplit("09:00")) #works!

#Flask seems to be error prone in general.
##Homepage that is also cloned to index.html to be robust and prevent errors when navigating. Both functions redirect to index.html.
##If the teacher box is selected then the fun == teacher if statement is run if its set to the time box then the else statement is executed.
#the teacher.txt or sched.txt files are written to depending on the query and this data is used then to find the relevant data to push
#to the webpage.
@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == "GET":
        return render_template('index.html')
        
    if request.method == 'POST':
        textbox = request.form['textbox'] #entry in textbox
        fun = request.form['fun']

        if fun =='teacher':
            #read = Details(textbox) #works
            read = searchTeacher(textbox)

            with open('teacher.txt','w') as f:
                f.write(json.dumps(read))
            #app.logger("POST works")    #throw error, debugging            
            return redirect(url_for('teacher', f = fun, name = textbox))
        else:
            read = scheduleSplit(textbox)
            with open('sched.txt','w') as f:
                f.write(json.dumps(read))
            return redirect(url_for('sched',f = fun,name = textbox))
            #return Flask.render_template('index.html', teacher = r[0])

#print(searchTeacher("jb")) #tesst, this of course works, but flask doesn't










#index.html page, same as above.
@app.route('/index.html', methods = ['GET','POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
        
    if request.method == 'POST':
        textbox = request.form['textbox'] #grab the data from the textbox
        fun = request.form['fun'] #which radio button did you select?

        if fun =='teacher':
            #read = Details(textbox) #works
            read = searchTeacher(textbox) #run the searchteacher func to find the teacher match

            with open('teacher.txt','w') as f: #open up a txt file to be written to
                f.write(json.dumps(read)) #write it and this is actually fed into the html file and outputted.
            #app.logger("POST works")    #throw error, debugging            
            return redirect(url_for('teacher', f = fun, name = textbox))
        else:
            read = scheduleSplit(textbox) #same as above, but this time its a schedule.
            with open('sched.txt','w') as f:
                f.write(json.dumps(read))
            return redirect(url_for('sched',f = fun,name = textbox))
            #return Flask.render_template('index.html', teacher = r[0])




#about page. Simple redirect.
@app.route('/about.html',methods = ['GET','POST'])
def about():
    if request.method == 'GET':

        return render_template('about.html') 

#teacher page, will populate based on index.html
@app.route('/teacher/<f>',methods = ["GET","POST"])
def teacher(f):
    if request.method == "GET":
        with open('teacher.txt') as f: #dont write here... UnboundLocalError: cannot access local variable 'read' where it is not associated with a value
                read = json.loads(f.read())
        return render_template('teacher.html', f = f, read=read) #load in the page

    if request.method == "POST": # was planning on having search available from the page, but best to just loop back to the original index.html for less confusion.
        textbox1 = request.form['textbox']
        read = searchTeacher(textbox1)
        with open('teacher.txt','w') as f: #would've rewrote things after entry into the textbox, but ran into too many issues on the html side
                f.write(json.dumps(read))
        return render_template('teacher.html',f=f)



@app.route('/class/<f>',methods = ["GET","POST"])
def sched(f):
    if request.method == "GET":
        with open('sched.txt') as f: #dont write here... UnboundLocalError: cannot access local variable 'read' where it is not associated with a value
                read = json.loads(f.read())
        return render_template('sched.html', f = f, read=read)

    if request.method == "POST":
        textbox1 = request.form['textbox']
        read = searchTeacher(textbox1)
        with open('sched.txt','w') as f:
                f.write(json.dumps(read))
        return render_template('sched.html',f=f)
app.run(host ='0.0.0.0', port = 81)


