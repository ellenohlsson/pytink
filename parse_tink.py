import re


def parse_sections(delimiter, data):
    
    # Data example to match single_section
    # ## Section 1
    # WHATEVER
    # ## Section 2 OR end of sections (\Z)
    single_sections = '^{} \w+.*?(?=^{} |\Z)'.format(delimiter, delimiter)
    sections = re.findall(single_sections, data, re.S | re.M)
        
    d = dict()
    section_name = '^{} (.+)$'.format(delimiter)    
    for section in sections:        
        key = re.match(section_name, section, re.M).group(1)
        
        if key not in d:
            d[key] = section
        else:
            print('ERROR: Section already exist')
            break
    
    return d


with open('tink-export-2020-04-10.txt', 'r') as f:
    d = f.read()
    
    s = parse_sections('##', d)
    
    s2 = parse_sections('###', s['Transactions:'])
    print(s2['Transaction 3,604'])
