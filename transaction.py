# TOOO rename (to filter?) and extend


def filter_exclude(transaction):

    if abs(transaction.balance) > 1.0:
        if 'Transfer' not in transaction.type:
            if transaction.category:
                if transaction.category not in ['Exkludera', 'Överföringar']:
                    return False
            else:
                return False

    return True


def uncategorized(transactions):
    l = list()
    for t in transactions:
        if 'Default' in t.type:
            if t.category is None:
                l.append(t)

    return l
