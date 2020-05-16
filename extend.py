from datetime import date
from dateutil.relativedelta import relativedelta
from itertools import tee, islice, chain

def transactions(transactions):

    # TODO add extension of whole catetegory
    # TODO add support for multiple descriptions because some companies change over time
    # TODO add a field that says how many months to extend if only 1 transition exists.
    #      Currently the algorithm needs two transactions to figure out a third and last extension.
    # TODO add minimum sum to extend
    # TODO indicate in tag that transaction is an extension
    extend_by = [
        {
        'description' : 'Bredband2',
        'original_description': 'BREDBAND2 AB',
        'start_date' : date(2018, 1, 1),
        'end_date': date(2020, 9, 1)
        },
        {
        'description' : 'If Skadeförsäk',
        'original_description': 'IF SKADEFÖRSÄK',
        'start_date' : date(2017, 12, 1),
        'end_date': date(2020, 12, 1)
        }
    ]

    for ext in extend_by:

        # Find all related transactions
        related = [t
            for t in transactions
            if t.description == ext['description'] and
               t.original_description == ext['original_description']
        ]

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

            if 'start_date' in ext:
                if r.date < ext['start_date']:
                    continue

            if 'end_date' in ext:
                if r.date > ext['end_date']:
                    continue

            if r_next:
                r.months_extend = _get_interval()
            else:
                r.months_extend = r_prev.months_extend
