line_of_cars = {'Oil': {'Quantity': 2, 'ticket_numbers': [2, 4]},
                'Tires': {'Quantity': 2, 'ticket_numbers': [1, 3]},
                'Diagnostics': {'Quantity': 0, 'ticket_numbers': []}
                }
counter = 0


def find_next_ticket():
    global counter

    if line_of_cars['Oil']['Quantity'] > 0:
        next_ticket = line_of_cars['Oil']['ticket_numbers'][0]
    elif line_of_cars['Tires']['Quantity'] > 0:
        next_ticket = line_of_cars['Tires']['ticket_numbers'][0]
    elif line_of_cars['Diagnostics']['Quantity'] > 0:
        next_ticket = line_of_cars['Diagnostics']['ticket_numbers'][0]
    else:
        next_ticket = 0
    if counter == 0:
        next_ticket = 1
        counter += 1
    return next_ticket, 12, 13


def pop_ticket():
    pass
    next_ticket = find_next_ticket()
    for key, value in line_of_cars.items():
        if value['Quantity'] > 0:
            for ticket in value['ticket_numbers']:
                if ticket == next_ticket:
                    print(line_of_cars[key]['ticket_numbers'].pop(0))
                    line_of_cars[key]['Quantity'] -= 1
    print(line_of_cars)


a, b = find_next_ticket()
print(a)
print(b)
