import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
import time


headers = {
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
     "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Cookie": "u=2taqha02.1gcix89.binudwsnnig0; luri=rossiya; buyer_location_id=621540; sx=H4sIAAAAAAAC%2F1TMQZKrIBAA0Lv02gUg0OBtRKUpiPITInxMefdZpWrmAu8DwgeKKMgsLrdsGrHEqKXUYPpAhQlENMXx8Ho%2B7CnfiUkc34%2F4qtX7kZ0VBthg4lpxRDEqvAdw574KZWMnKlTykpaWcpGJvuSyUWWmqkjjtXB36IKXC1JhZtmG6xdphGLsHsBLZ71CnJ1ckc16tdpvRnOuPRdG4Fe2ez%2FTvB3yfyhP64Trc1GK19z%2F9f2gvzI39%2F0TAAD%2F%2F%2B3hfdoBAQAA; abp=1; SEARCH_HISTORY_IDS=4; _gcl_au=1.1.1604485752.1651678723; _ga_9E363E7BES=GS1.1.1651696006.3.1.1651696119.29; _ga=GA1.1.290135889.1651678724; f=5.0c4f4b6d233fb90636b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac7b0d53c7afc06d0b0df103df0c26013a84dcacfe8ebe897bfa4d7ea84258c63d59c9621b2c0fa58f164b09365f5308e7ad09145d3e31a56934d62295fceb188db5b87f59517a23f23de19da9ed218fe287829363e2d856a2e992ad2cc54b8aa8d99271d186dc1cd03de19da9ed218fe2d50b96489ab264ed3de19da9ed218fe23de19da9ed218fe246b8ae4e81acb9fa38e6a683f47425a8352c31daf983fa077a7b6c33f74d335c84df0fd22b85d35f9230d9f49c8f2c8003f2e1a870b7803b8577330086cfc737f9d694871fd850cbe6b4ddffebbeebad28c8cb20c0b1c64521373224a87538e891e52da22a560f550df103df0c26013a0df103df0c26013aaaa2b79c1ae925950ba277d7861043a2f9f810e0587450d23de19da9ed218fe22c205742455dd3668a7ab30b906d7a78; ft=HIIMxkQUhE45HodxcJ4qDk6lM+Af+Utlw+VnhFB4TjV+qDVKVG/tQAUiP0pbuJ58VfTWpIGlNHHyk3a8/aJHobsv+GmYPUnBiv3fKbhQR05Qkjf0CozXqT0PvWHhCQWnorIjT9/v3LFcCFSvWJIxZozqzTRF1s2V/BOc/Z6YypaW26d47/lmJPJTPBGRvy+g; v=1651695534; sessid=c76fd001f8d439b0f0b7ee423172e9ef.1651695998; auth=1; dfp_group=93; isLegalPerson=0"
}

def get_html(url, retry=5):
    time.sleep(5)
    try:
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        print(f"[+] {url} {r.status_code}")
    except Exception as ex:
        time.sleep(60)
        if retry:
            print(f"INFO retry={retry} => {url}")
            return get_html(url, retry=(retry - 1))
        else:
            raise
    else:
        return r.text

# #Получаем количество страниц погинации
# def get_total_pages(html):
#     soup = BeautifulSoup(html, 'lxml')
#     pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
#     total_pages = pages.split('=')[1].split('&')[0]
#     return int(total_pages)

def write_csv(data):
    with open('avito_progect.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'], data['url'], data['price'], data['phone'], data['organisation']))



def get_page_data(html, retry=5):
    url_list = []
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='items-items-kAJAg').find_all('div', class_='iva-item-root-_lk9K')
    for ad in ads:
        try:
            title = ad.find('h3').text
        except:
            title = ''
        try:
            url = 'https://www.avito.ru' + ad.find('a', class_='link-link-MbQDP').get('href')
            urls = ad.find('a', class_='link-link-MbQDP').get('href').split('_')[-1]
            url_list.append(urls)
        except:
            url = ''
        try:
            price = ad.find('span', class_='price-text-_YGDY').text.replace('\u20bd', '')
        except:
            price = ''
        try:
            organ = ad.find('a', class_='style-link-STE_U').find('div', class_='style-title-_wK5H').text
        except:
            organ = ''
        try:
            city = ad.find('span', class_='geo-address-fhHd0').text
        except:
            city = ''
        try:
            rezin = ad.find('span', class_='iva-item-text-Ge6dR').text
        except:
            rezin = ''
        print(rezin)

        for i in url_list:
            try:
                time.sleep(5)
                qwe = f'https://m.avito.ru/api/1/items/{i}/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
                r = requests.get(qwe, headers=headers)
                htmls = r.text
                phone = htmls.split('=')[-1].split('B')[-1].split('"')[0]

            except Exception as ex:
                time.sleep(60)
                if retry:
                    print(f"INFO retry={retry} => {qwe}")
                    continue
                else:
                    raise

        data = {'title': title, 'url': url, 'price': price, 'phone': phone, 'organisation': organ}
        write_csv(data)




def make_all(url):
    html = get_html(url)
    get_page_data(html)

def main():
    url = 'https://www.avito.ru/rossiya/zapchasti_i_aksessuary/shiny_diski_i_kolesa/shiny-ASgBAgICAkQKJooLgJ0B?cd=1&f=ASgBAgICA0QKJooLgJ0B0LcN0oUz&p={}&user=2'
    urls = [url.format(str(i)) for i in range(1, 10)]

    with Pool(10) as p:
        p.map(make_all, urls)



if __name__ == '__main__':
    main()

