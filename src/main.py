import datetime
import csv
import json

# aliohjelma, joka lukee sähkönkulutustiedot csv-tiedostoista
def lue_sahkonkulutus():
    vuosikulutukset = {}
    for vuosi in range(2016, 2024):
        vuosikulutukset[vuosi] = {}
        tiedosto = f"data/consumption_{vuosi}0101_{vuosi+1}0101.csv"
        with open(tiedosto, "r", encoding="utf-8") as tiedosto_avaus:
            csv_tiedosto = csv.reader(tiedosto_avaus, delimiter=";")
            for rivi in csv_tiedosto:
                try:
                    if rivi[1] == "Kulutus":
                        continue

                    kuukausi = rivi[0]
                    kulutus = rivi[1]
                    lampotila = rivi[2]

                    if lampotila and kulutus == "":
                        vuosikulutukset[vuosi][kuukausi] = {
                            "Kulutus": 0.0,
                            "Lampötila": 0.0
                            }

                    elif lampotila == "":
                        vuosikulutukset[vuosi][kuukausi] = {
                            "Kulutus": float(kulutus.replace(",", ".")),
                            "Lampötila": 0.0
                            }

                    else:
                        vuosikulutukset[vuosi][kuukausi] = {
                            "Kulutus": float(kulutus.replace(",", ".")),
                            "Lampötila": float(lampotila.replace(",", "."))}


                except (ValueError, IndexError):
                    pass
    return vuosikulutukset


# aliohjelma luo json-tiedoston luetun datan perusteella
def luo_json_tiedosto(vuosikulutukset):
    with open("vuosikulutukset.json", "w", encoding="utf-8") as json_tiedosto:
        json.dump(vuosikulutukset, json_tiedosto, ensure_ascii=False, indent=4)


# aliohjelma haku, joka hakee vuosikulutukset
def haku(vuosikulutukset):
    while True:
        print()
        while True:
            vuosi = int(input("Anna vuosi: "))
            if vuosi < 2016 or vuosi > 2024:
                print("Virheellinen syöte! Tarkista, että vuosi on väliltä 2016-2024.")
            else:
                break
        kuukausi = input("Anna kuukausi: ").capitalize()
        try:
            if not kuukausi:
                print()
                print("Vuoden", vuosi, "kulutukset:\n")
                print("-" * 39)
                print("|".ljust(2), "Kuukausi".ljust(9), "|".ljust(3), "Kulutus".ljust(4), "|".rjust(2), "Lämpötila".ljust(9), "|")
                print("-" * 39)

                for kuu, tiedot in vuosikulutukset[int(vuosi)].items():
                    kulutus = "{:.2f}".format(tiedot["Kulutus"]).rjust(8)
                    lampotila = "{:.1f}".format(tiedot["Lampötila"]).rjust(6)
                    print("|".ljust(2), kuu.ljust(9), "|", kulutus.ljust(10), "|", lampotila.ljust(9), "|")
                print("-" * 39)
            else:
                print()
                print("Vuoden", vuosi, "kulutukset:\n")
                print("-" * 39)
                print("|".ljust(2), "Kuukausi".ljust(9), "|".ljust(3), "Kulutus".ljust(4), "|".rjust(2),
                      "Lämpötila".ljust(9), "|")
                print("-" * 39)
                kulutus = "{:.2f}".format(vuosikulutukset[int(vuosi)][kuukausi]["Kulutus"]).rjust(8)
                lampotila = "{:.1f}".format(vuosikulutukset[int(vuosi)][kuukausi]["Lampötila"]).rjust(6)
                print("|".ljust(2), kuukausi.ljust(9), "|", kulutus.ljust(10), "|", lampotila.ljust(9), "|")
                print("-" * 39)
        except KeyError:
            print("Virheellinen syöte. Tarkista vuosi on väliltä 2016-2023 ja kuukausi on väliltä tammikuu-joulukuu.")
        except ValueError:
            print("Virheellinen syöte.")
        except IndexError:
            print("Virheellinen syöte.")
        except Exception as virhe:
            print(f"Virhe: {virhe}")
        print()
        jatka = input("Haluatko hakea lisää tietoja? (k/e): ")
        if jatka.lower() != "k":
            break


# aliohjelma tulosta, joka tulostaa vuosikulutukset
def tulosta():
    print()
    print("*************************************************************************")
    print("*            Tervetuloa sähkönkulutustietojen hakuun!                   *")
    print("*************************************************************************\n")
    print("*************************************************************************")
    print("*  Sähkönkulutustiedot haettu onnistuneesti ja tallennettu tiedostoon.  *")
    print("*************************************************************************\n")
    print("**************************************************************************")
    print("*  Voit nyt hakea tietoja vuosikulutuksista. Syötä vain haluamasi vuosi  *")
    print("*  ja kuukausi, josta haluat tietoja. Jos et haluat hakea tietoja        *")
    print("*  yksittäisistä kuukausista, jätä kuukausi tyhjäksi, jolloin ohjelma    *")
    print("*  tulostaa kaikki kuukaudet kyseiseltä vuodelta.                        *")
    print("**************************************************************************\n")

    print("Aloita haku...")

def main():
    vuosikulutukset = lue_sahkonkulutus()
    luo_json_tiedosto(vuosikulutukset)
    tulosta()
    haku(vuosikulutukset)

    print("Ohjelma lopettu.")

if __name__ == "__main__":
    main()