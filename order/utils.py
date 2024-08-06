import datetime

def get_order_number(pk):
    ord_num = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    order_number = ord_num + str(pk)
    return order_number