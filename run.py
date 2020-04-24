import argparse

import parse
import export
import extend
import tag
import transaction


if __name__ == '__main__':

    transactions = list()
    transactions = parse.transactions('tink-export-2020-04-19.txt', 'Transactions:', 'transactions.csv')
    transactions.sort(key=lambda x: x.date)

    # Find uncategorized transactions and export for tagging gui
    uncategorized = transaction.uncategorized(transactions)
    if len(uncategorized) > 0:
        filename = 'tags.csv'
        tag.export_uncategorized(uncategorized, filename)
        print('Exported {} with missing tags. Please tag before proceeding.'.format(filename))

    else: # Everythings categorized, proceed.

        # Extend transactions
        extend.extend_transaction(transactions)
        l = list()
        for t in transactions:
            serialized_obj = t.serialize()
            for s in serialized_obj:
                l.append(s)

        l.sort(key=lambda x: x[1])
        l.insert(0, transactions[0].serialize_header())
        export.write_csv('final_export.csv', l)
