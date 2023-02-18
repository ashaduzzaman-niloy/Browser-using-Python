# IMPORTS
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# WEB ENGINE( pip install PyQtWebEngine)
from PyQt5.QtWebEngineWidgets import *

# MAIN WINDOW
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # ADD WINDOW ELEMENTS
        # ADD TAB WIGDETS TO DISPLAY WEB TABS
        self.showMaximized()
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # ADD DOUBLE CLICK EVENT LISTENER
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        # ADD TAB CLOSE EVENT LISTENER
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        # ADD ACTIVE TAB CHANGE EVENT LISTENER
        self.tabs.currentChanged.connect(self.current_tab_changed)


        # ADD NAVIGATION TOOLBAR
        navtb = QToolBar("Navigation")
        #navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        # ADD BUTTONS TO NAVIGATION TOOLBAR
        # HOME PAGE BUTTON
        home_btn = QAction("Home", self)
        navtb.addAction(home_btn)
        # NAVIGATE TO DEFAULT HOME PAGE
        home_btn.triggered.connect(self.navigate_home)

        # NEW TAB BUTTON
        newtab_btn = QAction("+", self)
        navtb.addAction(newtab_btn)
        # NAVIGATE TO DEFAULT HOME PAGE
        newtab_btn.triggered.connect(lambda _: self.add_new_tab())

        # RELOAD WEB PAGE BUTTON
        reload_btn = QAction("Reload", self)
        navtb.addAction(reload_btn)
        # RELOAD WEB PAGE
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        
        # PREVIOUS WEB PAGE BUTTON
        back_btn = QAction("Back", self) 
        navtb.addAction(back_btn)
        # NAVIGATE TO PREVIOUS PAGE
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        
        # ADD LABEL ICON TO SHOW THE SECURITY STATUS OF THE LOADED URL
        self.httpsicon = QLabel()  
        self.httpsicon.setPixmap(QPixmap())
        #navtb.addWidget(self.httpsicon)

        # ADD LINE EDIT TO SHOW AND EDIT URLS
        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)
        # LOAD URL WHEN ENTER BUTTON IS PRESSED
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # ADD STOP BUTTON TO STOP URL LOADING
        stop_btn = QAction("Stop", self)
        navtb.addAction(stop_btn)
        # STOP URL LOADING
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())

        # NEXT WEB PAGE BUTTON
        next_btn = QAction("Forward", self)
        navtb.addAction(next_btn)
        # NAVIGATE TO NEXT WEB PAGE
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())


        # ADD STYLESHEET TO CUSTOMIZE YOUR WINDOWS
        # STYLESHEET (DARK MODE)
        self.setStyleSheet("""
        QWidget{
           background-color: rgb(255, 255, 255);
           border: 0ex;
        }
        QTabWidget::pane {
            border: 0px;
            position: top;
            color: rgb(255, 255, 255);
            padding: 0px;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }
        
        QToolBar {
            border: 0px;
        }
        
        Qlabel, QToolButton {
            background: rgb(255, 255, 255);
            border: 0px solid rgb(90, 90, 90);
            border-radius: 0px;
            min-width: 0ex;
            padding: 2ex;
            margin-right: 0px;
            color: rgb(0, 0, 0);
        }

        QLabel:hover, QToolButton::hover, QTabBar::tab:hover {
            background-color: rgb(162, 228, 184);
            color: rgb(0, 0, 0);
        }
        
        QTabBar::tab {
            background-color: rgb(255, 255, 255);
            padding: 2ex;
            color: rgb(0, 0, 0);
        }
        
        QTabBar::tab:selected {
            background-color: rgb(255, 255, 255);
            padding: 2ex;
            color: rgb(0, 0, 0);
        }

        QLineEdit {
            border: 0ex solid rgb(35, 35, 35);
            border-radius: 0ex;
            padding: 2ex;
            background-color: rgb(255, 255, 255);
            color: rgb(0, 0, 0);
        }
        QLineEdit:hover {
            background-color: rgb(162, 228, 184);
        }

        QPushButton{
            background: rgb(255, 255, 255);
            border: 0px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
            padding: 0px;
            border-radius: 0px;
        }""")



        # LOAD DEFAULT HOME PAGE (GOOLE.COM)
        #url = http://www.google.com,
        #label = Homepage
        self.add_new_tab(QUrl('http://'), 'Homepage')

        # SHOW MAIN WINDOW
        self.show()

    # ############################################
    # FUNCTIONS
    ##############################################
    # ADD NEW WEB TAB
    def add_new_tab(self, qurl=None, label="Blank"):
        # Check if url value is blank
        if qurl is None:
            qurl = QUrl('http://')#pass empty string to url

        # Load the passed url
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # ADD THE WEB PAGE TAB
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # ADD BROWSER EVENT LISTENERS
        # On URL change
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        # On loadfinished
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))


    # ADD NEW TAB ON DOUBLE CLICK ON TABS
    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    # CLOSE TABS 
    def close_current_tab(self, i):
        if self.tabs.count() < 2: #Only close if there is more than one tab open
            return

        self.tabs.removeTab(i)


    # UPDATE URL TEXT WHEN ACTIVE TAB IS CHANGED
    def update_urlbar(self, q, browser=None):
        #q = QURL
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return
        # URL Schema
        if q.scheme() == 'https':
            # If schema is https change icon to locked padlock to show that the webpage is secure
            self.httpsicon.setPixmap(QPixmap())

        else:
            # If schema is not https change icon to locked padlock to show that the webpage is unsecure
            self.httpsicon.setPixmap(QPixmap())

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)



    # ACTIVE TAB CHANGE ACTIONS
    def current_tab_changed(self, i):
        # i = tab index
        # GET CURRENT TAB URL
        qurl = self.tabs.currentWidget().url()
        # UPDATE URL TEXT
        self.update_urlbar(qurl, self.tabs.currentWidget())
        # UPDATE WINDOWS TITTLE
        self.update_title(self.tabs.currentWidget())


    # UPDATE WINDOWS TITTLE
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current ACTIVE tab, ignore
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)


    # NAVIGATE TO PASSED URL
    def navigate_to_url(self):  # Does not receive the Url
        # GET URL TEXT
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            # pass http as default url schema
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)


    # NAVIGATE TO DEFAULT HOME PAGE
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://"))


app = QApplication(sys.argv)
# APPLICATION NAME
app.setApplicationName("Browser")


window = MainWindow()
app.exec_()