import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QFont

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        
        self.lbl_system_1 = QLabel(self)
        self.lbl_system_1.move(30, 20)
        self.lbl_system_1.setFont(QFont("Arial", 14))
        self.lbl_system_1.setText("x\' = 16 - (3x - y)^2")
        
        self.lbl_system_2 = QLabel(self)
        self.lbl_system_2.move(30, 40)
        self.lbl_system_2.setFont(QFont("Arial", 14))
        self.lbl_system_2.setText("y\' = (x - 3y)^2 - 16")
        
        self.text_label = QLabel(self)
        self.text_label.move(10, 70)
        self.text_label.setFont(QFont("Arial", 10))
        self.text_label.setText("За замовчуванням коефіцієнти "+
                                "alpha = 10^(-2)")
        
        self.text_label = QLabel(self)
        self.text_label.move(10, 100)
        self.text_label.setFont(QFont("Arial", 10))
        self.text_label.setText("Змінювати alpha за законом: ")
        
        self.combo = QComboBox(self)
        self.combo.addItem("Не змінювати", 0)
        self.combo.addItem("Різниця відстаней", 1)
        self.combo.addItem("Експоненційний", 2)
        self.combo.move(185, 98)
        self.combo.setCurrentIndex(0)

        button_1 = QPushButton("Побудувати фазовий\nпортрет", self)
        button_1.resize(120, 40)
        button_1.move(30, 140)
        button_1.clicked.connect(self.plot_the_whole_portrait)
        
        button_2 = QPushButton("Задати початкову\nточку", self)
        button_2.resize(120, 40)
        button_2.move(160, 140)
        button_2.clicked.connect(self.plot_phase_line)

        self.setGeometry(150, 150, 310, 200)
        self.setWindowTitle('Фазові портрети')
        self.show()
        
    def plot_the_whole_portrait(self):
        P = lambda x, y: 16 - (3*x - y)**2
        Q = lambda x, y: (x - 3*y)**2 - 16
        
        coords = []
        xs = np.arange(-4, 4.2, 0.2)
        ys = np.arange(-4, 4.2, 0.2)
        for i in xs:
            for j in ys:
                coords.append((i,j))
    
        xs = np.arange(-1.1, -0.92, 0.02)
        ys = np.arange(0.9, 1.12, 0.02)
        for i in xs:
            for j in ys:
                coords.append((i,j))
                
        x = []
        y = []
        k = 0
        
        choise = self.combo.currentIndex()

        for x0, y0 in coords:
            if ((x0,y0) == (-2,-2) or (x0,y0) == (-1,1) or
                (x0,y0) == (1,-1) or (x0,y0) == (2,2)):
                continue
            x.append([x0])
            y.append([y0])
            i = 0
            alpha = 10**(-2)

            while i < 100:
                V_x = P(x[k][i], y[k][i])
                V_y = Q(x[k][i], y[k][i])
              
                V_x_normed = V_x / np.sqrt(V_x**2 + V_y**2)
                V_y_normed = V_y / np.sqrt(V_x**2 + V_y**2)
                
                if choise == 1:
                    if i >= 2:
                        coord1 = np.array([x[k][i-2], y[k][i-2]])
                        coord2 = np.array([x[k][i-1], y[k][i-1]])
                        coord3 = np.array([x[k][i], y[k][i]])
                        alpha = self.normed_alpha(alpha, coord1,
                                                  coord2, coord3)
                elif choise == 2:
                    if i >= 1:
                        alpha = self.exponential_alpha(alpha, x[k][i],
                                                       y[k][i], x[k][i-1],
                                                       y[k][i-1])
                    
                x[k].append(x[k][i] + alpha*V_x_normed)
                y[k].append(y[k][i] + alpha*V_y_normed)

                i += 1
   
            k += 1
            
        plt.figure(figsize=(15, 8))
        for i in range(k):
            plt.plot(x[i], y[i], 'b-', linewidth=0.5)
  
        plt.grid(True)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.xticks(np.arange(-4, 4.5, 0.5))
        plt.yticks(np.arange(-4, 4.5, 0.5))
        plt.axis([-4, 4, -4, 4])
        plt.show()
        
    def plot_phase_line(self):
        P = lambda x, y: 16 - (3*x - y)**2
        Q = lambda x, y: (x - 3*y)**2 - 16
        
        x0, _ = QInputDialog.getDouble(self, 'Input Dialog', 'x0 = ',
                                       decimals=5)
        y0, _ = QInputDialog.getDouble(self, 'Input Dialog', 'y0 = ',
                                       decimals=5)
        N, _ = QInputDialog.getInt(self, 'Input Dialog', 'Кількість ітерацій')
        
        x = [x0]
        y = [y0]
        alpha = 10**(-2)
        choise = self.combo.currentIndex()
        
        for i in range(N):
            V_x = P(x[i], y[i])
            V_y = Q(x[i], y[i])
              
            V_x_normed = V_x / np.sqrt(V_x**2 + V_y**2)
            V_y_normed = V_y / np.sqrt(V_x**2 + V_y**2)
            
            if choise == 1:
                if i >= 2:
                    coord1 = np.array([x[i-2], y[i-2]])
                    coord2 = np.array([x[i-1], y[i-1]])
                    coord3 = np.array([x[i], y[i]])
                    alpha = self.normed_alpha(alpha, coord1,
                                                  coord2, coord3)
            elif choise == 2:
                if i >= 1:
                    alpha = self.exponential_alpha(alpha, x[i],
                                                   y[i], x[i-1],
                                                   y[i-1])
                    
            x.append(x[i] + alpha*V_x_normed)
            y.append(y[i] + alpha*V_y_normed)
            
        plt.figure(figsize=(15, 8))
        plt.plot(x, y, 'b-')
        plt.grid(True)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()
        
    def exponential_alpha(self, alpha, x1, y1, x2, y2):
        return alpha*np.exp((x2-x1)**2 + (y2-y1)**2)
    
    def normed_alpha(self, alpha, coord1, coord2, coord3):
        return(alpha + np.linalg.norm(coord3-coord2) -
               np.linalg.norm(coord2-coord1))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())