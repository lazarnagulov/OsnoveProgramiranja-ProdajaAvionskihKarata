from os import system
from time import sleep

from izuzeci import izuzeci
from common import konstante
from interfejsi import interfejsi

from datetime import datetime, timedelta
from korisnici import korisnici
from letovi import letovi
from aerodromi import aerodromi
from model_aviona import model_aviona
from konkretni_letovi import konkretni_letovi
from karte import karte
from izvestaji import izvestaji

svi_korisnici = dict()
sve_karte = dict()
svi_letovi = dict()
svi_konkretni_letovi = dict()
svi_aerodromi = dict()
svi_modeli_aviona = dict()

korisnik = dict()


# -------------------- LETOVI -------------------- #

def pretraga_najjeftinijih_letovi():
    try:
        polaziste = input("Unesite polazište: ")
        odrediste = input("Unesite odredište: ")
        najjeftiniji = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
        konstante.ZAGLAVLJE_LETOVI()
        for let in najjeftiniji:
            letovi.ispis_leta(let)
    except Exception as ex:
        print(ex)
    zaustavi()
    
def pretraga_letova():
    global svi_letovi, svi_konkretni_letovi

    try:
        polaziste = input("Polaziste: ")
        odrediste = input("Odredište: ")
        datum_polaska = input("Datum polaska: ")
        datum_dolaska = input("Datum dolaska: ")
        vreme_poletanja = input("Vreme poletanja: ")
        vreme_sletanja = input("Vreme sletanja: ")
        prevoznik = input("Prevoznik: ")

        filtrirani_letovi = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste,
                                                odrediste, datum_polaska, datum_dolaska, vreme_poletanja, vreme_sletanja, prevoznik)
        konstante.ZAGLAVLJE_KONKRETNI_LETOVI()
        for let in filtrirani_letovi:
            letovi.ispis_konkretnog_leta(let)
    except Exception as ex:
        print(ex)

    while True:
        unos = input("Pritisnite enter da biste nastavili. ")
        if unos == "":
            return
# TODO: Prodaja sledeće karte
#       Checkin za sledeći let
# -------------------- CHECKIN -------------------- #
def odabir_sedista(sifra_karte: int):
    global sve_karte, svi_konkretni_letovi
    konkretan_let = svi_konkretni_letovi[sve_karte[sifra_karte]['sifra_konkretnog_leta']]
    zauzetost = konkretan_let['zauzetost']
    letovi.ispis_matrice(zauzetost)
            
    red = input("Unesite red sedišta: ")
    pozicija = input("Unesite poziciju sedišta: ")
    try:
        letovi.checkin(sve_karte[sifra_karte], svi_letovi, konkretan_let, int(red), pozicija)
        sve_karte[sifra_karte]['status'] = konstante.STATUS_REALIZOVANA_KARTA
    except Exception as ex:
        print(ex)

    zaustavi()

