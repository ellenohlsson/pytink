def filter_exclude(transaction):

    if abs(transaction.balance) > 1.0:
        if 'Transfer' not in transaction.type:
            if transaction.modified_category:
                if transaction.modified_category not in ['Exkludera', 'Överföringar']:
                    return False
            else:
                return False

    return True


def uncategorized(transactions):
    l = list()
    for t in transactions:
        if abs(t.balance) > 1.0:
            if 'Default' in t.type:
                if t.modified_category is None:
                    l.append(t)

    return l
