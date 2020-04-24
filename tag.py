from collections import Counter
from datetime import date
import operator

import export


# Assumes that all transactions have no category
def export_uncategorized(transactions, filename):

    # Make sure transactions are sorted by date
    transactions.sort(key=lambda x: x.date)

    # Count number of transactions that have same descriptions
    to_count = list()
    for t in transactions:
        to_count.append((t.description, t.original_description))
    transaction_count = Counter(to_count).items()

    # Sort by number of transactions (descending)
    transaction_count = sorted(transaction_count, key=lambda x: x[1], reverse=True)

    # Export for tag gui
    l = list()
    for count in transaction_count:
        (description, original_description) = count[0]
        l.append([description,
                  original_description,
                  count[1],
                  _date_last_transaction((description, original_description), transactions),
                  'None'])

    # CSV Header
    l.insert(0, ['description',
                 'original_description',
                 'transaction_count',
                 'last_transaction',
                 'category'])

    export.write_csv(filename, l)


# Expects transactions to be sorted by date, ascending.
def _date_last_transaction(descriptions, transactions):
    for t in reversed(transactions):
        if t.description == descriptions[0] and \
           t.original_description == descriptions[1]:

            return t.date

    print('WARNING: Found no match for description. (tag.py)')
    return None
