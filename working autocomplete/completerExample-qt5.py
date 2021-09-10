from PyQt5 import (QtGui, QtCore)
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextEdit, QAction,
                             QFileDialog, QDialog, QFontComboBox, QComboBox,
                             QColorDialog, QGridLayout,
                             QHBoxLayout, QLabel, QWidget,  # Layout
                             QUndoStack, QUndoCommand,     # Undo
                             QCompleter)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtGui import (QTextListFormat, QFont, QTextCursor,
                         QTextCharFormat, QTextBlockFormat, 
                         QKeySequence,  # Shortcuts
                        )  

STARTTEXT = ('This TextEdit provides autocompletions for words that have ' +
'more than 3 characters.\nYou can trigger autocompletion using %s\n\n'''% (
QKeySequence("Ctrl+E").toString(QKeySequence.NativeText)))

# class DictionaryCompleter(QCompleter):
    # def __init__(self, parent=None):
        # wordsq = ["Apple", "Bottom", "Jeans"]
        # ## try:
            # ## f = open("/usr/share/dict/words","r")
            # ## for word in f:
                # ## words.append(word.strip())
            # ## f.close()
        # ## except IOError:
            # ## print ("dictionary not in anticipated location")
        # QCompleter.__init__(self, wordsq, parent)

class CompletionTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(CompletionTextEdit, self).__init__(parent)
        self.setMinimumWidth(400)
        self.setPlainText(STARTTEXT)
        self.completer = None
        self.moveCursor(QTextCursor.End)

    def setCompleter(self, completer):
        if self.completer is not None:
            self._completer.activated.disconnect()
            
        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.activated.connect(self.insertCompletion)
        self.completer = completer
        ##self.activated.connect(self.completer, QtCore.SIGNAL("activated(const QString&)"), self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        ##extra = (completion.length() - self.completer.completionPrefix().length())
        extra = (len(completion) - len(self.completer.completionPrefix()))
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        ##tc.insertText(completion.right(extra))
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

        ## has ctrl-E been pressed??
        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and
                      event.key() == QtCore.Qt.Key_E)
        if (not self.completer or not isShortcut):
            QTextEdit.keyPressEvent(self, event)

        ## ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier ,
                QtCore.Qt.ShiftModifier)
        if ctrlOrShift and event.text().isEmpty():
            # ctrl or shift key on it's own
            return

        ##eow = QtCore.QString("~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=") #end of word
        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=" #end of word

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and
                        not ctrlOrShift)

        completionPrefix = self.textUnderCursor()

        ##if (not isShortcut and (hasModifier or event.text().isEmpty() or
        if (not isShortcut and (hasModifier or not event.text() or
        len(completionPrefix) < 1 or
        ##eow.contains(event.text().right(1)))):
        (event.text()[-1] in eow))):
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

if __name__ == "__main__":

    app = QApplication([])
    
    words = ["Second", "Tier", "Post"]
    completer = QCompleter(words, None)
    
    #completer = DictionaryCompleter()
    te = CompletionTextEdit()
    te.setCompleter(completer)
    te.show()
    app.exec_()
