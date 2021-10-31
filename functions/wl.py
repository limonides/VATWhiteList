import json
import requests
from datetime import datetime
from functions.keys import Key
from functions.comand_line import Color as c


class Wl:

    def __init__(self, choise, identifier):
        self.date = datetime.today().strftime('%Y-%m-%d')
        if choise == 1:
            self.url = rf'https://wl-api.mf.gov.pl/api/search/nip/{identifier}?date={self.date}'
        elif choise == 2:
            self.url = rf'https://wl-api.mf.gov.pl/api/search/regon/{identifier}?date={self.date}'

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
        to_print = {}
        d = json.loads(response[1])
        to_print['STATUS HTTP'] = response[0]
        to_print['KOD BLEDU'] = d['code']
        to_print['KOMUNIKAT BLEDU'] = d['message']

        return to_print

    def decode_response(self, response):
        to_print = {}
        d = json.loads(response[1])
        to_print['STATUS HTTP'] = response[0]
        to_print['ZAPYTANO'] = d['result']['requestDateTime']
        to_print['ID ZAPYTANIA'] = d['result']['requestId']
        to_print['NAZWA'] = d['result']['subject']['name']
        to_print['NIP'] = d['result']['subject']['nip']
        to_print['REGON'] = d['result']['subject']['regon']
        to_print['PESEL'] = d['result']['subject']['pesel']
        to_print['NUMER KRS'] = d['result']['subject']['krs']
        to_print['STATUS PODATNIKA VAT'] = d['result']['subject']['statusVat']
        to_print['Adres siedziby działalności gospodarczej'] = d['result']['subject']['residenceAddress']
        to_print['Osoby wchodzących w skład organu uprawnionego do reprezentowania podmiotu'] = d['result']['subject']['representatives']
        to_print['Imiona i nazwiska prokurentów'] = d['result']['subject']['authorizedClerks']
        to_print['Wspólnicy'] = d['result']['subject']['partners']
        to_print['Data rejestracji jako podatnika VAT'] = d['result']['subject']['registrationLegalDate']
        to_print['Data odmowy rejestracji jako podatnika VAT'] = d['result']['subject']['registrationDenialDate']
        to_print['Podstawa prawna odmowy rejestracji'] = d['result']['subject']['registrationDenialBasis']
        to_print['Data przywrócenia jako podatnika VAT'] = d['result']['subject']['restorationDate']
        to_print['Podstawa prawna przywrócenia jako podatnika VAT'] = d['result']['subject']['restorationBasis']
        to_print['Data wykreślenia odmowy rejestracji jako podatnika VAT'] = d['result']['subject']['removalDate']
        to_print['Podstawa prawna wykreślenia odmowy rejestracji jako podatnika VAT'] = d['result']['subject']['removalBasis']
        to_print['Podmiot posiada maski kont wirtualnych'] = d['result']['subject']['hasVirtualAccounts']
        to_print['Numery kont bankowych'] = d['result']['subject']['accountNumbers']

        return to_print

    def print_response_person(self, data):
        i = 1
        for person in data:
            print(10 * '-')
            print(c.GREEN + f'OSOBA NR {i}' + c.END)
            print(10*'-')
            for key, value in person.items():
                print(f'{value}')
            i += 1

    def print_response(self, data):
        print(50*'#')
        for key, value in data.items():
            if value:
                if isinstance(value, bool):
                    if value:
                        print(c.BOLD + f'{key}' + c.END + ': TAK')
                    else:
                        print(c.BOLD + f'{key}' + c.END + ': NIE')
                elif isinstance(value, list) and value in Key.person_names:
                    Wl.print_response_person(value)
                else:
                    print(c.BOLD + f'{key}' + c.END + f': {value}')



