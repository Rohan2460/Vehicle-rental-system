from db import cursor, cnx


class Field:
    name = None
    field_type = None
    max_size = 255
    primary_key = False
    table_name = None
    foreign_key = None
    auto = False

    def __set_name__(self, owner:object, name:str):
        self.name = name
        self.table_name = vars(owner)["table_name"]
        
    def __init__(self, f_type:str|int, max:int=max_size, primary_key:bool=False, foreign_key:object=None, auto_increment:bool=False):
        self.field_type = f_type
        self.max_size = max
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.auto = auto_increment

    def __get__(self,  obj:object, cls):
        return self

    def get(self):
        query = f"{self.name} {'INT' if self.field_type == int else f'VARCHAR ({self.max_size})'}"
        if self.primary_key:
            query += " NOT NULL PRIMARY KEY"
        if self.foreign_key:
            query += f", FOREIGN KEY ({self.name}) REFERENCES {self.foreign_key.table_name}({self.foreign_key.name})"
        if self.auto:
            query += " NOT NULL AUTO_INCREMENT"
        return query


class Table:
    cnx = cnx
    cursor = cursor

    def get_fields(self, as_obj=False) -> list[str | Field]:
        data = []
        for key, value in vars(self.__class__).items():
            if isinstance(value, Field):
                data.append(value if as_obj else key)
        return data
    
    def fetch(self, fields:list=None, condition:str=None, join:str=None, return_as_txt=False) -> list[dict]:   
        data = self.get_fields()
        query = ""
        _fields = []

        if not fields == None:
            if not len(fields) == len(data):
                _fields = [i for i in fields]

        query = ", ".join(_fields)  if _fields else "*"
        query = "SELECT " + query + f" FROM {vars(self.__class__)["table_name"]}"
        if condition:
            query += " WHERE " + condition
        if return_as_txt:
            return query
        
        print("Fetch:", query)
        cursor.execute(query)

        temp_list = []
        for tup in cursor.fetchall():
            temp_dict = {} 
            for val, name in zip(tup, fields if fields else data):
                temp_dict[name] = val
            temp_list.append(temp_dict)
        return temp_list
    
    def raw_fetch(self, statement:str, named:bool=False, fields:list=None):
        print("Raw Fetch:", statement)
        cursor.execute(statement)
        data = self.get_fields()
        data_list = cursor.fetchall()
        if not named:
            return data_list
        
        temp_list = []
        for tup in data_list:
            temp_dict = {} 
            for val, name in zip(tup, fields if fields else data):
                temp_dict[name] = val
            temp_list.append(temp_dict)
        return temp_list

    def raw_store(self, statement:str):
        print("Raw Store:", statement)
        cursor.execute(statement)
        cnx.commit()
    
    def create(self, **query_fields):
        table = vars(self.__class__)["table_name"]
        fields = []
        values = []
        for key, val in query_fields.items():
            fields.append(key)
            values.append(val)

        query = f"INSERT INTO {table} ({", ".join(fields)}) VALUES ({", ".join([f"'{val}'" for val in values])})"
        print("Create:", query)
        cursor.execute(query)
        cnx.commit()

    def update(self, condition:str, **query_fields):
        values = []
        table = vars(self.__class__)["table_name"]
        for key, val in query_fields.items():
            values.append(f"{key}='{val}'")

        query = f"UPDATE {table} SET {", ".join(values)} WHERE {condition}"
        print("Update:", query)
        cursor.execute(query)
        cnx.commit()

    def create_table(self):
        fields = self.get_fields(as_obj=True)
        query = []
        for i in fields:
            query.append(i.get())

        query = f"CREATE TABLE {fields[0].table_name} ({", ".join(query)})"
        print("Create_Table:", query)
        cursor.execute(query)
        cnx.commit()