def prijava_na_let():
    global korisnik, svi_konkretni_letovi, sve_karte, svi_korisnici, svi_letovi, svi_aerodromi
    
    putnici = list()
    
    while True:
        unos = input(">> ")
        if unos == "1":
            broj_karte = int(input("Unesite broj karte: "))
            
            if broj_karte not in sve_karte:
                print("Karta ne postoji")
                zaustavi()
                continue
            
            if korisnik['uloga'] == konstante.ULOGA_KORISNIK and korisnik not in sve_karte[broj_karte]['putnici']:
                print("Korisnik nema kartu")
            else:      
                putnici = sve_karte[broj_karte]['putnici']
                for putnik in putnici:
                    if not putnik.get('pasos'):
                        print(f"Putnik {putnik['ime']} {putnik['prezime']} nema unet broj pasoša!")
                        pasos = input("Unesite broj pasoša za: ")
                        putnik['pasos'] = pasos
                    if not putnik.get('drzavljanstvo'):
                        print(f"Putnik {putnik['ime']} {putnik['prezime']} nema uneto državljanstvo!")
                        drzavljanstvo = input("Unesite državljanstvo: ")
                        putnik['drzavljanstvo'] = drzavljanstvo
                    if not korisnik.get('pol'):
                        print(f"Putnik {putnik['ime']} {putnik['prezime']} nema unet pol!")
                        pol = input("Unesite pol: ")
                        putnik['pol'] = pol                     
                odabir_sedista(broj_karte)
                sledeca = input("Prijaviti se na sledeći let? (Da/Ne): ")
                if sledeca == 'Da':                
                    sledece_karte = karte.kupovina_sledece_karte(svi_letovi, svi_konkretni_letovi, sve_karte[broj_karte]['sifra_konkretnog_leta'])
                    konstante.ZAGLAVLJE_KARTE()
                    if sledece_karte == []:
                        print("Sledeća karta nije pronađena")
                        zaustavi()
                        return
                    for karta in sledece_karte:
                        karte.ispis_karte(sledece_karte[karta], svi_konkretni_letovi, svi_letovi, svi_aerodromi)
                        prijava_na_let()
        elif unos == "2":
            if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
                nerealizovane = karte.pregled_nerealizovanaih_karata(korisnik, [sve_karte[karta] for karta in sve_karte])
                konstante.ZAGLAVLJE_KARTE()
                for karta in nerealizovane:
                    karte.ispis_karte(karta, svi_konkretni_letovi, svi_letovi, svi_aerodromi)
                zaustavi()
            else:
                print("Pretraga karata za prodavca/ admina nije implementirana")
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda")

        interfejsi.prijava_na_let()
        

# -------------------- KARTE -------------------- #

def izmena_karte():
    global izmena_karte, sve_karte
    
    while True:
        unos = input(">> ")
        
        if unos == "1":
            broj_karte = int(input("Unestite broj karte: "))
            try:
                karte.izmena_karte(sve_karte, svi_konkretni_letovi, broj_karte)
            except Exception as ex:
                print(ex)
        elif unos == "2":
            interfejsi.pretraga_karata()
            pretraga_karata()
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda")
            sleep(0.5)

    interfejsi.izmena_karte()

def brisanje_karata():
    global korisnik, sve_karte
    
    while True:
        unos = input(">> ")
        
        if unos == "1":
            broj_karte = input("Unestite broj karte: ")
            if broj_karte == "":
                break
            karte.brisanje_karte(korisnik, sve_karte, int(broj_karte))
        elif unos == "2":
            interfejsi.pretraga_karata()
            pretraga_karata()
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda")
            sleep(0.5)
        interfejsi.brisanje_karte()

def pretraga_karata():
    global svi_letovi, svi_konkretni_letovi, karte, svi_aerodromi, svi_korisnici

    try:
        polaziste = input("Unesite polazište: ")
        odrediste = input("Unesite odredište: ")
        datum_polaska = input("Unesite datum polaska: ")
        datum_dolaska = input("Unesite datum dolaska: ")
        if datum_polaska != "":
            datum_polaska = datetime.strptime(datum_polaska, konstante.FORMAT_DATETIME)
        if datum_dolaska != "":
            datum_dolaska = datetime.strptime(datum_dolaska, konstante.FORMAT_DATETIME)
        putnici = list()
        while True:
            ime = input("Unesite ime putnika: ")
            prezime = input("Unesite prezime putnika: ")
            if ime != "" and prezime != "": 
                putnik = {'ime': ime, 'prezime': prezime}
                for korisnik in svi_korisnici:
                    if svi_korisnici[korisnik]['ime'] == putnik['ime'] and svi_korisnici[korisnik]['prezime'] == putnik['prezime']:
                        putnik = svi_korisnici[korisnik]
                        break
                putnici.append(putnik)
            else:
                break
            unos = input("Uneti još putnika? (Da/Ne): ")
            if unos != "Da":
                break
        filtrirane = karte.pretraga_karata(sve_karte, svi_konkretni_letovi, svi_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, putnici)
        if filtrirane == []:
            print("Nije pronađena karta!")
        else:
            konstante.ZAGLAVLJE_KARTE()
            for karta in filtrirane:
                karte.ispis_karte(karta, svi_konkretni_letovi, svi_letovi, svi_aerodromi)
        zaustavi()
    except Exception as ex:
        print(ex)
        zaustavi()
        
