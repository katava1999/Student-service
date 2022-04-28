
students_path = 'data/students.json' 
profesori_path = 'data/profesori.csv'

import profesori
import studenti
import sys

def glavni_meni():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1.Prijava na sistem.")
    print("2.Registracija.")
    print("3.Izlazak iz aplikacije.")
    choice = input("Unesite redni br. zeljene opcije: ")
    if choice == str(1):
        prijava_na_sistem()
    elif choice == str(2):
        registracija()
    elif choice == str(3):
        izlazak_iz_app()   
    else:
        print("Opcija nije ponudjena")
        glavni_meni()
    
def prijava_na_sistem():
    try:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        kIme = input("Unesite indeks ili sifru profesora: ")
        lozinka = input("Unesite lozinku: ")
        if kIme != "" and  lozinka != "":
            for student in studenti.listStudents:
                if str(student["broj_indeksa"]) == kIme and str(student["lozinka"]) == lozinka:
                    glavni_meni_studenta(student)
            for row in profesori.listTeachers:
                if str(row[0]) == kIme and str(row[1]) == lozinka:
                    glavni_meni_profesora(row)
            print("Pogresno uneti podaci")
            glavni_meni()    
        print("Morate uneti podatke!!!")
        glavni_meni()
    except IndexError:
        print("Morate uneti tacne podatke!")
        glavni_meni()

def registracija():
    try:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1.Profesor.")
        print("2.Student.")
        print("3.Povratak u glavni meni.")
        reg_num =  int(input("Unesite redni br. zeljene opcije: "))
        if reg_num == 1:
            ime = input("Unesite Vase ime: ")
            prezime = input("Unesite Vase prezime: ")
            email = input("Unesite Vas email: ")
            lozinka = input("Unesite Vasu lozinku: ")
            konsultacije = str(input("Unesite novi termin u formatu 'Dan : sat': ")) 
            sifra_profesora=int(profesori.listTeachers[len(profesori.listTeachers)-1][0])+1
            new_professor= [sifra_profesora, lozinka, ime, prezime, email, konsultacije,]
            profesori.listTeachers.append(new_professor)
            profesori.new_table(profesori.listTeachers)
            glavni_meni()

        elif reg_num ==2:

            broj_indeksa = input("Unesite Vas broj indeksa: ")
            ime = input("Unesite Vase ime: ")
            prezime = input("Unesite Vase prezime: ")
            email = input("Unesite Vas email: ")
            lozinka = input("Unesite Vasu lozinku: ")
            ocene = []
            for student in studenti.listStudents:
                    if str(student["broj_indeksa"]) == str(broj_indeksa):
                        print("Postoji student sa datim indeksom")
                        glavni_meni()
                    else:
                        print("Uspesno registrovan student.")
                        new_student = {"broj_indeksa":broj_indeksa ,"lozinka":lozinka,"ime":ime, "prezime":prezime,"email":email,"ocene":ocene}
                        studenti.listStudents.append(new_student)
                        studenti.save_students(studenti.listStudents)
                        glavni_meni()
        else: 
            print("Morate uneti jednu od ponudjenih opcija.")
            registracija()  
    except ValueError:
        print("Unesite jednu od datih opcija!") 
        glavni_meni()




def izlazak_iz_app():
    print("Izasli ste iz aplikacije")
    sys.exit()

def glavni_meni_studenta(keys):
    print("*********************************")
    print("Dobrodosli na sistem "+ keys["ime"] )
    print("1.Globalna prosecna ocena.")
    print("2.Polozeni predmeti.")
    print("3.Nepolozeni predmeti.")
    print("4.Podaci profesora.")
    print("5.Povratak na glavni meni.")
    try:
        choice_s = int(input("Unesite redni br. zeljene opcije: "))
        if choice_s == 1:
            studenti.globalna_ocena(keys)
        elif choice_s == 2:
            studenti.polozeni_predmeti(keys)
        elif choice_s == 3:
            studenti.nepolozeni_predmeti(keys)
        elif choice_s == 4:
            studenti.podaci_o_profesoru(keys)
        elif choice_s == 5:
            glavni_meni()
        else:
            print("------------------")
            print("Morate uneti jednu od ponudjenih opcija.")
            glavni_meni_studenta(keys)
    except ValueError:
        print("------------------")
        print("Neispravan unos!")
        glavni_meni_studenta(keys)

def glavni_meni_profesora(profesor):
    print("------Meni Profesora------")
    print("Dobrodosli na sistem profesore " + profesor[3] )
    print("1.Dodavanje ocene studentu.")
    print("2.Brisanje ocene studentu.")
    print("3.Prosecna ocena za predmet.")
    print("4.Promena termina konsultacija.")
    print("5.Povratak na glavni meni.")
    try:
        choice_p = int(input("Unesite redni br. zeljene opcije: "))
        if choice_p == 1:
            profesori.unos_ocene(profesor)
        elif choice_p == 2:
            profesori.brisanje_ocene(profesor)
        elif choice_p == 3:
            profesori.prosek(profesor)
        elif choice_p == 4:
            profesori.konsultacije(profesor)
        elif choice_p == 5:
            glavni_meni()
        else:
            print("------------------")
            print("Morate uneti jednu od ponudjenih opcija.")
            glavni_meni_profesora(profesor)
    except (TypeError, ValueError):
        print("------------------")
        print("Morate uneti jednu od datih opcija.")
        glavni_meni_profesora(profesor)

glavni_meni()
