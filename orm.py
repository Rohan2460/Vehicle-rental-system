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
        self.table_name = owner.__name__
        
    def __init__(self, f_type:str|int, max:int=max_size, primary_key:bool=False, foreign_key:object=None, auto_increment:bool=False):
        self.field_type = f_type
        self.max_size = max
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.auto = auto_increment

    def __get__(self,  obj:object, cls):
        return self

    def get(self):
        query = f"{self.name} {'INT' if self.field_type == int else 'VARCHAR'}({self.max_size})"
        if self.primary_key:
            query += " PRIMARY KEY"
        if self.foreign_key:
            query += f" FOREIGN KEY REFERENCES {self.foreign_key.table_name}({self.foreign_key.name})"
        if self.auto:
            query += " AUTO_INCREMENT"
        return query



class Table:

    def get_fields(self, as_obj=False) -> list[str | Field]:
        data = []
        for key, value in vars(self.__class__).items():
            if isinstance(value, Field):
                data.append(value if as_obj else key)
        return data
    
    def fetch(self, fields=None):        
        data = self.get_fields()
        query = ""
        _fields = []

        if not fields == None:
            if not len(fields) == len(data):
                for i in fields:
                    _fields.append(i)
                _fields

        query = ", ".join(_fields)  if _fields else "*"
        query = "SELECT " + query + f" FROM {vars(self.__class__)["table_name"]}"

        print("Fetched:", query)

    def create(self, **query_fields):
        table = vars(self.__class__)["table_name"]
        fields = []
        values = []
        for key, val in query_fields.items():
            fields.append(key)
            values.append(val)

        query = f"INSERT INTO {table} ({", ".join(fields)}) VALUES ({", ".join([f"'{val}'" for val in values])})"
        print(query)

    def update(self, condition, **query_fields):
        values = []
        table = vars(self.__class__)["table_name"]
        for key, val in query_fields.items():
            values.append(f"'{key}'='{val}'")

        query = f"UPDATE {table} SET {", ".join(values)} WHERE {condition}"
        print(query)

    def create_table(self):
        fields = self.get_fields(as_obj=True)
        query = []
        for i in fields:
            query.append(i.get())

        query = f"CREATE TABLE {fields[0].table_name} ({", ".join(query)})"
        print(query)

