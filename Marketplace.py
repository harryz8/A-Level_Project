#pip install pillow
#python -m pip install requests
#imports modules
import tkinter
from Modules import OcadoScraper
from Modules import MsScraper
from Modules import BqScraper
from Modules import JDScraper
from Modules import ResultsObject
from webbrowser import open as wbopen
import os
from hashlib import sha256
from PIL import ImageTk, Image
import requests
from shutil import rmtree

#colours
mainBgCol = "white"
secondBgCol = "#dfdfdf"#"#D7E1EE"
fg1 = "#19b6e2"
fg1_light = "#e3f9ff"
fg2 = "#0E647C"#"#d14c14"#"#228B22"
# old fg2="#bae718"

#initialises root window
root = tkinter.Tk()
#set the application name
root.title("Marketplace")
root.config(bg=mainBgCol)
root.state("zoomed")
#set the applicaiton icon
root.iconbitmap("./Images/M.ico")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#clear temp folder
#https://www.tutorialspoint.com/How-to-delete-all-files-in-a-directory-with-Python
try:
    rmtree("./temp")
except FileNotFoundError:
    pass
os.mkdir("./temp")

#variables
widgets = []
asearchResults = []
searchResults = []
windowHeight = root.winfo_height()
windowWidth = root.winfo_width()
basket = []
totalResults = 0
saveBt = None
itemImages = []
username = "guest"
promotedResult = []

#creates first frame inside the root window
window = tkinter.Frame(root, bg=mainBgCol)
window.grid(row=0, column=0, sticky="nesw")
window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=0)
window.update()

#constants
#https://stackoverflow.com/questions/46495160/make-a-label-bold-tkinter
LARGEBOLDFONT = ("Verdana", "18", "bold")
LARGEUNDERLINEFONT = ("Verdana", "18", "underline")
LARGEFONT = ("Verdana", "18")
MEDIUMBOLDFONT = ("Verdana", "14", "bold")
MEDIUMFONT = ("Verdana", "14")
TITLEFONT = ("Verdana", "96", "bold")
SMALLFONT = ("Verdana", "11")

#images
bag_img = tkinter.PhotoImage(file="./Images/add_to_list.png")
filterImg = tkinter.PhotoImage(file="./Images/filter.png")
bagImg = tkinter.PhotoImage(file="./Images/list.png")
logoImg = tkinter.PhotoImage(file="./Images/logo.png")
saveImg = tkinter.PhotoImage(file="./Images/save.png")
searchImg = tkinter.PhotoImage(file="./Images/search.png")
homeImg = tkinter.PhotoImage(file="./Images/home.png")
ocadoImage = tkinter.PhotoImage(file="./Images/ocado_logo.png")
msImage = tkinter.PhotoImage(file="./Images/ms_logo.png")
bqImage = tkinter.PhotoImage(file="./Images/bq_logo.png")
jdImage = tkinter.PhotoImage(file="./Images/jd_logo.png")
noImage = tkinter.PhotoImage(file="./Images/No Image.png")

