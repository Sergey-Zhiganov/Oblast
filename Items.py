class Items:
    def __init__(self, ID_Item, accountingOfFinance_ID, category_ID, description, price):
        self.ID_Item = ID_Item
        self.AccountingOfFinance_ID = accountingOfFinance_ID
        self.Category_ID = category_ID
        self.Description = description
        self.Price = price

def Data(func = 0):
    if func == 0:
        return ['Items', 'ID', 'Учёт_финансов_ID', 'Категория_ID', 'Описание', 'Цена']
    else:
        return ['Items', 'ID', 'Учёт_финансов_ID', 'Категория_ID', 'Цена'], ['ID_Item', 'AccountingOfFinance_ID', 'Category_ID', 'Description', 'Price'], ['ID записи в учёте финансов (необязательно)', 'ID категории (необязательно)', 'описание','цену'], [1,2,3]