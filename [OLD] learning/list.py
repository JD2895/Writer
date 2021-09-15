import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, 
                             QListWidget, QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import (QFont, QTextDocument)
from PyQt5.QtCore import (Qt)

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.characterList = ["FRED", "ARTIE"]
        
        # Header
        self.charListTitle = QLabel('Characters')
        self.charListButtonTitle = QLabel('+/-')
        self.newCharacterEdit = QLineEdit()
        
        # Adding characters
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
        self.charMenuGrid.addWidget(self.charListTitle, 0, 0, 1, 4)
        self.charMenuGrid.addWidget(self.charListButtonTitle, 0, 4)
        self.charMenuGrid.addWidget(self.newCharacterEdit, 1, 0, 1, 4)
        self.charMenuGrid.addWidget(self.addCharacterButton, 1, 4)
        self.charMenuGrid.addLayout(self.characterListContainer, 2, 0, 1, 5)
        
        # Populate charactert 
        self.setCharacterList()

        self.setLayout(self.charMenuGrid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()
        
    def setCharacterList(self):
        # Remove old charMenuGrid
        rowCount = self.characterListContainer.rowCount()
        colCount = self.characterListContainer.columnCount()
        
        for i in range(rowCount):
            for j in range(colCount):
                print(i)
                print(j)
                if self.characterListContainer.itemAtPosition(i, j) is not None:
                    self.characterListContainer.itemAtPosition(i, j).widget().setParent(None)
                print(self.characterListContainer.itemAtPosition(i, j))
        
        
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
        self.setCharacterList()
        
    def removeCharacter(self, charName):
        print(charName)
        self.characterList.remove(charName)
        self.setCharacterList()
     
def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
