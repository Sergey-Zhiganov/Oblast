class Workers:
    def __init__(self, ID_Worker, fullName, position_ID, password):
        self.ID_Worker = ID_Worker
        self.FullName = fullName
        self.Position_ID = position_ID
        self.Password = password

def Data(func = 0):
    if func == 0:
        return ['Workers', 'ID', 'ФИО', 'Должность_ID', 'Пароль']
    else:
        return ['Workers', 'ID', 'ФИО', 'Должность_ID', 'Пароль'], ['ID_Worker', 'FullName', 'Position_ID', 'Password'], ['ФИО', 'ID должности', 'пароль'], [1, 3]