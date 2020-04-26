import argparse
import os

import parse
import export
import extend
import tag
import transaction


if __name__ == '__main__':

    transactions = parse.transactions('tink-export-2020-04-19.txt')
    transactions.sort(key=lambda x: x.date)
    export.transactions(transactions, 'raw_transactions_{}.csv'.format(export.date()))

    # Apply existing tags
    for f in tag.filenames(os.getcwd()):
        (tags, _) = export.read_csv(f)
        tag.apply(tags, transactions)

    # TODO: filter out unwanted transactions

    # Find still uncategorized transactions and export for tagging
    uncategorized = transaction.uncategorized(transactions)
    if len(uncategorized) > 0:
        filename = 'tags_{}.csv'.format(export.date())
        tag.export(uncategorized, filename)

    # Extend transactions
    extend.transactions(transactions)

    # Export final transactions
    l = list()
    for t in transactions:
        serialized_obj = t.serialize()
        for s in serialized_obj: # Handles extended transactions
            l.append(s)

    l.sort(key=lambda x: x[1])
    l.insert(0, transactions[0].serialize_header())
    export.write_csv('transactions_{}.csv'.format(export.date()), l)
