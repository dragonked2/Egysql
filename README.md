aaaaaaaa
EgySQL is a Python-based command-line tool designed for brute-forcing MySQL servers. It provides a simple yet powerful interface to automate the process of testing multiple username-password combinations against MySQL databases.
Features

<br>

![image](https://github.com/dragonked2/Egysql/assets/66541902/90f11cba-9a3d-43c8-8ba8-099669385bbb)


   EgySQL - MySQL Brute Force Tool

EgySQL is a Python-based command-line tool designed for brute-forcing MySQL servers. It provides a simple yet powerful interface to automate the process of testing multiple username-password combinations against MySQL databases.
Features

    Brute forces MySQL servers to test login credentials.
    Supports scanning a single IP or multiple IPs from a list.
    Utilizes multi-threading for faster execution.
    Performs common vulnerability checks for MySQL servers.
    Provides informative output messages and warnings.

Installation

    Clone the repository:

    bash

git clone https://github.com/dragonked2/Egysql.git

Install the required dependencies:

bash

pip install -r requirements.txt

Run the script:

bash

    python EgySQL.py

Usage

    Choose an option:
        Scan MySQL service on a single IP
        Scan MySQL service on multiple IPs from a list

    Enter the target IP, username, and password list file path.

    Sit back and let EgySQL perform the brute force attack.

Sample Command

bash

python EgySQL.py

Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.
License

This project is licensed under the MIT License - see the LICENSE file for details.
