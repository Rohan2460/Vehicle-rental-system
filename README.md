WINDOWS https://dev.mysql.com/downloads/installer/
LINUX sudo apt install mysql-server

pip install -r requirements.txt
Run setup.py first , then run main.py 


CREATE USER 'admin'@'localhost';
GRANT ALL PRIVILEGES ON \*.\* TO 'admin'@'localhost';
