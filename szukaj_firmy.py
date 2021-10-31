from functions.wl import Wl
from functions.statuses import HttpStatuses
from functions.command_line import Color

if __name__ == "__main__":
    while True:
        try:
            choice = input("1 - Wyszukaj po NIP.\n2 - Wyszukaj po REGON.\n\nTwój wybór:")
            choice = int(choice)
            if choice in [1, 2]:
                break
            else:
                print(Color.RED + 'Możesz wybrać z menu tylko OPCJE [1,2]' + Color.END)
                continue
        except ValueError as error:
            print(Color.RED + 'Możesz wybrać z menu tylko OPCJE [1,2]' + Color.END)
    if choice == 1:
        identifier = input("Podaj NIP: ")
    if choice == 2:
        identifier = input("Podaj REGON: ")

    wl = Wl(choice, identifier)
    resp = wl.get_response()
    if resp:
        if resp[0] in HttpStatuses.code_error:
            wl.print_response(wl.decode_response_error(resp))
        elif resp[0] == 200:
            wl.print_response(wl.decode_response(resp))