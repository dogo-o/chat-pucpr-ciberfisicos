import socket as sock
import threading

clientes = {}

def receber_dados(sock_conn, endereco):
    sock_conn.sendall('Informe seu nome para entrar no chat: '.encode())
    nome = sock_conn.recv(50).decode()
    clientes[nome]= sock_conn
    sock_conn.sendall(f'Bem vindo: {nome}'.encode())
    print(f"Conexão com sucesso com {nome} : {endereco}")
    broadcast(f'{nome} entrou no chat.',sock_conn)
    while True:
        try:
            mensagem = sock_conn.recv(1024).decode()
            if mensagem == 'sair': 
                print(f"{nome} saiu do chat.")
                broadcast(f'{nome} saiu do chat.',sock_conn)
                sock_conn.sendall(f'Voce saiu do chat.'.encode())
                del clientes[nome]
                sock_conn.close()
                return
                
            elif mensagem == 'unicast':
                destinatario = sock_conn.recv(1024).decode()
                if destinatario in clientes:
                    sock_conn.sendall(f'Agora você está enviando uma mensagem unicast para {destinatario}.'.encode())
                    unicast(destinatario, nome, sock_conn)
                else:
                    sock_conn.sendall(f'Cliente nao encontrado, voce voltou para o chat publico.'.encode())

            print(f"{nome} >> {mensagem}") # printa no servidor
            broadcast(f"{nome} >> {mensagem}", sock_conn) # o argumento sock_conn eh para garantir que, quem enviou a mensagem nao recebe ela de volta
        except:
            del clientes[nome]
            sock_conn.close()   
            return

def broadcast(mensagem,cliente_q_enviou):
    for cliente in clientes.values():
        if cliente != cliente_q_enviou:
            try:
                cliente.sendall(mensagem.encode())
            except:
                cliente.close()
                del clientes[cliente]

def unicast(destinatario, remetente, sock_conn):
    while True:
        mensagem = sock_conn.recv(1024).decode()
        clientes[destinatario].sendall(f"Mensagem privada de {remetente}: {mensagem}".encode())
        if mensagem == 'sair do unicast':
            break

HOST = '127.0.0.1'
PORTA = 9999

#Criamos o socket do servidor
socket_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
socket_server.bind((HOST,PORTA))
socket_server.listen()

print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

#Cria uma nova thread para cada cliente conectado
while True:
    sock_conn, ender = socket_server.accept()
    thread_cliente = threading.Thread(target=receber_dados, args=[sock_conn, ender])
    thread_cliente.start()
