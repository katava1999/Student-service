import csv

import studenti

profesori_path = 'data/profesori.csv'

listTeachers = []

def get_all_teachers():
    with open(profesori_path, 'r', encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                listTeachers.append(row)
                line_count += 1
            line_count += 1

def new_table(lista):
    with open(profesori_path, 'w', newline='') as f :
        writer = csv.writer(f)
        rowHeader=["Sifra", "Lozinka", "Ime", "Prezime", "Mail", "Termin konsultacija", "Sifra profesora"]
        writer.writerow(rowHeader)
        writer.writerows(lista)

def konsultacije(profesor):
    for t in listTeachers:
        if t[0] == str(profesor[0]):
            print(t[5])
            novi_termin = input("Unesite novi termin u formatu 'Dan : sat': ")
            t[5] = str(novi_termin)
    new_table(listTeachers)
    glavni_meni_profesora(profesor)

    
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
            unos_ocene(profesor)
        elif choice_p == 2:
            brisanje_ocene(profesor)
        elif choice_p == 3:
            prosek(profesor)
        elif choice_p == 4:
            konsultacije(profesor)
        elif choice_p == 5:
            pass
        else:
            print("------------------")
            print("Morate uneti jednu od ponudjenih opcija.")
            glavni_meni_profesora(profesor)
    except (TypeError, ValueError):
        print("------------------")
        print("Morate uneti jednu od datih opcija.")
        glavni_meni_profesora(profesor)


def unos_ocene(profesor):
    try:
        izbor = str(input("Unesite ime studenta: "))
        izabrani_studenti = get_students_by_name(izbor)
        brojac = 0
        if izabrani_studenti != None:
            for student in izabrani_studenti:
                brojac += 1
                print(str(brojac) + ". " + str(student["broj_indeksa"]) + " " + str(student["ime"]) + " "+ str(student["prezime"]))
            try:
                izabrani_student = {}
                izbor_indeksa =int(input("Unesite broj indeksa: "))
                for student in izabrani_studenti:
                    if izbor_indeksa == int(student["broj_indeksa"]):
                        print(str(student["ime"]) + " " + str(student["prezime"]))
                        izabrani_student = student
                brojac = 0
                for predmet in studenti.listSubjects:
                    brojac +=1
                    print(str(brojac) + ". "+  str(predmet[0]) +" " + str(predmet[1]))
                try:
                    izbor_predmeta = int(input("Unesite sifru predmeta: "))
                    predmet = studenti.predmeti_by_id(izbor_predmeta)
                    for ocene in izabrani_student["ocene"]:
                        if int(ocene["sifra_predmeta"]) == int(izbor_predmeta):
                            print("Predmet je polozen.")
                            glavni_meni_profesora(profesor)
                    
                    try:
                        ocena = int(input("Unesite ocenu: "))
                        if ocena >= 6 and ocena <=10:
                            nova_ocena = dodavanjeOcene(ocena, predmet, profesor)
                            izabrani_student["ocene"].append(nova_ocena)
                            studenti.save_students(studenti.listStudents)
                            print("-----------------------------")
                            print("Uspesno ste dodali ocenu.")
                            print(izabrani_student["ime"] + " je polozio sa ocenom " + str(ocena))
                            print("-----------------------------")
                            glavni_meni_profesora(profesor)
                        else:
                            print("Ocena nije u opsegu")
                    except (ValueError,TypeError):
                        print("Pogresno ste uneli ocenu!!!")
                except (ValueError,TypeError):
                    print("Ne postoji dati predmet")
            except (ValueError,TypeError):
                print("Ne postoji student sa datim indeksom")
    except(KeyError):
        print()
    glavni_meni_profesora(profesor)


def brisanje_ocene(profesor):
    try:
        izbor = str(input("Unesite ime studenta: "))
        izabrani_studenti = get_students_by_name(izbor)
        brojac = 0
        if izabrani_studenti != None:
            for student in izabrani_studenti:
                brojac += 1
                print(str(brojac) + ". " + str(student["broj_indeksa"]) + " " + str(student["ime"]) + " "+ str(student["prezime"]))
            try:
                izabrani_student = {}
                izbor_indeksa =int(input("Unesite broj indeksa: "))
                for student in izabrani_studenti:
                    if izbor_indeksa == int(student["broj_indeksa"]):
                        print(str(student["ime"]) + " " + str(student["prezime"]))
                        izabrani_student = student
                brojac = 0
                for ocene in izabrani_student["ocene"]:
                
                    brojac+=1
                    if int(ocene["sifra_profesora"]) == int(profesor[0]):
                        predmet = studenti.predmeti_by_id(ocene["sifra_predmeta"])
                        print(str(brojac) + ". "+  str(predmet[0]) +" " + str(predmet[1]))
                try:
                    izbor_predmeta = int(input("Unesite sifru predmeta: "))
                    predmet = studenti.predmeti_by_id(izbor_predmeta)

                    for i in range(len(izabrani_student["ocene"])):
                        if izabrani_student["ocene"][i]["sifra_predmeta"] == izbor_predmeta:
                            izabrani_student["ocene"].pop(i)
                            break
                
                    studenti.save_students(studenti.listStudents)
                    print("Obrisali ste ocenu")
                    glavni_meni_profesora(profesor)
                
                except (ValueError,TypeError,KeyError):
                    print("Ne postoji dati predmet")
            except (ValueError,KeyError):
                print("Ne postoji student sa datim indeksom")
    except(KeyError):
        print("Ne postoji student sa datim imenom")

    else:
        print("Niste izabrali ponudjeni predmet")
        glavni_meni_profesora(profesor)


def dodavanjeOcene(ocena, predmet, profesor):
    nova_ocena = {"sifra_predmeta": None,
                "sifra_profesora": None,
                "ocena": None}
    nova_ocena["sifra_predmeta"] = int(predmet[0])
    nova_ocena["sifra_profesora"] = int(profesor[0])
    nova_ocena["ocena"] = int(ocena)
    return nova_ocena


def get_students_by_name(name):
    izabrani = []
    for student in studenti.listStudents:
        if name.lower() == student["ime"].lower():
            izabrani.append(student)
    return izabrani
    

def prosek(profesor):
    try:
        brojac= 1
        for predmeti in studenti.listSubjects:
            print(str(brojac) + ". " + str(predmeti[0]) + "; " + str(predmeti[1]) + "\n")
            brojac+=1
        izbor = int(input("Unesite redni broj predmeta: "))
        predmet = studenti.listSubjects[izbor-1]
        br_ocena = 0
        ukupna = 0
        prosecna = 0
        nepolozen = True
        for student in studenti.listStudents:
            for ocene in student["ocene"]:
                if int(ocene["sifra_predmeta"]) == int(predmet[0]):
                    br_ocena +=1
                    ukupna += int(ocene["ocena"])
                    nepolozen = False
        
        if nepolozen == True:
            print("Predmet nije polozen")
        else:
            prosecna = ukupna/br_ocena
            print("Prosecna ocena je: " + str(prosecna) )
        glavni_meni_profesora(profesor)
    except(IndexError,ValueError,TypeError):
        print("Unesite jednu od datih ocena")
        glavni_meni_profesora(profesor)

get_all_teachers()