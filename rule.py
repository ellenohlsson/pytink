from datetime import date
from dateutil.relativedelta import relativedelta
from itertools import tee, islice, chain

import config


def _load_config(config_file):
    return config.load_config(config_file)


def _get_function_pointer(name):
    return getattr(__import__(__name__), '_action_{}'.format(name))


def apply(transactions, config_file):
    print('[Applying rules from {}]\n'.format(config_file))

    config   = _load_config(config_file)
    rules    = config['transactions']
    settings = config['settings']

    for rule in rules:
        filtered = _filter(transactions, rule, settings)

        if filtered:
            for action in rule['action']:

                if isinstance(action, dict):
                    # Action has argument (only one supported)
                    action_name = [*action.keys()][0]
                    action_arg  = [*action.values()][0]
                else:
                    action_name = action
                    action_arg = None

                try:
                    function = _get_function_pointer(action_name)
                    function(filtered, rule['rule'], action_arg)
                except AttributeError:
                    print('ERROR: "{}" action "{}" is not implemented.'.format(rule['rule'], action_name))
                    continue

        else:
            print('WARNING: rule "{}" filter returned no transactions.'.format(rule['rule']))


def _filter_related_transactions(related, filter):

    if 'category' in filter:
        categories = [c.lower() for c in filter['category']]

    for t in related:

        if 'start_date' in filter:
            if t.date < filter['start_date']:
                related.remove(t)
                continue

        if 'end_date' in filter:
            if t.date > filter['end_date']:
                related.remove(t)
                continue

        if 'min_amount' in filter:
            if filter['min_amount'] < 0:
                if t.balance > filter['min_amount']:
                    related.remove(t)
                    continue
            else:
                if t.balance < filter['min_amount']:
                    related.remove(t)
                    continue

        if 'max_amount' in filter:
            if filter['max_amount'] < 0:
                if t.balance < filter['max_amount']:
                    related.remove(t)
                    continue
            else:
                if t.balance > filter['max_amount']:
                    related.remove(t)
                    continue

        if 'category' in filter and t.modified_category:
            if t.modified_category.lower() not in categories:
                related.remove(t)
                continue

    return related


def _prev_and_nxt(some_iterable):
            prevs, items, nexts = tee(some_iterable, 3)
            prevs = chain([None], prevs)
            nexts = chain(islice(nexts, 1, None), [None])
            return zip(prevs, items, nexts)


def _filter(transactions, rule, settings):
    filter = rule['filter']
    match_warning = settings['match_warning']

    related = []

    # Do rough filtering
    if 'description' in filter:
        for d in filter['description']:
            related.append([t
                for t in transactions
                if t.description == d[0] and
                    t.original_description == d[1]
            ])

    elif 'category' in filter:
        for c in filter['category']:
            related.append([t
                for t in transactions
                if t.modified_category == c
            ])

    # Flatten above list and sort by date
    related = [transaction for subrelated in related for transaction in subrelated]
    related.sort(key=lambda x: x.date)

    # Do fine filtering
    related = _filter_related_transactions(related, filter)

    if len(related) * 100 / len(transactions) > match_warning:
        print(('WARNING: {} matched more than {} percent (setting: match_warning) '
               'of given transactions.'.format(rule['rule'], match_warning)))

    return related


def _action_extend_to_next(transactions, rule_name, default_months = None):

        def _get_interval():
            rel = relativedelta(t_next.date - relativedelta(months=1), t.date)
            if rel.days > 24: # TODO Tune this.
                return rel.months + 1
            else:
                return rel.months

        for t_prev, t, t_next in _prev_and_nxt(transactions):

            if t.months_extend is not None:
                print('WARNING: transaction in rule {} previously extended, overriding.'.format(rule_name))

            if t_next:
                # Calculate the difference in months between transactions
                t.months_extend = _get_interval()

            elif t_prev:
                # Take previous extension and set to this transaction
                t.months_extend = t_prev.months_extend

            else:
                # This transaction has only happened once, go with configuration
                if default_months:
                    t.months_extend = default_months - 1
                else:
                    print(('WARNING: action "extend_to_next" in rule "{}" found only one transaction. '
                           'Hence a default number of months needs to be in configuration. Skipping.'
                    ).format(rule_name))
                    break

            if t.months_extend > 0:
                t.add_note(rule_name.replace(' ', '_') + '__extend_to_next')
