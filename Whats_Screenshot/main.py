import sys # Sys é usado para manipular o sistema, como argumentos de linha de comando, o seja para obter o caminho do script.
from PyQt5.QtWidgets import QApplication
from interface import WhatsAppAutomatiouUI # Importa a interface gráfica gerada pelo Qt Designer

def main():
    app = QApplication(sys.argv) # Cria uma instância da aplicação Qt, Qt significa que é uma aplicação gráfica.
    window = WhatsAppAutomatiouUI() # Instancia a interface corretamente
    window.show() # Exibe a janela principal da aplicação.
    sys.exit(app.exec_()) # Inicia o loop de eventos da aplicação e garante que a aplicação seja encerrada corretamente ao fechar a janela.

if __name__ == "__main__": # Verifica se o script está sendo executado diretamente.
    main() # Chama a função main para iniciar a aplicação.



