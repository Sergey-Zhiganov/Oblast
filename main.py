import json, Workers, user, TypesOfOperations, DB_Work, Companies, Positions, Categories, PaymentMethods
import AccountingOfFinances, Permissions, Items, Orders_
from operator import attrgetter
from tabulate import tabulate
databases = ['Типы операций', 'Компании', 'Должности', 'Сотрудники', 'Категории', 'Способы оплаты', 'Учёт финансов', 'Разрешения', 'Склад', 'Заказы']
levels = ['Посмотр', 'Редактирование с одобрением', 'Редактирование', 'Полный доступ']

def Database():
    DB_Work.Execute('''
        CREATE TABLE IF NOT EXISTS TypesOfOperations(
            ID_TypeOfOperation INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Operation varchar(30) not null UNIQUE
        )
    ''')
    DB_Work.Execute('''
        CREATE TABLE IF NOT EXISTS Companies(
            ID_Company INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Company varchar(30) not null UNIQUE
        )
    ''')
    DB_Work.Execute('''
        CREATE TABLE IF NOT EXISTS Positions(
            ID_Position INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Position varchar(50) not null UNIQUE,
            Salary int not null,
            CONSTRAINT CN_Salary CHECK (Salary > 0)
        )
    ''')
    DB_Work.Execute('''
        CREATE TABLE IF NOT EXISTS Workers(
            ID_Worker INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            FullName varchar(30) not null UNIQUE,
            Position_ID int not null,
            Password varchar(30) not null,
            FOREIGN KEY (Position_ID) REFERENCES Positions(ID_Position) ON UPDATE CASCADE
        )
    ''')
    DB_Work.Execute('''
        CREATE TABLE IF NOT EXISTS Categories(
            ID_Category INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Category varchar(30) not null UNIQUE
        )
    ''')
    DB_Work.Execute('''
        CREATE TABLE IF NOT EXISTS PaymentMethods(
            ID_PaymentMethod INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            PaymentMethod varchar(40) not null UNIQUE
        )
    ''')
    DB_Work.Execute('''
        CREATE TABLE IF NOT EXISTS AccountingOfFinances(
            ID_AccountingOfFinance INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Data DATE NOT NULL,
            TypeOfOperation_ID INTEGER NOT NULL,
            Amount INTEGER NOT NULL,
            Company_ID INTEGER,
            Client varchar(30),
            Phone integer,
            Worker_ID INTEGER NOT NULL,
            Category_ID INTEGER NOT NULL,
            PaymentMethod_ID INTEGER NOT NULL,
            Taxes INTEGER,
            FOREIGN KEY (TypeOfOperation_ID) REFERENCES TypesOfOperations(ID_TypeOfOperation) ON UPDATE CASCADE,
            CONSTRAINT CN_Amount CHECK (Amount > 0),
            FOREIGN KEY (Company_ID) REFERENCES Companies(ID_Company) ON UPDATE CASCADE,
            FOREIGN KEY (Worker_ID) REFERENCES Workers(ID_Worker) ON UPDATE CASCADE,
            FOREIGN KEY (Category_ID) REFERENCES Categories(ID_Category) ON UPDATE CASCADE,
            FOREIGN KEY (PaymentMethod_ID) REFERENCES PaymentMethods(ID_PaymentMethod) ON UPDATE CASCADE
        )
    ''')
    DB_Work.Execute(''' 
        CREATE TABLE IF NOT EXISTS Permissions(
            ID_Permission integer primary key autoincrement UNIQUE,
            Worker_ID int,
            Position_ID int,
            Permission int not null,
            Level int not null,
            FOREIGN KEY (Worker_ID) REFERENCES Workers(ID_Worker) ON UPDATE CASCADE,
            FOREIGN KEY (Position_ID) REFERENCES Positions(ID_Position) ON UPDATE CASCADE,
            CONSTRAINT CN_Permission CHECK (10 >= Permission > 0),
            CONSTRAINT CN_Level CHECK (4 >= Level > 0)
        )
    ''')
    DB_Work.Execute('''
        CREATE TABLE IF NOT EXISTS Items(
            ID_Item integer primary key autoincrement UNIQUE,
            AccountingOfFinance_ID integer UNIQUE,
            Category_ID integer,
            Description varchar(60),
            Price integer not null,
            FOREIGN KEY (AccountingOfFinance_ID) REFERENCES AccountingOfFinances(ID_AccountingOfFinance) ON UPDATE CASCADE,
            FOREIGN KEY (Category_ID) REFERENCES Categories(ID_Category) ON UPDATE CASCADE
        )
    ''')
    DB_Work.Execute('''
        CREATE TABLE IF NOT EXISTS Orders(
            ID_Order integer primary key autoincrement unique,
            Item_ID integer unique not null,
            Client varchar(30) not null,
            Phone integer not null,
            PaymentMethod_ID INTEGER NOT NULL,
            FOREIGN KEY (Item_ID) REFERENCES Items(Item_ID) ON UPDATE CASCADE,
            FOREIGN KEY (PaymentMethod_ID) REFERENCES PaymentMethods(ID_PaymentMethod) ON UPDATE CASCADE
        )
    ''')

