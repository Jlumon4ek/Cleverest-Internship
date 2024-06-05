from bs4 import BeautifulSoup
import requests


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36'
}

request = requests.get(
    'https://ofd.soliq.uz/check?t=NA000000045091&r=797&c=20230227163754&s=320148011275', headers=headers)

soup = BeautifulSoup(request.text, "html.parser")


main_div = soup.find('div', class_='ticket-wrap')

h3_tags = main_div.find_all('h3')
for tag in h3_tags:
    print(' '.join(tag.text.split()))

na_tag = main_div.find('b')
print(na_tag.text.strip())

info_rows = main_div.find_all('tr')
for row in info_rows:
    columns = row.find_all('td')
    if columns and len(columns) == 1:
        print(' '.join(columns[0].text.split()))

product_table = soup.find('table', class_='products-tables')
product_rows = product_table.find_all('tr')

for row in product_rows:
    columns = row.find_all('td')
    if columns:
        print([' '.join(column.text.split()) for column in columns])
