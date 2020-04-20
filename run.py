import argparse

import parse
import export
import extend

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("tink_filename", help="Filename to tink export") # Ex: tink-export-2020-04-10.txt
    parser.add_argument("section_to_parse", help="Section to parse") # Ex: Transactions
    parser.add_argument("csv_filename", help="Filename of csv export") # Ex: filename of csv to be exported
    args = parser.parse_args()


    transactions = list()
    if 'Transactions' in args.section_to_parse:
        transactions = parse.parse_export(args.tink_filename, 'Transactions:', args.csv_filename)

    uncategorized = parse.get_uncategorized_transactions(transactions)
    uncategorized.sort(key=lambda x: x[1])
    uncategorized.insert(0, transactions[0].serialize_header())
    export.write_csv('uncategorized.csv', uncategorized)

    # Extend transactions
    extend.extend_transaction(transactions)
    l = list()
    for t in transactions:
        serialized_obj = t.serialize()
        for s in serialized_obj:
            l.append(s)

    l.sort(key=lambda x: x[1])
    l.insert(0, transactions[0].serialize_header())
    export.write_csv('extended.csv', l)
