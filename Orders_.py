class Orders:
    def __init__(self, ID_Order = None, item_ID = None, client = None, phone = None, paymendMethod_ID = None):
        self.ID_Order = ID_Order
        self.Item_ID = item_ID
        self.Client = client
        self.Phone = phone
        self.PaymentMethod_ID = paymendMethod_ID

def Data(func = 0):
    if func == 0:
        return ['Orders', 'ID', 'Предмет_ID', 'Клиент', 'Телефон', 'Способ_оплаты_ID']
    else:
        return ['Orders', 'ID', 'Предмет_ID', 'Клиент', 'Телефон', 'Способ_оплаты_ID'], ['ID_Order', 'Item_ID', 'Client', 'Phone', 'PaymentMethod_ID'], False, [1, 2, 4, 5]