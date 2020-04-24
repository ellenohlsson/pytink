def default_exclusion(trans):
    if abs(trans.balance) > 1.0:
        if 'Transfer' not in trans.type:
            if trans.modified_category:
                if trans.modified_category not in ['Exkludera', 'Överföringar']:
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
