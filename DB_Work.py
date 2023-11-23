import sqlite3, json, TypesOfOperations, Companies, Positions, Workers, Categories, PaymentMethods, AccountingOfFinances, Permissions
import Items, Orders_
from datetime import date
from tabulate import tabulate

def ToFromClass(values, data_table, func = 1):
    return_values = []
    if data_table == 'Orders':
        data_table = 'Orders_'
    for value in values:
        match data_table:
            case 'AccountingOfFinances':
                if func == 1:
                    return_values.append(AccountingOfFinances.AccountingOfFinances(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9]))
                else:
                    return_values.append([value.ID_AccountingOfFinance, value.Data, value.TypeOfOperation_ID, value.Amount, value.Company_ID, value.Client, value.Worker_ID, value.Category_ID, value.PaymentMethod_ID, value.Taxes])
            case 'Categories':
                if func == 1:
                    return_values.append(Categories.Categories(value[0], value[1]))
                else:
                    return_values.append([value.ID_Category, value.Category])
            case 'Companies':
                if func == 1:
                    return_values.append(Companies.Companies(value[0], value[1]))
                else:
                    return_values.append([value.ID_Company, value.Company])
            case 'Items':
                if func == 1:
                    return_values.append(Items.Items(value[0], value[1], value[2], value[3], value[4]))
                else:
                    return_values.append([value.ID_Item, value.AccountingOfFinance_ID, value.Category_ID, value.Description, value.Price])
            case 'Orders_':
                if func == 1:
                    return_values.append(Orders_.Orders(value[0], value[1], value[2], value[3], value[4]))
                else:
                    return_values.append([value.ID_Order, value.Item_ID, value.Client, value.Phone, value.PaymentMethod_ID])
            case 'PaymentMethods':
                if func == 1:
                    return_values.append(PaymentMethods.PaymentMethods(value[0], value[1]))
                else:
                    return_values.append([value.ID_PaymentMethod, value.PaymentMethod])
            case 'Permissions':
                if func == 1:
                    return_values.append(Permissions.Permissions(value[0], value[1], value[2], value[3], value[4]))
                else:
                    return_values.append([value.ID_Permission, value.Worker_ID, value.Position_ID, value.Permission, value.Level])
            case 'Positions':
                if func == 1:
                    return_values.append(Positions.Positions(value[0], value[1], value[2]))
                else:
                    return_values.append([value.ID_Position, value.Position, value.Salary])
            case 'TypesOfOperation':
                if func == 1:
                    return_values.append(TypesOfOperations.TypesOfOperations(value[0], value[1]))
                else:
                    return_values.append([value.ID_TypeOfOperation, value.Operation])
            case 'Workers':
                if func == 1:
                    return_values.append(Workers.Workers(value[0], value[1], value[2], value[3]))
                else:
                    return_values.append([value.ID_Worker, value.FullName, value.Position_ID, value.Password])
    return return_values

def Choice(text, type = 'int'):
    choose = None
    while choose == None:
        try:
            match type:
                case 'int':
                    choose = int(input(text))
                case 'date':
                    choose = date(choose)
            return choose
        except Exception as e:
            print(f'Ошибка: {e}')

def Database():
    global cur, conn
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()

def Execute(execute, func = None):
    try:
        with sqlite3.connect('main.db') as conn:
            cur = conn.cursor()
            data = cur.execute(execute)
        match func:
            case None:
                conn.commit()
                return ('0','0')
            case 'fetchone':
                return data.fetchone()
            case 'fetchall':
                return data.fetchall()
        return ('0','0')
    except Exception as e:
        print('Ошибка:', e)