def prodaja_karte():
       
    while True:
        unos = input(">> ")
        if unos == "1":
            konkretan_let = int(input("Šifra leta: "))
            if konkretan_let not in svi_konkretni_letovi:
                print("Let ne postoji")
                zaustavi()
            else:
                interfejsi.odabir_putnika_prodaja()
                odabir_putnika_prodaja(konkretan_let)
        elif unos == "2":
            interfejsi.filteri_za_pretragu_letova()
            pretraga_letova()
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            zaustavi()

        interfejsi.prodaja_karte()

def odabir_putnika_prodaja(sifra_konkretnog_leta: int):
    global korisnik, svi_korisnici
    
    putnici = list()
    kupac = dict()
    potvrda = False
    
    while True:
        unos = input(">> ")
        if unos == "1":
            korisnicko_ime = input("Unesite korisničko ime: ")
            kupac = svi_korisnici.get(korisnicko_ime)
            if kupac == None:
                print("Kupac nije pronađen!")
                zaustavi()
            else:
                if kupac not in putnici:
                    putnici.append(kupac)
                interfejsi.potvrda_prodaje()
                potvrda = potvrda_prodaje(sifra_konkretnog_leta, putnici, kupac)
                if potvrda:
                    interfejsi.prodaja_sledece()
                    unos = input(">> ")
                    if unos == "1":
                        moguci_letovi = karte.kupovina_sledece_karte(svi_letovi, svi_konkretni_letovi, sifra_konkretnog_leta)
                        if moguci_letovi == []:
                            print("Ne postoje sledeći letovi!")
                            zaustavi()
                            return
                        konstante.ZAGLAVLJE_KONKRETNI_LETOVI()
                        for let in moguci_letovi:
                            letovi.ispis_konkretnog_leta(let)
                        while True:
                            sifra_narednog_leta = input("Šifra narednog leta: ")
                            if sifra_narednog_leta == "":
                                return
                            if int(sifra_narednog_leta) in [let['sifra'] for let in moguci_letovi]:
                                interfejsi.odabir_putnika_prodavac()
                                odabir_putnika_prodavac(int(sifra_narednog_leta))
                                return
                    elif unos == "2":
                        return
                    else:
                        print("Nepostojeća komanda")
                        zaustavi()    
        elif unos == "2":
            ime_kupca = input("Unesite ime kupca: ")
            prezime_kupca = input("Unesite prezime kupca: ")
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            zaustavi()
        
        interfejsi.odabir_putnika_prodaja()


def odabir_putnika(sifra_konkretnog_leta: int):
    global korisnik, svi_korisnici
    
    putnici = list()
    kupac = dict()
    potvrda = False
    

    while True:
        unos = input(">> ")
        if unos == "1":
            if korisnik not in putnici:
                putnici.append(korisnik)
            interfejsi.potvrda_kupovine()
            potvrda = potvrda_kupovine(sifra_konkretnog_leta, putnici)
            if potvrda:
                interfejsi.kupovina_sledece()
                unos = input(">> ")
                if unos == "1":
                    moguci_letovi = karte.kupovina_sledece_karte(svi_letovi, svi_konkretni_letovi, sifra_konkretnog_leta)
                    if moguci_letovi == []:
                        print("Ne postoje sledeći letovi!")
                        zaustavi()
                        return
                    konstante.ZAGLAVLJE_KONKRETNI_LETOVI()
                    for let in moguci_letovi:
                        letovi.ispis_konkretnog_leta(let)
                    while True:
                        sifra_narednog_leta = input("Šifra narednog leta: ")
                        if sifra_narednog_leta == "":
                            return
                        if int(sifra_narednog_leta) in [let['sifra'] for let in moguci_letovi]:
                            interfejsi.odabir_putnika()
                            odabir_putnika(int(sifra_narednog_leta))
                            return
                elif unos == "2":
                    return
        elif unos == "2":
            ime = input("Ime putnika: ")
            prezime = input("Prezime putnika: ")
            if {'ime': ime, 'prezime': prezime} not in putnici:
                putnici.append({'ime': ime, 'prezime': prezime})
            interfejsi.potvrda_kupovine()
            potvrda = potvrda_kupovine(sifra_konkretnog_leta, putnici)
            if potvrda:
                interfejsi.kupovina_sledece()
                unos = input(">> ")
                if unos == "1":
                    moguci_letovi = karte.kupovina_sledece_karte(svi_letovi, svi_konkretni_letovi, sifra_konkretnog_leta)

                    if moguci_letovi == []:
                        print("Ne postoje sledeći letovi!")
                        zaustavi()
                        return

                    konstante.ZAGLAVLJE_KONKRETNI_LETOVI()
                    for let in moguci_letovi:
                        letovi.ispis_konkretnog_leta(let)
                    while True:
                        sifra_narednog_leta = input("Šifra narednog leta: ")
                        if sifra_narednog_leta == "":
                            return
                        if int(sifra_narednog_leta) in [let['sifra'] for let in moguci_letovi]:
                            interfejsi.odabir_putnika()
                            odabir_putnika(int(sifra_narednog_leta))
                            return
                elif unos == "2":
                    return
                else:
                    print("Komanda ne postoji!")
                    zaustavi()    
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            zaustavi()

        
        interfejsi.odabir_putnika()

