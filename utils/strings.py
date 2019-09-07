import re


alpha_pattern = re.compile(r'[\W_0-9]+')
cleanse_string = lambda string: alpha_pattern.sub('', string)

no_unicode_pattern = re.compile(r'[^\x00-\x7F]+')
remove_unicode = lambda string: no_unicode_pattern.sub('', string)


def _get_23(name):    
    return name.ljust(3, '2')[1:3]


def _get_235(name):
    five = name.ljust(5, '2')
    return f"{five[1:3]}{five[4]}"

get_23 = _get_23
get_235 = _get_235

