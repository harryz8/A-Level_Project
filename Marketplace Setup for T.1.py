import tkinter
import turtle
import os

#variables
MEDIUMFONT = ("Verdana", "14")
count = 1

#setup tk window
window = tkinter.Tk()
window.title("Marketplace Setup")
window.config(bg="white")

titleLb = tkinter.Label(window, text="Marketplace", bg="white", fg="#19b6e2", font=("Verdana", "96", "bold"))
titleLb.pack()
commentLb = tkinter.Label(window, text="Setup in progress...", fg="#19b6e2", bg="white", font=MEDIUMFONT)
commentLb.pack()
#https://stackoverflow.com/questions/54246872/how-to-combine-tkinter-and-turtle
#https://vegibit.com/change-pen-color-in-python-turtle/
#create turtle and place on canvas
loadingBarCanvas = tkinter.Canvas(window, width=800, height=20)
loadingBarSprite = turtle.RawTurtle(loadingBarCanvas)
loadingBarCanvas.pack()
loadingBarSprite.color("#19b6e2")
loadingBarSprite.width(20)
loadingBarSprite.hideturtle()
loadingBarSprite.penup()
loadingBarSprite.backward(400)
loadingBarSprite.pendown()
loadingBarSprite.forward(100)
def nextAction():
    #every 10ms do:
    global loadingBarSprite, count
    #move turtle to draw loading bar
    loadingBarSprite.forward(10)
    if count >= 80:
        window.destroy()
    elif count == 10:
        #https://datatofish.com/command-prompt-python/
        #https://stackoverflow.com/questions/16727941/how-do-i-execute-cmd-commands-through-a-batch-file
        #https://www.shellhacks.com/batch-file-comment-remark-windows/#:~:text=A%20batch%20file%20can%20be%20commented%20using%20either%20two%20colons,%2C%20won%27t%20be%20printed.
        #install required modules using the command prompt and pip
        os.system("cmd /c python -m pip install requests")
        os.system("cmd /c python -m pip install beautifulsoup4")
        os.system("cmd /c python -m pip install pillow")
    elif count == 20:
        #create folders
        os.mkdir("./Images")
        os.mkdir("./Users")
        os.mkdir("./Modules")
        os.mkdir("./Setup")
        os.mkdir("./Store Information")
    elif count == 30:
        #move files to the right folders
        os.rename("./home.png", "./Images/home.png")
        os.rename("./logo.png", "./Images/logo.png")
        os.rename("./ResultsObject.py", "./Modules/ResultsObject.py")
        os.rename("./bq.txt", "./Store Information/bq.txt")
    elif count == 40:
        os.rename("./add_to_list.png", "./Images/add_to_list.png")
        os.rename("./list.png", "./Images/list.png")
        os.rename("./bq_logo.png", "./Images/bq_logo.png")
        os.rename("./filter.png", "./Images/filter.png")
        os.rename("./jd_logo.png", "./Images/jd_logo.png")
    elif count == 50:
        os.rename("./M.ico", "./Images/M.ico")
        os.rename("./ms_logo.png", "./Images/ms_logo.png")
        os.rename("./ocado_logo.png", "./Images/ocado_logo.png")
        os.rename("./save.png", "./Images/save.png")
        os.rename("./search.png", "./Images/search.png")
    elif count == 60:
        os.rename("./No Image.png", "./Images/No Image.png")
        os.rename("./BqScraper.py", "./Modules/BqScraper.py")
        os.rename("./JDScraper.py", "./Modules/JDScraper.py")
        os.rename("./MsScraper.py", "./Modules/MsScraper.py")
        os.rename("./OcadoScraper.py", "./Modules/OcadoScraper.py")
    elif count == 70:
        os.rename("./jd.txt", "./Store Information/jd.txt")
        os.rename("./ms.txt", "./Store Information/ms.txt")
        os.rename("./ocado.txt", "./Store Information/ocado.txt")
        os.rename("./Marketplace Setup for T.1.py","./Setup/Marketplace Setup for T.1.py")
    if count != 80:
        count = count + 1
        window.after(10, nextAction)

window.after(10, nextAction)
window.mainloop()