def Json(current_db, execute, name):
    with open('main.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    data.append([current_db, execute, name])
    with open('main.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def Print_table(data_table, level = 0):
    values = Execute(f"SELECT * FROM {data_table[0]}", 'fetchall')
    values = ToFromClass(values, data_table[0])
    heads_list = data_table[1:]
    if data_table[0] == 'Workers' and level == 1:
        a = 0
        for i in values:
            values[a].Password = 'Скрыто'
            a += 1
    values = ToFromClass(values, data_table[0], 2)
    print(tabulate(values, headers=heads_list))
    if values == []:
        print()
        print('Нет данных')

def Watching(data_table, level, current_db, current_user, name_table, databases, levels):
    while True:
        Database()
        print('-------------------------------------')
        print('Таблица', name_table)
        print()
        Print_table(data_table, level)
        print('-------------------------------------')
        if name_table == 'Заказы':
            Orders(level, current_user)
            return
        print('0. Назад')
        if level > 0:
            print('1. Добавить данные')
            print('2. Редактировать данные')
            print('3. Удалить данные')
            choose_max = 3
            if level == 4:
                print('4. Посмотреть предложенные изменения')
                choose_max = 4
        else:
            choose_max = 0
        choose = None
        while choose == None:
            choose = Choice('Ваш выбор: ')
            if choose >= 0 and choose <= choose_max:
                print('-------------------------------------')
                if choose == 0:
                    return
                elif choose == 4:
                    Changes(current_db)
                else: 
                    data, data_DB, data_use, ints = None, None, None, None
                    select_data = []
                    names_table = []
                    match current_db:
                        case 0:
                            data, data_DB, data_use, ints = TypesOfOperations.Data(1)
                        case 1:
                            data, data_DB, data_use, ints = Companies.Data(1)
                        case 2:
                            data, data_DB, data_use, ints = Positions.Data(1)
                        case 3:
                            select_data = [Execute("SELECT * FROM Positions", 'fetchall')]
                            select_data = [ToFromClass(select_data[0], 'Positions')]
                            names_table = ['Positions']
                            data, data_DB, data_use, ints = Workers.Data(1)
                        case 4:
                            data, data_DB, data_use, ints = Categories.Data(1)
                        case 5:
                            data, data_DB, data_use, ints = PaymentMethods.Data(1)
                        case 6:
                            select_data.append(ToFromClass(Execute("SELECT * FROM TypesOfOperations", 'fetchall'), 'TypesOfOperations'))
                            select_data.append(ToFromClass(Execute("SELECT * FROM Companies", 'fetchall'), 'Companies'))
                            select_data.append(ToFromClass(Execute("SELECT * FROM Workers", 'fetchall'), 'Workers'))
                            select_data.append(ToFromClass(Execute("SELECT * FROM Categories", 'fetchall'), 'Categories'))
                            select_data.append(ToFromClass(Execute("SELECT * FROM PaymendMethods", 'fetchall'), 'PaymendMethods'))
                            names_table = ['TypesOfOperations', 'Companies', 'Workers', 'Categories', 'PaymendMethods']
                            data, data_DB, data_use, ints = AccountingOfFinances.Data(1)
                        case 7:
                            select_data.append(ToFromClass(Execute("SELECT * FROM Workers", 'fetchall'), 'Workers'))
                            select_data.append(ToFromClass(Execute("SELECT * FROM Positions", 'fetchall'), 'Positions'))
                            names_table = ['Workers', 'Positions', None, None]
                            db = []
                            a = 1
                            for i in databases:
                                db.append([a, i])
                                a += 1
                            select_data.append(db)
                            lvl = []
                            a = 1
                            for i in levels:
                                lvl.append([a, i])
                                a += 1
                            select_data.append(lvl)
                            data, data_DB, data_use, ints = Permissions.Data(1)
                        case 8:
                            select_data.append(ToFromClass(Execute("SELECT * FROM AccountingOfFinances", 'fetchall'), 'Items'))
                            select_data.append(ToFromClass(Execute("SELECT * FROM Categories", 'fetchall'), 'Categories'))
                            data, data_DB, data_use, ints = Items.Data(1)
                            names_table = ['AccountingOfFinances', 'Categories']
                    match choose:
                        case 1:
                            Insert(level, current_db, current_user, data, data_DB, data_use, ints, select_data, data_table, names_table)
                        case 2:
                            UpdateOrDelete(1, level, current_db, current_user, data, data_DB, ints, select_data)
                        case 3:
                            UpdateOrDelete(2, level, current_db, current_user, data, data_DB, ints, select_data)
            else:
                print('Неверный выбор')

def Insert(level, current_db, current_user, data, data_DB, data_use, ints, select_data, data_table, names_table):
    values = ''
    count = 2
    foreigns = 0
    for i in data_use:
        if 'ID' in i:
            if data_table[0] == 'Permissions' and foreigns > 1:
                select_data0 = select_data[foreigns]
            else:
                select_data0 = ToFromClass(select_data[foreigns], names_table[foreigns], 2)
            name = names_table[foreigns]
            if name != None:
                select_data0 = [name]
                select_data0 += data
                print()
                Print_table(select_data0, level)
                print()
            else:
                if foreigns == 2:
                    print(tabulate(select_data0, headers=['ID', 'Таблица']))
                else:
                    print(tabulate(select_data0, headers=['ID', 'Уровень']))
            foreigns += 1
        check = False
        while check == False:
            value = input(f'Введите {i}: ')
            if values != '':
                values += ', '
            if (data[0] == 'Permissions' or data[0] == 'Items') and (count == 2 or count == 3) and value == '':
                values += 'Null'
                check = True
            elif ints == None:
                if count == 2:
                    Choice(value, 'date')
                    values += f"'{value}'"
                    check = True
                elif count != 6:
                    try:
                        value = int(value)
                        values += f'{value}'
                        check = True
                    except:
                        print('Ошибка: не число')
                elif (count == 5 or count == 6) and value == '':
                    values += 'Null'
                    check = True
                else:
                    values += f"'{value}'"
                    check = True
            elif count in ints:
                try:
                    value = int(value)
                    values += f'{value}'
                    check = True
                except:
                    print('Ошибка: не число')
            else:
                values += f"'{value}'"
                check = True
        count += 1
    colums = ''
    for i in data_DB:
        if i != data_DB[0]:
            if colums != '':
                colums += ', '
            colums += i
    execute = f"INSERT INTO {data[0]} ({colums}) VALUES ({values})"
    if level > 2:
        Execute(execute)
        print('Правки внесены')
    else:
        print('Ваша правка отправлена на рассмотрение')
        Json(current_db, execute, current_user.name)

def UpdateOrDelete(func, level, current_db, current_user, data, data_DB, ints, select_data):
    a = 0
    for i in data_DB:
        a += 1
        print(f'{a}. {data[a]} ({i})')
    set_list = ''
    if func == 1:
        set = False
        while set == False:
            set_table = Choice('Выберете столбец, в котором отредактировать: ')
            if set_table > 0 and set_table <= a:
                if set_list != '':
                    set_list += ', '
                set_value = input('Введите новое значение: ')
                if select_data == None:
                    if set_table == 2:
                        set_value.format(date)
                        set_value = f"'{set_value}'"
                    elif set_table != 6:
                        set_value = int(set_value)
                    elif set_value == '' and (set_table == 5 or set_table == 6):
                        set_value = f"Null"
                elif set_table in ints:
                    set_value = int(set_value)
                else:
                    set_value = f"'{set_value}'"
                set_list += f"{data_DB[set_table - 1]} = {set_value}"
                set = input('Хотите выбрать ещё столбец? (Введите +, если да): ')
                if set != '+':
                    set = True
            else:
                print('Неверное значение')
    set = input('Нужно ли условие, какие столбцы затронуть? (Введите +, если да): ')
    where_list = ''
    if set == '+':
        set = False
        while set == False:
            where_table = Choice('Выберете столбец для условия: ')
            if where_table > 0 and where_table <= a:
                if where_list != '':
                    where_list += ' AND '
                else:
                    where_list = ' WHERE '
                where_value = input('Введите условие: ')
                where_list += f'{data_DB[where_table - 1]} {where_value}'
                set = input('Хотите ввести ещё условие? (Введите +, если да): ')
                if set != '+':
                    set = True
            else:
                print('Неверное значение')
    if func == 1:
        execute = f"UPDATE {data[0]} SET {set_list}{where_list}"
    else:
        execute = f"DELETE FROM {data[0]}{where_list}"
    if level > 2:
        Execute(execute)
        print('Правки внесены')
    else:
        Json(current_db, execute, current_user.name)
        print('Ваша правка отправлена на рассмотрение')

def Changes(current_db):
    with open('main.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    change_list = []
    print('0. Назад')
    a = 0
    number = 0
    if change_list == []:
        print('Нет предложенных изменений')
    else:
        for i in data:
            if i[0] == current_db:
                a += 1
                print(f'{a}. {i[1]} (Предложил: {i[2]})')
                change_list.append([i[1], number])
            number += 1
    choose = None
    while choose == None:
        choose = Choice('Ваш выбор: ')
        if choose == 0:
            return
        elif choose > a or choose < 0:
            choose = None
        if choose != None:
            accept = None
            while accept == None:
                print('0. Назад')
                print('1. Принять')
                print('2. Отклонить')
                accept = Choice('Ваш выбор: ')
                if accept != 0:
                    if accept == 1:
                        execute = data[choose - 1][1]
                        Execute(execute)
                    data.pop(choose - 1)
                    with open('main.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)
        else:
            print('Неверный выбор')

def Orders(level, current_user):
    data = Execute("SELECT * FROM Orders", 'fetchall')
    ids = []
    if data != []:
        data = ToFromClass(data, 'Orders')
        for i in data:
            ids += [i.ID_Order]
    while True:
        order = None
        while order == None:
            order = Choice('Введите ID заказа или 0 для возврата назад: ')
            if order == 0:
                return
            if order in ids and level > 0:
                item = Execute(f"SELECT * FROM Items WHERE ID_Item = {order}", 'fetchone')
                item = ToFromClass([item], 'Items')[0]
                if item.AccountingOfFinance_ID != None or item.Category_ID != None:
                    print('1. Принять')
                    print('2. Отклонить')
                    choose = None
                    while choose == None:
                        choose = Choice('Ваш выбор: ')
                        match choose:
                            case 1:
                                workers = Execute(f"SELECT * FROM Workers WHERE FullName = '{current_user.name}'", 'fetchone')
                                workers = ToFromClass([workers], 'Workers')[0]
                                if item.Category_ID == None:
                                    accountingOfFinances = Execute(f'''
                                        SELECT AccountingOfFinances.*
                                        FROM Orders
                                        JOIN Items ON Orders.Item_ID = Items.ID_Item
                                        JOIN AccountingOfFinances ON Items.AccountingOfFinance_ID = AccountingOfFinances.ID_AccountingOfFinance
                                    ''', 'fetchone')
                                    print(accountingOfFinances)
                                else:
                                    accountingOfFinances = (None, None, None, None, None, None, None, item.Category_ID, None, None)
                                accountingOfFinances = ToFromClass([accountingOfFinances], 'AccountingOfFinances')[0]
                                Execute(f'''
                                    INSERT INTO AccountingOfFinances(Data, TypeOfOperation_ID, Amount, Client, Phone, Worker_ID, Category_ID, PaymentMethod_ID)
                                    VALUES
                                    ('{date.today()}', 1, {item.Price}, '{data[order - 1].Client}', {data[order - 1].Phone}, {workers.ID_Worker}, {accountingOfFinances.Category_ID}, {data[order - 1].PaymentMethod_ID})
                                ''')
                        Execute(f"DELETE FROM Orders WHERE ID_Order = {order}")
                else:
                    print('Ошибка: предмет неверно оформлен на складе')
            else:
                print('Недопустимое значение')