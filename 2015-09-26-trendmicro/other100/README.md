# Fix my pdf (misc, 100p)

## PL 
`For ENG scroll down`

Dostajemy [taki oto pdf](fix_my_pdf.pdf) od autorów zadania.

Wszelkie próby załadowania go do jakiegoś czytnika pdf kończą się niepowodzeniem - wyraźnie wygląda na uszkodzony.

Możemy jeszcze otworzyć go z ciekawości w notepadzie/vimie/emacsie żeby przyjrzeć sie jego wewnętrzenej strukturze - niestety wszystkie streamy w pdfie są skompresowane, co oznacza że ręcznie ich nie podejrzymy.

W tym momencie należy więc skorzystać z jakiegoś narzędzia do dumpowania streamów pdfa. Do głowy przychodzi qpdf, ale jako dzieci windowsa wybieramy prostsze narzędzie - pdf stream dumper.

Ładujemy pdf, i jeden ze streamów wydaje sie ciekawszy (dla oka ludzkiego) niż pozostałe - zawiera XML z metadanymi. Szczególnie ciekawa jest zawartość `<xmpGImg:image>` - dekodujemy więc ją i zapisujemy do oddzielnego pliku (pamiętając żeby zamienić/usunąć wcześniej ciągi `&#xA;` z base64 - autor tego writeupa zapomniał o tym na początku i już myślał że jego pomysł na zadanie okazał się ślepą uliczką).

Otrzymujemy taki oto obrazek:

![](./result.jpg)

Odczytujemy z niego flagę: TMCTF{There is always light behind the clouds}.

## ENG

We get [this pdf file](fix_my_pdf.pdf) from the task authors.

All attempts to open it with a pdf reader fail - it seems to be broken.

We can still open it with notepad/vim/emacs to look at the internal structure -  unfortunately all pdf streams are compressed so we can't easily read them.

We decided to use a pdf stream dump tool. We could have used qpdf but since we're on windows at the moment we chose a different tool - pdf stream dumper.

We load the pdf and one of the streams seems more interesting than the others (at least from human point of view) - it contains XML with metadata.
Particularly insteresting is `<xmpGImg:image>` - we decode this and we save it to a different file (remembering to replace/remove `&#xA;` from base64 - author of this writeup forgot about this initially and almost assumed that his approach to solve the task was incorrect)

We finally get this picture:

![](./result.jpg)

We read the flag from it: `TMCTF{There is always light behind the clouds}.`
