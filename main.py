import pickle
import bot_classes


address_book = bot_classes.AddressBook()
filename = 'address_book.pkl'


def save_to_file():
    with open(filename, 'wb') as file:
        pickle.dump(address_book.data, file)


def load_from_file():
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            address_book.data = data
    except FileNotFoundError:
        pass


# Decorator:
def input_error(func):
    def wrapper(command):
        args = command.split(' ')
        if command.startswith('add') and len(args) < 3:
            print("Give me name and phone please")
        elif command.startswith('change') and len(args) < 3:
            print("Give me name and phone please")
        elif command.startswith('phone') and len(args) < 2:
            print("Enter user name")
        elif not (command.startswith('add')\
                  or command.startswith('change')\
                  or command.startswith('search')\
                  or command.startswith('phone') \
                  or command.startswith('delete') \
                  or command == "hello"\
                  or command == "show all"):
            print('Unknown command ╮( ˘ ､ ˘ )╭')
        else:
            func(command)

    return wrapper


# Handler function wrapped by decorator:
@input_error
def command_handler(command):
    if command.startswith('add'):
        name, phone = str(command.split(' ')[1]).capitalize(), command.split(' ')[2]
        new_record = bot_classes.Record(name)
        new_record.add_phone(phone)
        address_book.add_record(new_record)
    elif command.startswith('change'):
        name, phone = str(command.split(' ')[1]).capitalize(), command.split(' ')[2]
        target_record = address_book.find(name)
        target_record.edit_phone(target_record.phones[0].value, phone)
        print(f"{name}`s phone number has been successfully changed to {phone}")
    elif command.startswith('phone'):
        name = str(command.split(' ')[1]).capitalize()
        target_record = address_book.find(name)
        if target_record.phones:
            print(f'{name}`s phone is {target_record.phones[0].value}')
    elif command.startswith('search'):
        search_string = str(command.split(' ')[1])
        result = address_book.search(search_string)
        if len(result) < 2:
            print(f'There is {len(result)} record for your search:')
        else:
            print(f'There are {len(result)} records for your search:')
        for record in result:
            print(record)
    elif command.startswith('delete'):
        name = str(command.split(' ')[1]).capitalize()
        address_book.delete(name)
    elif command == "hello":
        print("How can I help you?")
    elif command == "show all":
        for chunk in address_book.iterator():
            for record in chunk:
                print(record)


# Main function:
def main():
    # Greeting:
    print('Hi! I`m a bot assistant (´･ᴗ･ ` )')
    waiting = True
    while waiting:
        command = input(': ').lower()
        if command == "good bye" or command == "close" \
                or command == "exit":
            print("Good bye!")
            waiting = False
        else:
            command_handler(command)


if __name__ == '__main__':
    load_from_file()
    main()
    save_to_file()