def login_or_register():
    #allows user to login or to make an account
    try:
        global signInBt
        signInBt.place_forget()
    except:
        pass
    global loginWindow, usernameEntry, passwordEntry, loginBt, username, usernameFrame, passwordFrame
    window.pack_forget()
    #removes main window and puts the login/register window on the screen
    loginWindow = tkinter.Frame(root, bg=mainBgCol)
    loginWindow.grid(row=0, column=0, sticky="nesw")
    loginWindow.columnconfigure(0, weight=0)
    loginWindow.columnconfigure(1, weight=1)
    loginWindow.rowconfigure(0, weight=2)
    loginWindow.rowconfigure(1, weight=1)
    loginWindow.rowconfigure(2, weight=1)
    loginWindow.rowconfigure(3, weight=1)
    loginWindow.rowconfigure(4, weight=1)
    loginWindow.rowconfigure(5, weight=50)
    loginWindow.rowconfigure(6, weight=1)
    logoLb = tkinter.Label(loginWindow, bg=mainBgCol, image=logoImg)
    logoLb.grid(row=0, column=0, sticky="nesw")
    titleFrame = tkinter.Frame(loginWindow, bg=fg1)
    titleFrame.grid(row=0, column=1, sticky="ew", pady=10, padx=10)
    titleFrame.columnconfigure(0, weight=1)
    titleFrame.rowconfigure(0, weight=1)
    titleLb = tkinter.Label(titleFrame, text="Marketplace", bg=mainBgCol, fg=fg1, font=TITLEFONT)
    titleLb.grid(row=0, column=0, sticky="nesw", pady=2, padx=2)
    usernameFrame = tkinter.Frame(loginWindow, bg=fg1)
    usernameFrame.grid(row=1, column=0, sticky="nesw", padx=10, pady=10, columnspan=2)
    usernameFrame.columnconfigure(0, weight=1)
    usernameFrame.rowconfigure(0, weight=1)
    usernameFrame.rowconfigure(1, weight=1)
    usernameLb = tkinter.Label(usernameFrame, text="Username:", font=LARGEFONT, bg=fg1, fg=mainBgCol)
    usernameLb.grid(row=0, column=0, sticky="nesw")
    usernameEntry = tkinter.Entry(usernameFrame, font=MEDIUMBOLDFONT, relief=tkinter.FLAT, fg=fg1, justify="center")
    usernameEntry.grid(row=1, column=0, sticky="nesw", padx=2, pady=2)
    usernameEntry.focus()
    passwordFrame = tkinter.Frame(loginWindow, bg=fg1)
    passwordFrame.grid(row=2, column=0, sticky="nesw", padx=10, pady=10, columnspan=2)
    passwordFrame.columnconfigure(0, weight=1)
    passwordFrame.rowconfigure(0, weight=1)
    passwordFrame.rowconfigure(1, weight=1)
    passwordLb = tkinter.Label(passwordFrame, text="Password:", font=LARGEFONT, bg=fg1, fg=mainBgCol)
    passwordLb.grid(row=1, column=0, sticky="nesw")
    passwordEntry = tkinter.Entry(passwordFrame, font=MEDIUMBOLDFONT, relief=tkinter.FLAT, show="*", fg=fg1, justify="center")#shows only *s
    passwordEntry.grid(row=2, column=0, sticky="nesw", padx=2, pady=2)
    def goguest():
        #continue to main part of program as a guest
        global username
        username = "guest"
        global loginWindow, window
        loginWindow.grid_forget()
        window.grid()
        window_setup()
    def logincheck(*args):
        #get entered details
        global usernameEntry, passwordEntry
        uname = usernameEntry.get()
        pswd = passwordEntry.get()
        insha = bytes(uname+pswd, "utf-8")
        #hash username and password
        h = sha256()
        h.update(insha)
        hashed = h.hexdigest()
        passgo = False
        #check hash against one saved under username.txt
        try:
            f = open("./Users/"+uname+".txt", "r")
            if f.read() == hashed:
                passgo = True
            f.close()
        except:
            pass
        if passgo == True:
            #if hashes are the same, log in and go to main part of program
            global username
            username = uname
            global loginWindow, window
            loginWindow.grid_forget()
            window.grid()
            window_setup()
        else:
            #give error if hashes are different
            error_popup("Incorrect Username/Password", "Incorrect username or password. Please try again.")
            usernameEntry.delete(0, tkinter.END)
            passwordEntry.delete(0, tkinter.END)
    def registeruser():
        #change into register window
        global loginBt, loginWindow, passwordEntry, numIndicator, lengthIndicator, capitalIndicator, validationFrame
        titleLb.config(text="Register")
        registerBt.config(state=tkinter.DISABLED)
        guestBt.config(state=tkinter.DISABLED)
        loginBt.config(command=contregister)
        loginWindow.bind("<Return>", contregister)
        passwordEntry.bind("<Return>", contregister)
        #password validation grid
        validationFrame = tkinter.Frame(loginWindow, bg=fg1, pady=2, padx=2)
        validationFrame.grid(row=3, column=0, columnspan=3)
        numIndicator = tkinter.Frame(validationFrame, bg="red", width=30)
        numIndicator.grid(row=0, column=0, sticky="nesw", padx=2, pady=2)
        lengthIndicator = tkinter.Frame(validationFrame, bg="red", width=30)
        lengthIndicator.grid(row=1, column=0, sticky="nesw", padx=2, pady=2)
        capitalIndicator = tkinter.Frame(validationFrame, bg="red", width=30)
        capitalIndicator.grid(row=2, column=0, sticky="nesw", padx=2, pady=2)
        numLabel = tkinter.Label(validationFrame, bg=mainBgCol, text="Number in password?", font=MEDIUMFONT)
        numLabel.grid(row=0, column=1, sticky="nesw", padx=2, pady=2)
        lengthLabel = tkinter.Label(validationFrame, bg=mainBgCol, text="Password at least 8 digits?", font=MEDIUMFONT)
        lengthLabel.grid(row=1, column=1, sticky="nesw", padx=2, pady=2)
        capitalLabel = tkinter.Label(validationFrame, bg=mainBgCol, text="Capital letter in password?", font=MEDIUMFONT)
        capitalLabel.grid(row=2, column=1, sticky="nesw", padx=2, pady=2)
        def updateindicators(*args):
            global numIndicator, lengthIndicator, capitalIndicator, passwordEntry
            pswd = passwordEntry.get()
            numIndicator.config(bg="red")
            capitalIndicator.config(bg="red")
            lengthIndicator.config(bg="red")
            #if rules are met, change to green
            for char in pswd:
                #https://stackoverflow.com/questions/40097590/detect-whether-a-python-string-is-a-number-or-a-letter
                if char.isdigit():
                    numIndicator.config(bg="green")
                    #https://www.geeksforgeeks.org/isupper-islower-lower-upper-python-applications/
                elif char.isupper():
                    capitalIndicator.config(bg="green")
            if len(pswd) >= 8:
                lengthIndicator.config(bg="green")
        def updateindicatorswait(*args):
            #wait 10ms
            root.after(10, updateindicators)
        #update indicators on key press
        #https://stackoverflow.com/questions/55603282/keybind-that-binds-to-every-key-in-tkinter
        passwordEntry.bind("<Key>", updateindicatorswait)
    def contregister(*args):
        #get entred details
        global usernameEntry, passwordEntry
        passwordEntry.config(bg=mainBgCol)
        usernameEntry.config(bg=mainBgCol)
        uname = usernameEntry.get()
        pswd = passwordEntry.get()
        numPresent = False
        capitalPresent = False
        for char in pswd:
            #https://stackoverflow.com/questions/40097590/detect-whether-a-python-string-is-a-number-or-a-letter
            if char.isdigit():
                numPresent = True
                #https://www.geeksforgeeks.org/isupper-islower-lower-upper-python-applications/
            elif char.isupper():
                capitalPresent = True
        if numPresent == True and capitalPresent == True and len(pswd) >= 8 and len(uname) != 0: #check the validation is met
            insha = bytes(uname+pswd, "utf-8")
            h = sha256()
            h.update(insha)
            hashed = h.hexdigest()
            #https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/
            #check for empty strings and that username is not taken
            if len(uname) != 0 and len(pswd) != 0 and os.path.exists("./Users/"+uname+".txt") == False:
                f = open("./Users/"+uname+".txt", "x")
                f.write(hashed)
                f.close()
                global username
                username = uname
                global loginWindow, window
                loginWindow.grid_forget()
                window.grid()
                window_setup()
            else:
                #warn user
                error_popup("Invalid Details", "Invalid Details\n\nIt is likely that this username is taken.")
        elif len(uname) != 0:#changes colours of entry widgets if details are missing or don't follow the rules
            passwordEntry.config(bg="#FF7A7A")
        elif numPresent == True and capitalPresent == True and len(pswd) >= 8:
            usernameEntry.config(bg="#FF7A7A")
        else:
            passwordEntry.config(bg="#FF7A7A")
            usernameEntry.config(bg="#FF7A7A")
    buttonFrame = tkinter.Frame(loginWindow, bg=fg1)
    buttonFrame.grid(column=0, row=6, sticky="nesw", pady=10, padx=10, columnspan=2)
    buttonFrame.columnconfigure(0, weight=1)
    buttonFrame.columnconfigure(1, weight=1)
    buttonFrame.columnconfigure(2, weight=1)
    buttonFrame.rowconfigure(0, weight=1)
    loginBt = tkinter.Button(buttonFrame, text="Login", font=LARGEBOLDFONT, relief=tkinter.FLAT, fg=fg1, bg=mainBgCol, command=logincheck)
    loginBt.grid(row=0, column=2, sticky="nesw", pady=2, padx=2)
    guestBt = tkinter.Button(buttonFrame, text="Continue as Guest", font=LARGEBOLDFONT, relief=tkinter.FLAT, fg=fg1, bg=mainBgCol, command=goguest)
    guestBt.grid(row=0, column=1, sticky="nesw", pady=2, padx=2)
    registerBt = tkinter.Button(buttonFrame, text="Add Account", font=LARGEBOLDFONT, relief=tkinter.FLAT, fg=fg1, bg=mainBgCol, command=registeruser)
    registerBt.grid(row=0, column=0, sticky="nesw", pady=2, padx=2)
    #bind keys to commands
    loginWindow.bind("<Return>", logincheck)
    passwordEntry.bind("<Return>", logincheck)

