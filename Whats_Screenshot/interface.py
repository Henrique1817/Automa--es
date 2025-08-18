from PyQt5.QtWidgets import (QApplication,QMainWindow, QHBoxLayout, QLabel, QVBoxLayout, QWidget, QLineEdit,
                             QPushButton, QMessageBox, QSystemTrayIcon, QMenu, QAction)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
import automation
import sys

# Durante todo o código o termo "self" é usado para referenciar a instância atual da classe, permitindo acessar seus atributos e métodos.

class automatcThread(QThread):
    finished = pyqtSignal(bool, str) # Sinal para indicar que a automação foi concluída

    def __init__(self, website, phone_number):
        super().__init__() # Inicializa a classe base QThread
        self.website = website
        self.phone_number = phone_number
    
    # self.run() é o método que será executado quando o thread for iniciado. Self é uma referência à instância atual da classe, permitindo acessar seus atributos e métodos.
    def run(self):
        try:
            automation.run_automation(self.website, self.phone_number) # Chama a função de automação com os parâmetros fornecidos
            self.finished.emit(True, "Print enviado com sucesso") # Emite o sinal
        except Exception as e:
            self.finished.emit (False, f"Erro ao enviar: {str(e)}") # Emite o sinal com erro; o "e" é a exceção capturada, e "str(e)" converte a exceção em uma string para exibição.
        
class WhatsAppAutomatiouUI(QMainWindow): # Classe principal da interface gráfica, herda de QMainWindow
    def __init__(self):
        super().__init__() # Inicializa a classe base QMainWindow
        self.initUI() # Chama o método para inicializar a interface do usuário
        self.initTrayIcon() # Inicializa o ícone da bandeja do sistema
        
    def initUI(self): # Método para configurar a interface do usuário
        self.setWindowTitle("WhatsApp Screenshot Automação") # Define o título da janela
        self.setGeometry(300, 300, 400, 200) # Define a geometria da janela (x, y, largura, altura)

        # Icone da janela
        try:
            self.setWindowIcon(QIcon("icon_whats.ico"))
        except:
            pass
        
        # Layout principal
        layout = QVBoxLayout()

        center_widget = QWidget() # Cria um widget central
        self.setCentralWidget(center_widget) # Define o widget central da janela

        # Layout principal
        layout = QVBoxLayout() # Cria um layout vertical para o widget central

        # Campo de entrada para o site
        website_layout = QHBoxLayout() # Cria um layout horizontal para o campo de entrada do site
        website_layout.addWidget(QLabel("Site:")) # Adiciona um rótulo ao layout
        self.website_input = QLineEdit() # Cria um campo de entrada de texto para o site
        self.website_input.setPlaceholderText("exemplo.com") # Define um texto de espaço reservado
        website_layout.addWidget(self.website_input)
        layout.addLayout(website_layout)

        # Campo de entrada para o número de telefone
        phone_layout = QHBoxLayout()
        phone_layout.addWidget(QLabel("Número de Telefone:"))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("5511912345678")
        phone_layout.addWidget(self.phone_input)
        layout.addLayout(phone_layout)

        # Botão para enviar 

        self.send_button = QPushButton("Enviar Print")
        self.send_button.clicked.connect(self.start_automation) # Conecta o botão ao método de automação
        layout.addWidget(self.send_button)

        # Configura o layout do widget central
        center_widget.setLayout(layout)


    def initTrayIcon(self): # Método para inicializar o ícone da bandeja do sistema
        self.tray_icon = QSystemTrayIcon(self)
        if self.tray_icon.isSystemTrayAvailable(): # Verifica se a bandeja do sistema está disponível
            self.tray_icon.setIcon(QIcon("icon_whats.icoo")) # Define o ícone da bandeja do sistema 
        else:
            pass

        show_action = QAction("Abrir", self)
        show_action.triggered.connect(self.show)

        quit_action = QAction("Sair", self)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.tray_icon.activated.connect(self.trayIconClicked)

    def trayIconClicked (self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def start_automation(self):
        website = self.website_input.text().strip()
        phone = self.phone_input.text().strip()

        if not website or not phone:
            QMessageBox.warning(self, "Atenção", "É necessário preencher todos os campos!")
            return

        # Garante que o número está no formato internacional
        if not phone.startswith("+"):
            phone = "+" + phone
        
        if not website.startswith("https://"):
            website = "https://www." + website

        self.send_button.setEnabled(False)
        self.send_button.setText("Processando...")

        self.automation_thread = automatcThread(website, phone)
        self.automation_thread.finished.connect(self.automation_finished)
        self.automation_thread.start()

    def automation_finished(self, sucesso, menssagem):
        self.send_button.setEnabled(True)
        self.send_button.setText("Enviar Print")

        if sucesso:
            QMessageBox.information(self, "Sucesso", menssagem)
        else:
            QMessageBox.critical(self, "Erro", menssagem)       

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        QMessageBox.information(self, "Aviso", "O aplicativo continua rodando em segundo plano, caso queira finalizar, clique no icone 'Sair' da bandeja")


