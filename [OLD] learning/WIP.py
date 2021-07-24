#!/usr/bin/python

import sys
from PyQt5.QtCore import (Qt, QBasicTimer, pyqtSignal)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QDesktopWidget,
                             QApplication, QTextEdit, QGridLayout,
                             QAction)
from PyQt5.QtGui import (QFont, QTextDocument)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Setup Script area
        self.scriptWid = ScriptWidget(self)
        self.setCentralWidget(self.scriptWid)

        # Bars
        self.statusbar = self.statusBar()
        self.menubar = self.menuBar()

        # Window sizing
        self.resize(380, 380)
        self.center()
        self.setWindowTitle('Script Editor WIP')
        self.show()

        ### Debug UI ###
        debug = self.menubar.addMenu("Debug")
        # Count text blocks
        txtBlkCountAct = QAction('Count Blocks', self)
        txtBlkCountAct.triggered.connect(self.countBlocks)
        debug.addAction(txtBlkCountAct)
        # Change format
        changeformatAct = QAction('Change Format', self)
        changeformatAct.triggered.connect(self.scriptWid.changeBlockFormat)
        changeformatAct.setShortcut('Shift+Tab')
        debug.addAction(changeformatAct)
        

    def countBlocks(self):
        print(self.scriptWid.scriptDoc.blockCount())

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))


class ScriptWidget(QWidget):
    # Fonts
    characterFont = QFont("Courier")
    characterFont.setCapitalization(QFont.AllUppercase)
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initEditUI()

    def initEditUI(self):
        self.scriptEdit = QTextEdit()
        self.scriptDoc = QTextDocument()
        self.scriptDoc.setDefaultFont(QFont("Courier"))
        self.scriptEdit.setDocument(self.scriptDoc)
        
        # Widget Layout
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.scriptEdit, 0, 0)
        self.setLayout(grid)
        self.show()

    def changeBlockFormat(sself):
        print("start changing block format")
        # Character font
        self.scriptEdit.setCurrentFont(QFont("Times"))

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
