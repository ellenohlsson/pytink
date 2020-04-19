import re

import parse as p

class Reimbursement():

    def __init__(self, reimbursement_section):
        self.id = p.get_section_id('- Part (\d*,*\d+)', reimbursement_section)

        self.all_fields = p.parse_fields(reimbursement_section)
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

        self.id = p.get_section_id('Transaction (\d*,*\d+)', transaction_section)
        self.reimbursements = dict()

        # Check if there's any repayments connected to this transaction
        re_lvl_hash = '^(#+) .+$'
        hash_lvls = re.findall(re_lvl_hash, transaction_section, re.M)

        if len(hash_lvls) > 1:

            # Split reimbursements
            rb_sections = p.split_sections('####', transaction_section)

            r = dict()
            for _, repay_str in rb_sections.items():
                rb = Reimbursement(repay_str)
                r[rb.id] = rb

                # Get rid of reimbursements from transaction section
                transaction_section = transaction_section.replace(repay_str, '')

            self.reimbursements = r

        self.all_fields = p.parse_fields(transaction_section)
        self._map_fields()

    def _map_fields(self):
        f = self.all_fields

        self.date = f['Date']
        self.description = f['Description']
        self.original_description = f['Original Description']
        self.amount = f['Amount']
        self.balance = self.amount - self.sum_reimbursements()
        self.type = f['Type']
        self.note = self.parse_note(f['Note'])

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

    def parse_note(self, note):
        n = re.findall(r'#(\w+)', note if note else '')
        return ';'.join(n) if n else None

    def serialize(self):
        return [self.id, self.date, self.description, self.balance, self.type, p.nonetype_to_str(self.modified_category), p.nonetype_to_str(self.note)]

    def serialize_header(self):
        return ['ID', 'Date', 'Description', 'Balance', 'Type', 'Modified_Category', 'Note']