from datetime import datetime
import csv
# TODO rename module to export_csv


# TODO replace with dictwriter_csv
def write_csv(filename, csv_list):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_list)


def read_csv(filename):
    content = []
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            content.append(row)

    return (content, csv_reader.fieldnames)


def dictwriter_csv(filename, csv_dict, fieldnames):
    with open(filename, 'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)

        csv_writer.writeheader()
        csv_writer.writerows(csv_dict)


def nonetype_to_str(n):
    if n is None:
        return 'None'
    return n


def date():
    return datetime.now().strftime('%Y-%m-%d_%H%M')


def transactions(transactions, filename):

    # Prepare CSV output
    l = list()
    for t in transactions:
        serialized_obj = t.serialize()
        for s in serialized_obj: # Handles extended transactions
            l.append(s)

    # Sort and add header
    l.sort(key=lambda x: x[1])
    l.insert(0, transactions[0].serialize_header())

    write_csv(filename, l)