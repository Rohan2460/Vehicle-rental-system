WINDOWS https://dev.mysql.com/downloads/installer/
LINUX sudo apt install mysql-server

pip install -r requirements.txt
Run setup.py first , then run main.py 


CREATE USER 'admin'@'localhost';
GRANT ALL PRIVILEGES ON \*.\* TO 'admin'@'localhost';


class Field():
    def __set_name__(self, owner, name):
        print(self.__repr__)
        self.query_fetch = f"SELECT {name} FROM {owner.table_name}"
        self.query_store = f"UPDATE {owner.table_name} SET {name}="
        
    def __get__(self,  obj:object, cls):
            print(self.query_fetch)

    def __set__(self, obj:object, data):
        print(self.query_store + str(data))