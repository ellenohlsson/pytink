import re
import ast

from datetime import datetime

import models
import export
import transaction


def get_section_id(re_id, section):
    m = re.findall(re_id, section)
    return int(m[0].replace(',', ''))


# Data example to match single_section
# ## Section 1 (^## \w+)
# WHATEVER (.*?)
# ## Section 2 OR end of sections (?=^## |\Z)
def split_sections(delimiter, data):
    single_sections = r'^{} \w+.*?(?=^{} |\Z)'.format(delimiter, delimiter)
    sections = re.findall(single_sections, data, re.S | re.M)

    d = dict()
    section_name = r'^{} (.+)$'.format(delimiter)
    for section in sections:
        key = re.match(section_name, section, re.M).group(1)

        if key not in d:
            d[key] = section
        else:
            print('ERROR: Section already exist3')
            break

    return d


def parse_datatype(key, value):
    if value:
        if 'Date' in key or 'Updated' in key:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').date()
        elif 'Amount' in key:
            return float(value)
        elif 'Payload' in key:
            return ast.literal_eval(value)
        else:
            return value

    else:
        return None


# Example:
# '    Amount:      123.0'
# '    Description: asdf'
def parse_fields(section):
    re_fields = r'^\s+(.+):\s+?(.*?)$'
    match = re.findall(re_fields, section, re.M)

    d = dict()
    for m in match:
        key, value = m

        if key not in d:
            d[key] = parse_datatype(key, value.strip())
        else:
            print('ERROR: Key already exist2')
            break

    return d


def _instantiate_transactions(sections):
    transactions = list()
    for _, section in sections.items():
        transactions.append(models.Transaction(section))

    return transactions


def transactions(filename, section_title, csv_filename):

    with open(filename, 'r') as f:
        fcontent = f.read()

        section_top = split_sections('##', fcontent)
        section_trans = split_sections('###', section_top[section_title])
        transactions = _instantiate_transactions(section_trans)

        l = list()
        # Prepare CSV output
        for t in transactions:
            if not transaction.default_exclusion(t):
                serialized_obj = t.serialize()
                for s in serialized_obj:
                    l.append(s)

        # Sort by date and add header
        l.sort(key=lambda x: x[1])
        l.insert(0, transactions[0].serialize_header())

        export.write_csv(csv_filename, l)

        return transactions
