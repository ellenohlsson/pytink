import argparse
import os

import parse
import export
import rule
import tag
import transaction


if __name__ == '__main__':

    # Load GDPR dump and parse transactions from it
    transactions = parse.transactions('tink-export-2020-04-19.txt')
    transactions.sort(key=lambda x: x.date)
    export.transactions(transactions, 'raw_transactions_{}.csv'.format(export.date()))

    # Filter out unwanted transactions (transfers and manual excludes)
    transactions = [t for t in transactions if not transaction.filter_exclude(t)]

    # Apply existing tags
    for f in tag.filenames(os.getcwd()):
        (tags, _) = export.read_csv(f)
        tag.apply(tags, transactions)

    # Filter out new unwanted transactions after applied tags (tagged transfers)
    transactions = [t for t in transactions if not transaction.filter_exclude(t)]

    # Find still uncategorized transactions and export for tagging
    uncategorized = transaction.uncategorized(transactions)
    if len(uncategorized) > 0:
        filename = 'tags_{}.csv'.format(export.date())
        tag.export(uncategorized, filename)

    # Apply rules
    rule.apply(transactions, 'rules.yaml')
    transactions.sort(key=lambda x: x.date)

    # Export final transactions
    export.transactions(transactions, 'transactions_{}.csv'.format(export.date()))
