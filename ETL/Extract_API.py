import requests
import pandas as pd

#URL Generation
def generate_url(API_Key):
    base_url = "http://api.exchangeratesapi.io/v1/latest?access_key="
    final_url = base_url+API_Key
    return final_url

API_key = "e61ca2e1cec53ea625cade99e6e9c497"


#Making a Request
def make_requests():
    req = requests.get(generate_url(API_key))
    req = req.json()
    rates = req['rates']
    return rates

#Adding data in DataFrame
def data_to_dataframe(rates):
    data = []
    for i in rates:
        data.append([i, rates[i]])
    df = pd.DataFrame(data = data, columns = ["Country", "Rate"])
    return(df)


if __name__ == "__main__":
    rates = make_requests()
    print(data_to_dataframe(rates))