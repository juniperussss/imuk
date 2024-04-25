### Tool to find unicode symbols for Synoptic events



def wmo_zu_unicode(wmo_code):
    if wmo_code < 10:
        unicode_base = 0x1F311  # Start Unicode point for single digit codes
    else:
        unicode_base = 0x1F3A0  # Start Unicode point for double digit codes

    return chr(unicode_base + wmo_code)

# Beispielaufrufe
for wmo_code in range(0, 100):
    unicode_symbol = wmo_zu_unicode(wmo_code)
    print("Unicode-Symbol für WMO-Code {}: {}".format(wmo_code, unicode_symbol))
