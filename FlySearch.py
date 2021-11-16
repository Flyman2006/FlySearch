# importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineCore import*
import os
import sys

# main window
class MainWindow(QMainWindow):

        # constructor
        global searchm
        searchm = 'http://search.brave.com'
        global searchm_s
        searchm_s = 'https://search.brave.com/search?q='
        global maschine
        maschine = 'brave'
        def __init__(self, *args, **kwargs):
                super(MainWindow, self).__init__(*args, **kwargs)
                self.resize(1200, 800)
                self.setWindowIcon(QIcon('icons/icon.png'))
                # creating a tab widget
                self.tabs = QTabWidget()
                # making document mode true
                self.tabs.setDocumentMode(True)

                # adding action when double clicked
                self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

                # adding action when tab is changed
                self.tabs.currentChanged.connect(self.current_tab_changed)

                # making tabs closeable
                self.tabs.setTabsClosable(True)

                # adding action when tab close is requested
                self.tabs.tabCloseRequested.connect(self.close_current_tab)

                # making tabs as central widget
                self.setCentralWidget(self.tabs)

                # creating a status bar
                self.status = QStatusBar()

                # setting status bar to the main window
                self.setStatusBar(self.status)

                # creating a tool bar for navigation
                navtb = QToolBar("Navigation")

                # adding tool bar tot he main window
                self.addToolBar(navtb)

                # creating back action
                back_btn = QAction(QIcon("icons/backward.png"),"Back to previous page", self)

                # setting status tip

                # adding action to back button
                # making current tab to go back
                back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

                # adding this to the navigation tool bar
                navtb.addAction(back_btn)

                # similarly adding next button
                next_btn = QAction(QIcon("icons/forward.png"),"Forward to next page", self)
                next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
                navtb.addAction(next_btn)

                # similarly adding reload button
                reload_btn = QAction(QIcon("icons/reload.png"),"Reload page", self)
                reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
                navtb.addAction(reload_btn)

                # creating home action
                home_btn = QAction(QIcon("icons/home.png"),"Start Page", self)          # adding action to home button
                home_btn.triggered.connect(self.navigate_home)
                navtb.addAction(home_btn)

                # adding a separator
                mini_map = QAction(' ', self)
                navtb.addAction(mini_map)

                # creating a line edit widget for URL
                self.urlbar = QLineEdit()

                # adding action to line edit when return key is pressed
                self.urlbar.returnPressed.connect(self.navigate_to_url)

                # adding line edit to tool bar
                navtb.addWidget(self.urlbar)
                mini_map2 = QAction(' ', self)
                navtb.addAction(mini_map2)
                self.tabs.setStyleSheet('width = 150px')

                # similarly adding stop action
                global maschine
                self.search_menu = QAction(maschine)
                navtb.addAction(self.search_menu)
                self.search_menu.triggered.connect(self.change_browser)

                # creating first tab
                global searchm
                self.add_new_tab(QUrl(searchm), 'Homepage')

                # showing all the components
                self.show()

                # setting window title
                self.setWindowTitle("FlySearch")
        # method for adding new tab
        def add_new_tab(self, qurl = None, label ="Blank"):

                # if url is blank
                if qurl is None:
                        # creating a google url
                        global searchm
                        qurl = QUrl(searchm)

                # creating a QWebEngineView object
                browser = QWebEngineView()

                # setting url to browser
                browser.setUrl(qurl)

                # setting tab index
                i = self.tabs.addTab(browser, label)
                self.tabs.setCurrentIndex(i)

                # adding action to the browser when url is changed
                # update the url
                browser.urlChanged.connect(lambda qurl, browser = browser:
                                                                self.update_urlbar(qurl, browser))

                # adding action to the browser when loading is finished
                # set the tab title
                browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                                                        self.tabs.setTabText(i, browser.page().title()))

        # when double clicked is pressed on tabs
        def tab_open_doubleclick(self, i):

                # checking index i.e
                # No tab under the click
                if i == -1:
                        # creating a new tab
                        self.add_new_tab()

        # wen tab is changed
        def current_tab_changed(self, i):

                # get the curl
                qurl = self.tabs.currentWidget().url()

                # update the url
                self.update_urlbar(qurl, self.tabs.currentWidget())

                # update the title
                self.update_title(self.tabs.currentWidget())

        # when tab is closed
        def close_current_tab(self, i):

                # if there is only one tab
                if self.tabs.count() < 2:
                        # do nothing
                        return

                # else remove the tab
                self.tabs.removeTab(i)

        # method for updating the title
        def update_title(self, browser):

                # if signal is not from the current tab
                if browser != self.tabs.currentWidget():
                        # do nothing
                        return

                # get the page title
                title = self.tabs.currentWidget().page().title()

                # set the window title
                self.setWindowTitle(title)

        # action to go to home
        def navigate_home(self):

                # go to google
                global searchm
                self.tabs.currentWidget().setUrl(QUrl(searchm))

        # method for navigate to url
        def navigate_to_url(self):
                # get the line edit text
                # convert it to QUrl object
                qs = QUrl(self.urlbar.text())
                qm = self.urlbar.text()
                if qm[0:3] != 'www':
                        global searchm_s
                        l = searchm_s + qm
                        qs = QUrl(l)
                        # set the url
                else:
                        if qs.scheme() == "":
                                qs.setScheme("http")

                # set the url
                self.tabs.currentWidget().setUrl(qs)
        def update_urlbar(self, q, browser = None):

                # If this signal is not from the current tab, ignore
                if browser != self.tabs.currentWidget():

                        return

                # set text to the url bar
                self.urlbar.setText(q.toString())

                # set cursor position
                self.urlbar.setCursorPosition(0)
        def change_browser(self):
                global searchm
                global searchm_s
                global maschine
                if maschine == 'google':
                        searchm = 'http://search.brave.com'
                        maschine = 'brave'
                        searchm_s = 'https://search.brave.com/search?q='
                else:
                        searchm = 'http://www.google.com'
                        searchm_s = 'https://www.google.com/search?q='
                        maschine = 'google'
                self.search_menu.setText(maschine)
sh = open("icons/style.txt")
stylesheet = sh.read()

# creating a PyQt5 application
app = QApplication(sys.argv)
# setting name to the application
app.setApplicationName("FlySearch")
app.setStyleSheet(stylesheet)
# creating MainWindow object
window = MainWindow()

# loop
app.exec_()

