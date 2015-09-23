## zer0-day (crypto, 50p, 824 solves)

> [eps1.9_zer0-day_b7604a922c8feef666a957933751a074.avi](zer0-day.bin)

Pobieramy wskazany plik. Jego zawartość to:

    RXZpbCBDb3JwLCB3ZSBoYXZlIGRlbGl2ZXJlZCBvbiBvdXIgcHJvbWlzZSBhcyBleHBlY3RlZC4g\n
    VGhlIHBlb3BsZSBvZiB0aGUgd29ybGQgd2hvIGhhdmUgYmVlbiBlbnNsYXZlZCBieSB5b3UgaGF2\n
    ZSBiZWVuIGZyZWVkLiBZb3VyIGZpbmFuY2lhbCBkYXRhIGhhcyBiZWVuIGRlc3Ryb3llZC4gQW55\n
    IGF0dGVtcHRzIHRvIHNhbHZhZ2UgaXQgd2lsbCBiZSB1dHRlcmx5IGZ1dGlsZS4gRmFjZSBpdDog\n
    eW91IGhhdmUgYmVlbiBvd25lZC4gV2UgYXQgZnNvY2lldHkgd2lsbCBzbWlsZSBhcyB3ZSB3YXRj\n
    aCB5b3UgYW5kIHlvdXIgZGFyayBzb3VscyBkaWUuIFRoYXQgbWVhbnMgYW55IG1vbmV5IHlvdSBv\n
    d2UgdGhlc2UgcGlncyBoYXMgYmVlbiBmb3JnaXZlbiBieSB1cywgeW91ciBmcmllbmRzIGF0IGZz\n
    b2NpZXR5LiBUaGUgbWFya2V0J3Mgb3BlbmluZyBiZWxsIHRoaXMgbW9ybmluZyB3aWxsIGJlIHRo\n
    ZSBmaW5hbCBkZWF0aCBrbmVsbCBvZiBFdmlsIENvcnAuIFdlIGhvcGUgYXMgYSBuZXcgc29jaWV0\n
    eSByaXNlcyBmcm9tIHRoZSBhc2hlcyB0aGF0IHlvdSB3aWxsIGZvcmdlIGEgYmV0dGVyIHdvcmxk\n
    LiBBIHdvcmxkIHRoYXQgdmFsdWVzIHRoZSBmcmVlIHBlb3BsZSwgYSB3b3JsZCB3aGVyZSBncmVl\n
    ZCBpcyBub3QgZW5jb3VyYWdlZCwgYSB3b3JsZCB0aGF0IGJlbG9uZ3MgdG8gdXMgYWdhaW4sIGEg\n
    d29ybGQgY2hhbmdlZCBmb3JldmVyLiBBbmQgd2hpbGUgeW91IGRvIHRoYXQsIHJlbWVtYmVyIHRv\n
    IHJlcGVhdCB0aGVzZSB3b3JkczogImZsYWd7V2UgYXJlIGZzb2NpZXR5LCB3ZSBhcmUgZmluYWxs\n
    eSBmcmVlLCB3ZSBhcmUgZmluYWxseSBhd2FrZSF9Ig==

Na pierwszy rzut oka to base64, wystarczy go zdekodować (pamiętając żeby "\n" nie traktowąc literalnie tylko wyciąć)

    Evil Corp, we have delivered on our promise as expected. The people of the
    world who have been enslaved by you have been freed. Your financial data has
    been destroyed. Any attempts to salvage it will be utterly futile. Face it: you
    have been owned. We at fsociety will smile as we watch you and your dark souls
    die. That means any money you owe these pigs has been forgiven by us, your
    friends at fsociety. The market's opening bell this morning will be the final
    death knell of Evil Corp. We hope as a new society rises from the ashes that
    you will forge a better world. A world that values the free people, a world
    where greed is not encouraged, a world that belongs to us again, a world
    changed forever. And while you do that, remember to repeat these words:
    "flag{We are fsociety, we are finally free, we are finally awake!}"

Mamy flagę i 50 punktów
