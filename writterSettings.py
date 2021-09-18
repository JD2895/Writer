from PyQt5.QtCore import (Qt)

# Change whether you want to use Tab to change formats
tabFormat = True
# Change whether you want Enter to automatically change formats
enterFormat = True

# Change the default author of scripts
defaultAuthor = "Josh Davis"

# Change whether scripts should start with default character suggestions
startWithDefaultCharacters = True
# Change the default characters in your scripts
defaultCharacters = ["ALEX", "CHARLIE", "FRANKIE", "JESSIE"]

# Alternative (and customizable) shortcuts for formatting
## Refer to https://doc.qt.io/qtforpython-5/PySide2/QtCore/Qt.html
actionFormat = Qt.ALT + Qt.Key_1
characterFormat = Qt.ALT + Qt.Key_2
dialogueFormat = Qt.ALT + Qt.Key_3
paranthesisFormat = Qt.ALT + Qt.Key_4
headingFormat = Qt.ALT + Qt.Key_5
transitionFormat = Qt.ALT + Qt.Key_6
# Cycle through formats
changeFormat = Qt.ALT + Qt.Key_QuoteLeft
# Add a new line AND change formats
newLineFormat = Qt.ALT + Qt.Key_Return
