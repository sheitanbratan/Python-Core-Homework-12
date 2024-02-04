from collections import UserDict
import datetime
import re


class NumberNotFound(Exception):
    def __init__(self, message='Number not found'):
        self.message = message
        super().__init__(self.message)


class BadBirthdayFormat(Exception):
    def __init__(self, message='Sorry, but birthday format is "YYYY-MM-DD"'):
        self.message = message
        super().__init__(self.message)


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)

    @property
    def name(self):
        return self.value

    @name.setter
    def name(self, new_name):
        self.value = new_name


class Phone(Field):
    def __init__(self, phone):
        super().__init__(self.phone_validation(phone))

    @property
    def phone(self):
        return self.value

    @phone.setter
    def phone(self, new_phone):
        self.value = Phone.phone_validation(new_phone)

    def phone_validation(self, phone):
        if len(phone) == 10 and phone.isnumeric():
            return phone
        else:
            raise ValueError


class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(self.birthday_validation(birthday))

    @property
    def birthday(self):
        return self.value

    @birthday.setter
    def birthday(self, new_birtday):
        self.value = Birthday.birthday_validation(new_birtday)

    def birthday_validation(self, birthday):
        date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}$')
        if birthday is not None:
            try:
                if bool(date_pattern.match(birthday)) is True:
                    return birthday
                else:
                    raise BadBirthdayFormat
            except BadBirthdayFormat as bbf:
                print(bbf.message)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = birthday
        self.phones = []

    def add_phone(self, phone):
        try:
            new_phone = Phone(phone)
            self.phones.append(new_phone)
            print(f"Phone {new_phone} added successfully to {self.name} record.")
        except ValueError as err:
            print(f'Error: {err}')

    def remove_phone(self, phone):
        try:
            for p in self.phones:
                if p.value == phone:
                    self.phones.remove(p)
            else:
                raise NumberNotFound
        except NumberNotFound as nnf:
            print(nnf.message)

    def find_phone(self, phone):
        try:
            for p in self.phones:
                if p.value == phone:
                    return p
            else:
                raise NumberNotFound
        except NumberNotFound as nnf:
            print(nnf.message)

    def edit_phone(self, phone, new_phone):
        for p in self.phones:
            if p.value == phone:
                p.value = new_phone
                return p
        else:
            raise ValueError

    def days_to_birthday(self, birthday):
        if birthday is not None:
            date_list = [int(birthday.split('-')[0]), int(birthday.split('-')[1]), int(birthday.split('-')[2])]
            birthday = datetime.date(date_list[0], date_list[1], date_list[2])
            result = (birthday - datetime.date.today()).days
            if result < 0:
                date_list[0] += 1
                birthday = '-'.join(str(date) for date in date_list)
                return Record.days_to_birthday(birthday)
            return f"There are {result} days until the next birthday."

    def __str__(self):
        return f"Contact name: {self.name.value}, phone: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict, dict):
    def __init__(self):
        super().__init__()
        self.data = {}

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            raise ValueError

    def find(self, name):
        if name in self.data:
            return self.data.get(name)
        else:
            print('Name not found')

    def search(self, search_string):
        found_records = []
        for record in self.data.values():
            if (
                search_string.lower() in record.name.value.lower()
                or any(search_string in phone.value for phone in record.phones)
            ):
                found_records.append(record)
        return found_records

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f'There is no more place for {name} in our address book')
        else:
            print('Name not found')

    def iterator(self, n=5):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i+n]




