import sys


def call_center(clients_list, recipients_list) -> list:
    return list(set(clients_list) - set(recipients_list))


def potential_clients(clients_list, participants_list) -> list:
    # participants in most recent event - all clients
    return list(set(participants_list) - set(clients_list))


def loyalty_program(clients_list, participants_list) -> list:
    # all clients - participants in most recent event
    return list(set(clients_list) - set(participants_list))


def main(task_name):
    clients = [  # all clients list
        'andrew@gmail.com',
        'jessica@gmail.com',
        'ted@mosby.com',
        'john@snow.is',
        'bill\_gates@live.com',
        'mark@facebook.com',
        'elon@paypal.com',
        'jessica@gmail.com',
    ]
    participants = [  # in most recent event
        'walter@heisenberg.com',
        'vasily@mail.ru',
        'pinkman@yo.org',
        'jessica@gmail.com',
        'elon@paypal.com',
        'pinkman@yo.org',
        'mr@robot.gov',
        'eleven@yahoo.com',
    ]
    recipients = [
        'andrew@gmail.com',
        'jessica@gmail.com',
        'john@snow.is',
    ]  # who viewed recent promotional email

    if task_name == "call_center":
        result = call_center(clients, recipients)
    elif task_name == "potential_clients":
        result = potential_clients(clients, participants)
    elif task_name == "loyalty_program":
        result = loyalty_program(clients, participants)
    else:
        raise ValueError(
            f"Invalid task name: {task_name}. One of the following was expected: call_center, potential_clients, loyalty_program."
        )

    print(result)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py [call_center|potential_clients|loyalty_program]")
        sys.exit(1)
    taskname = sys.argv[1]
    main(taskname)
