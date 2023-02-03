import datetime

def extra_hours():
    with open("hours.txt", 'r', encoding='utf-8') as f:
        hours = f.read()
    #hours = """E 17/09/2022 14:11,S 17/09/2022 18:25,E 18/09/2022 10:00,S 18/09/2022 15:01,E 22/09/2022 19:00,S 22/09/2022 23:55,E 25/09/2022 07:03,S 25/09/2022 12:49,E 26/09/2022 22:00,S 26/09/2022 22:55,E 29/09/2022 19:00,S 29/09/2022 20:55,E 30/09/2022 19:00,S 30/09/2022 20:21,E 01/10/2022 01:10,S 01/10/2022 02:36,E 02/10/2022 08:00,S 02/10/2022 11:30,E 06/10/2022 22:41,S 06/10/2022 23:55,E 09/10/2022 10:00,S 09/10/2022 17:10,E 12/10/2022 06:20,S 12/10/2022 12:44,E 16/10/2022 15:00,S 16/10/2022 18:39,E 16/10/2022 18:55,S 16/10/2022 19:50"""

    entrada = None
    saida = None

    adn_time_start = datetime.datetime.strptime("22:00", "%H:%M")
    adn_time_stop = datetime.datetime.strptime("05:00", "%H:%M")

    list_50 = []
    list_100 = []
    list_50_adn = []
    list_100_adn = []

    dict_day = {}

    for i in hours.split(","):

        if i[0] == "E":
            entrada = datetime.datetime.strptime(i[2:], "%d/%m/%Y %H:%M")
        elif i[0] == "S":
            saida = datetime.datetime.strptime(i[2:], "%d/%m/%Y %H:%M")
            if saida.hour == 0:
                saida = datetime.datetime.strptime(i[2:], "%d/%m/%Y %H:%M") - datetime.timedelta(seconds=1) + datetime.timedelta(days=1)
        else:
            print("Não foi possível identificar o tipo de hora.")

        if entrada and saida:

            total_hours = saida - entrada

            if saida.time() > adn_time_start.time():
                """print(saida - entrada)
                print(saida - entrada.replace(hour=22, minute=0, second=0))
                if entrada.time() < adn_time_start.time():
                    print(saida.replace(hour=22, minute=0, second=0) - entrada)
                print(entrada.time(), saida.time(), "\n")"""

                if entrada.weekday() == 6:  # Check if is Sunday
                    if entrada.time() > adn_time_start.time():
                        list_100_adn.append(saida - entrada)
                    else:
                        list_100_adn.append(saida - entrada.replace(hour=22, minute=0, second=0))
                    if entrada.time() < adn_time_start.time():
                        list_100.append(saida.replace(hour=22, minute=0, second=0) - entrada)
                else:
                    if entrada.time() > adn_time_start.time():
                        list_100_adn.append(saida - entrada)
                    else:
                        list_50_adn.append(saida - entrada.replace(hour=22, minute=0, second=0))
                    if entrada.time() < adn_time_start.time():
                        list_50.append(saida.replace(hour=22, minute=0, second=0) - entrada)

            elif entrada.time() < adn_time_stop.time():
                """print(saida - entrada)
                print(saida.replace(hour=5, minute=0, second=0) - entrada)
                if saida.time() > adn_time_stop.time():
                    print(saida - entrada.replace(hour=5, minute=0, second=0))
                print(entrada.time(), saida.time(), "\n")"""

                if entrada.weekday() == 6:  # Check if is Sunday
                    if saida.time() < adn_time_stop.time():
                        list_100_adn.append(saida - entrada)
                    else:
                        list_100_adn.append(saida.replace(hour=5, minute=0, second=0) - entrada)
                    if saida.time() > adn_time_stop.time():
                        list_100.append(saida - entrada.replace(hour=5, minute=0, second=0))
                else:
                    if saida.time() < adn_time_stop.time():
                        list_100_adn.append(saida - entrada)
                    else:
                        list_50_adn.append(saida.replace(hour=5, minute=0, second=0) - entrada)
                    if saida.time() > adn_time_stop.time():
                        list_50.append(saida - entrada.replace(hour=5, minute=0, second=0))
            else:

                if entrada.weekday() == 6:  # Check if is Sunday
                    list_100.append(total_hours)
                else:
                    list_50.append(total_hours)

            if entrada.date() not in dict_day:
                dict_day[entrada.date()] = total_hours
            else:
                dict_day[entrada.date()] = dict_day[entrada.date()] + total_hours

            entrada, saida = None, None

    for k, v in dict_day.items():
        if k.weekday() == 6:
            print(k, v, "{:.2f}".format(v.total_seconds()/3600), "S")
        else:
            print(k, v, "{:.2f}".format(v.total_seconds() / 3600))

    total_100 = sum(list_100, datetime.timedelta())
    total_100_adn = sum(list_100_adn, datetime.timedelta())
    total_50 = sum(list_50, datetime.timedelta())
    total_50_adn = sum(list_50_adn, datetime.timedelta())

    print("\nTotal de horas 50% = {:.2f}".format(total_50.total_seconds() / 3600))
    print("Total de horas 100% = {:.2f}".format(total_100.total_seconds()/3600))
    print("Total de horas 50% com ADN = {:.2f}".format(total_50_adn.total_seconds() / 3600))
    print("Total de horas 100% com ADN = {:.2f}".format(total_100_adn.total_seconds() / 3600))

    print("\nTotal de horas 100% = {:.2f}".format((total_100 + total_100_adn).total_seconds() / 3600))
    print("Total de horas 50% = {:.2f}".format((total_50 + total_50_adn).total_seconds() / 3600))

    print("Total de horas = {:.2f}".format((total_50 + total_100 + total_50_adn + total_100_adn).total_seconds()/3600))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    extra_hours()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
