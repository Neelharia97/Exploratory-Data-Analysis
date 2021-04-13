from bs4 import BeautifulSoup
import pandas as pd
import requests

#Data Extraction
def url_generator():
    url = "https://en.wikipedia.org/wiki/List_of_largest_banks?cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork-23455645&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ&cm_mmc=Email_Newsletter-_-Developer_Ed%2BTech-_-WW_WW-_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork-23455645&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ"
    soup = requests.get(url)
    final = soup.content
    page_content = BeautifulSoup(final, 'html.parser')
    return page_content

def data_to_dataframe():
    rank = []
    bank_name = []
    asset = []
    df = pd.DataFrame()
    page_object = url_generator().find_all(class_="wikitable sortable mw-collapsible")
    imp_data = page_object[0].find_all("tbody")
    for row in imp_data[0].find_all('tr'):
        col = (row.find_all('td'))
        if len(col) > 0:
            rank.append(col[0].get_text())
            bank_name.append(col[1].get_text())
            asset.append(col[2].get_text())

        data = {"Rank": rank,
                "Bank Name": bank_name,
                "Asset": asset}

        df = pd.DataFrame(data)
    return df

# Data Processing
def data_processing():
    # data_type = {"Rank": int,
    #              "Asset": float}
    df = data_to_dataframe()
    df['Rank'] = df['Rank'].str.replace('\n', '')
    df['Bank Name'] = df['Bank Name'].str.replace('\n', '')
    df['Asset'] = df['Asset'].str.replace('\n', '')
    df['Rank'] = df['Rank'].astype(int)

    final_asset = []
    for data in df["Asset"]:
        data = (data.split('.'))
        data1 = data[0].split(',')

        if len(data1) > 1:
            first_part = int(data1[0])
            first_part *= 1000
            second_part = int(data1[1])
            decimal = int(data[1]) / 100
            final_asset.append(first_part + second_part + decimal)
        elif len(data1) == 1:
            final_asset.append((int(data1[0]) + (int(data[1]) / 100)))
    df['Asset'] = final_asset
    return df

if __name__ == "__main__":
    # df = data_to_dataframe()
    print(data_processing())