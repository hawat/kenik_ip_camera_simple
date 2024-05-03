import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("My PyQt Example")

label = QLabel("Hello, World!")
combo_box = QComboBox()
combo_box.addItems(["Option 1", "Option 2", "Option 3"])

layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(combo_box)
window.setLayout(layout)

# Connect to a signal to track selection changes
def on_selection_changed(text):
    label.setText(f"You selected: {text}")

combo_box.currentTextChanged.connect(on_selection_changed)

window.show()
app.exec_()
