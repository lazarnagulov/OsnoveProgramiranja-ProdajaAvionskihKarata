from csv import DictReader, DictWriter
from common import konstante
from izuzeci import izuzeci
from konkretni_letovi import konkretni_letovi
from datetime import datetime, timedelta, date

sifra_konkretnog_leta = 1


def podesi_graf_letova(svi_letovi: dict) -> dict:
    graf = dict()
    for let in svi_letovi:
        polaziste = svi_letovi[let]['sifra_polazisnog_aerodroma']
        odrediste = svi_letovi[let]['sifra_odredisnog_aerodorma']
        vreme_poletanja = svi_letovi[let]['vreme_poletanja']
        vreme_poletanja = datetime.strptime(vreme_poletanja, "%H:%M")
        vreme_sletanja = svi_letovi[let]['vreme_sletanja']
        vreme_sletanja = datetime.strptime(vreme_sletanja, "%H:%M")
        tezina = vreme_sletanja - vreme_poletanja
        if graf.get(polaziste) == None:
            graf[polaziste] = [[odrediste, tezina]]
        else:
            graf[polaziste].append([odrediste, tezina])

    return graf


def najkraci_putevi_u_grafu(graf: dict, polaziste: str):
    beskonacno_vreme = timedelta(seconds=konstante.MAX_SEC)
    udaljenost = {i: beskonacno_vreme for i in graf}
    poseceno = {i: False for i in graf}
    udaljenost[polaziste] = timedelta(seconds=0)

    for cvorovi in graf[polaziste]:
        cvor = cvorovi[0]
        tezina = cvorovi[1]

        min_tezina = timedelta(seconds=konstante.MAX_SEC)
        min_index = ""

    return udaljenost


def najkrace_vreme_putovanja(polaziste: str, odrediste: str, datum: datetime):
    pass


def podesi_let(broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
               vreme_poletanja: str, vreme_sletanja: str, datum_pocetka_operativnosti: datetime, datum_kraja_operativnosti: datetime, sletanje_sutra: bool, prevoznik: str,
               dani: list, model: dict, cena: int) -> dict:
    svi_letovi = dict()
    svi_letovi.update(
        {
            broj_leta:
            {
                'broj_leta': broj_leta,
                'sifra_polazisnog_aerodroma': sifra_polazisnog_aerodroma,
                'sifra_odredisnog_aerodorma': sifra_odredisnog_aerodorma,
                'vreme_poletanja': vreme_poletanja,
                'vreme_sletanja': vreme_sletanja,
                'sletanje_sutra': sletanje_sutra,
                'datum_pocetka_operativnosti': datum_pocetka_operativnosti,
                'datum_kraja_operativnosti': datum_kraja_operativnosti,
                'prevoznik': prevoznik,
                'dani': dani,
                'model':
                {
                    'id': model['id'],
                    'naziv': model['naziv'],
                    'broj_redova': model['broj_redova'],
                    'pozicije_sedista': model['pozicije_sedista']
                },
                'cena': cena
            }
        }
    )

    return svi_letovi


