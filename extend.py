from datetime import date
from dateutil.relativedelta import relativedelta
from itertools import tee, islice, chain

import config


def _load_config(config_file):
    return config.load_config(config_file)


def _filter_related_transactions(related, config):

    for t in related:

        if 'start_date' in config:
            if t.date < config['start_date']:
                related.remove(t)
                continue

        if 'end_date' in config:
            if t.date > config['end_date']:
                related.remove(t)
                continue

        if 'min_amount' in config:
            if config['min_amount'] < 0:
                if t.balance > config['min_amount']:
                    related.remove(t)
                    continue
            else:
                if t.balance < config['min_amount']:
                    related.remove(t)
                    continue

        if 'max_amount' in config:
            if config['max_amount'] < 0:
                if t.balance < config['max_amount']:
                    related.remove(t)
                    continue
            else:
                if t.balance > config['max_amount']:
                    related.remove(t)
                    continue

        if 'category' in config:
            if t.modified_category != config['category']:
                related.remove(t)
                continue

    return related


def _prev_and_nxt(some_iterable):
            prevs, items, nexts = tee(some_iterable, 3)
            prevs = chain([None], prevs)
            nexts = chain(islice(nexts, 1, None), [None])
            return zip(prevs, items, nexts)


def transactions(transactions, config_file):

    extension_config = _load_config(config_file)['transaction']

    for config in extension_config:

        ### Find all related transactions
        related = []

        # Go through each possible description of transaction
        for d in config['description']:
            related.append([t
                for t in transactions
                if t.description == d[0] and
                   t.original_description == d[1]
            ])

        # Flatten above list and sort by date
        related = [transaction for subrelated in related for transaction in subrelated]
        related.sort(key=lambda x: x.date)

        # Go through optional configuration fields and do more filtering
        related = _filter_related_transactions(related, config)

        ### Extend transactions

        def _get_interval():
            rel = relativedelta(t_next.date - relativedelta(months=1), t.date)
            if rel.days > 24: # TODO Tune this.
                return rel.months + 1
            else:
                return rel.months

        for t_prev, t, t_next in _prev_and_nxt(related):

            if t_next:
                # Calculate the difference in months between transactions
                t.months_extend = _get_interval()

            elif t_prev:
                # Take previous extension and set to this transaction
                t.months_extend = t_prev.months_extend

            else:
                # This transaction has only happened once, go with configuration
                if 'default_months' in config:
                    t.months_extend = config['default_months'] - 1
                else:
                    print(('WARNING: extend rule "{}" found only one transaction. '
                           'Hence default_months needs to be in configuration. Skipping rule.'
                    ).format(config['rule']))
                    break

            if t.months_extend > 0:
                t.add_note('Extended_' + config['rule'].replace(' ', '_'))
