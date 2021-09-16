import sys
from enum import Enum
from PyQt5 import (QtGui, QtCore)
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextEdit, QAction,
                             QFileDialog, QDialog, QFontComboBox, QComboBox,
                             QColorDialog, QGridLayout,
                             QHBoxLayout, QLabel, QWidget,  # Layout
                             QUndoStack, QUndoCommand,     # Undo
                             QCompleter, QLineEdit, QPushButton,     # character menu
                             QCheckBox  # header menu
                             )
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtGui import (QTextListFormat, QFont, QTextCursor,
                         QTextCharFormat, QTextBlockFormat, 
                         QKeySequence  # Shortcuts
                         )  

class Main(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self,parent)
        
        self.undoStack = QUndoStack()
        
        self.setMinimumWidth(1000)
        self.filename = ""
        self.prevFormatState = FormatState.Action
        self.currFormatState = FormatState.Action
        
        self.setFontFormats()
        self.setBlockFormats()
        self.initUI()
        
        # Set starting format
        self.setStartingFormat()
 
    def initUI(self):
        # Initialising main widgets
        self.scriptEdit = CompletionTextEdit()
        # Initialise character menu
        self.initCharMenu()
        # Initialise header menu
        self.initHeaderMenu()
        
        # scriptEdit formatting
        self.scriptEdit.setStyleSheet("""
            QTextEdit {
                font: 12pt "Courier";
            }
        """)
        self.scriptEdit.setMaximumWidth(660)
        self.detectionEnabled = True
        self.scriptEdit.cursorPositionChanged.connect(self.detectFormat)         
        # Setting/Adding toolbars
        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()
        self.statusbar = self.statusBar()
        
        # Layout
        layoutWidget = QWidget()        
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(self.headerMenuGrid)
        mainLayout.addWidget(self.scriptEdit)
        mainLayout.addLayout(self.charMenuGrid)
        layoutWidget.setLayout(mainLayout)
        self.setCentralWidget(layoutWidget)
                
        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,1000,800) 
        self.setWindowTitle("Writer")

    def initToolbar(self):
        # New
        self.newAction = QAction(QtGui.QIcon("icons/new.png"),"New",self)
        self.newAction.setStatusTip("Create a new script.")
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.new)

        # Open
        self.openAction = QAction(QtGui.QIcon("icons/open.png"),"Open file",self)
        self.openAction.setStatusTip("Open existing script")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        # Save
        self.saveAction = QAction(QtGui.QIcon("icons/save.png"),"Save",self)
        self.saveAction.setStatusTip("Save script")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)
        
        # Print
        self.printAction = QAction(QtGui.QIcon("icons/print.png"),"Print script",self)
        self.printAction.setStatusTip("Print script")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.print)
        
        # Print Preview
        self.previewAction = QAction(QtGui.QIcon("icons/preview.png"),"Print preview",self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)
        
        # Cut
        self.cutAction = QAction(QtGui.QIcon("icons/cut.png"),"Cut to clipboard",self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.scriptEdit.cut)
        
        # Copy
        self.copyAction = QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.scriptEdit.copy)
        
        # Paste
        self.pasteAction = QAction(QtGui.QIcon("icons/paste.png"),"Paste from clipboard",self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.scriptEdit.paste)
        
        # Undo
        self.undoAction = QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.undoStack.undo)
        
        # Redo
        self.redoAction = QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.undoStack.redo)
        
        # Bullet List [TO REMOVE]
        bulletAction = QAction(QtGui.QIcon("icons/bullet.png"),"Insert bullet List",self)
        bulletAction.setStatusTip("Insert bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList) 
        
        # Number List [TO REMOVE]
        numberedAction = QAction(QtGui.QIcon("icons/number.png"),"Insert numbered List",self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addSeparator()
        
        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)
        self.toolbar.addSeparator()
        
        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        self.toolbar.addSeparator()
        
        self.toolbar.addAction(bulletAction)
        self.toolbar.addAction(numberedAction)
        self.toolbar.addSeparator()

      # Makes the next toolbar appear underneath this one
        self.addToolBarBreak()

    def initFormatbar(self):        
        # Color control
        fontColor = QAction(QtGui.QIcon("icons/font-color.png"),"Change font color",self)
        fontColor.triggered.connect(self.fontColor)
        backColor = QAction(QtGui.QIcon("icons/highlight.png"),"Change background color",self)
        backColor.triggered.connect(self.highlight)
        
        # Action
        self.actionFormatAction = QAction("Action",self)
        self.actionFormatAction.setCheckable(True)
        self.actionFormatAction.triggered.connect(lambda: self.changeFormatTo(FormatState.Action))
        self.actionFormatAction.setShortcut("Alt+1")
        # Character
        self.characterFormatAction = QAction("Character",self)
        self.characterFormatAction.setCheckable(True)
        self.characterFormatAction.triggered.connect(lambda: self.changeFormatTo(FormatState.Character))
        self.characterFormatAction.setShortcut("Alt+2")
        # Dialogue
        self.dialogueFormatAction = QAction("Dialogue",self)
        self.dialogueFormatAction.setCheckable(True)
        self.dialogueFormatAction.triggered.connect(lambda: self.changeFormatTo(FormatState.Dialogue))
        self.dialogueFormatAction.setShortcut("Alt+3")
        # Paranthesis
        self.paranthesisFormatAction = QAction("Paranthesis",self)
        self.paranthesisFormatAction.setCheckable(True)
        self.paranthesisFormatAction.triggered.connect(lambda: self.changeFormatTo(FormatState.Paranthesis))
        self.paranthesisFormatAction.setShortcut("Alt+4")
        # Heading
        self.headingFormatAction = QAction("Heading",self)
        self.headingFormatAction.setCheckable(True)
        self.headingFormatAction.triggered.connect(lambda: self.changeFormatTo(FormatState.Heading))
        self.headingFormatAction.setShortcut("Alt+5")
        # Transition
        self.transitionFormatAction = QAction("Transition",self)
        self.transitionFormatAction.setCheckable(True)
        self.transitionFormatAction.triggered.connect(lambda: self.changeFormatTo(FormatState.Transition))
        self.transitionFormatAction.setShortcut("Alt+6")
        # Change Styles
        self.changeStyleAction = QAction("Change Style",self)
        self.changeStyleAction.setEnabled(True)
        self.changeStyleAction.triggered.connect(self.changeStyle)
        self.changeStyleAction.setShortcut("Alt+`")
        # Custom New Line Style Change Shortcut
        self.customNewLineStyleAction = QAction("New Line Style",self)
        self.customNewLineStyleAction.setEnabled(True)
        self.customNewLineStyleAction.triggered.connect(self.customNewLineStyle)
        seq = QKeySequence(Qt.ALT+Qt.Key_Return)
        self.customNewLineStyleAction.setShortcut(seq)
        # Auto format toggle
        self.autoFormatOnLineChange = False
        self.autoFormatAction = QAction("Auto-Format",self)
        self.autoFormatAction.setCheckable(True)
        self.autoFormatAction.setChecked(self.autoFormatOnLineChange)
        self.autoFormatAction.triggered.connect(self.setAutoFormat)
        
        # Bold
        boldAction = QAction(QtGui.QIcon("icons/bold.png"),"Bold",self)
        boldAction.triggered.connect(self.bold)
        # Italics
        italicAction = QAction(QtGui.QIcon("icons/italic.png"),"Italic",self)
        italicAction.triggered.connect(self.italic)
        # Underline
        underlAction = QAction(QtGui.QIcon("icons/underline.png"),"Underline",self)
        underlAction.triggered.connect(self.underline)
        # Strike-through
        strikeAction = QAction(QtGui.QIcon("icons/strike.png"),"Strike-out",self)
        strikeAction.triggered.connect(self.strike)
        strikeAction.setShortcut("Ctrl+Shift+S")
        # Superscript
        superAction = QAction(QtGui.QIcon("icons/superscript.png"),"Superscript",self)
        superAction.triggered.connect(self.superScript)
        # Subscript
        subAction = QAction(QtGui.QIcon("icons/subscript.png"),"Subscript",self)
        subAction.triggered.connect(self.subScript) 
        
        # Align Left
        alignLeft = QAction(QtGui.QIcon("icons/align-left.png"),"Align left",self)
        alignLeft.triggered.connect(self.alignLeft)
        # Align Center
        alignCenter = QAction(QtGui.QIcon("icons/align-center.png"),"Align center",self)
        alignCenter.triggered.connect(self.alignCenter)
        # Align Right
        alignRight = QAction(QtGui.QIcon("icons/align-right.png"),"Align right",self)
        alignRight.triggered.connect(self.alignRight)
        
        self.formatbar = self.addToolBar("Format")
        
        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)
        self.formatbar.addSeparator()
        
        self.formatbar.addAction(self.actionFormatAction)
        self.formatbar.addAction(self.characterFormatAction)
        self.formatbar.addAction(self.dialogueFormatAction)
        self.formatbar.addAction(self.paranthesisFormatAction)
        self.formatbar.addAction(self.headingFormatAction)
        self.formatbar.addAction(self.transitionFormatAction)
        self.addAction(self.changeStyleAction)       # added this way to keep it hidden
        self.addAction(self.customNewLineStyleAction)       # added this way to keep it hidden
        self.formatbar.addSeparator()
        
        self.formatbar.addAction(self.autoFormatAction)
        self.formatbar.addSeparator()
        
        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)
        self.formatbar.addSeparator()
        
        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addSeparator()

    def initMenubar(self):
        menubar = self.menuBar()
        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")
        
        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.printAction)
        file.addAction(self.previewAction)
        
        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)
       
    ### CHARACATER MENU SECTION START ###
    ### - includes autocompletion code 
       
    def initCharMenu(self):
        # Default characterlist
        self.characterList = ["ALEX", "CHARLIE", "FRANKIE", "JESSIE"]
        
        # Adding autocompleter
        completer = QCompleter(self.characterList, None)
        self.scriptEdit.setCompleter(completer)
        
        # Header
        self.charListTitle = QLabel('Characters')
        self.charListButtonTitle = QLabel('+/-')
        self.newCharacterEdit = QLineEdit()
        
        # Add characters button
        self.addCharacterButton = QPushButton('+', self)
        self.addCharacterButton.clicked.connect(self.addCharacter)
        
        # Character list container
        self.characterListContainer = QGridLayout()
        self.characterListContainer.setSpacing(2)
        
        # Sizing
        self.charListTitle.setMaximumHeight(25)
        self.charListButtonTitle.setMaximumWidth(25)
        self.charListButtonTitle.setMaximumHeight(25)
        self.addCharacterButton.setMaximumWidth(25)
        self.addCharacterButton.setMaximumHeight(25)
        self.charMenuGrid = QGridLayout()
        self.charMenuGrid.setSpacing(2)
        
        # Build main charMenuGrid
        self.charMenuGrid.addWidget(self.charListTitle,             0, 0, 1, 4)
        self.charMenuGrid.addWidget(self.charListButtonTitle,       0, 4)
        self.charMenuGrid.addWidget(self.newCharacterEdit,          1, 0, 1, 4)
        self.charMenuGrid.addWidget(self.addCharacterButton,        1, 4)
        self.charMenuGrid.addLayout(self.characterListContainer,    2, 0, 1, 5)
        
        # Populate charactert 
        self.setCharacterList() 
        
    def setCharacterList(self):
        # Remove old charMenuGrid
        rowCount = self.characterListContainer.rowCount()
        colCount = self.characterListContainer.columnCount()
        
        for i in range(rowCount):
            for j in range(colCount):
                if self.characterListContainer.itemAtPosition(i, j) is not None:
                    self.characterListContainer.itemAtPosition(i, j).widget().setParent(None)
        
        counter = 0
        if (len(self.characterList) == 0):
            noTitle = QLabel('None')
            noTitle.setMaximumHeight(25)
            self.characterListContainer.addWidget(noTitle, counter, 0, 1, 4)
            counter = counter + 1
        else:
            for character in self.characterList:
                charTitle = QLabel(character)
                charTitle.setMaximumHeight(25)
                
                remButton = QPushButton('-', self)
                remButton.clicked.connect(lambda ignore, a=character : self.removeCharacter(a))
                remButton.setMaximumWidth(25)
                remButton.setMaximumHeight(25)
                
                self.characterListContainer.addWidget(charTitle, counter, 0, 1, 4)
                self.characterListContainer.addWidget(remButton, counter, 4)
                counter = counter + 1
        
        bottomSpace = QLabel(' ')
        self.characterListContainer.addWidget(bottomSpace, counter, 0, 1, 5, Qt.AlignBottom)
        
    def addCharacter(self):
        self.characterList.append(self.newCharacterEdit.text().upper())
        
        # Update autocompleter
        completer = QCompleter(self.characterList, None)
        self.scriptEdit.setCompleter(completer)
        
        # Update displayed list
        self.setCharacterList()
        
    def removeCharacter(self, charName):
        self.characterList.remove(charName)
        
        # Update autocompleter
        completer = QCompleter(self.characterList, None)
        self.scriptEdit.setCompleter(completer)
        
        # Update displayed list
        self.setCharacterList()
        
    ### CHARACATER MENU SECTION END ###
    
    ### HEADER MENU SECTION START ###
        
    def initHeaderMenu(self):
        # Script Title
        self.scriptTitle = QLabel('Title')
        self.scriptTitleEdit = QLineEdit()
        self.scriptTitleCheck = QCheckBox()
        self.scriptTitleCheck.setCheckState(Qt.Checked)
    
        # Author
        self.authorTitle = QLabel('Author')
        self.authorTitleEdit = QLineEdit()
        self.authorTitleCheck = QCheckBox()
        self.authorTitleCheck.setCheckState(Qt.Checked)
        
        # Author
        self.characterListTitle = QLabel('Character List')
        self.characterListTitleCheck = QCheckBox()
        self.characterListTitleCheck.setCheckState(Qt.Checked)
        
        self.generateHeaderButton = QPushButton("Generate")
        self.generateHeaderButton.clicked.connect(self.insertHeader)
        
        # Sizing
        self.scriptTitle.setMaximumHeight(25)
        self.scriptTitleCheck.setMaximumHeight(25)
        self.scriptTitleEdit.setMaximumHeight(25)
        
        self.authorTitle.setMaximumHeight(25)
        self.authorTitleCheck.setMaximumHeight(25)
        self.authorTitleEdit.setMaximumHeight(25)
        
        self.characterListTitle.setMaximumHeight(25)
        self.characterListTitleCheck.setMaximumHeight(25)
        
        midSpace = QLabel(' ')
        midSpace.setMaximumHeight(7)
        bottomSpace = QLabel(' ')
        
        self.headerMenuGrid = QGridLayout()
        self.headerMenuGrid.setSpacing(1)
        
        checkboxAlignment = Qt.AlignRight | Qt.AlignBottom
        
        # Build main headerMenuGrid
        self.headerMenuGrid.addWidget(self.scriptTitle,             0, 0)#, Qt.AlignBottom)
        self.headerMenuGrid.addWidget(self.scriptTitleCheck,        0, 1, Qt.AlignRight)#, checkboxAlignment)
        self.headerMenuGrid.addWidget(self.scriptTitleEdit,         1, 0, 1, 2)
        self.headerMenuGrid.addWidget(midSpace,                     2, 0, 1, 2)
        
        self.headerMenuGrid.addWidget(self.authorTitle,             3, 0)#, Qt.AlignBottom)
        self.headerMenuGrid.addWidget(self.authorTitleCheck,        3, 1, Qt.AlignRight)#, checkboxAlignment)
        self.headerMenuGrid.addWidget(self.authorTitleEdit,         4, 0, 1, 2)
        self.headerMenuGrid.addWidget(midSpace,                     5, 0, 1, 2)
        
        self.headerMenuGrid.addWidget(self.characterListTitle,      6, 0)
        self.headerMenuGrid.addWidget(self.characterListTitleCheck, 6, 1, Qt.AlignRight)
        self.headerMenuGrid.addWidget(midSpace,                     7, 0, 1, 2)
        
        self.headerMenuGrid.addWidget(self.generateHeaderButton,    8, 0, 1, 2)
        self.headerMenuGrid.addWidget(bottomSpace,                  9, 0, 1, 2, Qt.AlignBottom)
        
    def insertHeader(self):
        # Get cursor
        cursor = self.scriptEdit.textCursor()
        
        # Make one block space
        cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
        
        # Title
        if (self.scriptTitleCheck.checkState() == Qt.Checked):
            self.scriptEdit.setTextCursor(cursor)
            self.changeFormatTo(FormatState.Heading)
            cursor.insertText(self.scriptTitleEdit.text())
            cursor.insertBlock()
        
        # Author
        if (self.authorTitleCheck.checkState() == Qt.Checked):
            self.scriptEdit.setTextCursor(cursor)
            self.changeFormatTo(FormatState.Paranthesis)
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.insertText("By " + self.authorTitleEdit.text())
            cursor.insertBlock()
        
        # Character List
        if (self.characterListTitleCheck.checkState() == Qt.Checked):
            cursor.insertBlock()
            self.scriptEdit.setTextCursor(cursor)
            self.changeFormatTo(FormatState.Dialogue)
            cursor.insertText("Character list:")
            cursor.insertBlock()
            self.scriptEdit.setTextCursor(cursor)
            self.changeFormatTo(FormatState.Character)
            for characterName in self.characterList:
                cursor.insertText(characterName)
                cursor.insertBlock()
        
        # Apply any remaining changes
        self.scriptEdit.setTextCursor(cursor)
    ### HEADER MENU SECTION END ###
    
    ### MENUBAR FUNCTIONS START ###
    
    def new(self):
        spawn = Main(self)
        spawn.show()
        
    def open(self):
        # Get filename and show only .writer files
        self.filename = QFileDialog.getOpenFileName(self, 'Open File',".","(*.writer)")[0]
        if self.filename:
            with open(self.filename,"rt") as file:
                self.scriptEdit.setText(file.read())
                
    def save(self):
        # Only open dialog if there is no filename yet
        if not self.filename:
            self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]

        print(self.filename)
        # Append extension if not there yet
        if not self.filename.endswith(".writer"):
            self.filename += ".writer"

        # We just store the contents of the text file along with the
        # format in html, which Qt does in a very nice way for us
        with open(self.filename,"wt") as file:
            file.write(self.scriptEdit.toHtml())
        
    def preview(self):
        preview = QPrintPreviewDialog()
        preview.paintRequested.connect(lambda p: self.scriptEdit.print_(p))
        preview.exec_()
     
    def print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.scriptEdit.document().print_(dialog.printer())
                   
    def bulletList(self):
        cursor = self.scriptEdit.textCursor()
        # Insert bulleted list
        cursor.insertList(QTextListFormat.ListDisc)
        
    def numberList(self):
        cursor = self.scriptEdit.textCursor()
        cursor.insertList(QTextListFormat.ListDecimal)
          
    def fontColor(self):
        color = QColorDialog.getColor()
        self.scriptEdit.setTextColor(color)
     
    def highlight(self):
        color = QColorDialog.getColor()
        self.scriptEdit.setTextBackgroundColor(color)

    def bold(self):
        if self.scriptEdit.fontWeight() == QtGui.QFont.Bold:
            self.scriptEdit.setFontWeight(QtGui.QFont.Normal)
        else:
            self.scriptEdit.setFontWeight(QtGui.QFont.ExtraBold)
     
    def italic(self):
        state = self.scriptEdit.fontItalic()
        self.scriptEdit.setFontItalic(not state)
     
    def underline(self):
        state = self.scriptEdit.fontUnderline()
        self.scriptEdit.setFontUnderline(not state)
     
    def strike(self):
        fmt = self.scriptEdit.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.scriptEdit.setCurrentCharFormat(fmt)
     
    def superScript(self):
        fmt = self.scriptEdit.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        self.scriptEdit.setCurrentCharFormat(fmt)
     
    def subScript(self):
        fmt = self.scriptEdit.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        self.scriptEdit.setCurrentCharFormat(fmt)
       
    def alignLeft(self):
        self.scriptEdit.setAlignment(Qt.AlignLeft)
     
    def alignRight(self):
        self.scriptEdit.setAlignment(Qt.AlignRight)
     
    def alignCenter(self):
        self.scriptEdit.setAlignment(Qt.AlignCenter)    
        
    ### MENUBAR FUNCTIONS END ###
    
    def setFontFormats(self):
        self.actionFormat = QTextCharFormat();
        self.actionFormat.setFontFamily("Courier")
        self.actionFormat.setFontPointSize(12)
        self.actionFormat.setFontCapitalization(QFont.MixedCase)    #First letter is capitalized later
        self.actionFormat.setFontItalic(False)
        self.actionFormat.setFontUnderline(False)
        self.actionFormat.setFontLetterSpacing(101)                 #Added a small change to differentiate from Dialogue
        
        self.characterFormat = QTextCharFormat();
        self.characterFormat.setFontFamily("Courier")
        self.characterFormat.setFontPointSize(12)
        self.characterFormat.setFontCapitalization(QFont.AllUppercase)
        self.characterFormat.setFontItalic(False)
        self.characterFormat.setFontUnderline(False)
        self.characterFormat.setFontLetterSpacing(100)
        
        self.dialogueFormat = QTextCharFormat();
        self.dialogueFormat.setFontFamily("Courier")
        self.dialogueFormat.setFontPointSize(12)
        self.dialogueFormat.setFontCapitalization(QFont.MixedCase)  #First letter is capitalized later
        self.dialogueFormat.setFontItalic(False)
        self.dialogueFormat.setFontUnderline(False)
        self.dialogueFormat.setFontLetterSpacing(100)
        
        self.paranthesisFormat = QTextCharFormat();
        self.paranthesisFormat.setFontFamily("Courier")
        self.paranthesisFormat.setFontPointSize(12)
        self.paranthesisFormat.setFontCapitalization(QFont.MixedCase)
        self.paranthesisFormat.setFontItalic(True)
        self.paranthesisFormat.setFontUnderline(False)
        self.paranthesisFormat.setFontLetterSpacing(100)
        
        self.headingFormat = QTextCharFormat();
        self.headingFormat.setFontFamily("Courier")
        self.headingFormat.setFontPointSize(12)
        self.headingFormat.setFontCapitalization(QFont.AllUppercase)
        self.headingFormat.setFontItalic(False)
        self.headingFormat.setFontUnderline(True)
        self.headingFormat.setFontLetterSpacing(100)
        
        self.transitionFormat = QTextCharFormat();
        self.transitionFormat.setFontFamily("Courier")
        self.transitionFormat.setFontPointSize(12)
        self.transitionFormat.setFontCapitalization(QFont.AllUppercase)
        self.transitionFormat.setFontItalic(False)
        self.transitionFormat.setFontUnderline(False)
        self.transitionFormat.setFontLetterSpacing(101)             #Added a small change to differentiate from Character
        
    def setBlockFormats(self):
        self.actionBlock = QTextBlockFormat();
        self.actionBlock.setLeftMargin(0)
        self.actionBlock.setRightMargin(0)
        self.actionBlock.setAlignment(Qt.AlignLeft)
        
        self.characterBlock = QTextBlockFormat();
        self.characterBlock.setLeftMargin(240)
        self.characterBlock.setRightMargin(0)
        self.characterBlock.setAlignment(Qt.AlignLeft)
        
        self.dialogueBlock = QTextBlockFormat();
        self.dialogueBlock.setLeftMargin(120)
        self.dialogueBlock.setRightMargin(120)
        self.dialogueBlock.setAlignment(Qt.AlignLeft)
        
        self.paranthesisBlock = QTextBlockFormat();
        self.paranthesisBlock.setLeftMargin(190)
        self.paranthesisBlock.setRightMargin(190)
        self.paranthesisBlock.setAlignment(Qt.AlignLeft)
        
        self.headingBlock = QTextBlockFormat();
        self.headingBlock.setLeftMargin(0)
        self.headingBlock.setRightMargin(0)
        self.headingBlock.setAlignment(Qt.AlignCenter)
        
        self.transitionBlock = QTextBlockFormat();
        self.transitionBlock.setLeftMargin(0)
        self.transitionBlock.setRightMargin(0)
        self.transitionBlock.setAlignment(Qt.AlignRight)
        
    def changeStyle(self):
        if (self.currFormatState == FormatState.Action):
            self.changeFormatTo(FormatState.Character)
        elif (self.currFormatState == FormatState.Character):
            self.changeFormatTo(FormatState.Dialogue)
        elif (self.currFormatState == FormatState.Dialogue):
            self.changeFormatTo(FormatState.Paranthesis)
        elif (self.currFormatState == FormatState.Paranthesis):
            self.changeFormatTo(FormatState.Heading)
        elif (self.currFormatState == FormatState.Heading):
            self.changeFormatTo(FormatState.Transition)
        elif (self.currFormatState == FormatState.Transition):
            self.changeFormatTo(FormatState.Action)
            
    def customNewLineStyle(self):
        if (self.currFormatState == FormatState.Action):
            self.changeFormatTo(FormatState.Action, True)
        elif (self.currFormatState == FormatState.Character):
            self.changeFormatTo(FormatState.Dialogue, True)
        elif (self.currFormatState == FormatState.Dialogue):
            self.changeFormatTo(FormatState.Action, True)
        elif (self.currFormatState == FormatState.Paranthesis):
            self.changeFormatTo(FormatState.Dialogue, True)
        elif (self.currFormatState == FormatState.Heading):
            self.changeFormatTo(FormatState.Action, True)
        elif (self.currFormatState == FormatState.Transition):
            self.changeFormatTo(FormatState.Action, True)
        
    def formatAction(self, changeCursor):
        # Setup
        toSetReturnPosition = changeCursor.position()
        
        # Line format
        self.capitalizeFirst(changeCursor)
        changeCursor.select(QTextCursor.BlockUnderCursor)
        changeCursor.setCharFormat(self.actionFormat)
                
        # Return cursor to it's original position
        changeCursor.setPosition(toSetReturnPosition)
                
        # Apply the changes
        changeCursor.setBlockFormat(self.actionBlock)
        self.scriptEdit.setTextCursor(changeCursor)
                
        # Track state
        self.prevFormatState = self.currFormatState
        self.currFormatState = FormatState.Action
        self.setChecked(self.currFormatState)
        
    def formatCharacter(self, changeCursor):
        # Setup
        toSetReturnPosition = changeCursor.position()
        
        # Line format
        changeCursor.select(QTextCursor.BlockUnderCursor)
        changeCursor.setCharFormat(self.characterFormat)
        
        # Return cursor to it's original position
        changeCursor.setPosition(toSetReturnPosition)
        
        # Apply the changes
        changeCursor.setBlockFormat(self.characterBlock)
        ##changeCursor.setBlockCharFormat(self.characterFormat)
        self.scriptEdit.setTextCursor(changeCursor)
        
        # Track state
        self.prevFormatState = self.currFormatState
        self.currFormatState = FormatState.Character
        self.setChecked(self.currFormatState)
       
    def formatParanthesis(self, changeCursor):
        # Setup
        toSetReturnPosition = changeCursor.position()
        
        # Line format
        changeCursor.select(QTextCursor.BlockUnderCursor)
        changeCursor.setCharFormat(self.paranthesisFormat)
        
        # Return cursor to it's original position
        changeCursor.setPosition(toSetReturnPosition)
        
        # Apply the changes
        changeCursor.setBlockFormat(self.paranthesisBlock)
        self.scriptEdit.setTextCursor(changeCursor)
                
        # Track state
        self.prevFormatState = self.currFormatState
        self.currFormatState = FormatState.Paranthesis
        self.setChecked(self.currFormatState)
        
    def formatDialogue(self, changeCursor):
        # Setup
        toSetReturnPosition = changeCursor.position()
        
        # Line format
        #self.capitalizeFirst(changeCursor) TODO: fix this??? eg. change "character list: " from heading to dialogue
        changeCursor.select(QTextCursor.BlockUnderCursor)
        changeCursor.setCharFormat(self.dialogueFormat)
        
        # Return cursor to it's original position
        changeCursor.setPosition(toSetReturnPosition)
                
        # Apply the changes
        changeCursor.setBlockFormat(self.dialogueBlock)
        ##changeCursor.setBlockCharFormat(self.dialogueFormat)
        self.scriptEdit.setTextCursor(changeCursor)
                
        # Track state
        self.prevFormatState = self.currFormatState
        self.currFormatState = FormatState.Dialogue
        self.setChecked(self.currFormatState)
        
    def formatHeading(self, changeCursor):
        # Setup
        toSetReturnPosition = changeCursor.position()
        
        # Line format
        changeCursor.select(QTextCursor.BlockUnderCursor)
        changeCursor.setCharFormat(self.headingFormat)
        
        # Return cursor to it's original position
        changeCursor.setPosition(toSetReturnPosition)
                
        # Apply the changes
        changeCursor.setBlockFormat(self.headingBlock)
        self.scriptEdit.setTextCursor(changeCursor)
                
        # Track state
        self.prevFormatState = self.currFormatState
        self.currFormatState = FormatState.Heading
        self.setChecked(self.currFormatState)
        
    def formatTransition(self, changeCursor):
        # Setup
        toSetReturnPosition = changeCursor.position()
        
        # Line format
        changeCursor.select(QTextCursor.BlockUnderCursor)
        changeCursor.setCharFormat(self.transitionFormat)
        
        # Return cursor to it's original position
        changeCursor.setPosition(toSetReturnPosition)
                
        # Apply changes
        changeCursor.setBlockFormat(self.transitionBlock)
        self.scriptEdit.setTextCursor(changeCursor)
                
        # Track state
        self.prevFormatState = self.currFormatState
        self.currFormatState = FormatState.Transition
        self.setChecked(self.currFormatState)
        
    # ----- FORMAT HELPERS -----
    def changeFormatTo(self, newFormatState, newLine = False):
        # Get cursor
        toSet = self.scriptEdit.textCursor()
        
        # Start tracking undo
        formatUndo = QUndoCommand()
        formatUndo.setText("Changing preset format")
        
        #Disable format detection during format changing
        self.detectionEnabled = False
        
        # Optional add new line
        if (newLine):
            if (newFormatState == FormatState.Action):
               toSet.insertBlock(self.actionBlock, self.actionFormat)
            elif (newFormatState == FormatState.Character):
               toSet.insertBlock(self.characterBlock, self.characterFormat)
            elif (newFormatState == FormatState.Dialogue):
               toSet.insertBlock(self.dialogueBlock, self.dialogueFormat)
            elif (newFormatState == FormatState.Heading):
               toSet.insertBlock(self.headingBlock, self.headingFormat)
            elif (newFormatState == FormatState.Paranthesis):
               toSet.insertBlock(self.paranthesisBlock, self.paranthesisFormat)
            elif (newFormatState == FormatState.Transition):
               toSet.insertBlock(self.transitionBlock, self.transitionFormat)
                
            self.scriptEdit.setTextCursor(toSet)
            toSet = self.scriptEdit.textCursor()
        
        # Get/Init cursor position data
        self.cursorStartPosition = toSet.selectionStart()
        self.newCharactersBehindStart = 0
        self.cursorEndPosition = toSet.selectionEnd()
        self.newCharactersBehindEnd = 0
        
        # Get number of blocks to change
        startingBlock = 0
        endingBlock = 0
        if (self.cursorStartPosition != self.cursorEndPosition):
            toSet.setPosition(self.cursorStartPosition)
            startingBlock = toSet.blockNumber()
            toSet.setPosition(self.cursorEndPosition)
            endingBlock = toSet.blockNumber()
        else:
            toSet.setPosition(self.cursorStartPosition)
            startingBlock = toSet.blockNumber()
            endingBlock = startingBlock
        
        # Check if we're changing on an empty line
        noSelectedText = False
        if (self.cursorStartPosition == self.cursorEndPosition):
            toSet.select(QTextCursor.LineUnderCursor)
            if (toSet.selectedText() == ""):
                noSelectedText = True
                    
        # Go through all selected blocks
        toSet.setPosition(self.cursorStartPosition)
        while (startingBlock <= endingBlock):
            # Parantheses check
            if (self.currFormatState == FormatState.Paranthesis and newFormatState != FormatState.Paranthesis):
                self.changeParenthesis(toSet, False)
            # Colon check           
            if (self.currFormatState == FormatState.Transition and newFormatState != FormatState.Transition):
                self.changeColon(toSet, False)
                
            # Empty Line check
            toSet.select(QTextCursor.LineUnderCursor)
            emptyLine = (toSet.selectedText() == "")
            
            # Apply format
            if (newFormatState == FormatState.Action):
                if (emptyLine):
                    toSet.setBlockCharFormat(self.actionFormat)
                    self.scriptEdit.setTextCursor(toSet)
                self.formatAction(toSet)
            elif (newFormatState == FormatState.Character):
                if (emptyLine):
                    toSet.setBlockCharFormat(self.characterFormat)
                    self.scriptEdit.setTextCursor(toSet)
                self.formatCharacter(toSet)
            elif (newFormatState == FormatState.Dialogue):
                if (emptyLine):
                    toSet.setBlockCharFormat(self.dialogueFormat)
                    self.scriptEdit.setTextCursor(toSet)
                self.formatDialogue(toSet)
            elif (newFormatState == FormatState.Heading):
                if (emptyLine):
                    toSet.setBlockCharFormat(self.headingFormat)
                    self.scriptEdit.setTextCursor(toSet)
                self.formatHeading(toSet)
            elif (newFormatState == FormatState.Paranthesis):
                self.changeParenthesis(toSet, True)
                self.formatParanthesis(toSet)
            elif (newFormatState == FormatState.Transition):
                self.changeColon(toSet, True)
                self.formatTransition(toSet)
            
            startingBlock += 1
            toSet.movePosition(QTextCursor.NextBlock)
            
        # Set cursor positions
        if (self.cursorStartPosition == self.cursorEndPosition):
            self.cursorStartPosition += self.newCharactersBehindStart
            if (noSelectedText and newFormatState == FormatState.Paranthesis):
                self.cursorStartPosition += 1
            toSet.setPosition(self.cursorStartPosition)
        else:
            self.cursorStartPosition += self.newCharactersBehindStart
            toSet.setPosition(self.cursorStartPosition)
            self.cursorEndPosition += self.newCharactersBehindEnd
            toSet.setPosition(self.cursorEndPosition, QTextCursor.KeepAnchor)
            
        # Apply changes
        self.scriptEdit.setTextCursor(toSet)
            
        #Disable format detection during format changing
        self.detectionEnabled = True
                
    def trackChangesBeforeCursor(self, currentPosition, valueChange):
        if (currentPosition < self.cursorStartPosition):
            self.newCharactersBehindStart += valueChange
        if (currentPosition < self.cursorEndPosition):
            self.newCharactersBehindEnd += valueChange
        
    def changeParenthesis(self, toSet, changeMode):
        # initializing
        #charactersChanged = 0
        hasBrackets = False
            
        toSet.select(QTextCursor.BlockUnderCursor)
        toCheckBlock = toSet.selectedText().strip()
        if (toCheckBlock.startswith("(")):
            if (toCheckBlock.endswith(")")):
                hasBrackets = True
         
        if (changeMode):
            if (not hasBrackets):
                toSet.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
                self.trackChangesBeforeCursor(toSet.position(), 1) 
                toSet.insertText("(")
                toSet.movePosition(QTextCursor.EndOfBlock, QTextCursor.MoveAnchor)
                self.trackChangesBeforeCursor(toSet.position(), 1) 
                toSet.insertText(")")
        else:
            if (hasBrackets):
                toSet.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
                self.trackChangesBeforeCursor(toSet.position(), -1) 
                toSet.deleteChar()
                toSet.movePosition(QTextCursor.EndOfBlock, QTextCursor.MoveAnchor)
                self.trackChangesBeforeCursor(toSet.position(), -1) 
                toSet.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
                toSet.deleteChar()
            
    def changeColon(self, toSet, changeMode):
        # initializing
        hasColon = False
            
        toSet.select(QTextCursor.BlockUnderCursor)
        toCheckBlock = toSet.selectedText().strip()
        if (toCheckBlock.endswith(":")):
            hasColon = True
         
        if (changeMode):
            if (not hasColon):
                toSet.movePosition(QTextCursor.EndOfBlock, QTextCursor.MoveAnchor)
                self.trackChangesBeforeCursor(toSet.position(), 1) 
                toSet.insertText(":")
        else:
            if (hasColon):
                toSet.movePosition(QTextCursor.EndOfBlock, QTextCursor.MoveAnchor)
                self.trackChangesBeforeCursor(toSet.position(), -1) 
                toSet.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
                toSet.deleteChar()
            return
                        
    def capitalizeFirst(self, toCap):
        # CAUTION! Apart from capitalizing the first letter, 
        # this function appears to remove all other formatting
        toCap.select(QTextCursor.BlockUnderCursor)
        selectedText = toCap.selectedText().strip()
        sentences = selectedText.split(".")
        capitalizedBlock = ""
        
        if (sentences):#and len(sentences[0]) >= 1):  # Check if the list is empty
            sentenceCount = 0
            for sentence in sentences:
                if (sentenceCount >= 1):
                    capitalizedBlock += "."
                capitalizedBlock += sentence.capitalize()
                sentenceCount += 1
                
            if (toCap.blockNumber() > 0):       # Only add a newline if this block is after the first line
                capitalizedBlock = "\n" + capitalizedBlock
            
            toCap.deleteChar()
            toCap.insertText(capitalizedBlock)
            
    def detectFormat(self):
        # Get cursor
        toDetect = self.scriptEdit.textCursor()
        blockFormat = toDetect.charFormat()
        detectedType = 0
        
        if (self.detectionEnabled):
            # Get object to compare
            toCompare = QTextCharFormat();
            toCompare.setFontFamily(toDetect.charFormat().fontFamily())
            toCompare.setFontPointSize(toDetect.charFormat().fontPointSize())
            toCompare.setFontCapitalization(toDetect.charFormat().fontCapitalization())
            toCompare.setFontItalic(toDetect.charFormat().fontItalic())
            toCompare.setFontUnderline(toDetect.charFormat().fontUnderline())
            toCompare.setFontLetterSpacing(toDetect.charFormat().fontLetterSpacing())
        
            if (toCompare == self.actionFormat):
                self.setChecked(FormatState.Action)
                detectedType = FormatState.Action
            elif (toCompare == self.characterFormat):
                self.setChecked(FormatState.Character)
                detectedType = FormatState.Character
            elif (toCompare == self.dialogueFormat):
                self.setChecked(FormatState.Dialogue)
                detectedType = FormatState.Dialogue
            elif (toCompare == self.paranthesisFormat):
                self.setChecked(FormatState.Paranthesis)
                detectedType = FormatState.Paranthesis
            elif (toCompare == self.headingFormat):
                self.setChecked(FormatState.Heading)
                detectedType = FormatState.Heading
            elif (toCompare == self.transitionFormat):
                self.setChecked(FormatState.Transition)
                detectedType = FormatState.Transition
            else:
                detectedType = 7
                ## if no format is detected, force previous format
                ##if (self.autoFormatOnLineChange):
                self.changeFormatTo(self.currFormatState)
                ## if (toDetect.position() == 0):
                ##    print(toDetect.position())
            
            if (detectedType != 7):
                self.currFormatState = detectedType
            
        return detectedType
        
    def setAutoFormat(self):
        self.autoFormatOnLineChange = not self.autoFormatOnLineChange
        self.autoFormatAction.setChecked(self.autoFormatOnLineChange)
        
    def setChecked(self, newState):
        self.actionFormatAction.setChecked(False)
        self.characterFormatAction.setChecked(False)
        self.dialogueFormatAction.setChecked(False)
        self.paranthesisFormatAction.setChecked(False)
        self.headingFormatAction.setChecked(False)
        self.transitionFormatAction.setChecked(False)
        
        if (newState == FormatState.Action):
            self.actionFormatAction.setChecked(True)
        elif (newState == FormatState.Character):
            self.characterFormatAction.setChecked(True)
        elif (newState == FormatState.Dialogue):
            self.dialogueFormatAction.setChecked(True)
        elif (newState == FormatState.Paranthesis):
            self.paranthesisFormatAction.setChecked(True)
        elif (newState == FormatState.Heading):
            self.headingFormatAction.setChecked(True)
        elif (newState == FormatState.Transition):
            self.transitionFormatAction.setChecked(True)
            
    def setStartingFormat(self):
        toStart = self.scriptEdit.textCursor()
        startingType = self.detectFormat()
        if (startingType == FormatState.NoState):
            self.formatAction(toStart)
            self.setChecked(FormatState.Action)