def validacija_leta(broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                    vreme_poletanja: str, vreme_sletanja: str,  sletanje_sutra: bool, prevoznik: str,
                    dani: list, model: dict, cena: int, datum_pocetka_operativnosti: datetime = None,
                    datum_kraja_operativnosti: datetime = None):
    if not broj_leta or not sifra_odredisnog_aerodorma or not sifra_polazisnog_aerodroma or not vreme_poletanja or not vreme_sletanja or sletanje_sutra == "" or not prevoznik or not dani or not model or not cena:
        raise izuzeci.NepostojeciPodaci(
            "Gre??ka - Obavezni podaci nisu pravilno uneti!")
    if len(sifra_odredisnog_aerodorma) != 3 or len(sifra_polazisnog_aerodroma) != 3:
        raise izuzeci.NeispravnoUnetiPodaci(
            "Gre??ka - ??ifre aerodroma ne po??tuju IATA.")
    if not (str(broj_leta[0:2]).isalpha() and str(broj_leta[2:4]).isnumeric()) and len(broj_leta) > 4:
        raise izuzeci.NeispravanBrojLeta(
            f"Gre??ka - Broj leta mora biti oblika <slovo><slovo><broj><broj>. ({broj_leta})")
    try:
        sletanje_sati, sletanje_minuti = vreme_sletanja.split(":")
        poletanje_sati, poletanje_minuti = vreme_poletanja.split(":")
        if int(sletanje_minuti) >= 60 or int(poletanje_minuti) >= 60:
            raise izuzeci.NeispravnoVreme(
                f"Gre??ka - Minuti ne mogu biti ve??i od 59. ({poletanje_minuti} | {sletanje_minuti})")
        if int(sletanje_sati) >= 24 or int(poletanje_sati) >= 24:
            raise izuzeci.NeispravnoVreme(
                f"Gre??ka - Sati ne mogu biti ve??i od 23. ({poletanje_sati} | {sletanje_sati})")
    except:
        raise izuzeci.NeispravnoVreme(
            f"Gre??ka - Vreme se unosi u formati hh:mm. ({vreme_poletanja} | {vreme_sletanja})")

    if type(sletanje_sutra) != bool:
        raise izuzeci.NeispravnoUnetiPodaci(
            f"Gre??ka - sletanje_sutra mora biti True ili False. ({sletanje_sutra})")

    if cena < 0:
        raise izuzeci.NeispravnoUnetiPodaci(
            f"Gre??ka - cena mora biti broj ve??i od 0. ({cena})")

    if datum_kraja_operativnosti != None and datum_pocetka_operativnosti != None and datum_kraja_operativnosti < datum_pocetka_operativnosti:
        raise izuzeci.NeispravnoUnetiPodaci(
            "Gre??ka - Kraj operativnosti je pre po??etka.")


def ispis_konkretnog_leta(let: dict):
    datum_i_vreme_polaska = datetime.strftime(
        let['datum_i_vreme_polaska'], konstante.FORMAT_DATETIME_BEZ_SEKUNDI)
    datum_i_vreme_dolaska = datetime.strftime(
        let['datum_i_vreme_dolaska'], konstante.FORMAT_DATETIME_BEZ_SEKUNDI)
    print(f"{let['sifra']: <10}{let['broj_leta']: <10}{datum_i_vreme_polaska: <20}{datum_i_vreme_dolaska: <20}")


def ispis_leta(let: dict):
    print(f"{let['broj_leta']: <10}{let['sifra_polazisnog_aerodroma']: <10}{let['sifra_odredisnog_aerodorma']: <10}{let['vreme_poletanja']: <20}{let['vreme_sletanja']: <20}{let['prevoznik']: <30}{let['cena']: <5}")


