import PySimpleGUI as sg
import re

import export


categories = sorted(['Hyra', 'Ränta & Amortering', 'Media, Tele & IT', 'Drift', 'Försäkringar & Avgifter', 'Tjänster', 'Boende & Hushåll Övrigt',
              'Renovering & Bygg', 'Inredning & Möbler', 'Trädgård & Blommor', 'Hem & Trädgård Övrigt',
              'Livsmedel', 'Restaurang', 'Fika & Snacks', 'Alkohol & Tobak', 'Bar', 'Mat & Dryck Övrigt',
              'Bil & Bränsle', 'Tåg & Buss', 'Flyg', 'Taxi', 'Transport Övrigt',
              'Kläder & Accessoarer', 'Hemelektronik', 'Sport- & Fritidsatrtiklar', 'Böcker & Spel', 'Presenter', 'Shopping Övrigt',
              'Kultur & Nöje', 'Hobby', 'Sport & Träning', 'Semester', 'Fritid Övrigt',
              'Vård & Omsorg', 'Apotek', 'Optik', 'Skönhet', 'Hälsa & Skönhet Övrigt',
              'Kontantuttag', 'Utlägg', 'Barn', 'Husdjur', 'Välgörenhet', 'Utbildning', 'Okategoriserat', 'Övrigt',
              'Lön', 'Pension', 'Återbetalningar', 'Stöd & Bidrag', 'Sparränta & Utdelning', 'Övriga Inkomster',
              'Sparande', 'Överföringar', 'Exkludera'])


def num_transactions(tags, from_idx):
    return sum(int(t['transaction_count']) if t['category'] == 'None' else 0 for t in tags[from_idx:])


def match_categories(input, categories):

    early_metric = 0
    span_metric = 0
    metrics = list()
    for c in categories:

        # Does input match a category exactly?
        if re.fullmatch(input, c, re.I):
            return c

        # Search for partial matches
        m = re.search(input, c, re.I)
        try:
            early_metric = m.span(0)[0]                # We're does match start?
            span_metric  = m.span(0)[1] - m.span(0)[0] # How many chars were matched?
        except:
            early_metric = -1
            span_metric  = -1

        metrics.append((span_metric, early_metric, c))

    # Find longest match as early as possible in the string
    metrics.sort(key=lambda m: (-m[0], m[1]))

    # Take first non-zero longest match
    idx = next((idx for idx, m in enumerate(metrics) if m[0] > 0), None)

    return metrics[idx][2] if idx is not None else ''


def _is_active(idx):
    return idx > -1


def _enable_buttons(idx, window):
    if not hasattr(_enable_buttons, "prev_idx"):
        _enable_buttons.prev_idx = None

    if idx != _enable_buttons.prev_idx:
        if idx == 0:
            window['category'].update(disabled=False)
            window['tag_category'].update('')
            window['>'].Update(button_color=('white','#283b5b'))
        if idx > 0:
            window['<'].Update(disabled=False)
        elif idx < 1:
            window['<'].Update(disabled=True)
        elif idx >= len(tags) - 1:
            window['>'].Update(disabled=True)

    _enable_buttons.prev_idx = idx


# Import data
tag_file = 'tags.csv'
(tags, csv_fieldnames) = export.read_csv(tag_file)
transaction_count = num_transactions(tags, 0)

# Sort tags to have untagged first
tags.sort(key=lambda x: 1 if x['category'] == 'None' else 0, reverse=True)

# TODO add a button to see all categories
layout = [[sg.Text('Tag transaction:', font=('Helvetica', 8, 'bold'))],
          [sg.Text('description', size=(26, 1), font=('Helvetica', 12), key='description'), sg.Text('last_transaction', size=(15, 1), font=('Helvetica', 12), key='last_transaction')],
          [sg.Text('original_description', size=(26, 1), font=('Helvetica', 12), key='original_description'), sg.Text('transaction_count', size=(15, 1), font=('Helvetica', 12), key='transaction_count')],
          [sg.Text('tag_category', size=(30,1), key='tag_category', text_color='black', font=('Helvetica', 12, 'bold'))],
          [sg.Text('Enter category:', size=(15, 1), font=('Helvetica', 8, 'bold'))],
          [sg.Input(size=(25, 1), justification='left', key='category', enable_events=True, disabled=True, font=('Helvetica', 12, 'bold')), sg.Button('<', disabled=True, font=('Helvetica', 8, 'bold')), sg.Button('>', button_color=('red','#283b5b'), font=('Helvetica', 8, 'bold')), sg.Button('Save', disabled=True, font=('Helvetica', 8, 'bold'))],
          [sg.ProgressBar(transaction_count, orientation='h', size=(32, 10), key='progbar'), sg.Text('-/{}'.format(transaction_count), size=(11, 1), font=('Helvetica', 7), key='progtext')]]

window = sg.Window('pytink-tagger', layout, return_keyboard_events=True)

# Event loop
idx = -1
category = ''
while True:
    event, values = window.read()

    if event is None:  # if the X button clicked, just exit
        print('exit.')
        break

    if event == '>':
        idx = idx + 1

    elif event == '<' and _is_active(idx):
        idx = idx - 1 if idx > 0 else 0

    elif event == 'Save' and _is_active(idx):
        export.dictwriter_csv(tag_file, tags, csv_fieldnames)
        window['Save'].Update(disabled=True)

    elif event == 'category' and _is_active(idx):
        # TODO fix render glitch when pressing erase in input with zero chars
        category = match_categories(values['category'], categories)
        window['tag_category'].update(category)
        continue # Skip rest of update

    elif event == 'Return:44' and _is_active(idx): # Return key was pressed
        if category:
            tags[idx]['category'] = category

            # Update UI
            category = ''
            window['tag_category'].update(category)
            window['category'].update('')
            window['Save'].Update(disabled=False)

            # Go to next transaction
            idx = idx + 1

    # Update UI
    _enable_buttons(idx, window)

    if _is_active(idx):

        # Transaction view
        window['description'].update(tags[idx]['description'])
        window['original_description'].update(tags[idx]['original_description'])
        window['last_transaction'].update(tags[idx]['last_transaction'])
        window['transaction_count'].update(tags[idx]['transaction_count'])

        # Is user not typing anything? Then show the transactions category (if any)
        if len(values['category']) == 0:
            window['tag_category'].update(tags[idx]['category'] if tags[idx]['category'] != 'None' else '')

        # Progress bar
        prog = transaction_count - num_transactions(tags, idx)
        window['progtext'].update('{}/{}'.format(prog, transaction_count))
        window['progbar'].update_bar(prog)
