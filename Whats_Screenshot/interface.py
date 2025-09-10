from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QLabel, QVBoxLayout, 
                             QWidget, QLineEdit, QPushButton, QMessageBox, QSystemTrayIcon, 
                             QMenu, QAction, QTextEdit, QGroupBox, QProgressBar)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import automation
import sys

class AutomationThread(QThread):
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(str)

    def __init__(self, website, phone_number, mens):
        super().__init__()
        self.website = website
        self.phone_number = phone_number
        self.mens = mens
    
    def run(self):
        try:
            self.progress.emit("Iniciando automação...")
            automation.run_automation(self.website, self.phone_number, self.mens)
            self.finished.emit(True, "Print enviado com sucesso!")
        except Exception as e:
            self.finished.emit(False, f"Erro ao enviar: {str(e)}")

class WhatsAppAutomationUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initTrayIcon()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("WhatsApp Screenshot Automação")
        self.setGeometry(500, 500, 600, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #25D366;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #128C7E;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)

        # Ícone da janela
        try:
            self.setWindowIcon(QIcon("icon_whats.ico"))
        except:
            pass
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Grupo de configurações
        config_group = QGroupBox("Configurações")
        config_layout = QVBoxLayout()
        
        # Campo do site
        site_layout = QHBoxLayout()
        site_layout.addWidget(QLabel("Site:"))
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("https://exemplo.com")
        #self.website_input.setText("https://")  # Já inicia com https://
        site_layout.addWidget(self.website_input)
        config_layout.addLayout(site_layout)

        # Campo do telefone
        phone_layout = QHBoxLayout()
        phone_layout.addWidget(QLabel("Número:"))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("5511912345678 (com DDD)")
        phone_layout.addWidget(self.phone_input)
        config_layout.addLayout(phone_layout)

        # Campo da mensagem
        msg_layout = QHBoxLayout()
        msg_layout.addWidget(QLabel("Mensagem:"))
        self.mens_input = QLineEdit()
        self.mens_input.setPlaceholderText("Print solicitado")
        self.mens_input.setText("Print solicitado")  # Mensagem padrão
        msg_layout.addWidget(self.mens_input)
        config_layout.addLayout(msg_layout)

        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Área de log
        log_group = QGroupBox("Log de Execução")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

        # Botão de enviar
        self.send_button = QPushButton("🚀 Enviar Print")
        self.send_button.clicked.connect(self.start_automation)
        main_layout.addWidget(self.send_button)

        # Status bar
        self.statusBar().showMessage("Pronto para iniciar")

    def initTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(self)
        if self.tray_icon.isSystemTrayAvailable():
            try:
                self.tray_icon.setIcon(QIcon("icon_whats.ico"))
            except:
                pass

        show_action = QAction("Abrir", self)
        show_action.triggered.connect(self.show)
        quit_action = QAction("Sair", self)
        quit_action.triggered.connect(self.quit_app)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.trayIconClicked)

    def trayIconClicked(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def log_message(self, message):
        self.log_text.append(f"{message}")
        self.statusBar().showMessage(message)
        QApplication.processEvents()  # Atualiza a UI

    def start_automation(self):
        website = self.website_input.text().strip()
        phone = self.phone_input.text().strip()
        mens = self.mens_input.text().strip()

        if not website or not phone:
            QMessageBox.warning(self, "Atenção", "Preencha todos os campos obrigatórios!")
            return

        # Validação básica do URL
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website

        # Validação do número de telefone
        if not phone.startswith('+55'):
            if phone.startswith('55'):
                phone = '+' + phone
            else:
                phone = '+55' + phone
        else:
            pass

        # Remove caracteres não numéricos (exceto +)
        phone = ''.join(c for c in phone if c.isdigit() or c == '+')

        self.send_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.log_text.clear()

        self.automation_thread = AutomationThread(website, phone, mens)
        self.automation_thread.finished.connect(self.automation_finished)
        self.automation_thread.progress.connect(self.log_message)
        self.automation_thread.start()

    def automation_finished(self, sucesso, mens):
        self.send_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        if sucesso:
            QMessageBox.information(self, "Sucesso", mens)
            self.log_message("✅ Processo concluído com sucesso!")
        else:
            QMessageBox.critical(self, "Erro", mens)
            self.log_message("❌ Erro no processo!")

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "WhatsApp Automação",
            "O aplicativo continua em segundo plano. Clique no ícone para abrir.",
            QSystemTrayIcon.Information,
            2000
        )

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Estilo visual melhorado
    app.setStyle('Fusion')
    
    window = WhatsAppAutomationUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()