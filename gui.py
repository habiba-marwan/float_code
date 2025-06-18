# till start is pressed statment indicating we are waiting for start 
# start button --> yb3at le el esp eno ybd2 
#till float is out of the water --> statment indicating that its still underwater
#always listen for esp to indicate that its out of the water --> if so pop a statment then 
# plot the values sent by esp
import random
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor
# Matplotlib imports
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PrettyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("float readings")
        self.setFixedSize(800, 600)

        # Nice background
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f4f8"))
        self.setPalette(palette)

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Message label
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.message_label)

        # Label to show statment
        self.label = QLabel("please start calculation", self)
        self.label.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(self.label)


        # Start button with 3 states
        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize(140, 40)
        self.start_button.setStyleSheet(self.button_style())
        self.start_button.clicked.connect(self.handle_button_click)

        # Add button centered
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

         # Matplotlib Figure
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.setLayout(layout)

        # Timer to simulate event delay
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.reset_button)

    def button_style(self):
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                font-size: 16px;
                padding: 8px 16px;
            }
            QPushButton:disabled {
                background-color: #9E9E9E;
            }
            QPushButton:hover:!disabled {
                background-color: #45a049;
            }
        """

    def handle_button_click(self):
        # Change to PENDING state
        self.label.hide()  # Makes it invisible
        self.start_button.setText("Pending...")
        self.start_button.setDisabled(True)
        self.message_label.setText("⏳ Waiting for float to calculate data...")

        # Simulate event duration: 3 seconds
        self.timer.start(3000)

    def reset_button(self):
        # After timer: reset to START state
        self.start_button.setText("Start")
        self.start_button.setDisabled(False)
        self.message_label.setText("✅ Done! Ready to start again.")
        self.plot_data()
        
   

    def plot_data(self):
        # Generate random data
        data = [random.randint(0, 10) for _ in range(10)]

        # Clear previous plot
        self.figure.clear()

        # Create new plot
        ax = self.figure.add_subplot(111)
        ax.plot(data, marker='o')
        ax.set_title("pressure sensor readings")
        ax.set_xlabel("time (seconds) ")
        ax.set_ylabel("pressure (KPa)")
        self.figure.tight_layout()
        # Refresh canvas
        self.canvas.draw()
        self.label.setText("✅ New data plotted!")


# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrettyWindow()
    window.show()
    sys.exit(app.exec())
