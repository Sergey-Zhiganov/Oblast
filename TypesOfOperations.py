class TypesOfOperations:
    def __init__(self, ID_TypeOfOperation, operation):
        self.ID_TypeOfOperation = ID_TypeOfOperation
        self.Operation = operation

def Data(func = 0):
    if func == 0:
        return ['TypesOfOperations', 'ID', 'Операция']
    else:
        return ['TypesOfOperations', 'ID', 'Операция'], ['ID_TypeOfOperation', 'Operation'], ['операцию'], [1]