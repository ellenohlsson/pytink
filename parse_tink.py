import re
import ast
from datetime import datetime


def get_section_name():
    pass


def split_sections(delimiter, data):

    # Data example to match single_section
    # ## Section 1 (^## \w+)
    # WHATEVER (.*?)
    # ## Section 2 OR end of sections (?=^## |\Z)
    single_sections = '^{} \w+.*?(?=^{} |\Z)'.format(delimiter, delimiter)
    sections = re.findall(single_sections, data, re.S | re.M)

    d = dict()
    section_name = '^{} (.+)$'.format(delimiter)
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
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        elif 'Amount' in key:
            return float(value)
        elif 'Payload' in key:
            return ast.literal_eval(value)
        else:
            return value

    else:
        return None


def parse_fields(section):
    d = dict()

    re_lvl_hash = '^(#+) .+$'
    hash_lvls = re.findall(re_lvl_hash, section, re.M)


    if len(hash_lvls) == 1:
        re_fields = '^\s+(.+):\s+?(.*?)$'
        match = re.findall(re_fields, section, re.M)

        for m in match:
            key, value = m

            if key not in d:
                d[key] = parse_datatype(key, value.strip())
            else:
                print('ERROR: Key already exist2')
                break
    else:
        print('WARNING: Repayments not yet supported')

    return d


def parse_transactions(transactions):

    d = dict()
    for key, transaction in transactions.items():
        field_dict = parse_fields(transaction)

        if key not in d:
            d[key] = field_dict
        else:
            print('ERROR: Key already exist1')
            break

    return d


with open('tink-export-2020-04-10.txt', 'r') as f:
    d = f.read()

    s = split_sections('##', d)

    transaction_section = split_sections('###', s['Transactions:'])
    # print(transaction_section['Transaction 1'])
    transactions = parse_transactions(transaction_section)

    for i, (k, v) in enumerate(transactions.items()):
        print(k, v['Date'], type(v['Date']), i)

        if i >= 1:
            break

    print('herde')
