import os
from datetime import datetime

from huobi.client.trade import TradeClient
from huobi.constant import *
from huobi.utils import *


access_key = os.environ.get('ACCESS_KEY')
secret_key = os.environ.get('SECRET_KEY')
assert access_key and secret_key, 'ACCESS_KEY or SECRET_KEY env variables not found'
trade_client = TradeClient(api_key=access_key, secret_key=secret_key, init_log=True)

def build_notification_text(order_obj) -> str:
    """
    Build notification text
    """

    dt_str_format = '%m/%d/%Y, %H:%M:%S'

    text = f'{order_obj.symbol.upper()}\n' + \
        f'Order Type: {order_obj.type}\n' + \
        f'Order State: {order_obj.state}\n' + \
        f'Price: {order_obj.price}\n' + \
        f'Amount: {order_obj.amount}\n' + \
        f'Filled Fees: {order_obj.filled_fees}\n' + \
        f'Created at: {datetime.fromtimestamp(order_obj.created_at / 1e3).strftime(dt_str_format)}'

    if order_obj.canceled_at:
        dt = datetime.fromtimestamp(order_obj.canceled_at / 1e3)
        text += f'\nCanceled at: {dt.strftime(dt_str_format)}'

    if order_obj.finished_at:
        dt = datetime.fromtimestamp(order_obj.finished_at / 1e3)
        text += f'\nFinished at: {dt.strftime(dt_str_format)}'

    return text

def callback(upd_event: 'OrderUpdateEvent'):
    """
    Order update callback
    """

    print('---- order update : ----')
    upd_event.print_object()

    order_id = upd_event.data.orderId
    order_obj = trade_client.get_order(order_id=order_id)
    LogInfo.output(f'---- get order by order id : {order_id} ----')
    order_obj.print_object()
    print()
    
    tg_message = build_notification_text(order_obj)

    print(f'TG: {tg_message}')

def subscribe():
    """
    Subscribe to spot order events 
    """

    from huobi.client.generic import GenericClient
    generic_client = GenericClient()
    symbols = ','.join([list_obj.symbol for list_obj in generic_client.get_exchange_symbols()])
    print(symbols)
    trade_client.sub_order_update(symbols=symbols, callback=callback)

if __name__ == "__main__":
    subscribe()

    import time
    while True:
        time.sleep(1)