def potvrda_kupovine(sifra_konkretnog_leta: int, putnici: list) -> bool:
        unos = input(">> ")
        if unos == "1":
            slobodna_mesta = list()
            try:
                slobodna_mesta = svi_konkretni_letovi[sifra_konkretnog_leta]['zauzetost']
            except:
                slobodna_mesta = letovi.podesi_matricu_zauzetosti(
                    svi_letovi, svi_konkretni_letovi[sifra_konkretnog_leta])
            karta = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta, putnici, slobodna_mesta, korisnik, datum_prodaje = datetime.now())
            return True
        elif unos == "X":
            return False
        else:
            print("Nepostojeća komanda")

def potvrda_prodaje(sifra_konkretnog_leta: int, putnici: list, kupac: dict) -> bool:
        global korisnik
        unos = input(">> ")
        if unos == "1":
            slobodna_mesta = list()
            try:
                slobodna_mesta = svi_konkretni_letovi[sifra_konkretnog_leta]['zauzetost']
            except:
                slobodna_mesta = letovi.podesi_matricu_zauzetosti(svi_letovi, svi_konkretni_letovi[sifra_konkretnog_leta])
            try:
                karta = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta, putnici, slobodna_mesta, kupac, prodavac = korisnik, datum_prodaje = datetime.now())
            except Exception as ex:
                print(ex)
                zaustavi()
            return True
        elif unos == "X":
            return False
        else:
            print("Nepostojeća komanda")
            zaustavi()

def kupovina_karte():
    global korisnik, sve_karte, svi_konkretni_letovi, svi_letovi

    while True:
        unos = input(">> ")
        if unos == "1":
            konkretan_let = int(input("Šifra leta: "))
            if konkretan_let not in svi_konkretni_letovi:
                print("Let ne postoji")
            else:
                interfejsi.odabir_putnika()
                odabir_putnika(konkretan_let)
        elif unos == "2":
            interfejsi.filteri_za_pretragu_letova()
            pretraga_letova()
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            zaustavi()

        interfejsi.kupovina_karata()

# -------------------- KORISNIK -------------------- #

