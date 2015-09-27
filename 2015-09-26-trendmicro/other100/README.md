# Fix my pdf (misc, 100p)

Dostajemy [taki oto pdf](fix_my_pdf.pdf) od autorów zadania.

Wszelkie próby załadowania go do jakiegoś czytnika pdf kończą się niepowodzeniem - wyraźnie wygląda na uszkodzony.

Możemy jeszcze otworzyć go z ciekawości w notepadzie/vimie/emacsie żeby przyjrzeć sie jego wewnętrzenej strukturze - niestety wszystkie streamy w pdfie są skompresowane, co oznacza że ręcznie ich nie podejrzymy.

W tym momencie należy więc skorzystać z jakiegoś narzędzia do dumpowania streamów pdfa. Do głowy przychodzi qpdf, ale jako dzieci windowsa wybieramy prostsze narzędzie - pdf stream dumper.

Ładujemy pdf, i jeden ze streamów wydaje sie ciekawszy (dla oka ludzkiego) niż pozostałe - zawiera XML z metadanymi. Szczególnie ciekawa jest zawartość `<xmpGImg:image>` - dekodujemy więc ją i zapisujemy do oddzielnego pliku (pamiętając żeby zamienić/usunąć wcześniej ciągi `&#xA;` z base64 - autor tego writeupa zapomniał o tym na początku i już myślał że jego pomysł na zadanie okazał się ślepą uliczką).

Otrzymujemy taki oto obrazek: []('result.jpg')

Odczytujemy z niego flagę: TMCTF{There is always light behind the clouds}.
