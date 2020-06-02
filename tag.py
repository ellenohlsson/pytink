from collections import Counter
from datetime import date
import glob
import os
import operator

from export import write_csv

# Assumes that all transactions have no category
def export(transactions, filename):

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

    write_csv(filename, l)


# Expects transactions to be sorted by date, ascending.
def _date_last_transaction(descriptions, transactions):
    for t in reversed(transactions):
        if t.description == descriptions[0] and \
           t.original_description == descriptions[1]:

            return t.date

    print('WARNING: Found no match for description. (tag.py)')
    return None


def apply(tags, transactions):

    for t in tags:

        if t['category'] != 'None':
            # Find all related transactions
            related = [tr
                for tr in transactions
                if tr.modified_category == None and
                tr.description == t['description'] and
                tr.original_description == t['original_description']
            ]

            # Assign category
            if len(related) > 0:
                for r in related:
                    r.modified_category = t['category']
            else:
                # This probably means that an older tags file have the same
                # tag as a never tags file.
                # This can be a problem if category is not the same for both.
                print('WARNING: tag {} could not be applied.'.format(t))


def filenames(dir):
    cwd = os.getcwd()
    os.chdir(dir)

    l = list()
    for f in glob.glob('tags_*-*-*_*.csv'):
        l.append(f)

    os.chdir(cwd)

    return l
