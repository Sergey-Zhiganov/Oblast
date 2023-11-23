class Categories:
    def __init__(self, ID_Category, category):
        self.ID_Category = ID_Category
        self.Category = category

def Data(func = 0):
    if func == 0:
        return ['Categories', 'ID', 'Категория']
    else:
        return ['Categories', 'ID', 'Категория'], ['ID_Category', 'Category'], ['категорию'], [1]