def window_setup():
    #sets up the ui for the main part of the program
    global sidebar, username, mainframe, footerFrame, saveBt
    #creates side navigation bar
    #https://www.geeksforgeeks.org/how-to-change-border-color-in-tkinter-widget/
    sidebar = tkinter.Frame(window, width=150, height=windowHeight, bg=secondBgCol, borderwidth=0, highlightthickness=2, highlightcolor=fg1, relief="raised")
    sidebar.grid(column=0, row=0, sticky="nesw", rowspan=2)
    global scrollbar, pageLabel, canvas, wp, filterBt, bagBt
    global searchEntry, resultFrame
    #https://www.tutorialspoint.com/python/tk_place.htm
    #https://www.geeksforgeeks.org/python-place-method-in-tkinter/#:~:text=The%20Place%20geometry%20manager%20is,or%20relative%20to%20another%20window.
    #https://www.tutorialspoint.com/python3/tk_anchors.htm#:~:text=Python%203%20%2D%20Tkinter%20Anchors,-Advertisements&text=Anchors%20are%20used%20to%20define,be%20used%20for%20Anchor%20attribute.&text=For%20example%2C%20if%20you%20use,vertically%20around%20the%20reference%20point.
    bagBt = tkinter.Button(sidebar, image=bagImg, borderwidth=0, command=basketNewOrLoad, bg=secondBgCol)
    bagBt.place(relx=0.5, y=110, anchor=tkinter.N)
    homeBt = tkinter.Button(sidebar, image=homeImg, borderwidth=0, command=clearandback, bg=secondBgCol)
    homeBt.place(relx=0.5, y=2, anchor=tkinter.N)
    filterBt = tkinter.Button(sidebar, image=filterImg, borderwidth=0, command=filter_popup, bg=secondBgCol)
    pageLabelFrame = tkinter.Frame(sidebar, bg=fg1)
    pageLabelFrame.place(y=windowHeight-37, relx=0.5, anchor=tkinter.N)
    pageLabel = tkinter.Label(pageLabelFrame, text=f"{str(totalResults)} results", font=MEDIUMFONT, bg=secondBgCol, fg=fg1)
    pageLabel.grid(column=0, row=0, sticky="nesw", padx=2, pady=2)
    saveBt = tkinter.Button(sidebar, image=saveImg, relief=tkinter.FLAT, bg=secondBgCol, command=save_basket_popup)
    #creates the footer
    footerFrame = tkinter.Frame(window, bg=secondBgCol, borderwidth=0, highlightthickness=2, highlightcolor=fg1, relief="raised")
    footerFrame.grid(column=1, row=1, sticky="nesw")
    footerFrame.columnconfigure(0, weight=1)
    footerFrame.rowconfigure(0, weight=1)
    #creates the mainframe in the centre of the page
    mainframe = tkinter.Frame(window, bg=mainBgCol, borderwidth=0)
    mainframe.grid(column=1, row=0, sticky="nesw")
    mainframe.update()
    mainframe.columnconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=0)
    mainframe.columnconfigure(2, weight=0)
    mainframe.rowconfigure(0, weight=0)
    mainframe.rowconfigure(1, weight=1)
    mainframe.rowconfigure(2, weight=0)
    searchBt = tkinter.Button(mainframe, bg=mainBgCol, relief="flat", image=searchImg, command=loadingpage)
    searchBt.grid(column=1, row=0, sticky="nesw")
    #
    #creates the search bar
    searchFrame = tkinter.Frame(mainframe, bg=mainBgCol, borderwidth=0)
    searchFrame.grid(column=0, row=0, sticky="nesw")
    searchFrame.update()
    #https://stackoverflow.com/questions/3950687/how-to-find-out-the-current-widget-size-in-tkinter
    wp = searchFrame.winfo_width()
    #https://stackoverflow.com/questions/4310489/how-do-i-remove-the-light-grey-border-around-my-canvas-widget
    entcanvas = tkinter.Canvas(searchFrame, height=70, width=wp, bg=mainBgCol, highlightthickness=0)
    entcanvas.grid(column=0, row=0, sticky="nesw", columnspan=2)
    #https://www.hashbangcode.com/article/drawing-shapes-tkinter-canvas-element-python
    #Creates the border for the entry widget
    entcanvas.create_oval(5, 9, 50, 61, outline=fg1, width=2, fill=fg1_light)
    entcanvas.create_rectangle(31,9,wp-57,61, outline=fg1, width=2, fill=fg1_light)
    entcanvas.create_oval(wp-75, 9, wp-30, 61, outline=fg1, width=2, fill=fg1_light)
    #https://stackoverflow.com/questions/44160181/tkinter-call-function-when-entry-box-is-clicked
    #https://python-course.eu/tkinter/events-and-binds-in-tkinter.php
    searchEntry = tkinter.Entry(entcanvas, justify="center", font=LARGEFONT, bg=fg1_light, borderwidth=0)
    searchEntry.place(x=30, y=10, height=50, width=wp-86)
    searchEntry.insert(0, "Search all sites")
    searchEntry.bind("<Return>", loadingpage)
    searchEntry.bind("<Button-1>", clearSearchEntry)
    #
    #creates the frame's scrollbar
    # full code from https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
    #https://www.daniweb.com/programming/software-development/threads/270735/tkinter-remove-padding#:~:text=Just%20a%20little%20quirk%20in%20Tkinter.%20Since%20the,bd%3D-2%20to%20cancel%20it.%20Yep%2C%20that%20did%20it.
    canvas = tkinter.Canvas(mainframe, bg=mainBgCol, borderwidth=-2, relief=tkinter.FLAT)
    canvas.grid(column=0, row=1, sticky="nesw", columnspan=2)
    resultFrame = tkinter.Frame(canvas, bg=mainBgCol, borderwidth=0)
    resultFrame.columnconfigure(0, weight=1)
    resultFrame.columnconfigure(1, weight=1)
    createwindow = canvas.create_window(0,0, window=resultFrame, anchor=tkinter.NW)
    scrollbar = tkinter.Scrollbar(mainframe, orient='vertical', command=canvas.yview)
    scrollbar.grid(column=2, row=1, sticky="nsew")
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)
    canvas.config(yscrollcommand = scrollbar.set)
    #https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
    #scroll with wheel when mouse on canvas
    def mousewheel(event):
        #distance travelled down
        distance = -1*(event.delta/120)
        canvas.yview_scroll(int(distance), "units")
    canvas.bind_all("<MouseWheel>", mousewheel)
    def _configure_interior(event):
        # Update the scrollbars to match the size of the inner frame.
        size = (resultFrame.winfo_reqwidth(), resultFrame.winfo_reqheight())
        canvas.config(scrollregion="0 0 %s %s" % size)
        if resultFrame.winfo_reqwidth() != canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            canvas.config(width=resultFrame.winfo_reqwidth())
    resultFrame.bind('<Configure>', _configure_interior)
    def _configure_canvas(event):
        if resultFrame.winfo_reqwidth() != canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            canvas.itemconfigure(createwindow, width=canvas.winfo_width())
    canvas.bind('<Configure>', _configure_canvas)
    welcomepage()

def welcomepage():
    #creates the home screen
    global signInBt, sidebar, footerFrame, searchEntry, canvas
    searchEntry.config(state=tkinter.NORMAL)
    try:
        signInBt.place()
    except:
        pass
    clearresultframe()
    global saveBt
    saveBt.place_forget()
    sidebar.update()
    try:
        global filterBt
        filterBt.place_forget()
    except:
        pass
    #make scrolled up
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)
    global widgets
    #sign in button if guest, else sign out button
    if username == "guest":
        signInBt = tkinter.Button(sidebar, text="Sign In", command=login_or_register, relief="flat", font=MEDIUMFONT, fg=secondBgCol, bg=fg1)
        signInBt.place(relx=0.5, y=220, anchor = tkinter.N)
    else:
        signInBt = tkinter.Button(sidebar, text="Sign Out", command=login_or_register, relief="flat", font=MEDIUMFONT, fg=secondBgCol, bg=fg1)
        signInBt.place(relx=0.5, y=220, anchor = tkinter.N)
    frame1 = tkinter.Frame(resultFrame, bg=mainBgCol)
    frame1.grid(column=0, row=1, sticky="nesw", padx=2, pady=2, columnspan=2)
    frame1.rowconfigure(0, weight=1)
    frame1.columnconfigure(0, weight=1)
    frame1.columnconfigure(1, weight=1)
    frame1.columnconfigure(2, weight=1)
    frame1.columnconfigure(3, weight=1)
    #create store grid and link to store delivery info
    img1 = tkinter.Button(frame1, image=ocadoImage, bg=mainBgCol, highlightthickness=2, highlightcolor=mainBgCol, relief=tkinter.FLAT, bd=0, command=lambda: store_information_popup("ocado"))
    img1.grid(column=0, row=0, sticky="nesw")
    img2 = tkinter.Button(frame1, image=msImage, bg=mainBgCol, highlightthickness=2, highlightcolor=mainBgCol, relief=tkinter.FLAT, bd=0, command=lambda: store_information_popup("ms"))
    img2.grid(column=1, row=0, sticky="nesw")
    img3 = tkinter.Button(frame1, image=bqImage, bg=mainBgCol, highlightthickness=2, highlightcolor=mainBgCol, relief=tkinter.FLAT, bd=0, command=lambda: store_information_popup("bq"))
    img3.grid(column=2, row=0, sticky="nesw")
    img4 = tkinter.Button(frame1, image=jdImage, bg=mainBgCol, highlightthickness=2, highlightcolor=mainBgCol, relief=tkinter.FLAT, bd=0, command=lambda: store_information_popup("jd"))
    img4.grid(column=3, row=0, sticky="nesw")
    helloFrame = tkinter.Frame(resultFrame, bg=fg1)
    helloFrame.grid(column=0, row=0, columnspan=2, pady=20)
    helloFrame.columnconfigure(0, weight=1)
    helloFrame.rowconfigure(0, weight=1)
    helloLb = tkinter.Label(helloFrame, bg=mainBgCol, text = "Hello "+username[0].upper()+username[1:], font=TITLEFONT, fg=fg1)
    helloLb.grid(column=0, row=0, sticky="nesw", padx=2, pady=2)
    #helpful message
    helpMessage = tkinter.Label(footerFrame, text="Tip: Search in the box at the top of the page or click on the images above to go to the stores' websites.", bg=secondBgCol, fg=fg1, font=MEDIUMFONT)
    helpMessage.grid(column=0, row=0, sticky="nesw")
    #append widgets to a list "widgets" so that they can be later grid_forget()ed
    widgets.append(helpMessage)
    widgets.append(helloFrame)
    widgets.append(frame1)

