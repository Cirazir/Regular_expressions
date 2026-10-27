import csv
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)
def fix_names(contacts):
    """Раскладываем Ф+ИО / ФИО / Ф+И+О по полям lastname, firstname, surname."""
    result = [contacts[0]]  # заголовок не трогаем
    for contact in contacts[1:]:
        # склеиваем три первых поля и делим по пробелам
        # (split() без аргумента — чтобы не бояться двойных пробелов)
        parts = " ".join(contact[:3]).split()
        if len(parts) == 3:      # «Фамилия Имя Отчество»
            contact[:3] = parts
        elif len(parts) == 2:    # «Фамилия Имя» или «Фамилия И.О.»
            contact[:3] = [parts[0], parts[1], ""]
        elif len(parts) == 4:    # «Соловьева И.» + «Софья В.»
            contact[:3] = [parts[0], parts[2], parts[3]]
        result.append(contact)
    return result