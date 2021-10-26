import json
import requests
from datetime import datetime
from errors import HttpStatuses


class WlConnect:

    def __init__(self):
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.url = rf'https://wl-api.mf.gov.pl/api/search/nip/8961601905?date={self.date}'

    def get_response(self):
        status_code = None
        try:
            r = requests.get(self.url, timeout=3)
            status_code = r.status_code
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)

        if status_code:
            return r.status_code, r.text
        else:
            return None

    def decode_response_error(self, response):
        d = json.loads(response[1])
        print('STATUS HTTP: ', response[0])
        print('KOD BLEDU: ', d['code'])
        print('KOMUNIKAT BLEDU: ', d['message'])

    def decode_response_nip(self, response):
        d = json.loads(response[1])
        print(d)
        print('STATUS HTTP: ', response[0])
        print(30 * "-")
        print('ZAPYTANO: ', d['result']['requestDateTime'])
        print('ID ZAPYTANIA: ', d['result']['requestId'])


if __name__ == "__main__":
    wl = WlConnect()
    resp = wl.get_response()
    if resp:
        if resp[0] in HttpStatuses.code_error:
            wl.decode_response_error(resp)
        elif resp[0] == 200:
            wl.decode_response_nip(resp)
    # print('JSON ', json)
    # print('STATUS CODE ', status_code)