"""
Funkcija koja vra??a matricu zauzetosti sedi??ta. Svaka stavka sadr??i oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""


def matrica_zauzetosti(konkretan_let: dict) -> list:
    return konkretan_let['zauzetost']


"""
Pomo??na funkcija koja pode??ava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedi??ta i postavlja ih na "nezauzeto".
"""


def podesi_matricu_zauzetosti(svi_letovi: dict, konkretan_let: dict) -> list:
    matrica_zauzetosti = list()
    let = svi_letovi[konkretan_let['broj_leta']]
    broj_redova = let['model']['broj_redova']
    pozicije_sedista = let['model']['pozicije_sedista']
    pozicije_sedista = [False for i in range(len(pozicije_sedista))]
    for _ in range(broj_redova):
        matrica_zauzetosti.append(pozicije_sedista)
    konkretan_let.update({'zauzetost': matrica_zauzetosti})
    return matrica_zauzetosti


"""
Funkcija koja zauzima sedi??te na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi po??inju od 1. 
Vra??a gre??ku ako se sedi??te ne mo??e zauzeti iz bilo kog razloga.
"""


def checkin(karta: dict, svi_letovi: dict, konkretni_let: dict, red: int, pozicija: str) -> (dict, dict):
    zauzetost = list()

    vreme_vazenja = datetime.now() + timedelta(hours=48)
    if vreme_vazenja > konkretni_let['datum_i_vreme_polaska']:
        raise izuzeci.NeispravnoUnetiPodaci("Gre??ka - Checkin je ve?? pro??ao")

    if konkretni_let.get('zauzetost') == None:
        zauzetost = podesi_matricu_zauzetosti(svi_letovi, konkretni_let)
    else:
        zauzetost = matrica_zauzetosti(konkretni_let)

    ukupan_br_redova = svi_letovi[konkretni_let['broj_leta']
                                  ]['model']['broj_redova']
    if red < 0 or red > ukupan_br_redova:
        raise izuzeci.NeispravnoUnetiPodaci("Gre??ka - Red ne postoji!")

    pozicije_sedista: list = svi_letovi[konkretni_let['broj_leta']
                                        ]['model']['pozicije_sedista']
    if pozicija not in pozicije_sedista:
        raise izuzeci.NeispravnoUnetiPodaci(
            "Gre??ka - Pozicija nije pravilno uneta!")

    if konkretni_let['zauzetost'][red-1][ord(pozicija) - ord('A')]:
        raise izuzeci.ZauzetoMesto("Gre??ka - Mesto je zauzeto")

    karta.update({'sediste': f"{pozicija}{red}"})
    konkretni_let['zauzetost'][red-1][ord(pozicija) - ord('A')] = True

    return (konkretni_let, karta)


"""
Funkcija koja vra??a listu konkretni letova koji zadovoljavaju slede??e uslove:
1. Polazi??te im je jednako odredi??tu prosle??enog konkretnog leta
2. Vreme i mesto poletanja im je najvi??e 120 minuta nakon sletanja konkretnog leta
"""


def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    odrediste = svi_letovi[konkretni_let['broj_leta']
                           ]['sifra_odredisnog_aerodorma']
    vreme_poletanja = konkretni_let['datum_i_vreme_dolaska'] + \
        timedelta(minutes=120)

    letovi = list()

    for konkretan_let in svi_konkretni_letovi:
        polaziste = svi_letovi[svi_konkretni_letovi[konkretan_let]
                               ['broj_leta']]['sifra_polazisnog_aerodroma']
        vreme = svi_konkretni_letovi[konkretan_let]['datum_i_vreme_polaska']
        if vreme_poletanja >= vreme and polaziste == odrediste:
            letovi.append(svi_konkretni_letovi[konkretan_let])

    return letovi


"""
Funkcija koja vra??a sve konkretne letove ??ije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""


def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:

    pocetni = (datum_polaska - timedelta(days=broj_fleksibilnih_dana)).date()
    krajnji = (datum_polaska + timedelta(days=broj_fleksibilnih_dana)).date()

    filtriranik_letovi = list()
    for konkretan_let in konkretni_letovi:
        try:
            konkretan_datum = konkretni_letovi[konkretan_let]['datum_i_vreme_polaska'].date(
            )
            sifra_polazista = svi_letovi[konkretni_letovi[konkretan_let]
                                         ['broj_leta']]['sifra_polazisnog_aerodroma']
            sifra_odredista = svi_letovi[konkretni_letovi[konkretan_let]
                                         ['broj_leta']]['sifra_odredisnog_aerodorma']
        except:
            continue
        if not polaziste or polaziste == sifra_polazista:
            if not odrediste or odrediste == sifra_odredista:
                if konkretan_datum <= krajnji and konkretan_datum >= pocetni:
                    filtriranik_letovi.append(konkretni_letovi[konkretan_let])
    return filtriranik_letovi


"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""