def loadingpage(*args, passTo="search"):
    try:
        global signInBt
        signInBt.place_forget()
    except:
        pass
    clearresultframe()
    try:
        global saveBt
        saveBt.place_forget()
    except:
        pass
    try:
        global filterBt
        filterBt.place_forget()
    except:
        pass
    global widgets
    loadingLabel = tkinter.Label(resultFrame, bg=fg2, fg=mainBgCol, font=LARGEBOLDFONT, text="Loading...")
    loadingLabel.grid(column=0, row=0, padx=5, pady=5, columnspan=2)
    widgets.append(loadingLabel)
    #decide what to load next
    if passTo == "search":
        window.after(10, search)
    elif passTo == "list":
        window.after(10, lambda:buildbasketframe(args[0]))
    elif passTo == "build":
        global searchResults
        window.after(10, lambda:buildwidgetsframe(searchResults.outpt()))

def search():
    #get search data from all scrapers
    global promotedResult
    promotedResult = []
    clearresultframe()
    #catches different unsuitable searches
    searchTxt = searchEntry.get().strip("'").strip('"').strip("/").strip("*")
    if searchTxt == " ":
        searchTxt = ""
    if searchTxt == "":
        error_popup("No input", "Please enter a suitable search term to start a search.")
        clearandback()
    else:
        #https://www.pythontutorial.net/python-basics/python-check-if-file-exists/
        #try:
        if os.path.exists("./temp/"+searchTxt.lower()+".txt"):
            #try to get cached results
            global asearchResults
            #https://stackoverflow.com/questions/6048085/writing-unicode-text-to-a-text-file
            f = open("./temp/"+searchTxt.lower()+".txt", "rb")
            data = f.read().decode("utf8")
            f.close()
            data = data.split("\n")
            data = data[:-1]
            asearchResults = []
            for item in data:
                row = item.split("¬")
                asearchResults.append(row)
            global searchResults
            searchResults = ResultsObject.ro(asearchResults)
        else:
            #or get results from scraping
            try:
                ocadoSearch = OcadoScraper.os(searchTxt)
                ocadoData = ocadoSearch.outpt()
            except AttributeError:
                ocadoData = []
            try:
                msSearch = MsScraper.ms(searchTxt)
                msData = msSearch.outpt()
            except AttributeError:
                msData = []
            try:
                bqSearch = BqScraper.bq(searchTxt)
                bqData = bqSearch.outpt()
            except AttributeError:
                bqData = []
            try:
                jdSearch = JDScraper.jd(searchTxt)
                jdData = jdSearch.outpt()
            except AttributeError:
                jdData = []
            #cache this search
            sortitems(ocItems=ocadoData, msItems=msData, bqItems=bqData, jdItems=jdData)
            f = open("./temp/"+searchTxt.lower()+".txt", "wb")
            for item in asearchResults:
                for object2 in item:
                    #https://stackoverflow.com/questions/6048085/writing-unicode-text-to-a-text-file
                    f.write((object2+"¬").encode('utf8'))
                f.write(("\n").encode("utf8"))
            f.close()
        #display results
        displayPromotedResult()
        #buildwidgetsframe(searchResults.outpt())
        """except:
            #if an exception is raised, you will end up with this error
            error_popup("Error", "Error: Either the network connection is down, or you have entered an invalid term.")
            clearandback()"""

def sortitems(ocItems=[], msItems=[], bqItems=[], jdItems=[]):
    global searchResults, asearchResults, totalResults, searchEntry, promotedResult
    weighted_totals = []
    #check if items have been passed
    if len(ocItems) > 0 or len(msItems) > 0 or len(bqItems) > 0 or len(jdItems) > 0:
        #sorts results in to an alternating list by site
        asearchResults = []
        counter = 1
        while True:
            if counter == 1 and len(ocItems) != 0:
                #https://tutorial.eyehunts.com/python/python-list-pop-first-element-example-code/
                item = ocItems.pop(0)
                asearchResults.append(item)
                #calculate valuation numuber
                rating = item[5]
                if rating == "N/A":
                    rating = 2.5
                weight = (((1000-float(item[1]))/1000)*2) + float(rating)/5
                weighted_totals.append(weight)
            elif counter == 2 and len(msItems) != 0:
                item = msItems.pop(0)
                asearchResults.append(item)
                #calculate valuation numuber
                rating = item[5]
                if rating == "N/A":
                    rating = 2.5
                weight = (((1000-float(item[1]))/1000)*2) + float(rating)/5
                weighted_totals.append(weight)
            elif counter == 3 and len(bqItems) != 0:
                item = bqItems.pop(0)
                asearchResults.append(item)
                #calculate valuation numuber
                rating = item[5]
                if rating == "N/A":
                    rating = 2.5
                weight = (((1000-float(item[1]))/1000)*2) + float(rating)/5
                weighted_totals.append(weight)
            elif counter == 4 and len(jdItems) != 0:
                item = jdItems.pop(0)
                asearchResults.append(item)
                #calculate valuation numuber
                rating = item[5]
                if rating == "N/A":
                    rating = 2.5
                weight = (((1000-float(item[1]))/1000)*2) + float(rating)/5
                weighted_totals.append(weight)
            elif len(ocItems)==0 and len(msItems)==0 and len(bqItems)==0 and len(jdItems)==0:
                break
            counter = counter+1
            if counter == 5:
                counter = 1
        #save best value result
        promotedResult.append(asearchResults[weighted_totals.index(max(weighted_totals))])
    else:
        #creates error popup if search term does not return any results
        error_popup("No Results", "Error: There are no results for this search term. Plese try a different term.")
        clearandback()
    searchResults = ResultsObject.ro(asearchResults)

