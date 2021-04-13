import Extract_API as api
import Extract_WikiPedia as wiki
import sqlite3 as sql

global df_wiki, df_api
def extract():
    # Getting Data from WikiPedia
    df_wiki = wiki.data_processing()
    #Getting Data from API source
    rate = api.make_requests()
    df_api = api.data_to_dataframe(rate)

    return df_api, df_wiki

def transform(a,b):
    pass
#Load data into SQL database
def load():
    a, b = extract()
    conn = sql.connect('LOADED.db')
    cur = conn.cursor()
    cur2 = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS ListOfBank(Rank TEXT, BankName TEXT, Asset TEXT)")
    for (rows, rs) in b.iterrows():
        rank = str(rs[0])
        name = str(rs[1])
        asset = str(rs[2])
        param_banks = (rank,name, asset)
        cur.execute("INSERT INTO ListOfBank VALUES(?,?,?)", param_banks)


    cur2.execute("CREATE TABLE IF NOT EXISTS ExchangeRate(Country TEXT, Rate FLOAT)")
    for (rows1, rs1) in a.iterrows():
        name1 = str(rs1[0])
        asset1 = str(rs1[1])
        param = (name1,asset1)
        cur2.execute("INSERT INTO ExchangeRate VALUES( ?,? )",param)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    load()