def prijavljeni_korisnik():
    global svi_letovi, korisnik, sve_karte, svi_konkretni_letovi, svi_aerodromi

    while True:
        unos = input(">> ")
        if unos == "1":
            nerealizovani = letovi.pregled_nerealizovanih_letova(svi_letovi)            
            konstante.ZAGLAVLJE_LETOVI()
            for let in nerealizovani:
                letovi.ispis_leta(let)
            zaustavi()
        elif unos == "2":
            interfejsi.filteri_za_pretragu_letova()
            pretraga_letova()
        elif unos == "3":
            interfejsi.kupovina_karata()
            kupovina_karte()
        elif unos == "4":
            interfejsi.prijava_na_let()
            prijava_na_let()
        elif unos == "5":
            pretraga_najjeftinijih_letovi()
        elif unos == "6":
            try:
                polaziste = input("Unesite polazište: ")
                odrediste = input("Unesite odredište: ")
                datum = input("Unesite datum: ")
                datum = datetime.strptime(datum, "%Y-%m-%d")
                broj_fleksibilnih_dana = int(input("Unesite broj fleksibilnih dana: "))
                            
                fleksibilni_letovi = letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum, broj_fleksibilnih_dana, None)
            
                konstante.ZAGLAVLJE_KONKRETNI_LETOVI()
                for let in fleksibilni_letovi:
                    letovi.ispis_konkretnog_leta(let)
            except Exception as ex:
                print(ex)
            zaustavi()
        elif unos == "7":
            nerealizovane = karte.pregled_nerealizovanaih_karata(korisnik, [sve_karte[karta] for karta in sve_karte])
            konstante.ZAGLAVLJE_KARTE()
            for karta in nerealizovane:
                karte.ispis_karte(karta, svi_konkretni_letovi, svi_letovi, svi_aerodromi)
            zaustavi()
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)

        interfejsi.korisnicki(korisnik)

# -------------------- PRODAVAC -------------------- #
def izmena_letova():
    pass

def prijavljeni_prodavac():
    global korisnik

    while True:
        unos = input(">> ")
        if unos == "1":
            interfejsi.prodaja_karte()
            prodaja_karte()
        elif unos == "2":
            interfejsi.prijava_na_let()
            prijava_na_let()
        elif unos == "3":
            interfejsi.izmena_karte()
            izmena_karte()
        elif unos == "4":
            interfejsi.brisanje_karte()
            brisanje_karata()
        elif unos == "5":
            interfejsi.pretraga_karata()
            pretraga_karata()
        elif unos == "X":
            return
        else:
            print("Nepostojeća komanda!")
            sleep(0.5)
        interfejsi.prodavacki(korisnik)

# -------------------- ADMIN -------------------- #
# TODO: Pretraga letova (NE KONKRETNIH)

def registracija_novog_prodavca():
    global svi_korisnici
        
    unos = input(">> ")
    if unos == "1":
        korisnicko_ime = input("Unesite korisničko ime: ")
        if korisnicko_ime in svi_korisnici:
            if svi_korisnici[korisnicko_ime]['uloga'] != konstante.ULOGA_PRODAVAC:
                svi_korisnici[korisnicko_ime]['uloga'] = konstante.ULOGA_PRODAVAC
                return
            else:
                print("Korisnik je već prodavac!")
                sleep(0.5)
        else:
            print("Korisnik ne postoji!")
            sleep(0.5)
    if unos == "2":
        interfejsi.registracija()
        try:
            korisnik = korisnici.registracija(svi_korisnici)
            korisnik['uloga'] = konstante.ULOGA_PRODAVAC
            korisnici.sacuvaj_korisnike(konstante.PUTANJA_KORSINICI, ",", svi_korisnici)
        except Exception as ex:
            print(ex)
    if unos == "X":
        return
    else:
        print("Komanda ne postoji!")
        sleep(0.5)
        