def displayPromotedResult():
    #displays the promoted result
    global signInBt
    signInBt.place_forget()
    global canvas, saveBt
    clearresultframe()
    try:
        saveBt.place_forget()
    except:
        pass
    #scroll to the top
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)
    global widgets, promotedResult
    #variables
    promotedColour = "orange"
    item_list = promotedResult[0]
    name = item_list[0]
    oneResult = tkinter.Frame(resultFrame, bg=promotedColour)
    oneResult.grid(row=0, column=0, sticky="", padx=5, pady=5, columnspan=2)
    #Sets up the responsive layout
    oneResult.rowconfigure(0, weight=1)
    oneResult.rowconfigure(1, weight=1)
    oneResult.rowconfigure(2, weight=1)
    oneResult.rowconfigure(3, weight=1)
    oneResult.rowconfigure(4, weight=0)
    oneResult.rowconfigure(5, weight=0)
    oneResult.columnconfigure(0, weight=1)
    oneResult.columnconfigure(1, weight=0)
    #display item information
    promotionLabel = tkinter.Label(oneResult, text="We recommend:", font=LARGEUNDERLINEFONT, fg=mainBgCol, bg=promotedColour)
    promotionLabel.grid(row=0, column=0, columnspan=2, sticky="nsw")
    itemName = tkinter.Label(oneResult, text=name, bg=promotedColour, font=MEDIUMBOLDFONT, fg=mainBgCol, wraplength=(wp-160))
    itemName.grid(row=1, column=0, sticky="nesw", columnspan=2)
    #https://pythonexamples.org/python-tkinter-change-background-color-during-mouse-click/
    def addPromotedToBasket():
        #add an item to list
        global basket, promotedResult, bagBt
        basket.append(promotedResult[0])
        #blink icon yellow
        bagBt.config(bg="Yellow")
        def revertcol():
            global bagBt
            bagBt.config(bg=secondBgCol)
        bagBt.after(500, revertcol)
    bag_bt_promoted = tkinter.Button(oneResult, image=bag_img, command=addPromotedToBasket, relief="flat", bg=promotedColour, activebackground=promotedColour)
    bag_bt_promoted.grid(row=3, column=1, sticky="nesw")
    buybt_promoted = tkinter.Button(oneResult, bg=mainBgCol, relief='flat', text='More Info ⤤', fg=promotedColour, font=MEDIUMBOLDFONT, command=lambda: wbopen(str(item_list[2])))
    buybt_promoted.grid(row=5, column=0, columnspan=2, padx=4, pady=4, sticky="nesw")
    itemPrice = tkinter.Label(oneResult, text="£"+item_list[1], bg=promotedColour, font=MEDIUMFONT, fg=mainBgCol)
    itemPrice.grid(row=2, column=0, sticky="nesw")
    #https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
    #https://www.plus2net.com/python/tkinter-image-resize.php#:~:text=Python%20tkinter%20image%20resize%201%20resize%20%28%29%20with,images%20Upload%20and%20display%20image%20file%20%E2%86%92%20
    #https://www.tutorialspoint.com/how-do-i-use-pil-with-tkinter
    #https://stackoverflow.com/questions/38489386/python-requests-403-forbidden
    #get image from the internet
    if item_list[4] != None:
        passed = 0
        while passed < 10:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                itemImg = Image.open(requests.get(item_list[4], stream=True, headers=headers).raw)
                #resize that image
                resizedImg = itemImg.resize((100,100))
                itemImages.append(ImageTk.PhotoImage(resizedImg))
                itemImage = tkinter.Label(oneResult, image=itemImages[-1], bg=promotedColour)
                itemImage.grid(row=3, column=0, sticky="nesw")
                passed = 10
            except:
                passed = passed +1
    else:
        global noImage
        itemImage = tkinter.Label(oneResult, image=noImage, bg=promotedColour)
        itemImage.grid(row=3, column=0, sticky="nesw")
    itemLocation = tkinter.Label(oneResult, text=item_list[3], bg=promotedColour, font=MEDIUMFONT, fg=mainBgCol)
    itemLocation.grid(row=4, column=0, sticky="nesw")
    itemRating = tkinter.Label(oneResult, text="User rating: "+item_list[5], bg=promotedColour, font=MEDIUMFONT, fg=mainBgCol)
    itemRating.grid(row=4, column=1, sticky="nesw")
    #give user the option to search all of the results
    global loadResultsAfterPromoted
    def loadAllResults():
        loadingpage(passTo="build")
    loadResults = tkinter.Button(resultFrame, text="Load All Results", bg=fg1, fg=mainBgCol, command=loadAllResults, relief=tkinter.FLAT, font=MEDIUMBOLDFONT)
    loadResults.grid(row=1, column=0, sticky="", padx=5, pady=5, columnspan=2)
    widgets.append(loadResults)
    widgets.append(oneResult)

def addtobasket(item2):
    #add an item to list
    global basket, searchResults, bagBt
    basket.append(searchResults.outpt()[item2])
    #blink icon yellow
    bagBt.config(bg="Yellow")
    def revertcol():
        global bagBt
        bagBt.config(bg=secondBgCol)
    bagBt.after(500, revertcol)

def removebasketitem(item):
    #remove item from list
    global basket
    basket.remove(item)
    buildbasketframe(basket)

def buildbasketframe(item_List_Inner):
    #display current list
    global signInBt, searchEntry
    searchEntry.config(state=tkinter.DISABLED)
    signInBt.place_forget()
    global canvas, resultframe, footerFrame
    clearresultframe()
    #scroll up to top
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)
    global widgets, sidebar, filterBt, mainframe
    sumprices = 0
    #for each item in list, add to grid
    for item in range(0, len(item_List_Inner)):
        #2x2 grid
        col = item%2
        rw = item//2
        itemFrame = tkinter.Frame(resultFrame, bg=fg2)
        itemFrame.grid(row=rw, column=col, sticky="nesw", padx=5, pady=5)
        #Sets up the responsive layout
        itemFrame.rowconfigure(0, weight=0)
        itemFrame.rowconfigure(1, weight=0)
        itemFrame.rowconfigure(2, weight=0)
        itemFrame.rowconfigure(3, weight=0)
        itemFrame.rowconfigure(4, weight=1)
        itemFrame.rowconfigure(5, weight=0)
        itemFrame.columnconfigure(0, weight=1)
        itemFrame.columnconfigure(1, weight=0)
        #display all information
        item_list = item_List_Inner[item]
        name = item_List_Inner[item][0]
        itemName = tkinter.Label(itemFrame, text=name, bg=fg2, font=MEDIUMBOLDFONT, fg=mainBgCol, wraplength=(wp-160)/2)
        itemName.grid(row=0, column=0, sticky="nesw", columnspan=2)
        try:
            filterBt.place_forget()
        except:
            pass
        #https://pythonexamples.org/python-tkinter-change-background-color-during-mouse-click/
        #allows each item to have individual remove and buy buttons
        exec("cross_bt"+str(item)+" = tkinter.Button(itemFrame, text=\"Remove\", command=lambda: removebasketitem(basket["+str(item)+"]), relief=\"flat\", bg='white', fg=fg2, activebackground=fg2, font=MEDIUMBOLDFONT)")
        exec("cross_bt"+str(item)+".grid(row=5, column=1, columnspan=2, padx=4, pady=4, sticky=\"nesw\")")
        exec("buybt"+str(item)+" = tkinter.Button(itemFrame, bg=mainBgCol, relief='flat', text='Buy ⤤', fg=fg2, font=MEDIUMBOLDFONT, command=lambda: wbopen(\""+str(item_List_Inner[item][2])+"\"))")
        exec("buybt"+str(item)+".grid(row=5, column=0, padx=4, pady=4, sticky=\"nesw\")")
        #show save button if not guest
        if username != "guest":
            global saveImg, saveBt
            saveBt.place(y=220, relx=0.5, anchor=tkinter.N)
        clearSearchEntry()
        searchEntry.insert(0, "List")
        itemPrice = tkinter.Label(itemFrame, text="£"+item_List_Inner[item][1], bg=fg2, font=MEDIUMFONT, fg=mainBgCol)
        itemPrice.grid(row=1, column=0, sticky="nesw", columnspan=3)
        sumprices = sumprices + float(item_List_Inner[item][1])
        #https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
        #https://www.plus2net.com/python/tkinter-image-resize.php#:~:text=Python%20tkinter%20image%20resize%201%20resize%20%28%29%20with,images%20Upload%20and%20display%20image%20file%20%E2%86%92%20
        #https://www.tutorialspoint.com/how-do-i-use-pil-with-tkinter
        #https://stackoverflow.com/questions/38489386/python-requests-403-forbidden
        #gets image from web
        if item_List_Inner[item][4] != None:
            passed = 0
            while passed < 10:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    itemImg = Image.open(requests.get(item_List_Inner[item][4], stream=True, headers=headers).raw)
                    #resize that image
                    resizedImg = itemImg.resize((100,100))
                    itemImages.append(ImageTk.PhotoImage(resizedImg))
                    itemImage = tkinter.Label(itemFrame, image=itemImages[-1], bg=fg2)
                    itemImage.grid(row=2, column=0, sticky="nesw", columnspan=3)
                    passed = 10
                except:
                    passed = passed +1
        else:
            global noImage
            itemImage = tkinter.Label(itemFrame, image=noImage, bg=fg2)
            itemImage.grid(row=2, column=0, sticky="nesw")
        itemLocation = tkinter.Label(itemFrame, text=item_List_Inner[item][3], bg=fg2, font=MEDIUMFONT, fg=mainBgCol)
        itemLocation.grid(row=3, column=0, sticky="nesw", columnspan=3)
        itemRating = tkinter.Label(itemFrame, text=" User rating: " + item_List_Inner[item][5], bg=fg2, font=MEDIUMFONT, fg=mainBgCol)
        itemRating.grid(row=3, column=1, sticky="nesw", columnspan=2)
        #get descriptions for different stores' items
        getDescription = []
        if item_List_Inner[item][3] == "Ocado":
            getDescription = OcadoScraper.getdetails(item_List_Inner[item][2])
        elif item_List_Inner[item][3] == "B & Q":
            getDescription = BqScraper.getdetails(item_List_Inner[item][2])
        elif item_List_Inner[item][3] == "JD Sports":
            getDescription = JDScraper.getdetails(item_List_Inner[item][2])
        elif item_List_Inner[item][3] == "Marks and Spencer":
            getDescription = MsScraper.getdetails(item_List_Inner[item][2])
        if len(getDescription) > 1:
            getDescription = getDescription[:-1]
        else:
            getDescription = []
        #https://www.tutorialspoint.com/how-to-word-wrap-text-in-tkinter-text#:~:text=It%20is%20used%20to%20fit,WORD%2C%20CHARS%2C%20or%20NONE.
        #display descriptions in a text widget
        itemDescription = tkinter.Text(itemFrame, bg=mainBgCol, font=SMALLFONT, fg=fg2, wrap=tkinter.WORD, relief=tkinter.FLAT, height=5)
        itemDescription.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nesw")
        itemDescription.insert("0.0", getDescription)
        #https://www.geeksforgeeks.org/python-tkinter-scrollbar/
        #add scroll bar
        itemScroll = tkinter.Scrollbar(itemFrame)
        itemScroll.grid(row=4, column=2, sticky="ns")
        itemDescription.config(yscrollcommand=itemScroll.set)
        itemScroll.config(command=itemDescription.yview)
        widgets.append(itemFrame)
    #Sum prices in basket and display
    #https://www.w3schools.com/python/ref_func_round.asp
    totalPriceLb = tkinter.Label(footerFrame, text="Total Price: £"+str(round(sumprices,2)), font=MEDIUMFONT, bg=secondBgCol)
    totalPriceLb.grid(column=0, row=0, sticky="nes")
    widgets.append(totalPriceLb)
    #adds a label displaying the number of items
    global totalResults
    totalResults = len(item_List_Inner)
    global pageLabel
    pageLabel.config(text=f"{str(totalResults)} results")
    #widgets.append(itemFrame)

