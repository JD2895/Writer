import sys
from PyQt5 import (QtGui, QtCore)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextEdit, QAction,
                             QFileDialog, QDialog, QFontComboBox, QComboBox,
                             QColorDialog, QGridLayout,
                             QHBoxLayout, QLabel, QWidget)  # Layout)                         
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtGui import (QTextListFormat, QFont, QTextCursor,
                         QTextCharFormat)

class Main(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self,parent)
        self.setMinimumWidth(800)
        self.filename = ""
        
        self.setFontFormats()
        self.initUI()
 
    def initUI(self):
        # Initialising script editor widget
        self.scriptEdit = QTextEdit(self)
        self.scriptEdit.setFontFamily("Courier")
        self.scriptEdit.setFontPointSize(12)
        self.scriptEdit.setMaximumWidth(660)
         
        # Setting/Adding toolbars
        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()
        self.statusbar = self.statusBar()
        
        # Layout
        layoutWidget = QWidget()        
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(QLabel(' '))
        mainLayout.addWidget(self.scriptEdit)
        mainLayout.addWidget(QLabel(' '))
        layoutWidget.setLayout(mainLayout)
        self.setCentralWidget(layoutWidget)
                
        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,1030,800) 
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
        self.undoAction.triggered.connect(self.scriptEdit.undo)
        
        # Redo
        self.redoAction = QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.scriptEdit.redo)
        
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
        
        # Character
        capitalAction = QAction("Character",self)
        capitalAction.triggered.connect(self.formatCharacter)
        capitalAction.setShortcut("Alt+1")
        # Dialogue
        dialogueAction = QAction("Dialogue",self)
        dialogueAction.triggered.connect(self.formatDialogue)
        dialogueAction.setShortcut("Alt+2")
        
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
        # Align Justify
        alignJustify = QAction(QtGui.QIcon("icons/align-justify.png"),"Align justify",self)
        alignJustify.triggered.connect(self.alignJustify)
        
        self.formatbar = self.addToolBar("Format")
        
        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)
        self.formatbar.addSeparator()
        
        self.formatbar.addAction(capitalAction)
        self.formatbar.addAction(dialogueAction)
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
        self.formatbar.addAction(alignJustify)
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
        
    # ----- BREAK ----- 1
    
    def preview(self):
        # Open preview dialog
        preview = QPrintPreviewDialog()
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.scriptEdit.print_(p))
        preview.exec_()
     
    def print(self):
        # Open printing dialog
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.scriptEdit.document().print_(dialog.printer())
            
    # ----- BREAK ----- 2
            
    def bulletList(self):
        cursor = self.scriptEdit.textCursor()
        # Insert bulleted list
        cursor.insertList(QTextListFormat.ListDisc)
        
    def numberList(self):
        cursor = self.scriptEdit.textCursor()
        # Insert list with numbers
        cursor.insertList(QTextListFormat.ListDecimal)
        
    # ----- BREAK ----- 3
        
    def fontFamily(self,font):
        self.scriptEdit.setCurrentFont(font)
     
    def fontSize(self, fontsize):
        self.scriptEdit.setFontPointSize(int(fontsize))
        
    # ----- BREAK ----- 4
        
    def fontColor(self):
        # Get a color from the text dialog
        color = QColorDialog.getColor()
        # Set it as the new text color
        self.scriptEdit.setTextColor(color)
     
    def highlight(self):
        color = QColorDialog.getColor()
        self.scriptEdit.setTextBackgroundColor(color)

    # ----- BREAK ----- 5

    def bold(self):
        if self.scriptEdit.fontWeight() == QtGui.QFont.Bold:
            self.scriptEdit.setFontWeight(QtGui.QFont.Normal)
        else:
            self.scriptEdit.setFontWeight(QtGui.QFont.Bold)
     
    def italic(self):
        state = self.scriptEdit.fontItalic()
        self.scriptEdit.setFontItalic(not state)
     
    def underline(self):
        state = self.scriptEdit.fontUnderline()
        self.scriptEdit.setFontUnderline(not state)
     
    def strike(self):
        # Grab the text's format
        fmt = self.scriptEdit.currentCharFormat()
        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        # And set the next char format
        self.scriptEdit.setCurrentCharFormat(fmt)
     
    def superScript(self):
        # Grab the current format
        fmt = self.scriptEdit.currentCharFormat()
        # And get the vertical alignment property
        align = fmt.verticalAlignment()
        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        # Set the new format
        self.scriptEdit.setCurrentCharFormat(fmt)
     
    def subScript(self):
        # Grab the current format
        fmt = self.scriptEdit.currentCharFormat()
        # And get the vertical alignment property
        align = fmt.verticalAlignment()
        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        # Set the new format
        self.scriptEdit.setCurrentCharFormat(fmt)
        
    # ----- BREAK ----- 6
    
    def alignLeft(self):
        self.scriptEdit.setAlignment(Qt.AlignLeft)
     
    def alignRight(self):
        self.scriptEdit.setAlignment(Qt.AlignRight)
     
    def alignCenter(self):
        self.scriptEdit.setAlignment(Qt.AlignCenter)
     
    def alignJustify(self):
        self.scriptEdit.setAlignment(Qt.AlignJustify)
        
    # ----- BREAK ----- Final
    
    def setFontFormats(self):
        self.generalFormat = QTextCharFormat();
        self.generalFormat.setFontFamily("Courier")
        self.generalFormat.setFontPointSize(12)
        
        self.characterFormat = QTextCharFormat();
        self.characterFormat.setFontFamily("Courier")
        self.characterFormat.setFontPointSize(12)
        self.characterFormat.setFontCapitalization(QFont.AllUppercase)
        
        self.dialogueFormat = QTextCharFormat();
        self.dialogueFormat.setFontFamily("Courier")
        self.dialogueFormat.setFontPointSize(12)
        self.dialogueFormat.setFontCapitalization(QFont.AllLowercase)   #First letter is capitalized later
        
        self.paranthesisFormat = QTextCharFormat();
        self.paranthesisFormat.setFontFamily("Courier")
        self.paranthesisFormat.setFontPointSize(12)
        self.paranthesisFormat.setFontCapitalization(QFont.AllLowercase)
        
    def formatCharacter(self):
        # Setup
        toSet = self.scriptEdit.textCursor()
        toSetOgPosition = toSet.position()
        toSetBlockFmt = self.scriptEdit.textCursor().blockFormat()
        
        # Line format
        toSet.select(QTextCursor.LineUnderCursor)
        toSet.setCharFormat(self.characterFormat)
        
        # Return cursor to it's original position
        toSet.setPosition(toSetOgPosition, QTextCursor.MoveAnchor)
        
        # Block format
        toSetBlockFmt.setLeftMargin(240)
        toSetBlockFmt.setRightMargin(0)
        
        # Apply the changes
        toSet.setBlockFormat(toSetBlockFmt)
        self.scriptEdit.setTextCursor(toSet)
        
        # Apply alignment
        self.scriptEdit.setAlignment(Qt.AlignLeft)
        
    def formatDialogue(self):
        # Setup
        toSet = self.scriptEdit.textCursor()
        toSetOgPosition = toSet.position()
        toSetBlockFmt = self.scriptEdit.textCursor().blockFormat()
        
        # Line format
        toSet.select(QTextCursor.LineUnderCursor)
        toSet.setCharFormat(self.dialogueFormat)
        toSet.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
        toSet.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        toSet.setCharFormat(self.characterFormat)
        
        # Return cursor to it's original position
        toSet.setPosition(toSetOgPosition, QTextCursor.MoveAnchor)
        
        # Block format
        toSetBlockFmt.setLeftMargin(120)
        toSetBlockFmt.setRightMargin(120)
        
        # Apply changes
        toSet.setBlockFormat(toSetBlockFmt)
        self.scriptEdit.setTextCursor(toSet)
        
        # Apply alignment
        self.scriptEdit.setAlignment(Qt.AlignLeft)
 
def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()

# To do:
# [ ] SCENE HEADING (centered, upper case)
# [ ] Action (left aligned, regular case)
# [x] CHARACTER (left aligned indented, upper case)
# [x] Dialogue (left aligned less indented, regular case)
# [ ] (Paranthetical) (centered, in brackets, italics?)
# [ ] TRANSITION (right aligned, uppercase)
# [ ] Set page size
# [ ] Auto complete character names