def izmena_letova():
    global svi_letovi
    
    while True:
        unos = input(">> ")
        
        if unos == "1":
            broj_leta = input("Broj leta: ")
            if broj_leta not in svi_letovi:
                print("Let ne postoji")
            else:
                try:
                    sifra_polazisnog_aerodroma = input("Šifra polazišnog aerodroma: ")
                    sifra_odredisnog_aerodroma = input("Šifra odredišnog aerodroma: ")
                    vreme_poletanja = input("Vreme poletanja: ")
                    vreme_sletanja = input("Vreme sletanja: ")
                    sletanje_sutra = input("Sletanje sutra (Da/Ne): ") == "Da"
                    prevoznik = input("Prevoznik:")
                    print("Unesite dane. Pritisnite enter da potvrdite.")
                    dani = list()
                    while True:
                        dan = input(">> ")
                        if dan == "":
                            break
                        dani.append(dan)
                    model = int(input("Id modela: "))
                    cena = float(input("Cena: "))
                    datum_pocetka_operativnosti = input(f"Datum početka operativnosti ({konstante.FORMAT_DATETIME}):  ")
                    datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, konstante.FORMAT_DATETIME)
                    datum_kraja_operativnosti = input(f"Datum kraja operativnosti ({konstante.FORMAT_DATETIME}):  ")
                    datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, konstante.FORMAT_DATETIME)
                    
                    letovi.izmena_letova(svi_letovi, broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodroma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti)
                except Exception as ex:
                    print(ex)
                    zaustavi()
        elif unos == "2":
            print("Pretraga letova nije implementirana")
        elif unos == "X":
            return
        else:
            print("Komanda ne postoji")
            sleep(0.5)
        
        
        interfejsi.izmena_letova()


def kreiranje_letova():
    global svi_konkretni_letovi, svi_letovi, svi_modeli_aviona

    try:
        broj_leta = input("Broj leta: ")
        sifra_polazisnog_aerodroma = input("Šifra polazišnog aerodroma: ")
        sifra_odredisnog_aerodroma = input("Šifra odredišnog aerodroma: ")
        vreme_poletanja = input("Vreme poletanja: ")
        vreme_sletanja = input("Vreme sletanja: ")
        sletanje_sutra = input("Sletanje sutra (Da/Ne): ") == "Da"
        prevoznik = input("Prevoznik: ")
        print("Unesite dane. Pritisnite enter da potvrdite.")
        dani = list()
        while True:
            dan = input(">> ")
            if dan == "":
                break
            dani.append(int(dan))
        for avion in svi_modeli_aviona:
            model_aviona.ispis_modela_aviona(svi_modeli_aviona[avion])
        model = int(input("ID modela: "))
        model = svi_modeli_aviona[model]
        cena = float(input("Cena: "))
        datum_pocetka_operativnosti = input(f"Datum početka operativnosti ({konstante.FORMAT_DATETIME}): ")
        datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, konstante.FORMAT_DATETIME)
        datum_kraja_operativnosti = input(f"Datum kraja operativnosti ({konstante.FORMAT_DATETIME}): ")
        datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, konstante.FORMAT_DATETIME)

        letovi.kreiranje_letova(svi_letovi, broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodroma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena,datum_pocetka_operativnosti,datum_kraja_operativnosti)
        kreirani_letovi = konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi, svi_letovi[broj_leta])
        for kreiran_let in kreirani_letovi:
            letovi.podesi_matricu_zauzetosti(svi_letovi, kreirani_letovi[kreiran_let])
    except Exception as ex:
         print(ex)
    zaustavi()
