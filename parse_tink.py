import re
import ast
import csv

from datetime import datetime


class Reimbursement():

    def __init__(self, reimbursement_section):
        self.id = get_section_id('- Part (\d*,*\d+)', reimbursement_section)

        self.all_fields = parse_fields(reimbursement_section)
        self._map_fields()


    def _map_fields(self):
        f = self.all_fields

        self.date = f['Date']
        self.amount = f['Amount']
        self.category = f['Category']
        self.counterpart_description = f['Counterpart Description']
        self.counterpart_amount = f['Counterpart Amount']


class Transaction():

    def __init__(self, transaction_section):

        self.id = get_section_id('Transaction (\d*,*\d+)', transaction_section)
        self.reimbursements = dict()

        # Check if there's any repayments connected to this transaction
        re_lvl_hash = '^(#+) .+$'
        hash_lvls = re.findall(re_lvl_hash, transaction_section, re.M)

        if len(hash_lvls) > 1:

            # Split reimbursements
            rb_sections = split_sections('####', transaction_section)

            r = dict()
            for _, repay_str in rb_sections.items():
                rb = Reimbursement(repay_str)
                r[rb.id] = rb

                # Get rid of reimbursements from transaction section
                transaction_section = transaction_section.replace(repay_str, '')

            self.reimbursements = r

        self.all_fields = parse_fields(transaction_section)
        self._map_fields()

    def _map_fields(self):
        f = self.all_fields

        self.date = f['Date']
        self.description = f['Description']
        self.original_description = f['Original Description']
        self.amount = f['Amount']
        self.balance = self.amount - self.sum_reimbursements()
        self.type = f['Type']

        # Optional field
        try:
            self.modified_category = f['Modified category']
        except:
            self.modified_category = None

    def sum_reimbursements(self):
        sum = 0
        for _, r in self.reimbursements.items():
            sum += r.amount
        return sum

    def serialize(self):
        return [self.id, self.date, self.description, self.balance, self.type, nonetype_to_str(self.modified_category)]

    def serialize_header(self):
        return ['ID', 'Date', 'Description', 'Balance', 'Type', 'Modified Category']


def get_section_id(re_id, section):
    m = re.findall(re_id, section)
    return int(m[0].replace(',', ''))


def nonetype_to_str(n):
    if n is None:
        return 'None'
    return n


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
    # Example:
    # '    Amount:      123.0'
    # '    Description: asdf'
    re_fields = '^\s+(.+):\s+?(.*?)$'
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


def get_transactions(sections):
    transactions = list()
    for _, section in sections.items():
        transactions.append(Transaction(section))

    return transactions


def write_csv(filename, csv_list):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_list)


def parse_export(filename, section_title, csv_filename):

    with open(filename, 'r') as f:
    fcontent = f.read()

    section_top = split_sections('##', fcontent)
        section_trans = split_sections('###', section_top[section_title])
    transactions = get_transactions(section_trans)

    def _exclude(trans):
        if abs(trans.balance) > 1.0:
            if 'Transfer' not in trans.type:
                if trans.modified_category:
                    if 'Exkludera' not in trans.modified_category:
                        return False
                else:
                    return False
        return True

    l = list()
    # Prepare CSV output
    for t in transactions:
        if not _exclude(t):
            l.append(t.serialize())

    # Sort by date and add header
    l.sort(key=lambda x: x[1])
    l.insert(0, transactions[0].serialize_header())

        write_csv(csv_filename, l)


if __name__ == '__main__':
    parse_export('tink-export-2020-04-10.txt', 'Transactions:', 'transactions.csv')
