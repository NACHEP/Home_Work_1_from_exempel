from Bot_new import (AddContact, ExitBot, SearchContact, EditContact, RemoveContact, SaveToFile, LoadFromFile,
                     Congratulate, ViewContact)

if __name__ == "__main__":
    choices = {
        'add': AddContact(),
        'search': SearchContact(),
        'edit': EditContact(),
        'remove': RemoveContact(),
        'save': SaveToFile(),
        'load': LoadFromFile(),
        'congratulate': Congratulate(),
        'view': ViewContact(),
        'exit': ExitBot(),
    }

    print('Hello. I am your contact-assistant. What should I do with your contacts?')
    bot = None
    bot_instance = None

    while True:
        action = input('Type help for a list of commands or enter your command\n').strip().lower()

        if not action:
            print("Please enter a valid action.")
            continue

        if action in choices:
            bot_instance = choices[action]
            bot_instance.book.load("auto_save")
            bot_instance.handle()
        else:
            print("Incorrect action!")

        if action == 'help':
            format_str = str('{:%s%d}' % ('^',20))
            for command in choices:
                print(format_str.format(command))
            action = input().strip().lower()

        if action in ['add', 'remove', 'edit']:
            bot_instance.book.save("auto_save")

        if action == 'exit':
            break


"""
from Bot_new import (AddContact, ExitBot, SearchContact, EditContact, RemoveContact, SaveToFile, LoadFromFile,
                     Congratulate, ViewContact)

if __name__ == "__main__":
    choices = {
        'add': AddContact(),
        'search': SearchContact(),
        'edit': EditContact(),
        'remove': RemoveContact(),
        'save': SaveToFile(),
        'load': LoadFromFile(),
        'congratulate': Congratulate(),
        'view': ViewContact(),
        'exit': ExitBot(),
    }

    print('Hello. I am your contact-assistant. What should I do with your contacts?')

    while True:
        action = input("Choose an action (type 'exit' to quit): ")

        if not action:
            print("Please enter a valid action.")
            continue

        if action in choices:
            choices[action].handle()
        else:
            print("Incorrect action!")
"""