# pytink
Parser for Tink GDPR dump with some added features not available in Tink itself.

Project came about since Tink doesn't offer its users the option of exporting
their data in a reasonable format to do more in depth analysis of their economies.

This project is work in progress and can currently:
* parse the transaction and reimbursement part of the GDPR dump reliably.
* tag uncategorized\* transactions in a custom UI.
* apply rules to sets of transactions to extend their cost in time or label them as fixed cost.
* filter transactions in some rudimentary way.
* export CSV of either raw or treated transactions.

\* By uncategorized transaction I unfortunately mean all transactions you've let Tink automatically label.
The GDPR export only contains categories for transactions you've manually changed.

To do a Tink GDPR dump head over to [Tink](https://account.tink.se), sign in and do a dump.
Next, open run.py and tinker around. 
Aim is to eventually use pytink as a module and move run.py out of it.

Currently this project is much more mature than my expense graph project [rexpense](https://github.com/ellenohlsson/rexpense),
but if you feel like checking that out I've decided to also make that public.
