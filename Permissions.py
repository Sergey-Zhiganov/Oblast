class Permissions:
    def __init__(self, ID_Permission, worker_ID, position_ID, permission, level):
        self.ID_Permission = ID_Permission
        self.Worker_ID = worker_ID
        self.Position_ID = position_ID
        self.Permission = permission
        self.Level = level

def Data(func = 0):
    if func == 0:
        return ['Permissions', 'ID', 'Сотрудник_ID', 'Должность_ID', 'Разрешение', 'Уровень']
    else:
        return ['Permissions', 'ID', 'Сотрудник_ID', 'Должность_ID', 'Разрешение', 'Уровень'], ['ID_Permission', 'Worker_ID', 'Position_ID', 'Permission', 'Level'], ['ID сотрудника (необязательно)', 'ID должности (необязательно)', 'ID разрешения', 'ID уровеня'], [1,2,3,4]