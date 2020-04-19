import csv


def write_csv(filename, csv_list):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_list)