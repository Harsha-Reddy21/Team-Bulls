from NorenRestApiPy.NorenApi import  NorenApi
from threading import Timer
import pandas as pd
import time
import concurrent.futures
import streamlit as st
from datetime import datetime
api = None
class Order:
     def __init__(self, buy_or_sell:str = None, product_type:str = None,
                 exchange: str = None, tradingsymbol:str =None, 
                 price_type: str = None, quantity: int = None, 
                 price: float = None,trigger_price:float = None, discloseqty: int = 0,
                 retention:str = 'DAY', remarks: str = "tag",
                 order_id:str = None):
        self.buy_or_sell=buy_or_sell
        self.product_type=product_type
        self.exchange=exchange
        self.tradingsymbol=tradingsymbol
        self.quantity=quantity
        self.discloseqty=discloseqty
        self.price_type=price_type
        self.price=price
        self.trigger_price=trigger_price
        self.retention=retention
        self.remarks=remarks
        self.order_id=None


    #print(ret)

    


def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')

    return time.mktime(data)


class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
        global api
        api = self

    def place_basket(self, orders):

        resp_err = 0
        resp_ok  = 0
        result   = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

            future_to_url = {executor.submit(self.place_order, order): order for order in  orders}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
            try:
                result.append(future.result())
            except Exception as exc:
                print(exc)
                resp_err = resp_err + 1
            else:
                resp_ok = resp_ok + 1

        return result
                
    def placeOrder(self,order: Order):
        ret = NorenApi.place_order(self, buy_or_sell=order.buy_or_sell, product_type=order.product_type,
                            exchange=order.exchange, tradingsymbol=order.tradingsymbol, 
                            quantity=order.quantity, discloseqty=order.discloseqty, price_type=order.price_type, 
                            price=order.price, trigger_price=order.trigger_price,
                            retention=order.retention, remarks=order.remarks)
        #print(ret)

        return ret
    

from dotenv import load_dotenv
load_dotenv()

def shoonya_login():
    import pyotp
    import logging
    import os
    # from dotenv

    #enable dbug to see request and responses
    logging.basicConfig(level=logging.DEBUG)

    api = ShoonyaApiPy()
    token=os.getenv('token')
    user        = os.getenv('user')
    pwd         = os.getenv('pwd')
    vc          = os.getenv('vc')
    app_key     = os.getenv('app_key')
    imei        = os.getenv('imei')
    factor2     = pyotp.TOTP(token).now()

    #make the api call
    ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)


    # def login(userid='',password='',twoFA=None, vendor_code=None, api_secret=None,imei=None):
    #     api = ShoonyaApiPy()
    #     ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)

    #     return api

    # final_api=login()
    print(ret)
    

    return api


def get_results(api):
    print('start')
    print('api',api)
    print("end")
    lastBusDay = datetime(2025,3,27)
    lastBusDay = lastBusDay.replace(hour=0, minute=0, second=0, microsecond=0)
    banknifty_token='26009'
    nifty_future_token='35006'
    banknifty_future_token='35012'
    results = api.get_time_price_series(exchange='NSE', token='26000', starttime=lastBusDay.timestamp(), interval=5)

    

    return results


def get_stock_results(api,stock_token):
    lastBusDay = datetime(2025,7,27)
    lastBusDay = lastBusDay.replace(hour=0, minute=0, second=0, microsecond=0)
    results = api.get_time_price_series(exchange='NSE', token=stock_token, starttime=lastBusDay.timestamp(), interval=15)

    return results


def get_option_token(api,script):
    res=api.searchscrip(exchange='NFO', searchtext=script)
    print(script)
    
    token=res['values'][0]['token']
    print(token)
    return token


def get_option_data(api,i,option,number):
    if option=='PE':
        number=number+(i*50)
        script='28AUG NIFTY '+str(number) +' PE'
    else:
        number=number-(i*50)
        script='28AUG NIFTY '+str(number) +' CE'

    token=get_option_token(api,script)
    
    lastBusDay = datetime(2025,3,27)
    lastBusDay = lastBusDay.replace(hour=0, minute=0, second=0, microsecond=0)
    results = api.get_time_price_series(exchange='NFO', token=token, starttime=lastBusDay.timestamp(), interval=5)
    
    return results