def buildwidgetsframe(item_List_Inner, mode="search", numberDisplayed=50):
    #builds a grid to display search results
    global signInBt
    signInBt.place_forget()
    global canvas, saveBt
    clearresultframe()
    #scroll to the top
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)
    global widgets, searchEntry, sidebar, filterBt
    #https://stackoverflow.com/questions/17911091/append-integer-to-beginning-of-list-in-python
    #show results in the UI
    for item in range(0, min(numberDisplayed, len(item_List_Inner))):
        #whichever is shorter: numberDisplayed or number of item in list
        col = item%2
        rw = item//2
        itemFrame = tkinter.Frame(resultFrame, bg=fg2)
        itemFrame.grid(row=rw, column=col, sticky="nesw", padx=5, pady=5)
        #Sets up the responsive layout
        itemFrame.rowconfigure(0, weight=1)
        itemFrame.rowconfigure(1, weight=1)
        itemFrame.rowconfigure(2, weight=1)
        itemFrame.rowconfigure(3, weight=0)
        itemFrame.rowconfigure(4, weight=0)
        itemFrame.columnconfigure(0, weight=1)
        itemFrame.columnconfigure(1, weight=0)
        #display item information
        item_list = item_List_Inner[item]
        name = item_List_Inner[item][0]
        itemName = tkinter.Label(itemFrame, text=name, bg=fg2, font=MEDIUMBOLDFONT, fg=mainBgCol, wraplength=(wp-160)/2)
        itemName.grid(row=0, column=0, sticky="nesw", columnspan="2")
        if mode == "search":
            try:
                saveBt.place_forget()
            except:
                pass
            #https://pythonexamples.org/python-tkinter-change-background-color-during-mouse-click/
            #create specific add-to-list and more info buttons for each item
            exec("bag_bt"+str(item)+" = tkinter.Button(itemFrame, image=bag_img, command=lambda: addtobasket("+str(item)+"), relief=\"flat\", bg=fg2, activebackground=fg2)")
            exec("bag_bt"+str(item)+".grid(row=2, column=1, sticky=\"nesw\")")
            exec("buybt"+str(item)+" = tkinter.Button(itemFrame, bg=mainBgCol, relief='flat', text='More Info ⤤', fg=fg2, font=MEDIUMBOLDFONT, command=lambda: wbopen(\""+str(item_List_Inner[item][2])+"\"))")
            exec("buybt"+str(item)+".grid(row=4, column=0, columnspan=2, padx=4, pady=4, sticky=\"nesw\")")
            filterBt.place(y=220, relx=0.5, anchor=tkinter.N)
        itemPrice = tkinter.Label(itemFrame, text="£"+item_List_Inner[item][1], bg=fg2, font=MEDIUMFONT, fg=mainBgCol)
        itemPrice.grid(row=1, column=0, sticky="nesw")
        #https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
        #https://www.plus2net.com/python/tkinter-image-resize.php#:~:text=Python%20tkinter%20image%20resize%201%20resize%20%28%29%20with,images%20Upload%20and%20display%20image%20file%20%E2%86%92%20
        #https://www.tutorialspoint.com/how-do-i-use-pil-with-tkinter
        #https://stackoverflow.com/questions/38489386/python-requests-403-forbidden
        #get image from the internet
        if item_List_Inner[item][4] != None:
            passed = 0
            while passed < 10:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    itemImg = Image.open(requests.get(item_List_Inner[item][4], stream=True, headers=headers).raw)
                    #resize that image
                    resizedImg = itemImg.resize((100,100))
                    itemImages.append(ImageTk.PhotoImage(resizedImg))
                    itemImage = tkinter.Label(itemFrame, image=itemImages[-1], bg=fg2)
                    itemImage.grid(row=2, column=0, sticky="nesw")
                    passed = 10
                except:
                    passed = passed +1
        else:
            global noImage
            itemImage = tkinter.Label(itemFrame, image=noImage, bg=fg2)
            itemImage.grid(row=2, column=0, sticky="nesw")
        itemLocation = tkinter.Label(itemFrame, text=item_List_Inner[item][3], bg=fg2, font=MEDIUMFONT, fg=mainBgCol)
        itemLocation.grid(row=3, column=0, sticky="nesw")
        itemRating = tkinter.Label(itemFrame, text="User rating: "+item_List_Inner[item][5], bg=fg2, font=MEDIUMFONT, fg=mainBgCol)
        itemRating.grid(row=3, column=1, sticky="nesw")
        widgets.append(itemFrame)
    if len(item_List_Inner) > numberDisplayed:
        #button to display more of trhe results on the UI
        def loadmoreresults():
            buildwidgetsframe(searchResults.outpt(), numberDisplayed=numberDisplayed+50)
        moreLink = tkinter.Button(resultFrame, bg=mainBgCol, text="More results", command=loadmoreresults, fg="#0000EE", font=("Verdana", "14", "underline"), relief=tkinter.FLAT)
        moreLink.grid(row=numberDisplayed//2+1, column=0, columnspan=2, sticky="nesw", padx=5, pady=5)
        widgets.append(moreLink)
    #adds a label displaying the number of results
    global totalResults
    totalResults = min(numberDisplayed, len(item_List_Inner))
    global pageLabel
    pageLabel.config(text=f"{str(totalResults)} results")
    #adds the store choice menu to the footer
    storeChoiceFrame = tkinter.Frame(footerFrame, bg=secondBgCol, borderwidth=0)
    storeChoiceFrame.grid(row=0, column=0, sticky="nesw", padx=5, pady=5)
    storeChoiceFrame.rowconfigure(0, weight=1)
    storeChoiceFrame.rowconfigure(1, weight=1)
    storeChoiceFrame.columnconfigure(0, weight=1)
    storeChoiceFrame.columnconfigure(1, weight=1)
    storeChoiceFrame.columnconfigure(2, weight=1)
    storeChoiceFrame.columnconfigure(3, weight=1)
    storeChoiceFrame.columnconfigure(4, weight=1)
    #https://coderslegacy.com/python/list-of-tkinter-widgets/
    global storeChoice
    storeChoice = tkinter.StringVar()
    #https://www.pythontutorial.net/tkinter/tkinter-radio-button/
    storeChoices = [["Ocado","Ocado"], ["B & Q","B & Q"], ["M & S","Marks and Spencer"], ["JD Sports","JD Sports"], ["Original", "or"]]
    #create radio buttons
    for choice in range(0, len(storeChoices)):
        aRadioButton = tkinter.Radiobutton(storeChoiceFrame, text=storeChoices[choice][0], variable=storeChoice, value=storeChoices[choice][1], bg=secondBgCol, fg=fg2, font=MEDIUMFONT)
        aRadioButton.grid(row=0, column=choice, sticky="nesw")
    def selectStore():
        #get selected store
        global storeChoice, searchResults
        if storeChoice.get() != "":
            if storeChoice.get() == "or":
                searchResults.reinstateOriginal()
            else:
                searchResults.reinstateOriginal()
                #sort search results by the chosen shop
                searchResults.shop_only(storeChoice.get())
            clearresultframe()
            buildwidgetsframe(searchResults.outpt())
    storeChoiceSubmit = tkinter.Button(storeChoiceFrame, bg=fg2, fg=secondBgCol, font=MEDIUMFONT, text="Select", relief=tkinter.FLAT, command=selectStore)
    storeChoiceSubmit.grid(row=1, column=2, sticky="ns")
    #warn user if no results
    if len(item_List_Inner) == 0:
        noResultLabel = tkinter.Label(resultFrame, text="No results", font=MEDIUMBOLDFONT, fg=fg2, bg=mainBgCol)
        noResultLabel.grid(row=0, column=0, sticky="nesw", columnspan=2)
        widgets.append(noResultLabel)
    #append frames to "widgets" list so they can be grid_forget()ed
    widgets.append(storeChoiceFrame)

def basketNewOrLoad():
    #allows a signed in user to choose whether to view the current basket or open a saved one
    try:
        global signInBt
        signInBt.place_forget()
    except:
        pass
    clearresultframe()
    global canvas
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)
    #scroll to top
    try:
        global saveBt
        saveBt.place_forget()
    except:
        pass
    try:
        global filterBt
        filterBt.place_forget()
    except:
        pass
    global widgets, basket, username
    def newBasket():
        #open current basket
        loadingpage(basket, passTo="list")
    def loadBasket():
        #open choose basket popup
        load_basket_popup()
    if username != "guest":
        loadButton = tkinter.Button(resultFrame, text="Import a List", relief=tkinter.FLAT, fg="white", bg=fg2, font=LARGEBOLDFONT, command=loadBasket)
        loadButton.grid(column=0, row=0, sticky="nesw", padx=2, pady=2)
        widgets.append(loadButton)
    newButton = tkinter.Button(resultFrame, text="Current List", relief=tkinter.FLAT, fg="white", bg=fg2, font=LARGEBOLDFONT, command=newBasket)
    newButton.grid(column=1, row=0, sticky="nesw", padx=2, pady=2)
    widgets.append(newButton)

