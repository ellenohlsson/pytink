from datetime import datetime
import csv


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
