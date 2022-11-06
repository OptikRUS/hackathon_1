import cfscrape
import requests


class CianParser:
    params = {
        'deal_type': 'sale',
        'engine_version': '2',
        'offer_type': 'flat',
        'origin': 'map',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;'
                  'q=0.9,image/avif,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3;q=0.9',

        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',

        'cookie': '_CIAN_GK=476c87e5-88bb-4b2b-8943-a702a890b203; '
                  'adb=1; _ga=GA1.2.966413921.1663938900;'
                  'login_mro_popup=1; uxfb_usertype=searcher;'
                  'tmr_lvid=6f48b073fd547936815a20b410462acb;'
                  'tmr_lvidTS=1663938900639;'
                  '_ym_uid=1663938901663132680;'
                  '_ym_d=1663938901;'
                  'uxs_uid=bad7eee0-3b41-11ed-ad4a-abe8a80ef4dc;'
                  'afUserId=dc1364df-70ba-40be-9a5d-2d2863c83fc8-p;'
                  '_gcl_au=1.1.603139711.1663938960;'
                  'hide_route_tab_onboarding=1;'
                  'pview=6;'
                  'sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D;'
                  '_gpVisits={"isFirstVisitDomain":true,"todayD":"Tue%20Oct%2025%202022","idContainer":"10002511"};'
                  'AF_SYNC=1666717253611; session_region_id=4914;'
                  'session_main_town_region_id=4914; tmr_reqNum=436;'
                  '__cf_bm=JzszpUpWy0AuMc.cyuVXEACn33vqXvOWK3Eg2ZiPKdk-1667058806-0-ATBfO1Mvv2wOro7A0LZ7k+aYuQIx3FC+GNDqw2R1L7KFTvv8nxU9pt/z3FRlPYpAgt2vrgFI4UiXc9CZSp4vRck=',

        'dnt': '1',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',

        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/107.0.0.0 Safari/537.36',
    }

    def __init__(self, bbox, floor, min_year, max_year, house_material_type='1', room_type='1'):
        self.url = 'https://www.cian.ru/export/xls/offers/'
        self.params["bbox"] = bbox
        self.params[f"room{room_type}"] = '1'
        self.params["house_material%5B6%5D"] = house_material_type
        self.params["minfloorn"] = floor
        self.params["maxfloorn"] = floor
        self.params["min_house_year"] = min_year
        self.params["max_house_year"] = max_year

    @property
    def get_doc(self):
        with requests.session() as session:
            session.headers = self.headers
            scraper = cfscrape.create_scraper(sess=session)
            response = scraper.get(self.url, params=self.params)
            return response.content