def clearresultframe():
    global widgets
    x = widgets
    widgets = []
    for item in x:
        item.grid_forget()

def clearandback():
    #go back to home screen
    global saveBt
    try:
        saveBt.place_forget()
    except:
        pass
    global searchEntry
    clearSearchEntry()
    searchEntry.insert(0, "Home")
    clearresultframe()
    welcomepage()

def clearSearchEntry(*args):
    #empty search bar
    global searchEntry
    searchEntry.delete(0, tkinter.END)

def filter_popup():
    #let user choose a sort method
    #https://stackoverflow.com/questions/16116876/tkinter-listbox-insert-error-invalid-command-name-50054760-50055432
    popup = tkinter.Toplevel(window)
    popup.title("Filter")
    popup.iconbitmap("./Images/M.ico")
    sortLb = tkinter.Label(popup, text="Sort By:", font=MEDIUMFONT)
    sortLb.pack()
    global sortBoxw, searchResults
    #https://coderslegacy.com/python/list-of-tkinter-widgets/#:~:text=Python%20Tkinter%20Widgets%3A%201%20Buttons%3A%20The%20Python%20Tkinter,Label%3A%20...%206%20Menu%3A%20...%207%20ComboBox%3A%20
    #list sort methods
    sortBoxw = tkinter.Listbox(popup, font=MEDIUMFONT)
    sortBoxw.pack()
    sortBoxw.insert(tkinter.END, "Original List")
    sortBoxw.insert(tkinter.END, "Price Low to High")
    sortBoxw.insert(tkinter.END, "Price High to Low")
    sortBoxw.insert(tkinter.END, "Alphabetical Shop")
    sortBoxw.insert(tkinter.END, "Rating Low to High")
    sortBoxw.insert(tkinter.END, "Rating High to Low")
    def go_sort():
        global searchResults
        #get chosen sort
        sortBoxValue = sortBoxw.get(sortBoxw.curselection())
        popup.destroy()
        #get list sorted by chosen sort
        if sortBoxValue == "Original List":
            searchResults.reinstateOriginal()
        elif sortBoxValue == "Price Low to High":
            searchResults.sort_price(True)
        elif sortBoxValue == "Price High to Low":
            searchResults.sort_price(False)
        elif sortBoxValue == "Rating Low to High":
            searchResults.sort_rating(True)
        elif sortBoxValue == "Rating High to Low":
            searchResults.sort_rating(False)
        elif sortBoxValue == "Alphabetical Shop":
            searchResults.alphabeticalShop()
        clearresultframe()
        #print(searchResults.outpt())
        buildwidgetsframe(searchResults.outpt())
    goSortBt = tkinter.Button(popup, text="Sort", command=go_sort, relief=tkinter.FLAT, bg="#19b6e2", fg="white", font=MEDIUMBOLDFONT)
    goSortBt.pack()

def error_popup(title, message):
    #display an error message in a pop-up
    #https://stackoverflow.com/questions/16116876/tkinter-listbox-insert-error-invalid-command-name-50054760-50055432
    errorPopupRoot = tkinter.Toplevel(window)
    errorPopupRoot.iconbitmap("./Images/M.ico")
    errorPopupRoot.title(title)
    errorPopupLb = tkinter.Label(errorPopupRoot, text=message, font=MEDIUMFONT)
    errorPopupLb.pack()
    def error_popup_exit():
        errorPopupRoot.destroy()
    errorPopupCloseBt = tkinter.Button(errorPopupRoot, text="Close", command=error_popup_exit, relief=tkinter.FLAT, bg="#19b6e2", fg="white", font=MEDIUMBOLDFONT)
    errorPopupCloseBt.pack()

