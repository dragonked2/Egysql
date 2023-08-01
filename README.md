EgySQL is a powerful and flexible multi-service brute force tool designed to help you test the security of your services and ensure the strength of your passwords. With support for various popular services, including MongoDB, MySQL, MSSQL, SQLite, SSH, FTP, and RDP, EgySQL is a one-stop solution for security professionals, system administrators, and ethical hackers.
Features
<br>
![image](https://github.com/dragonked2/Egysql/assets/66541902/90f11cba-9a3d-43c8-8ba8-099669385bbb)


    Multi-Service Support: Brute force passwords for MongoDB, MySQL, MSSQL, SQLite, SSH, FTP, and RDP.
    Connection Check: Ensure the target service is reachable before starting the brute force.
    Password List: Load your custom password list for targeted and efficient brute forcing.
    Verbose Mode: Enable verbose mode to see detailed progress and results.
    User-Friendly Interface: An interactive command-line interface using curses library for ease of use.

How to Use

    Clone the repository:


git clone https://github.com/dragonked2/Egysql.git
cd egysql

    Install the required dependencies:

pip install paramiko pyodbc pymongo mysql-connector-python windows-curses

    Run the EgySQL script:

python egysql.py

    Choose the service you want to brute force by selecting the corresponding number.

    Enter the target host, username, and the path to your password list file.

    Optionally, enable verbose mode to get detailed feedback during the brute force process.

Example Usage

Here's an example of how you can use EgySQL to perform a brute force attack against a MongoDB service:

markdown

[*] Welcome to EgySQL - The Ultimate Multi-Service Brute Force Tool
[*] AliElTop 1.0
Choose a service to bruteforce:
1. MongoDB
2. MySQL
3. MSSQL
4. SQLite (not ready yet)
5. SSH
6. FTP
7. RDP (not ready yet)
Q. Quit

Enter your choice: 1

You chose MongoDB.

Enter the target host: example.com
Enter the username: admin
Enter the password list file path: passwords.txt
Enable verbose mode? (Y/N): N

[*] Starting MongoDB bruteforce for admin@example.com...

[+] Successfully logged in with credentials: admin:strongPassword123

Disclaimer

EgySQL is intended for legal and ethical use only. The authors are not responsible for any illegal use or damage caused by this tool. Always ensure you have proper authorization to perform any security testing or password brute force attacks.
Contributions

Contributions to EgySQL are welcome! If you find a bug or want to add support for additional services, feel free to create a pull request. Let's work together to make EgySQL even better!
License

EgySQL is licensed under the MIT License. See LICENSE for more information.

Get ready to secure your services with EgySQL!
