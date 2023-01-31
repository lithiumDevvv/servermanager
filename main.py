import paramiko

class Server:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        
    def run_command(self, client, command):
        try:
            client.connect(hostname=self.host, username=self.username, password=self.password)
            stdin, stdout, stderr = client.exec_command(command)
            print(f"Results from server {self.host}:")
            print(stdout.read().decode())
        except paramiko.ssh_exception.AuthenticationException:
            print(f"Could not authenticate to {self.host} with provided credentials")
        except paramiko.ssh_exception.SSHException:
            print(f"Could not connect to {self.host}")
        finally:
            client.close()

class ServerManager:
    def __init__(self, servers=[]):
        self.servers = [Server(server['host'], server['username'], server['password']) for server in servers]
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    def add_server(self, host, username, password):
        self.servers.append(Server(host, username, password))
    
    def remove_server(self, host):
        for index, server in enumerate(self.servers):
            if server.host == host:
                self.servers.pop(index)
                print(f"{host} removed from server list")
                break
        else:
            print(f"{host} not found in server list")
    
    def run_command_on_all(self, command):
        for server in self.servers:
            server.run_command(self.client, command)
    
    def run_command_on_server(self, host, command):
        for server in self.servers:
            if server.host == host:
                server.run_command(self.client, command)
                break
        else:
            print(f"{host} not found in server list")
    
    def display_servers(self):
        print("List of servers:")
        for server in self.servers:
            print(server.host)
        
    def print_help_menu(self):
            print("Enter a number for the corresponding action:")
            print("1. Add a server")
            print("2. Remove a server")
            print("3. Display servers")
            print("4. Run command on all servers")
            print("5. Run command on a specific server")
            print("6. Quit")

servers = [    {'host': 'host1.example.com', 'username': 'user1', 'password': 'password1'},    {'host': 'host2.example.com', 'username': 'user2', 'password': 'password2'},]

manager = ServerManager(servers)
manager.print_help_menu()
while True:
    choice = input("Your choice: ")
    
    if choice == '1':
        host = input("Enter hostname: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        manager.add_server(host, username, password)
    elif choice == '2':
        host = input("Enter hostname to remove: ")
        manager.remove_server(host)
    elif choice == '3':
        manager.display_servers()
    elif choice == '4':
        command = input("Enter command: ")
        manager.run_command_on_all(command)
    elif choice == '5':
        host = input("Enter hostname: ")
        command = input("Enter command: ")
        manager.run_command_on_server(host, command)
    elif choice == '6':
        break
    else:
        print("Invalid choice. Try again.")
