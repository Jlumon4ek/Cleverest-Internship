import requests
import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re


headers = {
    'authority': '2gis.kz',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,kk;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'spid=1713354351363_a2dff892997bad485a417ea3d67f25ca_je824jsrwokxtpc2; _2gis_webapi_user=030aacab-6277-45b4-a5cc-5b585ba7f5c0; dg5_jur={%22ru_sng%22:{%22status%22:%22agree%22%2C%22ts%22:1714361972856%2C%22v%22:2}}; dg5_pos=71.443111%3B51.129548%3B11; _2gis_webapi_session=f6f2b432-c1d2-40be-a178-06a3dfd2b20c; _ym_uid=1717566715150000631; _ym_d=1717566715; tmr_lvid=c21a4dfa61ef3897c16eecd01df64374; tmr_lvidTS=1717566714898; _ym_isad=2; domain_sid=LSDR2Uub8Lzuq3iVY8M4Z%3A1717566715447; country=2; language=en; city=67; _gid=GA1.2.1827224265.1717574364; _ym_visorc=w; _fbp=fb.1.1717574364797.804214238416632393; _ga=GA1.1.776802413.1717566714; tmr_detect=1%7C1717575540817; _ga_P27NC6GZM0=GS1.1.1717574599.2.1.1717575540.0.0.0; dg5_auth_refresh_token=ae2d38f8990ba01188d8dfe31a356a215668f840; dg5_auth_access_token=6c5e73ee1d8471992aa3412cc4c2aedc49da3ada',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36'
}

urls = []

async def gather_links_from_page(url, session):
    tasks = []
    async with session.get(url=url, headers=headers) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")

        main_div = soup.find_all("div", class_="_1kf6gff")

        for div in main_div:
            title = div.find("span", class_="_1al0wlf").text

            link = 'https://2gis.kz' + \
                div.find("a", class_="_1rehek")['href']

            
            tasks.append(gather_every_restaurant({'title': title, 'link': link}, session))

        await asyncio.gather(*tasks)


async def gather_every_restaurant(dict, session):
    link = dict['link']
    name = dict['title']

    async with session.get(link, headers=headers) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")

        temp = soup.find("a", class_="_1qhm93s")['href']
        pattern = re.compile(r'%7C([\d.]+)%2C([\d.]+)')

        match = pattern.search(temp)
        if match:
            latitude = match.group(2)
            longitude = match.group(1)

            try:
                name = name.encode('latin1').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                name = name.encode('utf-8').decode('utf-8')

            name = name.replace('\xa0', '')

            urls.append({
                "Name": name,
                "Latitude": latitude, 
                "Longitude": longitude
            })
                
    
async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for page in range(1, 85):
            
            url = f'https://2gis.kz/astana/search/Поесть/page/{page}'

            tasks.append(gather_links_from_page(url, session))
    
        await asyncio.gather(*tasks)


    with open("2gis.json", "w", encoding='utf-8') as file:
        json.dump(urls, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(main())