def pregled_nerealizovanih_letova(svi_letovi: dict) -> list:
    trenutno_vreme = datetime.now()
    nerealizovani_letovi = list()

    for let in svi_letovi:
        if type(svi_letovi[let]['datum_pocetka_operativnosti']) == str:
            svi_letovi[let]['datum_pocetka_operativnosti'] = datetime.strptime(
                svi_letovi[let]['datum_pocetka_operativnosti'], konstante.FORMAT_DATETIME)
        if svi_letovi[let]['datum_pocetka_operativnosti'] >= trenutno_vreme:
            nerealizovani_letovi.append(svi_letovi[let])

    return nerealizovani_letovi


"""
Funkcija koja omogucava pretragu leta po zadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
"""


def pretraga_letova(svi_letovi: dict, konkretni_letovi: dict, polaziste: str = "", odrediste: str = "", datum_polaska: str = "", datum_dolaska: str = "",
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "") -> list:
    filtrirano = list()

    for konkretan_let in konkretni_letovi:
        let = svi_letovi[konkretni_letovi[konkretan_let]['broj_leta']]
        try:
            datum_i_vreme_dolaska = konkretni_letovi[konkretan_let]['datum_i_vreme_polaska'].date(
            )
            datum_i_vreme_polaska = konkretni_letovi[konkretan_let]['datum_i_vreme_dolaska'].date(
            )
        except:
            raise izuzeci.NeispravnoUnetiPodaci(
                f"Gre??ka - Datum nije formata {konstante.FORMAT_DATE}")
        if not datum_polaska or datum_polaska.date() == datum_i_vreme_dolaska:
            if not datum_dolaska or datum_dolaska.date() == datum_i_vreme_polaska:
                if not odrediste or let['sifra_odredisnog_aerodorma'] == odrediste:
                    if not polaziste or let['sifra_polazisnog_aerodroma'] == polaziste:
                        if not vreme_poletanja or let['vreme_poletanja'] == vreme_poletanja:
                            if not vreme_sletanja or let['vreme_sletanja'] == vreme_sletanja:
                                if not prevoznik or let['prevoznik'] == prevoznik:
                                    filtrirano.append(
                                        konkretni_letovi[konkretan_let])
    return filtrirano


def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str = ""):
    filtrirano = list()
    for let in svi_letovi:
        if polaziste == svi_letovi[let]['sifra_polazisnog_aerodroma'] or polaziste == "":
            if odrediste == svi_letovi[let]['sifra_odredisnog_aerodorma'] or odrediste == "":
                filtrirano.append(svi_letovi[let])
    sortirano = sorted(filtrirano, key=lambda l: l['cena'])
    return sortirano[:10]


"""
Funkcija koja kreira novi re??nik koji predstavlja let sa prosle??enim vrednostima. Kao rezultat vra??a kolekciju
svih letova pro??irenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.

CHECKPOINT2: Baca gre??ku sa porukom ako podaci nisu validni.
"""


def kreiranje_letova(svi_letovi: dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float, datum_pocetka_operativnosti: datetime = None,
                     datum_kraja_operativnosti: datetime = None
                     ) -> dict:
    validacija_leta(broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, vreme_poletanja, vreme_sletanja,
                    sletanje_sutra, prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti)
    let = podesi_let(broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, vreme_poletanja, vreme_sletanja,
                     datum_pocetka_operativnosti, datum_kraja_operativnosti,  sletanje_sutra, prevoznik, dani, model, cena)
    svi_letovi.update(let)
    return svi_letovi


def ispis_matrice(matrica: list):
    for red in range(len(matrica)):
        sedista = matrica[red]
        sedista_karakateri = ["" for _ in range(len(matrica[red]))]
        i = 0
        while i < len(sedista):
            if sedista[i]:
                sedista_karakateri[i] = 'X'
            else:
                sedista_karakateri[i] = chr(ord('A') + i)
            i += 1
        print(f"Red {red}:", end='')
        for mesto in sedista_karakateri:
            print(mesto, end=' ')
        print()


"""
Funkcija koja menja let sa prosle??enim vrednostima. Kao rezultat vra??a kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.

CHECKPOINT2: Baca gre??ku sa porukom ako podaci nisu validni.
"""


