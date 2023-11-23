class Positions:
    def __init__(self, ID_Position, position, salary):
        self.ID_Position = ID_Position
        self.Position = position
        self.Salary = salary

def Data(func = 0):
    if func == 0:
        return ['Positions', 'ID', 'Должность', 'Зарплата']
    else:
        return ['Positions', 'ID', 'Должность', 'Зарплата'], ['ID_Position', 'Position', 'Salary'], ['должность', 'зарплату'], [1, 3]