from orm import Table, Field

class Purchase(Table):
    table_name = "Purchases"
    p_id = Field(int)
    date = Field(int)

class User(Table):
    table_name = "Users"
    name = Field(str, primary_key=True)
    age = Field(int, auto_increment=True)
    phone = Field(int, max=9)
    date = Field(int, foreign_key=Purchase.date)


u = User()
p = Purchase()

u.create_table()