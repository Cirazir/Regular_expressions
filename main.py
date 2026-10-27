import csv
import re
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)


# ---------- функции ----------

def fix_names(contacts):
    """Раскладываем Ф+ИО / ФИО / Ф+И+О по полям lastname, firstname, surname."""
    result = [contacts[0]]  # заголовок не трогаем
    for contact in contacts[1:]:
        parts = " ".join(contact[:3]).split()
        if len(parts) == 3:      # Ф И О
            contact[:3] = parts
        elif len(parts) == 2:    # Ф ИО
            contact[:3] = [parts[0], parts[1], ""]
        elif len(parts) == 4:    # «Соловьева И.» + «Софья В.»
            contact[:3] = [parts[0], parts[2], parts[3]]
        result.append(contact)
    return result


PHONE_RE = re.compile(
    r"(\+7|8)\s*\(?\s*(\d{3})\s*\)?[\s-]?"    # +7 или 8 и код оператора
    r"(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})"      # остальные 7 цифр
    r"(?:\s*\(?\s*(доб\.?)\s*(\d+)\s*\)?)?"   # необязательный добавочный
)


def format_phone(match):
    phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
    if match.group(7):
        phone += f" доб.{match.group(7)}"
    return phone


def fix_phones(contacts):
    for contact in contacts[1:]:
        contact[5] = PHONE_RE.sub(format_phone, contact[5])
    return contacts


def merge_duplicates(contacts):
    """Склеиваем записи с одинаковыми Фамилией и Именем."""
    merged = {}
    for contact in contacts[1:]:
        key = (contact[0], contact[1])
        if key not in merged:
            merged[key] = contact[:]
        else:
            for i, value in enumerate(contact):
                if not merged[key][i] and value:
                    merged[key][i] = value
    return [contacts[0]] + list(merged.values())


# ---------- выполнение ----------

contacts_list = fix_names(contacts_list)
contacts_list = fix_phones(contacts_list)
contacts_list = merge_duplicates(contacts_list)


with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerows(contacts_list)
