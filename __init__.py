import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
import speech_recognition as sr
import time
import pyttsx3
import webbrowser
import os

StartupInfo = '<head><style>body {background-color: white;}</style></head><center><img src="https://raw.githubusercontent.com/777irug/google-assistant/main/homepage.gif" height="300"></center>'
IconLibrary = os.getcwd()
ApplicationLogo = os.getcwd() + "/VisualElements_512.svg"

Voice = pyttsx3.init()
voices = Voice.getProperty('voices') 
Voice.setProperty('voice', voices[1].id) 
Voice.setProperty("rate", 150)
Voice.runAndWait()

class GoogleAssistant(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Assistant")
        self.setWindowIcon(QIcon(ApplicationLogo))
        self.setFixedHeight(450)
        self.setFixedWidth(1000)
        self.setWindowFlags(Qt.CustomizeWindowHint)

        self.ToolBar = QToolBar()
        self.ToolBar.setStyleSheet("background-color : white; color : black")
        self.ToolBar.setMovable(False)
        self.addToolBar(Qt.BottomToolBarArea ,self.ToolBar)

        self.WakeUp = QAction(QIcon(IconLibrary + "/wakeup_btn.png"), "Hey Google", self)
        self.WakeUp.triggered.connect(self.WakeUp)
        self.ToolBar.addAction(self.WakeUp)

        self.userinput = QLineEdit()
        self.userinput.setStyleSheet("background-color : None; color : black; border-radius : 5")
        self.ToolBar.addWidget(self.userinput)

        self.search_btn = QAction(QIcon(IconLibrary + "/search.png"), "Search", self)
        self.search_btn.triggered.connect(self.GSrch)
        self.ToolBar.addAction(self.search_btn)

        self.ChromiumEngine = QWebEngineView()
        self.ChromiumEngine.setHtml(StartupInfo)
        self.setCentralWidget(self.ChromiumEngine)

        self.show()

    def WakeUp(self):
        try:
            listener = sr.Recognizer()
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source)
                InputFromUser = listener.listen(source, None, 10)
                command = listener.recognize_google(InputFromUser)
                KeywordChecker = command.lower()
                if "hey google" in KeywordChecker:
                    KeywordChecker = KeywordChecker.replace("hey google ", "")
                    
                    if "time" in KeywordChecker:
                        Time = time.strftime("%H:%M %p")
                        TimeSpeak = time.strftime("%H %M %p")
                        ResultHTML = """
                        <center>
                        <img src="https://raw.githubusercontent.com/777irug/google-assistant/main/homepage.gif"><br><br>
                        </center>
                        <hr>
                        <h2 style="color:DodgerBlue;font-family:calibri">""" + command + """</h2>
                        <h1 style="color:DodgerBlack;font-family:Arial">""" + Time + """</h1>
                        """
                        self.ChromiumEngine.setHtml(ResultHTML)
                        Output = "the time is currently" + TimeSpeak
                        pyttsx3.speak(Output)
                                    
                    elif "date" in KeywordChecker:
                        Date = time.asctime()
                        pyttsx3.speak(Date)
                        ResultHTML = """
                        <center>
                        <img src="https://raw.githubusercontent.com/777irug/google-assistant/main/homepage.gif"><br><br>
                        </center>
                        <hr>
                        <h2 style="color:DodgerBlue;font-family:calibri">""" + command + """</h2>
                        <h1 style="color:DodgerBlack;font-family:Arial">""" + Date + """</h1>
                        """
                        self.ChromiumEngine.setHtml(ResultHTML)
                                
                    else:
                        pyttsx3.speak("Sorry about That, Please Say That again!")
        
        except Exception as e:
            print(e)
            pyttsx3.speak("Something went wrong, please check that you're connected to network!")

    def GSrch(self):
        Query = self.userinput.text()
        GoogleSearchEngineQuery = "https://www.google.com/search?q=" + Query
        webbrowser.open(GoogleSearchEngineQuery)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GoogleAssistant()
    sys.exit(app.exec_())
