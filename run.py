import argparse

import parse
import export
import extend
import tag
import transaction


if __name__ == '__main__':

    transactions = list()
    transactions = parse.transactions('tink-export-2020-04-19.txt',
                                      'Transactions:',
                                      'raw_transactions_{}.csv'.format(export.date()))
    transactions.sort(key=lambda x: x.date)

    # Apply existing tags
    # TODO read all tags files and apply
    (tags, _) = export.read_csv('tags.csv')
    tag.apply(tags, transactions)

    # Find still uncategorized transactions and export for tagging gui
    uncategorized = transaction.uncategorized(transactions)
    if len(uncategorized) > 0:
        filename = 'tags_{}.csv'.format(export.date())
        tag.for_ui(uncategorized, filename)

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