def Autorization():
    global current_user
    while True:
        workers_list = DB_Work.Execute("SELECT * FROM Workers", 'fetchall')
        workers = []
        if workers_list != []:
            workers = DB_Work.ToFromClass(workers_list, 'Workers')
        with open('admin.json', 'r') as file:
            admin = json.load(file)
        auto = False
        while auto == False:
            print('Для выхода из программы, нажмите enter. Для входа в аккаунт гостя, введите "guest"')
            fullname = input('Введите ФИО: ')
            if fullname == 'guest':
                Guest()
            elif fullname != '':
                password = input('Введите пароль: ')
                if (fullname != admin['name'] or password != admin['password']) and workers != []:
                    for i in workers:
                        if i.FullName == fullname and i.Password == password:
                            positions = DB_Work.Execute('''
                                SELECT Positions.*
                                FROM Workers
                                JOIN Positions ON Workers.Position_ID = Positions.ID_Position
                                ''', 'fetchone')
                            positions = DB_Work.ToFromClass([positions], 'Positions')[0]
                            current_user = user.User(fullname, positions.Position, positions.ID_Position)
                            auto = True
                elif workers == [] and (fullname != admin['name'] or password != admin['password']):
                    pass
                else:
                    current_user = user.User('admin', 'admin', 0)
                    auto = True
                if auto == False:
                    print('Неверное ФИО или пароль')
                else:
                    User()
                    auto = True
            else:
                return

def User():
    global current_db
    print(f'Пользователь: {current_user.name} | Должность: {current_user.position}')
    while True:
        if current_user.name != 'admin':
            workers = DB_Work.Execute(f"SELECT * FROM Workers WHERE FullName = '{current_user.name}'", 'fetchone')
            worker = DB_Work.ToFromClass([workers], 'Workers')[0]
            permissions = DB_Work.Execute(f'''
                SELECT Permissions.*
                FROM Workers
                JOIN Permissions ON Permissions.Worker_ID = Workers.ID_Worker OR Permissions.Position_ID = Workers.Position_ID
                WHERE ID_Worker = {worker.ID_Worker} OR Workers.Position_ID = {worker.Position_ID}
            ''','fetchall')
            permissions = DB_Work.ToFromClass(permissions, 'Permissions')
            subdata = []
            data0 = []
            a = 0
            for i in permissions:
                if i not in data0:
                    data0.append(i.Permission)
                    subdata.append(i)
                elif i.Level > subdata[a].Level:
                    subdata[a].Level = i
                a += 1
            data = sorted(subdata, key=attrgetter('Permission'))
        else:
            data0 = [1,2,3,4,5,6,7,8,9,10]
            data = [[None, None, None, 1,4], [None, None, None, 2,4], [None, None, None, 3,4], [None, None, None, 4,4], [None, None, None, 5,4], [None, None, None, 6,4], [None, None, None, 7,4], [None, None, None, 8,4], [None, None, None, 9,4], [None, None, None, 10,1]]
            data = DB_Work.ToFromClass(data, 'Permissions')
        print('0. Выйти из аккаунта')
        if data == []:
            print('У вас нет разрешений. Обратитесь к администратору для выдачи разрешений')
        else:
            for i in data:
                print(f'{i.Permission}. {databases[i.Permission-1]} ({levels[i.Level-1]})')
        if current_user.position_id == 0:
            print('11. Сменить имя пользователя и пароль')
        current_db = DB_Work.Choice('Ваш выбор: ')
        if current_user.position_id == 0 and current_db == 11:
            ChangeAdmin()
            current_db = 0
        if current_db == 0:
            return
        if current_db in data0:
            current_db -= 1
            data_table = 0
            match current_db:
                case 0:
                    data_table = TypesOfOperations.Data()
                case 1:
                    data_table = Companies.Data()
                case 2:
                    data_table = Positions.Data()
                case 3:
                    data_table = Workers.Data()
                case 4:
                    data_table = Categories.Data()
                case 5:
                    data_table = PaymentMethods.Data()
                case 6:
                    data_table = AccountingOfFinances.Data()
                case 7:
                    data_table = Permissions.Data()
                case 8:
                    data_table = Items.Data()
                case 9:
                    data_table = Orders_.Data()
            for i in data:
                if current_db + 1 == i.Permission:
                    level = i
            DB_Work.Watching(data_table, level.Level, current_db, current_user, databases[current_db], databases, levels)
        else:
            current_db = None
            print('Неверная функция')

