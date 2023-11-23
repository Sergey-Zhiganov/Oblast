class AccountingOfFinances:
    def __init__(self, ID_AccountingOfFinance, data, typeOfOperation_ID, amount, company_ID, client, worker_ID, category_ID, paymendMethod_ID, taxes):
        self.ID_AccountingOfFinance = ID_AccountingOfFinance
        self.Data = data
        self.TypeOfOperation_ID = typeOfOperation_ID
        self.Amount = amount
        self.Company_ID = company_ID
        self.Client = client
        self.Worker_ID = worker_ID
        self.Category_ID = category_ID
        self.PaymentMethod_ID = paymendMethod_ID
        self.Taxes = taxes

def Data(func = 0):
    if func == 0:
        return ['AccountingOfFinances', 'ID', 'Дата', 'Тип_операции_ID', 'Сумма', 'Компания_ID', 'Клиент', 'Сотрудник_ID', 'Категория_ID', 'Способ оплаты_ID', 'Налог']
    else:
        return ['AccountingOfFinances', 'ID', 'Дата', 'Тип_операции_ID', 'Сумма', 'Компания_ID', 'Клиент', 'Сотрудник_ID', 'Категория_ID', 'Способ оплаты_ID', 'Налог'], ['ID_AccountingOfFinance', 'Data', 'TypeOfOperation_ID', 'Amount', 'Company_ID', 'Client', 'Worker_ID', 'Category_ID', 'PaymentMethod_ID', 'Taxes'], ['дату (ДД.ММ.ГГГГ)', 'ID типа операции', 'сумму', 'ID компании (необязательно)', 'клиента (необязательно)', 'ID сотрудника', 'ID категории', 'ID способа оплаты', 'налог'], None