# TODO: Popraviti datume
def prikaz_izvestaja():
    global sve_karte, svi_konkretni_letovi, svi_letovi, svi_aerodromi
    while True:
        unos = input(">> ")
        if unos == "1":
            try:
                dan_prodaje = input(f"Dan prodaje ({konstante.FORMAT_DATE} 0:0:0): ")
                dan_prodaje = datetime.strptime(dan_prodaje, konstante.FORMAT_DATETIME)
                prodate_karte = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(sve_karte, dan_prodaje) 
                if prodate_karte == []:
                    print("Nema prodatih karata!")
                    zaustavi()
                else:
                    konstante.ZAGLAVLJE_KARTE()
                    for karta in prodate_karte:
                        karte.ispis_karte(karta, svi_konkretni_letovi, svi_letovi, svi_aerodromi)
            except Exception as ex:
                print(ex)
            zaustavi()
        elif unos == "2":
            try:
                dan_polaska = input(f"Dan polaska ({konstante.FORMAT_DATE}): ")
                dan_polaska = datetime.strptime(dan_polaska, konstante.FORMAT_DATE)
                prodate_karte = izvestaji.izvestaj_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, dan_polaska)
                if prodate_karte == []:
                    print("Nema prodatih karata!")
                    zaustavi()
                else:
                    konstante.ZAGLAVLJE_KARTE()
                    for karta in prodate_karte:
                        karte.ispis_karte(karta, svi_konkretni_letovi, svi_letovi, svi_aerodromi)
            except Exception as ex:
                print(ex)
            zaustavi()
        elif unos == "3":
            try:
                dan_prodaje = input(f"Dan prodaje ({konstante.FORMAT_DATE}): ")
                dan_prodaje = datetime.strptime(dan_prodaje, konstante.FORMAT_DATE)
                prodavac = input("Prodavac: ")
                prodate_karte = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, dan_prodaje, prodavac)
                if prodate_karte == []:
                    print("Nema prodatih karata!")
                    zaustavi()
                else:
                    konstante.ZAGLAVLJE_KARTE()
                    for karta in prodate_karte:
                        karte.ispis_karte(karta, svi_konkretni_letovi, svi_letovi, svi_aerodromi)
            except Exception as ex:
                print(ex)
            zaustavi()
        elif unos == "4":
            try:
                dan_prodaje = input(f"Dan prodaje ({konstante.FORMAT_DATE}): ")
                dan_prodaje = datetime.strptime(dan_prodaje, konstante.FORMAT_DATE)
                broj_prodatih_karata, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte, svi_konkretni_letovi, svi_letovi, dan_prodaje)
                print(f"Dana {dan_prodaje} je prodato {broj_prodatih_karata}.")
                print(f"Ukupna cena je {cena}.")
                zaustavi()
            except Exception as ex:
                print(ex)
            zaustavi()
        elif unos == "5":
            try:
                dan_polaska = input(f"Dan polaska ({konstante.FORMAT_DATE}): ")
                dan_polaska = datetime.strptime(dan_polaska, konstante.FORMAT_DATE)
                broj_prodatih_karata, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, svi_letovi, dan_polaska)
                print(f"Prodato je {broj_prodatih_karata} karata za {dan_polaska}.")
                print(f"Ukupna cena je {cena}.")
            except Exception as ex:
                print(ex)
            zaustavi()
        elif unos == "6":
            try:
                dan_prodaje = input(f"Dan prodaje ({konstante.FORMAT_DATE}): ")
                dan_prodaje = datetime.strptime(dan_prodaje, konstante.FORMAT_DATE)
                prodavac = input("Prodavac: ")
                broj_prodatih_karata, cena = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, dan_prodaje, prodavac)
                print(f"{prodavac} je prodao {broj_prodatih_karata} dana {dan_prodaje}.")
                print(f"Ukupna cena je {cena}.")
            except Exception as ex:
                print(ex)
            zaustavi()
        elif unos == "7":
            izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte, svi_konkretni_letovi, svi_letovi)
            zaustavi()
        elif unos == "X":
            return
        else:
            print("Komanda ne postoji!")
            sleep(0.5)
    
        interfejsi.prikaz_izvestaja()

def prijavljeni_admin_glavni():
    global korisnik
    
    while True:
        unos = input(">> ")
        if unos == "1":
            interfejsi.pretraga_karata()
            pretraga_karata()
        elif unos == "2":
            interfejsi.registracija_novog_prodavca()
            registracija_novog_prodavca()
        elif unos == "3":
            interfejsi.kreiranje_letova()
            kreiranje_letova()
        elif unos == "4":
            interfejsi.izmena_letova()
            izmena_letova()
        elif unos == "5":
            interfejsi.brisanje_karte()
            brisanje_karata()
        elif unos == "6":
            interfejsi.prikaz_izvestaja()
            prikaz_izvestaja()
        elif unos == "X":
            return

        interfejsi.adminski(korisnik)


def prijavljeni_admin():
    global korisnik

    while True:
        unos = input(">> ")
        if unos == "A":
            interfejsi.adminski(korisnik)
            prijavljeni_admin_glavni()
        elif unos == "K":
            interfejsi.korisnicki(korisnik)
            prijavljeni_korisnik()
        elif unos == "X":
            korisnici.logout(korisnik)
            return
        
        interfejsi.adminski_pocetni(korisnik)


