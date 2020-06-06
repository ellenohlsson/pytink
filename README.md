# pytink
Parser for the financial smartphone app "Tink" GDPR dump with some added features not available in the app itself.

Project came about since Tink doesn't offer its users the option of exporting
their data in a reasonable format to do more in depth analysis of their economies.

This project is work in progress and can currently:
* parse the transaction and reimbursement part of the GDPR dump reliably.
* tag uncategorized\* transactions in a custom UI.
* apply rules to sets of transactions to extend their cost in time, label them as fixed cost or create groups.
* filter transactions in some rudimentary way.
* export CSV of raw and treated transactions.

\* By uncategorized transaction I unfortunately mean all transactions you've let Tink automatically label.
The GDPR export only contains categories for transactions you've manually changed.

Aim is to eventually use pytink as a module and move run.py out of it.

## Usage
1. To do a Tink GDPR dump head over to [Tink](https://account.tink.se), sign in and do a dump.
2. Checkout or download code for pytink.
3. Install Python 3.8 and then do "pip install -r requirements.txt". (or use supplied Dockerfile)
3. Edit rules and add your own in rules.yaml. If no rules are wanted, comment out that section in run.py.
4. Open run.py and change at least input file name to your GDRP dump (first filename in file). Run with "python run.py"
5. Raw, treated and uncategorized transaction CSV files should have been exported.
6. Optionally tag all uncategorized transactions with the tagging ui. Update "tag_file" (with generated tag file from previous step) in tag_ui.py then run it. When done, proceed to run run.py again to apply tags to CSV files.
7. Import CSV into your application of choice, plot and analyze your spending in more detail then ever possible with Tink itself!

Currently this project is much, much, more mature than my expense graph project [rexpense](https://github.com/ellenohlsson/rexpense),
but if you feel like checking that out I've decided to also make that public.
