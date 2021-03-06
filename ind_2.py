#!/usr/bin/env python3
# -*- config: utf-8 -*-

# Вариант 12. Использовать словарь, содержащий следующие ключи: фамилия, имя; номер телефона;
# дата рождения (список из трех чисел). Написать программу, выполняющую следующие
# действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
# записи должны быть размещены по алфавиту; вывод на экран информации о людях, чьи
# дни рождения приходятся на месяц, значение которого введено с клавиатуры; если таких
# нет, выдать на дисплей соответствующее сообщение.

from dataclasses import dataclass, field
import sys
from typing import List
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class Person:
    name: str
    phone: int
    birthday: List[int]


@dataclass
class People:
    people: List[Person] = field(default_factory=lambda: [])

    def add(self, name: str, phone: int, birthday: List[int]) -> None:

        self.people.append(
            Person(
                name=name,
                phone=phone,
                birthday=birthday
            )
        )

        self.people.sort(key=lambda person: person.name)

    def __str__(self) -> str:

        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 8,
            '-' * 8,
            '-' * 8
            )
        table.append(line)
        table.append(
             '| {:^3} | {:^30} | {:^20} | {:^8} | {:^8} | {:^8} |'.format(
                    "№",
                    "ФИО",
                    "Номер телефона",
                    "День",
                    "Месяц",
                    "Год"
                )
        )
        table.append(line)

        for idx, person in enumerate(self.people, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>8} | {:>8} | {:>8} |'.format(
                    idx,
                    person.name,
                    person.phone,
                    person.birthday[0],
                    person.birthday[1],
                    person.birthday[2]
                )
            )

        table.append(line)

        return '\n'.join(table)

    def select(self, period):
        parts = command.split(' ', maxsplit=2)
        period = int(parts[1])
        result = []
        count = 0
        for person in self.people:
            if period == person.birthday[1]:
                count += 1
                result.append(person)
        return result

    def load(self, filename) -> None:
        with open(filename, 'r', encoding="utf8") as fin:
            xml = fin.read()

        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)

        self.people = []
        for person_element in tree:
            name, phone, birthday = None, None, None
            for element in person_element:
                if element.tag == 'name':
                    name = element.text
                elif element.tag == 'phone':
                    phone = element.text
                elif element.tag == 'birthday':
                    birthday = element.text
                    birthday = birthday.replace("[", "")
                    birthday = birthday.replace("]", "")
                    birthday = list(map(int, birthday.split(',')))

                if name is not None and phone is not None \
                        and birthday is not None:
                    self.people.append(
                        Person(
                            name=name,
                            phone=phone,
                            birthday=birthday
                        )
                    )

    def save(self, filename) -> None:
        root = ET.Element('People')
        for person in self.people:
            person_element = ET.Element('Person')

            name_element = ET.SubElement(person_element, 'name')
            name_element.text = person.name

            phone_element = ET.SubElement(person_element, 'phone')
            phone_element.text = person.phone

            birthday_element = ET.SubElement(person_element, 'birthday')
            birthday_element.text = str(person.birthday)

            root.append(person_element)

        tree = ET.ElementTree(root)
        with open(filename, 'wb') as fout:
            tree.write(fout, encoding='utf8', xml_declaration=True)


if __name__ == '__main__':

    people = People()

    while True:
        command = input(">>> ").lower()

        if command == 'exit':
            break

        elif command == 'add':
            name = input("Фамилия и инициалы: ")
            phone = input("Телефон: ")
            birthday = list(map(int, input("Дата рождения в формате: дд,мм,гггг ").split(',')))

            people.add(name, phone, birthday)

        elif command == 'list':
            print(people)

        elif command.startswith('select '):
            parts = command.split(maxsplit=1)
            selected = people.select(parts[1])

            if selected:
                for idx, person in enumerate(selected, 1):
                    print(
                        '{:>4}: {}'.format(idx, person.name)
                    )
            else:
                print("В этом месяце именинников нема")

        elif command.startswith('load '):
            parts = command.split(maxsplit=1)
            people.load(parts[1])

        elif command.startswith('save '):
            parts = command.split(maxsplit=1)
            people.save(parts[1])

        elif command == 'help':
            print("Список команд:\n")
            print("add - добавить работника;")
            print("list - вывести список работников;")
            print("select <стаж> - запросить работников со стажем;")
            print("load <имя_файла> - загрузить данные из файла;")
            print("save <имя_файла> - сохранить данные в файл;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)
