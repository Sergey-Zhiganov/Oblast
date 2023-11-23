class Companies:
    def __init__(self, ID_Company, company):
        self.ID_Company = ID_Company
        self.Company = company

def Data(func = 0):
    if func == 0:
        return ['Companies', 'ID', 'Компания']
    else:
        return ['Companies', 'ID', 'Компания'], ['ID_Company', 'Company'], ['компанию'], [1]