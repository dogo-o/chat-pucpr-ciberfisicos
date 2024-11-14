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
            socket_cliente.sendall(mensagem.encode())
            continue
        socket_cliente.sendall(mensagem.encode())  # Envia a mensagem privada para o destinatário escolhido
    else:
        socket_cliente.sendall(mensagem.encode()) # envia msg
        if mensagem == 'unicast' and not modo_unicast:
            modo_unicast = True
            destinatario = input(f"Digite o nome do destinatário: ")
            socket_cliente.sendall(destinatario.encode())  # Envia o nome do destinatário ao servidor