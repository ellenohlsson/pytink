# pytink
Parser for Tink GDPR dump with some added features not available in Tink itself

Project came about since Tink doesn't offer it's users the option of exporting
their data and do more in depth analysis of the spending.

This project is work in progress and can currently only:
* parse the transaction and reimbursement part of the GDPR dump reliably.
* tag uncategorized\* transactions in custom GUI.
* extend configured transactions to divide amount per month until next transaction.
* filter transactions in some rudimentary way.
* export CSV of either raw or treated transactions.

\* By uncategorized transaction I unfortunately mean all transactions you've let Tink automatically label.
The GDPR export only contains categorise for transactions you've manually changed.

To do a Tink GDPR dump head over to [Tink](https://account.tink.se), sign in and do a dump.
Next, open run.py and tinker around. 
Aim is to eventually use pytink as a module and move run.py out of it.

Currently this project is more mature than my expense graph project [rexpense](https://github.com/ellenohlsson/rexpense),
but if you feel like checking that out I've decided to also make that public.
