#!/usr/bin/env python3
# -*- config: utf-8 -*-

# 13. Создать класс Goods (товар). В классе должны быть представлены поля: на именование
# товара, дата оформления, цена товара, количество единиц товара, номер накладной, по
# которой товар поступил на склад. Реализовать методы изменения цены товара, изменения
# количества товара (увеличения и умень шения), вычисления стоимости товара.


class Goods:

    def __init__(self, name=' ', date=' ', price=0, num=0, waybill=' '):
        price = int(price)
        num = int(num)

        self.__name = name
        self.__date = date
        self.__price = abs(price)
        self.__num = abs(num)
        self.__waybill = waybill

    @property
    def name(self):
        return self.__name

    @property
    def date(self):
        return self.__date

    @property
    def price(self):
        return self.__price

    @property
    def num(self):
        return self.__num

    @property
    def waybill(self):
        return self.__waybill

    # def read(self, prompt=None):
    #     line = input() if prompt is None else input(prompt)
    #     parts = list(map(str, line.split(',', maxsplit=5)))
    #
    #     self.__name = parts[0]
    #     self.__date = parts[1]
    #     self.__price = abs(int(parts[2]))
    #     self.__num = abs(int(parts[3]))
    #     self.__waybill = parts[4]

    def __str__(self):
        return f"Наименование товара: {self.__name}\n" \
            f"Дата оформления: {self.__date}\n" \
            f"Цена товара: {self.__price}\n" \
            f"Количество едениц товара: {self.__num}\n" \
            f"Номер накладной: {self.__waybill}\n"

    def __repr__(self):
        return self.__str__()

    def __add__(self, new):
        if isinstance(new, Goods):
            price = self.price + new.price
            num = self.num + new.num

            return Goods(name=self.__name, date=self.__date, price=price, num=num, waybill=self.waybill)

    def __sub__(self, new):
        if isinstance(new, Goods):
            price = self.price - new.price
            num = self.num - new.num

            return Goods(name=self.__name, date=self.__date, price=price, num=num, waybill=self.waybill)

    def __mul__(self, new):
        if isinstance(new, Goods):
            old_total = self.price * self.num
            new_total = new.price * new.num

            return old_total, new_total
        else:
            raise ValueError()

    def __lt__(self, new):
        return self.__num < new.__num

    def __eq__(self, new):
        return self.__num == new.__num

    def __ne__(self, new):
        return self.__num != new.__num

    def __gt__(self, new):
        return self.__num > new.__num

    def __ge__(self, new):
        return self.num >= new.num

    def __le__(self, new):
        return self.num <= new.num


if __name__ == '__main__':
    a1 = Goods("Товар", "дата", 1000, 10, "накладная")
    a2 = Goods("Товар", "дата", 500, 5, "накладная")

    print(f"{a1}")
    print()
    print(f"{a2}")

    print(f"количество1 < количество2: {a1 < a2}")
    print(f"количество1 > количество2: {a1 > a2}")
    print(f"количество1 != количество2: {a1 != a2}")
    print(f"количество1 == количество2: {a1 == a2}")
    print(f"количество1 >= количество2: {a1 >= a2}")
    print(f"количество1 <= количество2: {a1 <= a2}\n")

    print(f"{a1 + a2}")
    print(f"{a1 - a2}")
    print(f"Старая сумма, новая сумма = {a1 * a2}")