# Ease of tracking/comparing states
class FormatState(Enum):
    Action = 0
    Character = 1
    Dialogue = 2
    Paranthesis = 3
    Heading = 4
    Transition = 5
    NoState = 6
   
# Modifying the QTextEdit implementation in order to allow autocompletion
class CompletionTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(CompletionTextEdit, self).__init__(parent)
        self.completer = None

    def setCompleter(self, completer):
        if self.completer is not None:
            self.completer.activated.disconnect()
            
        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.activated.connect(self.insertCompletion)
        self.completer = completer
        
    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) - len(self.completer.completionPrefix()))
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QTextEdit.focusInEvent(self, event)
       
    def keyReleaseEvent(self, event):
        print(str(self.parent().parent().prevFormatState) + " : " + str(self.parent().parent().currFormatState))
        if ((event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Return)) and 
        ((self.parent().parent().prevFormatState == FormatState.Character) or 
        (self.parent().parent().currFormatState == FormatState.Character))):
            print("STORE CHARACTER")
        
    def keyPressEvent(self, event):    
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (
            QtCore.Qt.Key_Enter,
            QtCore.Qt.Key_Return,
            QtCore.Qt.Key_Escape,
            QtCore.Qt.Key_Tab,
            QtCore.Qt.Key_Backtab):
                event.ignore()
                return
                
        # the prefered format switching shortcut
        if (event.key() == (QtCore.Qt.Key_Tab)):
            self.parent().parent().changeStyle()
            return
        
        # shortcut for new line format
        if (event.key() in (
            QtCore.Qt.Key_Enter,
            QtCore.Qt.Key_Return)):
            self.parent().parent().customNewLineStyle()
            return
                    
        ## only show suggestions for characters
        if not self.parent().parent().characterFormatAction.isChecked():
            QTextEdit.keyPressEvent(self, event)
            return

        QTextEdit.keyPressEvent(self, event)

        ## ctrl or shift key on it's own?
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier ,
                QtCore.Qt.ShiftModifier)
        if ctrlOrShift and not event.text():
            # ctrl or shift key on it's own
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=" #end of word

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and
                        not ctrlOrShift)

        completionPrefix = self.textUnderCursor()

        if (hasModifier or not event.text() or
        len(completionPrefix) < 1 or (event.text()[-1] in eow)):
            self.completer.popup().hide()
            return

        if (completionPrefix != self.completer.completionPrefix()):
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(
                self.completer.completionModel().index(0,0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr) ## popup it up!
        
def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()

# To do:
# [X] SCENE HEADING (centered, upper case)
# [X] Action (left aligned, regular case)
# [x] CHARACTER (left aligned indented, upper case)
# [x] Dialogue (left aligned less indented, regular case)
# [X] (Paranthetical) (centered, in brackets, italics?)
# [X] TRANSITION (right aligned, uppercase)
# [X] Set page size
# [ ] Make shortcuts customizable (external text editor)
# [ ] Auto complete character names
# [X] Shortcut to switch styles
