from abc import ABC, abstractmethod

from AddressBook import AddressBook, Record, Phone, Birthday, Email, Status, Note, Name


class AbstractBot(ABC):
    def __init__(self):
        self.book = AddressBook()

    @abstractmethod
    def handle(self):
        pass


class AddContact(AbstractBot):
    def handle(self):
        record = self.create_record()
        return self.book.add(record)

    @staticmethod
    def create_record():
        name = Name(input("Name: ")).value.strip()
        phones = Phone().value
        birth = Birthday().value
        email = Email().value.strip()
        status = Status().value.strip()
        note = Note(input("Note: ")).value
        record = Record(name, phones, birth, email, status, note)
        return record


class SearchContact(AbstractBot):

    def handle(self):
        print("There are following categories: \nName \nPhones \nBirthday \nEmail \nStatus \nNote")
        category = input('Search category: ')
        pattern = input('Search pattern: ')
        result = (self.book.search(pattern, category))
        return self.show_result(result)

    @staticmethod
    def show_result(result):
        for account in result:
            if account['birthday']:
                birth = account['birthday'].strftime("%d/%m/%Y")
            else:
                birth = "N/A"
            naw_result = "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: ', '.join(account['phones']) \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50
            print(naw_result)


class EditContact(AbstractBot):

    def handle(self):
        contact_name = input('Contact name: ')
        parameter = input('Which parameter to edit(name, phones, birthday, status, email, note): ').strip()
        new_value = input("New Value: ")
        self.edit_new(contact_name, parameter, new_value)

    def edit_new(self, contact_name, parameter, new_value):
        self.book.edit(contact_name, parameter, new_value)


class RemoveContact(AbstractBot):
    def handle(self):
        pattern = input("Remove (contact name or phone): ")
        return self.book.remove(pattern)


class SaveToFile(AbstractBot):

    def handle(self):
        file_name = self.give_a_name()
        return self.book.save(file_name)

    @staticmethod
    def give_a_name():
        files_name = input("File name: ")
        return files_name


class LoadFromFile(AbstractBot):

    def handle(self):
        file_name = self.load_a_file()
        return self.book.load(file_name)

    @staticmethod
    def load_a_file():
        loaded_fil = input("File name: ")
        return loaded_fil


class Congratulate(AbstractBot):

    def handle(self):
        result = self.book.congratulate()
        print(result)


class ViewContact(AbstractBot):

    def handle(self):
        self.view_contact()

    def view_contact(self):
        print(self.book)


class ExitBot(AbstractBot):

    def handle(self):
        print("Bye!")
        exit()
