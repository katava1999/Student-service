import csv
import json


students_path = 'data/students.json' 
profesori_path = 'data/profesori.csv'


listStudents = []
listSubjects = []


def get_all_subjects():
    with open('data/predmeti.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                listSubjects.append(row)
                line_count += 1
            line_count += 1
            
            
def predmeti_by_id(id):
    for row in listSubjects:
        if str(row[0]) == str(id):
            return row

def get_all_students():
    with open(students_path,'r', encoding='UTF-8') as file_json:
        listStudentsInput = json.load(file_json)
        for student in listStudentsInput:
            listStudents.append(student)


def save_students(listStudents):
    with open('data/students.json', 'w', encoding='UTF-8') as json_file:
        json.dump(listStudents, json_file, indent=2)


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
            globalna_ocena(keys)
        elif choice_s == 2:
            polozeni_predmeti(keys)
        elif choice_s == 3:
            nepolozeni_predmeti(keys)
        elif choice_s == 4:
            podaci_o_profesoru(keys)
        elif choice_s == 5:
            pass
        else:
            print("------------------")
            print("Morate uneti jednu od ponudjenih opcija.")
            glavni_meni_studenta(keys)
    except ValueError:
        print("------------------")
        print("Neispravan unos!")
        glavni_meni_studenta(keys)


def globalna_ocena(student):
    try:
        ukupna_ocena = 0
        ukupan_broj_ocena = 0 
        for keys in student["ocene"]:
            ukupna_ocena += keys["ocena"]
            ukupan_broj_ocena +=1
        print("-------------------")
        print( "Globalna prosecna ocena studenta je: " + str(ukupna_ocena/ukupan_broj_ocena))
        print("-------------------")  
        glavni_meni_studenta(student)
    except ZeroDivisionError:
        print("Ucenik nema polozenih ispita!")
        glavni_meni_studenta(student)

def polozeni_predmeti(student):
    print("-------------------")
    for keys in student["ocene"]:
        predmet = predmeti_by_id(keys["sifra_predmeta"])
        print(str(predmet[1]) +": "+ str(keys["ocena"]))
    print("-------------------")
    glavni_meni_studenta(student)

def nepolozeni_predmeti(student):
    nepolozeni_predmeti = []
    for row in listSubjects:
        if provera_predmeta(row[0],student["ocene"]) == False:
            nepolozeni_predmeti.append(row)
    print("-------------------")
    print("SIFRA & PREDMET")
    for nepolozen_predmet in nepolozeni_predmeti:
        print(nepolozen_predmet[0] + "  |" + nepolozen_predmet[1])
    glavni_meni_studenta(student)


def provera_predmeta(id_predmeta, lista_polozenih_predmeta):
        for polozen_predmet in lista_polozenih_predmeta:
            if str(polozen_predmet["sifra_predmeta"]) == str(id_predmeta):
                return True
        return False


def podaci_o_profesoru(student_prosledjeni):
    detalji_predmeti = {}
    try:
        print("====================")
        for row in listSubjects:

            print(row[0] + "  |" + row[1]) 
            detalji_predmeti[row[0]] =  row[1]

        print("\n")
        print("====================")
        izbor = input("Unesite sifru predmeta: ")
        print("\n")
        for student in listStudents:
            for ocene in student["ocene"]:
                if izbor == str(ocene["sifra_predmeta"]):

                    profesor = get_profesor_by_id(str(ocene["sifra_profesora"]))

                    for sifra, naziv in detalji_predmeti.items():
                        if str(sifra) == str(ocene["sifra_predmeta"]):
                            print(naziv + " predaje " + profesor[2] + " " + profesor[3] )   
                        
    except (ValueError,TypeError):
        print("Error")
    glavni_meni_studenta(student_prosledjeni) 


def get_profesor_by_id(id):
    for row in listTeachers:
        if str(row[0]) == str(id):
            return row


listTeachers = []

def get_all_teachers():
    with open(profesori_path, 'r', encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                listTeachers.append(row)
                line_count += 1
            line_count +=1

get_all_students()
get_all_subjects()