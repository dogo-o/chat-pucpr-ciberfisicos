import socket as sock
import threading

HOST = '127.0.0.1' 
PORTA = 9999 

socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)    
socket_cliente.connect((HOST,PORTA))

#Criamos um loop para envio de dados
print(5*"*" + "INICIANDO CHAT" + 5*"*")

def receber_mensagens():
    while True:
        try:
            mensagem = socket_cliente.recv(1024).decode()
            if mensagem: # se a mensagem nao estiver vazia
                print(mensagem)
            else: 
                break
        except:
            socket_cliente.close()
            break
        
#cria outra thread para RECEBER mensagens enqto ainda pode ENVIAR mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

modo_unicast = False

while True:
    mensagem = input('')
    if mensagem == 'sair':
        socket_cliente.sendall(mensagem.encode()) # envia sair para o servidor
        print("******* Chat terminado *******")
        socket_cliente.close() 
        break  

    if modo_unicast:
        if mensagem == 'sair do unicast':
            modo_unicast = False
            print("Você voltou ao chat público.")
    else:
        if mensagem.startswith('unicast '):
            partes = mensagem.split(' ', 1)
            if len(partes) == 2:
                print('Voce entrou no modo mensagem PRIVADA, digite "sair do unicast" a qualquer momento para sair.')
                modo_unicast = True


            
    socket_cliente.sendall(mensagem.encode()) # envia a mensagem pro servidor tratar independentemente se for broadcast ou unicast
                                              # como trata: A função unicast cria um loop exclusivo para troca de mensagens privadas entre o remetente e o destinatário, quando o servidor entra na função unicast, ele não retorna mais ao loop principal do servidor até que o unicast seja encerrado (com o comando sair do unicast)