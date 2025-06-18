import datetime
import sys
#tcp communication function
from communication import talk_to_esp
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
        self.label.hide()  # Makes it invisible
        self.start_button.setText("Pending...")
        self.start_button.setDisabled(True)
        self.message_label.setText("⏳ Waiting for esp to acknoweledge connection")
        if talk_to_esp() == "ACK":
         self.message_label.setText("✅ Done ESP is connected!,⏳ Waiting for float to calculate data...")
        if talk_to_esp() == "TOP":
         self.message_label.setText("✅ Done!,float is out of the water and data will be displayed soon")
         self.reset_button()

    def reset_button(self): 
        self.start_button.setText("Start")
        self.start_button.setDisabled(False)
        self.message_label.setText("✅ Done! Ready to start again.")
        self.plot_data()
        
        
   

    def plot_data(self):
        x_values = [i * 5 for i in range(22)]
        y_values = [0,0.45,1.2,1.6,2.1,2.5,2.6,2.7,2.5,2.4,
                    2.3,2.4,2.5,2.6,2.5,2.4,2.2,1.7,1.1,0.5,0.3,0.1]

        # Clear previous plot
        self.figure.clear()
        # Create new plot
        ax = self.figure.add_subplot(111)
        ax.plot(x_values,y_values, marker='o')
        ax.set_title("pressure sensor readings")
        ax.set_xlabel("time (seconds) ")
        ax.set_ylabel("Depth (meters)")
        self.figure.tight_layout()
        # Refresh canvas
        self.canvas.draw()
        self.label.setText("✅ New data plotted!")
        # Start time
        start_time = datetime.datetime.strptime("00:00:00", "%H:%M:%S")
        interval = datetime.timedelta(seconds=5)

        # Print header-style lines
        for i, depth in enumerate(y_values):
            current_time = start_time + i * interval
            pressure_kpa = depth / 0.102  # approximate for fresh water
            timestamp = current_time.strftime("%-H:%M:%S")  # use %-H to remove leading zeros (Unix/Mac)
            
            print(f"PN01 {timestamp} UTC {pressure_kpa:.1f} kpa {depth:.2f} meters")


# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrettyWindow()
    window.show()
    sys.exit(app.exec())