def save_basket_popup():
    #let user name their list before save
    global basket, username
    #https://stackoverflow.com/questions/16116876/tkinter-listbox-insert-error-invalid-command-name-50054760-50055432
    popup = tkinter.Toplevel(window)
    popup.title("Save List")
    popup.iconbitmap("./Images/M.ico")
    savenameLb = tkinter.Label(popup, text="List name:", font=MEDIUMFONT)
    savenameLb.pack()
    savenameEntry = tkinter.Entry(popup, font=MEDIUMFONT, justify=tkinter.CENTER)
    savenameEntry.pack()
    def save_basket():
        #get chosen name and save list in their user area
        basketName = savenameEntry.get()
        #validate name
        #https://www.mtu.edu/umc/services/websites/writing/characters-avoid/
        #https://www.learndatasci.com/solutions/python-string-contains/#:~:text=The%20easiest%20and%20most%20effective,can't%20find%20the%20substring.
        if basketName == "" or basketName == " " or "#"in basketName or "<"in basketName or ">"in basketName or "$"in basketName or "+"in basketName or "%"in basketName or "€"in basketName or "`"in basketName or "*"in basketName or "'"in basketName or '"'in basketName or "|"in basketName or "{"in basketName or "}"in basketName or "?"in basketName or "="in basketName or "/"in basketName or ":"in basketName or ";"in basketName or "\\"in basketName or "@"in basketName or "¦"in basketName or basketName[0] == "!" or basketName[0] == " " or basketName[0] == "&":
            error_popup("Inappropriate Name", "The name may contain an inappropriate character. Please start the name with a letter or number.")
        #https://www.w3schools.com/python/python_file_handling.asp
        else:
            try:
                f = open("./Users/"+username+"/"+basketName+".txt", "wb")
            except FileNotFoundError:
                #https://www.geeksforgeeks.org/create-a-directory-in-python/
                os.mkdir("./Users/"+username+"/")
                f = open("./Users/"+username+"/"+basketName+".txt", "wb")
            for item in basket:
                for data in item:
                    f.write((data+"¬").encode("utf8"))
                f.write(("\n").encode("utf8"))
            f.close()
            popup.destroy()
    saveButton = tkinter.Button(popup, text="Save", command=save_basket, relief=tkinter.FLAT, bg=fg1, fg=mainBgCol, font=MEDIUMBOLDFONT)
    saveButton.pack()

def load_basket_popup():
    #let user choose a list to load in
    #https://stackoverflow.com/questions/16116876/tkinter-listbox-insert-error-invalid-command-name-50054760-50055432
    global basket, username
    popup = tkinter.Toplevel(window)
    popup.title("Load List")
    popup.iconbitmap("./Images/M.ico")
    loadnameLb = tkinter.Label(popup, text="List name:", font=MEDIUMFONT)
    loadnameLb.pack()
    #https://coderslegacy.com/python/list-of-tkinter-widgets/#:~:text=Python%20Tkinter%20Widgets%3A%201%20Buttons%3A%20The%20Python%20Tkinter,Label%3A%20...%206%20Menu%3A%20...%207%20ComboBox%3A%20
    loadnameBox = tkinter.Listbox(popup, font=MEDIUMFONT)
    loadnameBox.pack()
    #https://pynative.com/python-list-files-in-a-directory/#:~:text=How%20to%20List%20All%20Files%20of%20a%20Directory,function.%20...%204%20Use%20isfile%20%28%29%20function%20
    #list all availiable lists to open
    try:
        baskets = os.listdir("./Users/"+username+"/")
        for item in baskets:
            loadnameBox.insert(tkinter.END, item[:-4])
    except:
        error_popup("No Lists", "This account has no saved lists.")
    def load_basket():
        #open file...
        f = open("./Users/"+username+"/"+loadnameBox.get(loadnameBox.curselection())+".txt", "rb")
        data = f.read().decode("utf8")
        f.close()
        #... convert to list...
        data = data.split("\n")
        for item in range(0, len(data)):
            data[item] = data[item].strip("\n")
            data[item] = data[item].split("¬")
            data[item] = data[item][:-1]
        global basket
        goneNotice = False
        basket = []
        #... update price and rating data for each item...
        for item in data[:-1]:
            if item[3] == "Ocado":
                count = 0
                passThrough = False
                while count < 10 and passThrough == False:
                    try:
                        instUpdate = OcadoScraper.update(item)
                        item = instUpdate.outpt()
                        passThrough = True
                    except:
                        count = count + 1
                if count >= 10:
                    item = None
                    goneNotice = True
            elif item[3] == "B & Q":
                count = 0
                passThrough = False
                while count < 10 and passThrough == False:
                    try:
                        instUpdate = BqScraper.update(item)
                        item = instUpdate.outpt()
                        passThrough = True
                    except:
                        count = count + 1
                if count >= 10:
                    item = None
                    goneNotice = True
            elif item[3] == "JD Sports":
                count = 0
                passThrough = False
                while count < 10 and passThrough == False:
                    try:
                        instUpdate = JDScraper.update(item)
                        item = instUpdate.outpt()
                        passThrough = True
                    except:
                        count = count + 1
                if count >= 10:
                    item = None
                    goneNotice = True
            elif item[3] == "Marks and Spenser":
                count = 0
                passThrough = False
                while count < 10 and passThrough == False:
                    try:
                        instUpdate = MsScraper.update(item)
                        item = instUpdate.outpt()
                        passThrough = True
                    except:
                        count = count + 1
                if count >= 10:
                    item = None
                    goneNotice = True
            if item != None:
                basket.append(item)
        popup.destroy()
        if goneNotice == True:
            #if an item in the basket can no longer be found, display this error
            error_popup("Item Not Availiable", "An item in your list is no longer available.\nIt has been removed.")
        loadingpage(basket, passTo="list")
    replaceWarn = tkinter.Label(popup, text="Warning:\nThe current list will be replaced.", font=SMALLFONT)
    replaceWarn.pack()
    loadButton = tkinter.Button(popup, text="Load", command=load_basket, relief=tkinter.FLAT, bg=fg1, fg=mainBgCol, font=MEDIUMBOLDFONT)
    loadButton.pack()

def store_information_popup(store):
    #initialise the popup window
    popup = tkinter.Toplevel(window, bg=mainBgCol)
    popup.title("Store Information")
    popup.iconbitmap("./Images/M.ico")
    #load store info from file
    f = open("./Store Information/"+store+".txt")
    #get info from file
    info = f.read()
    f.close()
    info = info.split("\n")
    #button command procedure
    def open_webpage(page=info[1]):
        global popup
        wbopen(page)
        popup.destroy()
    #add the popup window's widgets
    storeImgFile = None
    if store == "ocado":
        storeImgFile = ocadoImage
    elif store == "ms":
        storeImgFile = msImage
    elif store == "bq":
        storeImgFile = bqImage
    elif store == "jd":
        storeImgFile = jdImage
    storeImg = tkinter.Label(popup, image=storeImgFile, bg=mainBgCol)
    storeImg.pack()
    #https://stackoverflow.com/questions/11949391/how-do-i-use-tkinter-to-create-line-wrapped-text-that-fills-the-width-of-the-win
    storeLabel = tkinter.Label(popup, text=info[2]+"\n"+info[3], fg=fg1, bg=mainBgCol, font=MEDIUMFONT, wraplength=500)
    storeLabel.pack()
    #button to open store's website
    openWebButton = tkinter.Button(popup, text="Open Website ⤤", command=open_webpage, relief=tkinter.FLAT, bg=fg1, fg=mainBgCol, font=MEDIUMBOLDFONT)
    openWebButton.pack()

window_setup()
root.mainloop()