def ChangeAdmin():
    name = input('Введите новое имя: ')
    password = input('Введите новый пароль: ')
    with open('admin.json', 'w') as file:
        json.dump({'name': name, 'password': password}, file)

def Guest():
    print('Пользователь: Гость')
    while True:
        data = DB_Work.Execute('''
            SELECT Items.ID_Item, Items.Description, Categories.Category, Items.Price
            FROM Items
            JOIN Categories ON Items.Category_ID = Categories.ID_Category
            UNION
            SELECT Items.ID_Item, Items.Description, Categories.Category, Items.Price
            FROM Items
            JOIN AccountingOfFinances ON Items.AccountingOfFinance_ID = AccountingOfFinances.ID_AccountingOfFinance
            JOIN Categories ON AccountingOfFinances.Category_ID = Categories.ID_Category
        ''', 'fetchall')
        if data == []:
            print('Нет товара на продажу')
            return
        headers = ['ID', 'Описание', 'Категория', 'Цена']
        print()
        print(tabulate(data, headers=headers))
        print()
        while True:
            ids = []
            for i in data:
                ids.append(i[0])
            order = Orders_.Orders()
            order.Item_ID = DB_Work.Choice('Введите ID товара, который хотите купить: ')
            if order.Item_ID in ids:
                order.Client = input('Введите ваше ФИО в формате "Фамилия И. О.": ')
                order.Phone = DB_Work.Choice("Введите ваш номер телефона (только цифры): ")
                pm_data = DB_Work.Execute("SELECT * FROM PaymentMethods", 'fetchall')
                if pm_data == []:
                    print('Ошибка: обратитесь к сотруднику (не занесены способы оплаты)')
                    return
                pm_data = DB_Work.ToFromClass(pm_data, 'PaymentMethods')
                ids = []
                for i in pm_data:
                    ids.append(i.ID_PaymentMethod)
                headers = ['ID', 'Спопоб оплаты']
                pm_data = DB_Work.ToFromClass(pm_data, 'PaymentMethods', 2)
                print()
                print(tabulate(pm_data, headers=headers))
                print()
                while order.PaymentMethod_ID == None:
                    order.PaymentMethod_ID = DB_Work.Choice("Ваш выбор: ")
                    if order.PaymentMethod_ID in ids:
                        DB_Work.Execute(f"INSERT INTO Orders(Item_ID, Client, Phone, PaymentMethod_ID) VALUES ({order.Item_ID}, '{order.Client}', {order.Phone}, {order.PaymentMethod_ID})")
                        print('Ваш заказ создан. Ожидайте, с вами свяжутся')
                        return
                    else:
                        order.PaymentMethod_ID = None
                        print('Неверный выбор')
            else:
                print('Товар не найден')
            

try:
    with open('main.json', 'x'):
        pass
    with open('main.json', 'w') as file:
        json.dump([], file)
except:
    pass

try:
    with open('admin.json', 'x'):
        pass
    with open('admin.json', 'w') as file:
        json_input = {'name': 'admin', 'password': 'admin'}
        json.dump(json_input, file)
except:
    pass

Database()
Autorization()