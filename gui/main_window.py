from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QLabel, QPushButton, QLineEdit, QTextEdit
from PySide6.QtGui import QIcon, QPalette, QColor, QFont
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from typing import List
import pyqtgraph as pg
import random as rand
import serial
def xor_byte_strings(bytes_str1, bytes_str2):
        # Ensure both input strings are of equal length
        if len(bytes_str1) != len(bytes_str2):
         raise ValueError("Input byte strings must have the same length")

        # Perform XOR byte by byte
        result = bytes([a ^ b for a, b in zip(bytes_str1, bytes_str2)])

        return result
class MainWindow(QMainWindow):
    promotie: str = "2023-2024"
    team: List = [
        "MITRAN LUCA",
        "ENACHE STEFAN",
    ]
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Proiect Microprocesoare {self.promotie}")
        self.setWindowIcon(QIcon("./icon.png"))
        

        primary_layout = QVBoxLayout()
        secondary_layout = QHBoxLayout()
        tertiary_layout = QVBoxLayout()

        team_box = QGroupBox("Membrii echipei")
        bold_font = QFont()
        bold_font.setBold(True)
        team_box.setFont(bold_font)

        first_member = QLabel(f"Membru 1: {self.team[0]}")
        second_member = QLabel(f"Membru 2: {self.team[1]}")
        team_box_layout = QVBoxLayout()
        team_box_layout.addWidget(first_member,1)
        team_box_layout.addWidget(second_member,1)
        team_box.setLayout(team_box_layout)

        control_panel_box = QGroupBox("Control Panel")
        control_panel_box.setFont(bold_font)

        button1 = QPushButton("Control 1")
        button2 = QPushButton("Control 2")
        button3 = QPushButton("Send")
        button3.clicked.connect(self.send_input)
        self.line_edit = QLineEdit()
        self.line_edit.setAlignment(Qt.AlignmentFlag.AlignBottom)
        line_edit_label = QLabel("Input:", parent=self.line_edit)
        control_panel_box_layout = QVBoxLayout()
        control_panel_box_layout.setSpacing(5)
        control_panel_box_layout.addWidget(button1,1)
        control_panel_box_layout.addWidget(button2,1)

        control_panel_box_layout.addStretch()
        control_panel_box_layout.addWidget(line_edit_label)
        control_panel_box_layout.addWidget(self.line_edit, 1)
        control_panel_box_layout.addWidget(button3,1)

        control_panel_box.setLayout(control_panel_box_layout)

        tertiary_layout.addWidget(team_box, 1)
        tertiary_layout.addWidget(control_panel_box,5)

        self.plot_widget = pg.PlotWidget()
        

        secondary_layout.addWidget(self.plot_widget, 3)
        secondary_layout.addLayout(tertiary_layout, 1)

        primary_layout.addLayout(secondary_layout, 4)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        debug_box = QGroupBox("Debug")
        debug_box_layout = QVBoxLayout()
        debug_box_layout.addWidget(self.text_edit, 1)
        debug_box.setLayout(debug_box_layout)

        primary_layout.addWidget(debug_box, 1)

        widget = QWidget()
        widget.setLayout(primary_layout)
        
        self.setCentralWidget(widget)
        
        
        
       
       
        self.x_rotation = list(range(100))  # 100 time points
        self.y_rotation = list(range(100))  # 100 data points


        self.pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.plot_widget.plot(self.x_rotation, self.y_rotation, pen=self.pen)

    
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
    

    def send_input(self):
        input = self.line_edit.text()
        self.line_edit.clear()
        self.text_edit.insertPlainText(f"INPUT: {input}\n")
        
    def update_plot_data(self):
         ser = serial.Serial('COM11', 38400)
         data = ser.read(24)

        #  print(data)
        #  result=data.split(b'\x10\x10')
        #  if data[1]!=b'\x10':
        #      result.pop(0)
        #  if data[len(data)-2]!=b'\x10':
        #      result.pop(len(result)-1)
        #  print (result)
         result_rotation=[]
         for i in range(0,len(data)-1):
            if data[i]==0x10 and data[i+1]==0x99:
                if i+3<len(data):
                    byte=data[i+2]*256
                    byte+=data[i+3]
                    byte=byte.to_bytes(2,'big')
                    result_rotation.append(byte)
                i+=4
                continue
         result_temp=[]
         for i in range(0,len(data)-1):
            if data[i]==0x22 and data[i+1]==0x88:
                if i+3<len(data):
                    byte=data[i+2]*256
                    byte+=data[i+3]
                    byte=byte.to_bytes(2,'big')
                    result_temp.append(byte)
                i+=4
                continue
         print(data)
         print(result_rotation)
         self.x_rotation = self.x_rotation[len(result_rotation):]
         for i in result_rotation:
            self.x_rotation.append(self.x_rotation[-1] + 1)

         self.y_rotation = self.y_rotation[len(result_rotation):]
         for i in result_rotation:
            altered= int.from_bytes(i,'big')
            altered=altered/65535
            altered=altered*180
            self.y_rotation.append( altered)
         #random_color = QColor(rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255))

         #self.pen = pg.mkPen(color=random_color)

         # Set the new pen to the data line
         #self.data_line.setPen(self.pen)

         self.data_line.setData(self.x_rotation, self.y_rotation)
