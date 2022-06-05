import os
from datetime import datetime

from huobi.client.trade import TradeClient
from huobi.constant import *
from huobi.utils import *

import telegram_bot


access_key = os.environ.get('ACCESS_KEY')
secret_key = os.environ.get('SECRET_KEY')
assert access_key and secret_key, 'ACCESS_KEY or SECRET_KEY env variables not found'

TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
TELEGRAM_USER_ID = os.environ.get('TELEGRAM_USER_ID')
assert TELEGRAM_API_TOKEN and TELEGRAM_USER_ID, 'TELEGRAM_API_TOKEN or TELEGRAM_USER_ID env variables not found'

trade_client = TradeClient(api_key=access_key, secret_key=secret_key, init_log=True)


def build_notification_text(order_obj) -> str:
    """
    Build notification text
    """

    dt_str_format = '%m/%d/%Y, %H:%M:%S'

    order_state = order_obj.state.upper()

    text = f'#{order_obj.symbol.upper()}\n'

    if order_state == 'SUBMITTED':
        text += '🆕 '
    elif order_state == 'FILLED':
        text += '✅ '
    elif order_state == 'CANCELED':
        text += '🚫 '
    text += f'{order_obj.type.upper()} order {order_state}\n'

    text += f'Price: {"%.8f" % float(order_obj.price)}\n'
    text += f'Amount: {"%.8f" % float(order_obj.amount)}\n'
    text += f'Order Id: #ID{order_obj.id}\n'
    
    if float(order_obj.filled_fees):
        text += f'Filled Fees: {"%.8f" % float(order_obj.filled_fees)}\n'
    
    text += f'Created at: {datetime.fromtimestamp(order_obj.created_at / 1e3).strftime(dt_str_format)}'

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
    
    telegram_bot.send_text(TELEGRAM_USER_ID, build_notification_text(order_obj))

def subscribe():
    """
    Subscribe to spot order events 
    """
    
    symbols = os.environ.get('SYMBOLS')
    if not symbols:
        print('[WARNING] SYMBOLS env variable not found. All symbols will be tracked. Operation in this mode may not be stable.\n\
            https://github.com/kuznetsov-m/huobi-spot-order-notification/issues/2'
        )
        from huobi.client.generic import GenericClient
        generic_client = GenericClient()
        symbols = ','.join([list_obj.symbol for list_obj in generic_client.get_exchange_symbols()])
    print(f'Tracked symbols: {symbols}')
    trade_client.sub_order_update(symbols=symbols, callback=callback)

if __name__ == "__main__":
    telegram_bot.send_text(TELEGRAM_USER_ID, 'Bot restarted')

    subscribe()

    import time
    while True:
        time.sleep(1)