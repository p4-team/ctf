# Anonymous exchange (misc, 253p)

> I've bought some bitcoins with my credit cards, and some of them attracted attention, but I don't know which ones. Could you find out?

> Challenge running at anon.ctfcompetition.com:1337


Connecting to the challenge, we are presented the following menu:
```
Hey. Could you tell me if my cards ccard0x1 through ccard0x40 have attracted the wrong type of attention? Flagged cards are displayed in their dumps, and their encryption is deterministic. I seem to have the wrong encoding on my terminal, so I'll need help there.
I'll patch you into a management interface in a few seconds.


Welcome to our telnet dogecoin exchange !.
We've currently frozen most of the operations pending an investigation into potential credit card fraud with law enforcement.
 - NEWACC to create an account.
 - NEWCARD to create a test credit card.
 - ASSOC <cardx> <accounty> to associate cardx to accounty.
 - BACKUP to generate a anonymized encrypted jsonified maybe-emojified backup.
```
Let's try typing some of the commands:
```
NEWACC
OK: Account uaccount0x1 created.
NEWCARD
OK: Card ucard0x1 created.
ASSOC ccard0x1 uaccount0x1
OK: Card ccard0x1 associated with account uaccount0x1.
BACKUP
[{"cards":[],"account":"d5d061c7916d633d"},
{"account":"2e110af22576601e","cards":[]},
{"account":"c514f2320ec707bf","cards":[{"card":"f3d94eb824490d44"}]},
{"account":"2dc5381fae066a60","cards":[{"card":"9573c3b0c238bf93"}]},
{"cards":[],"account":"746cb63871de2c89"},

[...]
]

So, which cards are burnt?
Answer with a string of zeroes and ones, no spaces.
```

The whole dump had a couple hundred of accounts and cards. Some of the cards had not only its
ID in the dump, but also `"flagged" : "1"` pair, meaning the card is burnt.

We need to know which of the cards with specific names are burnt, but we don't know
which card IDs (such as "9573c3b0c238bf93"), correspond to which card name (such as
"ccard0x40"). We can insert our own cards and accounts to the system though, so we can
make some kind of special structure in the account-card graph. In fact, the graph is pretty
sparse, as we are allowed only three cards per account and three accounts per card. That means,
on average, the graph will have a lot of rather small components, and a long chain of 
accounts and cards will be very rare. If we insert such a chain ourselves, then we will
know which card IDs correspond to which card names (for now, just our cards).

Let's make such a graph:
```
ucard0xff
    |
uaccount0x1 - ucard0x1 - uaccount0x2 - ucard0x2 - uaccount0x3 - ... - ucard0x41 - uaccount0x42
    |
ucard0xfe
```

Now, if we find a long chain in the received dump, it's very likely our structure. We can even
know which end is which, because one of them ends with two cards, and the other with an account.

So we're able to distinguish our cards and accounts from the whole mess. Let's connect the
queried cards to our known accounts: `ccard0x1` to `uaccount0x2`, `ccard0x2` to `uaccount0x3`
and so on. Then, we can easily find those cards in the dump too, and find which of them
are flagged.

After answering the query, we receive the flag. The solution implementation is in `doit.py`
file.