# -------------------- OSTALO -------------------- #

def zaustavi():
    while True:
        kraj = input("Pritisnite enter.")
        if kraj == "":
            break

def pocetna_strana():
    global svi_korisnici, korisnik, svi_konkretni_letovi, svi_letovi, svi_aerodromi, svi_modeli_aviona

    while True:
        unos = input(">> ")
        if unos == "1":
            interfejsi.registracija()
            try:
                korisnici.registracija(svi_korisnici)
            except Exception as ex:
                print(ex)
                zaustavi()
        elif unos == "2":
            try:
                korisnik = korisnici.prijava(svi_korisnici)
                if korisnik != None:
                    if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
                        interfejsi.korisnicki(korisnik)
                        prijavljeni_korisnik()
                    elif korisnik['uloga'] == konstante.ULOGA_ADMIN:
                        interfejsi.adminski_pocetni(korisnik)
                        prijavljeni_admin()
                    elif korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
                        interfejsi.prodavacki(korisnik)
                        prijavljeni_prodavac()
            except Exception as ex:
                print(ex)
                zaustavi()
        elif unos == "3":
            nerealizovani = letovi.pregled_nerealizovanih_letova(svi_letovi)
            konstante.ZAGLAVLJE_LETOVI()
            for let in nerealizovani:
                letovi.ispis_leta(let)
            zaustavi()
        elif unos == "4":
            try:
                interfejsi.filteri_za_pretragu_letova()
            except Exception as ex:
                print(ex)
                zaustavi()
            pretraga_letova()
        elif unos == "5":
            pretraga_najjeftinijih_letovi()
        elif unos == "6":
            polaziste = input("Unesite polazište: ")
            odrediste = input("Unesite odredište: ")
            datum = input("Unesite datum: ")
            datum = datetime.strptime(datum, "%Y-%m-%d")
            broj_fleksibilnih_dana = int(input("Unesite broj fleksibilnih dana: "))
                        
            fleksibilni_letovi = letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum, broj_fleksibilnih_dana, None)
            konstante.ZAGLAVLJE_KONKRETNI_LETOVI()
            for let in fleksibilni_letovi:
                letovi.ispis_konkretnog_leta(let)
            zaustavi()
        elif unos == "X":
            print("Izlazak iz aplikacije...")
            korisnici.sacuvaj_korisnike(konstante.PUTANJA_KORSINICI, ",", svi_korisnici)
            karte.sacuvaj_karte(sve_karte, konstante.PUTANJA_KARTE, ",")
            letovi.sacuvaj_letove(konstante.PUTANJA_LETOVI, ",", svi_letovi)
            konkretni_letovi.sacuvaj_kokretan_let(konstante.PUTANJA_KONKRETNI_LETOVI, ",", svi_konkretni_letovi)
            aerodromi.sacuvaj_aerodrome(konstante.PUTANJA_AERODROMI, ",", svi_aerodromi)
            model_aviona.sacuvaj_modele_aviona(konstante.PUTANJA_MODELI_AVIONA, ",", svi_modeli_aviona)
            return
        else:
            print("Nepostojeća komanda")
            sleep(0.5)

        interfejsi.pocetna_strana()

def inicializacija():
    global svi_konkretni_letovi, svi_korisnici, sve_karte, svi_letovi, svi_aerodromi, svi_modeli_aviona

    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla(konstante.PUTANJA_KORSINICI, ",")
    sve_karte = karte.ucitaj_karte_iz_fajla(konstante.PUTANJA_KARTE, ",")
    svi_letovi = letovi.ucitaj_letove_iz_fajla(konstante.PUTANJA_LETOVI, ",")
    svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let(konstante.PUTANJA_KONKRETNI_LETOVI, ",")
    svi_aerodromi = aerodromi.ucitaj_aerodrom(konstante.PUTANJA_AERODROMI, ",")
    svi_modeli_aviona = model_aviona.ucitaj_modele_aviona(konstante.PUTANJA_MODELI_AVIONA, ",")     
    
    interfejsi.pocetna_strana()
    pocetna_strana()