def get_current_position(api):
    ret = api.get_positions()
    if ret:
        for pos in ret:
            if pos['netqty']!='0':
                symbol=pos['tsym']
                buy=symbol[-6]
                if buy=='C':
                    return 'buy',symbol,pos['netqty']
                elif buy=='P':
                    return 'sell',symbol,pos['netqty']
                
    return '','',0


def get_ltp(api,position,level):
    exch  = 'NFO'
    token = '57133'
    ret = api.get_quotes(exchange=exch, token=token)
    ltp=int(float(ret['lp']))

    if position=='buy':
        if ltp>=level:
            st.write(f'target achieved at {ltp}. exiting!!!')
            p,tsym,q=get_current_position(api)
            cancel_and_exit(api)
            if tsym:
                exit_order(api,tsym)
                st.write('Squared off ',tsym)

            return True 
        return False 
    else:
        if ltp<=level:
            st.write(f'target achieved at {ltp}. exiting!!!')
            p,tsym,q=get_current_position(api)
            cancel_and_exit(api)
            if tsym:
                exit_order(api,tsym)
                st.write('Squared off ',tsym)
            
            return True 
        return False 
    
def cancel_and_exit(api):
    ret = api.get_order_book()
    if ret:
        for r in ret:
            status=r['status']
            orderno=r['norenordno']
            if status=='OPEN':
                ret = api.cancel_order(orderno=orderno)

    
def exit_order(api,strike):
    
    res=api.searchscrip(exchange='NFO', searchtext=strike)
    token=res['values'][0]['token']
    ret = api.get_quotes(exchange='NFO', token=token)
    price=float(ret['lp'])
    ret = api.place_order(buy_or_sell='S', product_type='M',
                        exchange='NFO', tradingsymbol=strike, 
                        quantity=75, discloseqty=0,price_type='LMT', price=price, trigger_price=0,
                        retention='DAY', remarks='my_order_001')


def execute_order(api,strike):
    
    res=api.searchscrip(exchange='NFO', searchtext=strike)
    token=res['values'][0]['token']
    ret = api.get_quotes(exchange='NFO', token=token)
    price=float(ret['lp'])
    ret = api.place_order(buy_or_sell='B', product_type='M',
                        exchange='NFO', tradingsymbol=strike, 
                        quantity=75, discloseqty=0,price_type='LMT', price=price, trigger_price=0,
                        retention='DAY', remarks='my_order_001')
    
    ret = api.place_order(buy_or_sell='S', product_type='M',
                        exchange='NFO', tradingsymbol=strike, 
                        quantity=75, discloseqty=0,price_type='SL-LMT', price=price-30, trigger_price=price-28,
                        retention='DAY', remarks='my_order_001')
    
    st.write(strike)

def get_mtm(api):
    ret = api.get_positions()
    mtm = 0
    pnl = 0
    day_m2m=0
    if ret:
        for i in ret:
            mtm += float(i['urmtom'])
            pnl += float(i['rpnl'])
            day_m2m = mtm + pnl
    return day_m2m

def execute_stock_order(api,stock_token):

    ret = api.get_quotes(exchange='NSE', token=stock_token)
    price=float(ret['lp'])
    tradingsymbol=ret['tsym']
    print(price)
    total_amount=10000
    quantity=int(total_amount//price)
    ret = api.place_order(buy_or_sell='B', product_type='M',
                        exchange='NSE', tradingsymbol=tradingsymbol, 
                        quantity=quantity, discloseqty=0,price_type='LMT', price=price, trigger_price=0,
                        retention='DAY', remarks='my_order_001')




if __name__ == '__main__':
    api = shoonya_login()
    print(execute_stock_order(api,'11287'))