def izmena_letova(svi_letovi: dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                  vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra:   bool, prevoznik: str,
                  dani: list, model: dict, cena: float, datum_pocetka_operativnosti: datetime,
                  datum_kraja_operativnosti: datetime) -> dict:
    if broj_leta not in svi_letovi:
        raise izuzeci.NepostojeciLet("Gre??ka - Broj leta ne postoji.")
    validacija_leta(broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma,
                    vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti)
    svi_letovi.update(podesi_let(broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, vreme_poletanja,
                      vreme_sletanja, datum_pocetka_operativnosti, datum_kraja_operativnosti, sletanje_sutra, prevoznik, dani, model, cena))
    return svi_letovi


"""
Funkcija koja cuva sve letove na zadatoj putanji
"""


def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    with open(putanja, 'w', newline='') as f:
        csv_pisac = DictWriter(f, ['broj_leta', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma', 'vreme_poletanja', 'vreme_sletanja', 'datum_pocetka_operativnosti', 'datum_kraja_operativnosti', 'sletanje_sutra', 'prevoznik',
                                   'dani', 'model', 'naziv', 'broj_redova', 'pozicije_sedista', 'cena'], delimiter=separator)
        for let in svi_letovi:
            csv_pisac.writerow({
                'broj_leta': svi_letovi[let]['broj_leta'],
                'sifra_polazisnog_aerodroma': svi_letovi[let]['sifra_polazisnog_aerodroma'],
                'sifra_odredisnog_aerodorma': svi_letovi[let]['sifra_odredisnog_aerodorma'],
                'vreme_poletanja': svi_letovi[let]['vreme_poletanja'],
                'vreme_sletanja': svi_letovi[let]['vreme_sletanja'],
                'datum_pocetka_operativnosti': svi_letovi[let]['datum_pocetka_operativnosti'],
                'datum_kraja_operativnosti': svi_letovi[let]['datum_kraja_operativnosti'],
                'sletanje_sutra': svi_letovi[let]['sletanje_sutra'],
                'prevoznik': svi_letovi[let]['prevoznik'],
                'dani': ",".join(str(dan) for dan in svi_letovi[let]['dani']),
                'model': svi_letovi[let]['model']['id'],
                'naziv': svi_letovi[let]['model']['naziv'],
                'broj_redova': int(svi_letovi[let]['model']['broj_redova']),
                'pozicije_sedista': ",".join(str(pozicija) for pozicija in svi_letovi[let]['model']['pozicije_sedista']),
                'cena': float(svi_letovi[let]['cena'])
            })


"""
Funkcija koja u??itava sve letove iz fajla i vra??a ih u re??niku.
"""


def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja, "r") as f:
        svi_letovi = dict()
        csv_citac = DictReader(f, ['broj_leta', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma', 'vreme_poletanja', 'vreme_sletanja', 'datum_pocetka_operativnosti', 'datum_kraja_operativnosti', 'sletanje_sutra',
                                   'prevoznik', 'dani', 'model', 'naziv', 'broj_redova', 'pozicije_sedista', 'cena'], delimiter=separator)
        for let in csv_citac:
            dani = [int(dan) for dan in let['dani'].split(",")]
            model = {
                'id': int(let['model']),
                'naziv': let['naziv'],
                'broj_redova': int(let['broj_redova']),
                'pozicije_sedista': [str(pozicija) for pozicija in let['pozicije_sedista'].split(",")]
            }
            svi_letovi.update(podesi_let
                              (
                                  let['broj_leta'],
                                  let['sifra_polazisnog_aerodroma'],
                                  let['sifra_odredisnog_aerodorma'],
                                  let['vreme_poletanja'],
                                  let['vreme_sletanja'],
                                  let['datum_pocetka_operativnosti'],
                                  let['datum_kraja_operativnosti'],
                                  let['sletanje_sutra'] == 'True',
                                  let['prevoznik'],
                                  dani,
                                  model,
                                  float(let['cena'])
                              )
                              )

        return svi_letovi
