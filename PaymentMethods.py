class PaymentMethods:
    def __init__(self, ID_PaymendMethod, paymendMethod):
        self.ID_PaymentMethod = ID_PaymendMethod
        self.PaymentMethod = paymendMethod

def Data(func = 0):
    if func == 0:
        return ['PaymentMethods', 'ID', 'Способ оплаты']
    else:
        return ['PaymentMethods', 'ID', 'Способ оплаты'], ['ID_PaymentMethod', 'PaymentMethod'], ['способ оплаты'], [1]