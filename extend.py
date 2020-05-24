from datetime import date
from dateutil.relativedelta import relativedelta
from itertools import tee, islice, chain

import config


def _load_config(config_file):
    return config.load_config(config_file)


def transactions(transactions, config_file):

    extend = _load_config(config_file)['transaction']

    for ext in extend:

        ### Find all related transactions
        related = []

        # Go through each possible description of transaction
        for d in ext['description']:
            related.append([t
                for t in transactions
                if t.description == d[0] and
                t.original_description == d[1]
            ])

        # Flatten above list and sort by date
        related = [transaction for subrelated in related for transaction in subrelated]
        related.sort(key=lambda x: x.date)

        def _prev_and_nxt(some_iterable):
            prevs, items, nexts = tee(some_iterable, 3)
            prevs = chain([None], prevs)
            nexts = chain(islice(nexts, 1, None), [None])
            return zip(prevs, items, nexts)

        def _get_interval():
            rel = relativedelta(r_next.date - relativedelta(months=1), r.date)
            if rel.days > 24: # TODO Tune this.
                return rel.months + 1
            else:
                return rel.months

        # Extend transaction to one month before the next related one
        for r_prev, r, r_next in _prev_and_nxt(related):

            ### Skip transactions that are outside of criterias
            # TODO: these must be moved outside of this loop
            #       otherwise they will be used in next transaction under certain circumstances.

            if 'start_date' in ext:
                if r.date < ext['start_date']:
                    continue

            if 'end_date' in ext:
                if r.date > ext['end_date']:
                    continue

            if r_next:
                # Calculate the difference in months between transactions
                r.months_extend = _get_interval()

            elif r_prev:
                # Take previous extension and set to this transaction
                r.months_extend = r_prev.months_extend

            else:
                # This transaction has only happened once, go with default
                if 'default_months' in ext:
                    r.months_extend = ext['default_months'] - 1
                else:
                    print(('WARNING: transaction with description "{}" has only happened once '
                           'hence default_months needs to be in configuration. Skipping extension.'
                    ).format(r.description))


            r.add_note('Extended_pytink')
