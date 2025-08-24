from main import get_indices_data
import os
import pandas as pd
from data.announcements import get_announcements
from data.earnings import get_earnings_data
from data.money_control import get_moneycontrol_stocks_in_news
# df=pd.read_csv(f'images/nifty_data.csv')
from collections import defaultdict
from shoonya_login import shoonya_login,get_stock_results
api=shoonya_login()
print(api)
results=get_stock_results(api,'11287')
# from firstock_login import get_results,get_stock_results
# results=get_results()
# print(results)
# df=pd.DataFrame(results)
# df=pd.to_csv('images/nifty_data.csv',index=False)
# df.to_csv('current_data.csv',index=False)
    # Build a DataFrame from API results (list or dict) instead of treating it as a CSV path
    
final_data = pd.read_csv('finaldata_23_oct.csv')
def get_initial_images(images):
    final_dict=defaultdict(int)
        


    view_table={
        'Fully Bearish. Initiate the position':6,
        'Fully Bullish. Initiate the position':6,
        'Fully Bullish':4,
        'Fully Bearish':4,
        'Bullish':3,
        'Bearish':3,
        'Bullish consolidation. Initiate the position':6,
        'Bearish consolidation. Initiate the position':6,
        'Bullish consolidation':3,
        'Bearish consolidation':3,
        'nan-not':0
        }

    not_visited=['nannot','NAN',float('nan')]
    
    for i in range(len(images)):
        if final_data['Description'][images[i]] not in not_visited and not pd.isna(final_data['Description'][images[i]]):
            final_dict[final_data['Description'][images[i]]]+=(10-(i//3))*view_table[final_data['Description'][images[i]]]
            

    total_value=0
    for key in final_dict:
        total_value+=final_dict[key]
    percentages={}
    for key in final_dict:
        percentages[key]=round(final_dict[key]*100/total_value,2)
    for key in final_dict:
        if key=='Fully Bullish':
            if 'Fully Bullish. Initiate the position' in percentages:
                percentages['Fully Bullish. Initiate the position']+=percentages[key]
            else:
                percentages['Fully Bullish. Initiate the position']=percentages[key]
            del percentages[key]
        elif key=='Fully Bearish':
            if 'Fully Bearish. Initiate the position' in percentages:
                percentages['Fully Bearish. Initiate the position']+=percentages[key]
            else:
                percentages['Fully Bearish. Initiate the position']=percentages[key]
            del percentages[key]
        elif key=='Bullish consolidation. Initiate the position':
            if 'Bullish consolidation' in percentages:
                percentages['Bullish consolidation']+=percentages[key]
            else:
                percentages['Bullish consolidation']=percentages[key]
            del percentages[key]
        elif key=='Bearish consolidation. Initiate the position':
            if 'Bearish consolidation' in percentages:
                percentages['Bearish consolidation']+=percentages[key]
            else:
                percentages['Bearish consolidation']=percentages[key]
            del percentages[key]
    sorted_percentages = dict(sorted(percentages.items(), key=lambda item: item[1],reverse=True))

    
    print(sorted_percentages)
    return sorted_percentages





def get_data(df):
    import pandas as pd
    df_5 = df[:5][::-1]
    df_10 = df[:10][::-1]
    df_15 = df[:15][::-1]
    df_20 = df[:20][::-1]


    indices, distances = get_indices_data(df_5, df_10, df_15, df_20)
    return indices, distances


from fastapi import FastAPI
app=FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/get_indices")
def get_indices(stock_token:str):
    results=get_stock_results(api,stock_token)
    df=pd.DataFrame(results)
    df.to_csv('images/nifty_data.csv',index=False)
    indices,distances=get_data(df)
    print(indices)
    images=get_initial_images(indices[:30])
    return {"Signals":images,'Main_Singal':images["Fully Bullish. Initiate the position"]}

@app.get("/health")
def health():
    return {"message": "Healthy"}


@app.get("/get_announcements")
def get_nse_announcements():
    announcements=get_announcements()
    return {"announcements":announcements}

@app.get("/get_earnings")
def get_earnings():
    earnings=get_earnings_data()
    return {"earnings":earnings}

@app.get("/money_control")
def get_money_control():
    money_control=get_moneycontrol_stocks_in_news()
    return {"money_control":money_control}

if __name__=='__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
