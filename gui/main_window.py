from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QLabel, QPushButton, QLineEdit, QTextEdit
from PySide6.QtGui import QIcon, QPalette, QColor, QFont
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtCore import QUrl
from typing import List
import pyqtgraph as pg
import random as rand
import serial

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

        button1 = QPushButton("Reverse")
        button1.setIcon(QIcon('reverse.png'))
        button1.clicked.connect(self.reverse_leds)
       
        button3 = QPushButton("Send")
        button3.clicked.connect(self.send_input)
        self.line_edit = QLineEdit()
        self.line_edit.setAlignment(Qt.AlignmentFlag.AlignBottom)
        line_edit_label = QLabel("Input:", parent=self.line_edit)
        control_panel_box_layout = QVBoxLayout()
        control_panel_box_layout.setSpacing(5)
        control_panel_box_layout.addWidget(button1,1)
        

        control_panel_box_layout.addStretch()
        control_panel_box_layout.addWidget(line_edit_label)
        control_panel_box_layout.addWidget(self.line_edit, 1)
        control_panel_box_layout.addWidget(button3,1)

        control_panel_box.setLayout(control_panel_box_layout)

        tertiary_layout.addWidget(team_box, 1)
        tertiary_layout.addWidget(control_panel_box,5)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.plotItem.setTitle('Senzor de rotatie')
        #widget senzor temperatura
        self.plot_widget_2 = pg.PlotWidget()
        self.plot_widget_2.plotItem.setTitle('Senzor de temperatura')
        #Am creat un layout de grafice pe care sa il includem in secondary_layout
        plots_layout = QVBoxLayout()
        plots_layout.addWidget(self.plot_widget, 1)
        plots_layout.addWidget(self.plot_widget_2, 1)


        secondary_layout.addLayout(plots_layout, 3)
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
        
        
        
       
       
        self.x_rotation = list(0 for _ in range(100)) 
        self.y_rotation = list(1000 for _ in range(100))  

        self.plot_widget.setYRange(0, 200, padding=0)
        self.penR = pg.mkPen(color=(255, 0, 0))
        self.brushR = pg.mkBrush(QColor(255, 0, 0))
        self.penG = pg.mkPen(color=(255, 255, 0))
        self.brushG = pg.mkBrush(QColor(255, 255, 0))
        self.penB = pg.mkPen(color=(0, 0, 255))
        self.brushB = pg.mkBrush(QColor(0, 0, 255))
        self.data_lineR =  self.plot_widget.scatterPlot(self.x_rotation, self.y_rotation, pen=self.penR,brush=self.brushR)
        self.data_lineG =  self.plot_widget.scatterPlot(self.x_rotation, self.y_rotation, pen=self.penG,brush=self.brushG)
        self.data_lineB =  self.plot_widget.scatterPlot(self.x_rotation, self.y_rotation, pen=self.penB,brush=self.brushB)
      
       

        self.pen2 = pg.mkPen(color=(0, 0, 255))
        self.x_temperature=list(0 for _ in range(100))
        self.y_temperature=list(1000 for _ in range(100))
        self.data_line2 =  self.plot_widget_2.plot(self.x_temperature, self.y_temperature, pen=self.pen2)
        self.plot_widget_2.setYRange(0, 80, padding=0)

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
    
        self.srl=serial.Serial('COM11', 38400)
        self.last='N'
    def alert_temperature(self):
        filename = "alerta.mp3"
        player = QMediaPlayer()
        audio_output = QAudioOutput()
        player.setAudioOutput(audio_output)
        player.setSource(QUrl.fromLocalFile(filename))
        audio_output.setVolume(50)
        player.play()

        QMessageBox.warning(self, 'Alerta Cutremur', 'Activitate seismica, ramaneti calm')
    def reverse_leds(self):
        if self.last=='N':
            self.last='R'
        else:
            self.last='N'

        self.srl.write(self.last.encode())
    def send_input(self):
        input = self.line_edit.text()
        self.line_edit.clear()
        self.text_edit.insertPlainText(f"INPUT: {input}\n")
        
    def update_plot_data(self):
        
         data = self.srl.read(48)

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
        
         self.x_rotation = self.x_rotation[len(result_rotation):]
         for i in result_rotation:
            self.x_rotation.append(self.x_rotation[-1] + 1)

         self.y_rotation = self.y_rotation[len(result_rotation):]
         for i in result_rotation:
            altered= int.from_bytes(i,'big')
            altered=altered/65535
            altered=altered*180
            self.y_rotation.append( altered)
            
        
         self.x_temperature = self.x_temperature[len(result_temp):]
         
         for i in result_temp:
            self.x_temperature.append(self.x_temperature[-1] + 1)

         self.y_temperature = self.y_temperature[len(result_temp):]
         for i in result_temp:
           
            altered= int.from_bytes(i,'big')
            altered=altered/1024
            altered=altered
            if altered>50:
                 self.alert_temperature()
            self.y_temperature.append( altered)
         
         xr=[]
         yr=[]
         xg=[]
         yg=[]
         xb=[]
         yb=[]
         for x,y in zip(self.x_rotation,self.y_rotation):
             if y<60:
                 xr.append(x)
                 yr.append(y)
                 continue
             if y<120:
                 xg.append(x)
                 yg.append(y)
                 continue
             if y<180:
                 xb.append(x)
                 yb.append(y)
                 continue
         
        
       
         self.data_lineR.setData(xr, yr)
         self.data_lineG.setData(xg, yg)
         self.data_lineB.setData(xb, yb)
        
         self.data_line2.setData(self.x_temperature, self.y_temperature)