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
        self.title = QLabel('Characters')
        self.mod = QLabel('+/-')
        self.newCharacterEdit = QLineEdit()
        
        # Adding characters
        self.addCharacterButton = QPushButton('+', self)
        self.addCharacterButton.clicked.connect(self.addCharacter)
        # Character list container
        self.characterListContainer = QGridLayout()
        self.characterListContainer.setSpacing(2)
        
        # Sizing
        self.title.setMaximumHeight(25)
        self.mod.setMaximumWidth(25)
        self.mod.setMaximumHeight(25)
        self.addCharacterButton.setMaximumWidth(25)
        self.addCharacterButton.setMaximumHeight(25)
        self.grid = QGridLayout()
        self.grid.setSpacing(2)

        # Build main grid
        self.grid.addWidget(self.title, 0, 0, 1, 4)
        self.grid.addWidget(self.mod, 0, 4)
        self.grid.addWidget(self.newCharacterEdit, 1, 0, 1, 4)
        self.grid.addWidget(self.addCharacterButton, 1, 4)
        self.grid.addLayout(self.characterListContainer, 2, 0, 1, 5)
        
        # Populate charactert 
        self.setGridList()
        

        self.setLayout(self.grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()
        
    def setGridList(self):
        # Remove old grid
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
        self.setGridList()
        
    def removeCharacter(self, charName):
        print(charName)
        self.characterList.remove(charName)
        self.setGridList()
     
def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
