from datetime import datetime as dt, timedelta
from collections import UserList
import pickle
from info import *
import os


class AddressBook(UserList):
    def __init__(self):
        # super().__init__()
        self.data = []
        self.counter = -1

    def __str__(self):
        result = []
        # print(result)
        for account in self.data:
            if account["birthday"]:
                day_of_birth: object = account["birthday"].strftime("%d/%m/%Y")
            else:
                day_of_birth = ""
            if account["phones"]:
                new_value = []
                for phone in account["phones"]:
                    print(phone)
                    if phone:
                        new_value.append(phone)
                phone = ", ".join(new_value)
            else:
                phone = ""
            result.append(
                "_" * 50
                + "\n"
                + f"Name: {account['name']} \nPhones: {phone} \nBirthday: {day_of_birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"
                + "_" * 50
                + "\n"
            )
        return "\n".join(result)

    def __next__(self):
        global date_of_birth
        phones = []
        self.counter += 1
        if self.counter == len(self.data):  # add
            self.counter = -1  # add
            raise StopIteration  # add
        if self.data[self.counter]["birthday"]:
            date_of_birth = self.data[self.counter]["birthday"].strftime("%d/%m/%Y")
        if self.counter == len(self.data):
            self.counter = -1
            raise StopIteration
        for number in self.data[self.counter]["phones"]:
            if number:
                phones.append(number)
        result = (
            "_" * 50
            + "\n"
            + f"Name: {self.data[self.counter]['name']} \nPhones: {', '.join(phones)} \nBirthday: {date_of_birth} \nEmail: {self.data[self.counter]['email']} \nStatus: {self.data[self.counter]['status']} \nNote: {self.data[self.counter]['note']}\n"
            + "_" * 50
        )
        return result

    def __iter__(self):
        return self

    def __setitem__(self, index, record):
        self.data[index] = {
            "name": record.name,
            "phones": record.phones,
            "birthday": record.birthday,
        }

    def __getitem__(self, index):
        return self.data[index]

    @staticmethod
    def log(action):
        current_time = dt.strftime(dt.now(), "%H:%M:%S")
        message = f"[{current_time}] {action}"
        with open("logs.txt", "a") as file:
            file.write(f"{message}\n")

    def add(self, record):
        account = {
            "name": record.name,
            "phones": record.phones,
            "birthday": record.birthday,
            "email": record.email,
            "status": record.status,
            "note": record.note,
        }
        self.data.append(account)
        self.log(f"Contact {record.name} has been added.")

    def save(self, file_name):
        try:
            with open(file_name + ".bin", "wb") as file:
                pickle.dump(self.data, file)
            self.log("Addressbook has been saved!")
        except Exception as e:
            print(f"Error saving address book: {e}")

    def load(self, file_name):
        emptyness = os.stat(file_name + ".bin")
        if emptyness.st_size != 0:
            try:
                with open(file_name + ".bin", "rb") as file:
                    self.data = pickle.load(file)
                self.log("Addressbook has been loaded!")
            except Exception as e:
                print(f"Error loading address book: {e}")
        else:
            self.log("Adressbook has been created!")
        return self.data

    def search(self, pattern, category):
        result = []
        category_new = category.strip().lower().replace(" ", "")
        pattern_new = pattern.strip().lower().replace(" ", "")

        for account in self.data:
            if category_new == "phones":
                for phone in account["phones"]:
                    if phone.lower().startswith(pattern_new):
                        result.append(account)
            elif account[category_new].lower().replace(" ", "") == pattern_new:
                result.append(account)
        if not result:
            print("There is no such contact in address book!")
        return result

    def edit(self, contact_name, parameter, new_value):
        names = []
        try:
            for account in self.data:
                names.append(account["name"])
                if account["name"] == contact_name:
                    if parameter == "birthday":
                        new_value = Birthday(new_value).value
                    elif parameter == "email":
                        new_value = Email(new_value).value
                    elif parameter == "status":
                        new_value = Status(new_value).value
                    elif parameter == "phones":
                        new_contact = new_value.split(" ")
                        new_value = []
                        for number in new_contact:
                            new_value.append(Phone(number).value)
                    if parameter in account.keys():
                        account[parameter] = new_value
                    else:
                        raise ValueError
            if contact_name not in names:
                raise NameError
        except ValueError:
            print("Incorrect parameter! Please provide correct parameter")
        except NameError:
            print("There is no such contact in address book!")
        else:
            self.log(f"Contact {contact_name} has been edited!")
            return True
        return False

    def remove(self, pattern):
        flag = False
        for account in self.data:
            if account["name"] == pattern:
                self.data.remove(account)
                self.log(f"Contact {account['name']} has been removed!")
                flag = True
            """if pattern in account['phones']:
                        account['phones'].remove(pattern)
                        self.log.log(f"Phone number of {account['name']} has been removed!")"""
        return flag

    @staticmethod
    def __get_current_week():
        now = dt.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]

    def congratulate(self):
        result = []
        WEEKDAYS = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        current_year = dt.now().year
        congratulate = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
        }
        for account in self.data:
            if account["birthday"]:
                new_birthday = account["birthday"].replace(year=current_year)
                birthday_weekday = new_birthday.weekday()
                if (
                    self.__get_current_week()[0]
                    <= new_birthday.date()
                    < self.__get_current_week()[1]
                ):
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(account["name"])
                    else:
                        congratulate["Monday"].append(account["name"])
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {' '.join(value)}")
        return "_" * 50 + "\n" + "\n".join(result) + "\n" + "_" * 50

    """
if __name__ == "__main__":
    address_book = AddressBook()


    # Example: Add a contact
    address_book.add({'name': Joe,
                   'phones': +380958913434,
                   'birthday': 12/5/2000,
                   'email': joe@gmail.com,
                   'status': friend,
                   'note': bestfriend} )


    # Example: Print the address book
    print(address_book)

    # Example: Search for a contact
    search_result = address_book.search('John Doe', 'name')
    print('Search result:', search_result)

    # Example: Edit a contact
    address_book.edit('John Doe', 'birthday', '1991-01-01')

    # Example: Save and load the address book
    address_book.save('my_address_book')
    loaded_address_book = AddressBook()
    loaded_address_book.load('my_address_book')
    print('Loaded address book:', loaded_address_book)

    # Example: Remove a contact
    address_book.remove('John Doe')

    # Example: Print the address book after removing
    print(address_book)

    # Example: Congratulate on birthdays
    birthday_congratulations = address_book.congratulate()
    print(birthday_congratulations)

"""
