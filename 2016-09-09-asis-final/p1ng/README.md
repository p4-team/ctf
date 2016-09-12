## p1ng (Forensics, 121p)

###ENG
[PL](#pl-version)

We are given interesting file, that looks like regular png file.

![](p1ng.png)

Though your browser may or may not support it. Because (surprise!) it's not regular png file - it's so called APNG file (animated png). After we discovered it (using tweakpng) we tried to unpack all the frames with available tools. Unfortunately, no ready-to-use program was able to unpack this image (i'm not sure why). So we hacked something in PHP, using stackoverflow of course:

```php
<?php

function splitapng($data) {
  $parts = array();

  // Save the PNG signature   
  $signature = substr($data, 0, 8);
  $offset = 8;
  $size = strlen($data);
  while ($offset < $size) {
    // Read the chunk length
    $length = substr($data, $offset, 4);
    $offset += 4;

    // Read the chunk type
    $type = substr($data, $offset, 4);
    $offset += 4;

    // Unpack the length and read the chunk data including 4 byte CRC
    $ilength = unpack('Nlength', $length);
    $ilength = $ilength['length'];
    $chunk = substr($data, $offset, $ilength+4); 
    $offset += $ilength+4;

    if ($type == 'IHDR')
      $header = $length . $type . $chunk;  // save the header chunk
    else if ($type == 'IEND')
      $end = $length . $type . $chunk;     // save the end chunk
    else if ($type == 'IDAT') 
      $parts[] = $length . $type . $chunk; // save the first frame
    else if ($type == 'fdAT') {
      // Animation frames need a bit of tweaking.
      // We need to drop the first 4 bytes and set the correct type.
      $length = pack('N', $ilength-4);
      $type = 'IDAT';
      $chunk = substr($chunk,4);
      $parts[] = $length . $type . $chunk;
    }
  }

  // Now we just add the signature, header, and end chunks to every part.
  for ($i = 0; $i < count($parts); $i++) {
    $parts[$i] = $signature . $header . $parts[$i] . $end;
  }

  return $parts;
}

$filename = 'p1ng';

$handle = fopen($filename, 'rb');
$filesize = filesize($filename);
$data = fread($handle, $filesize);
fclose($handle);

$parts = splitapng($data);

for ($i = 0; $i < count($parts); $i++) {
  $handle = fopen("part-$i.png",'wb');
  fwrite($handle,$parts[$i]);
  fclose($handle);
}
```

To be honest, we have stolen this script from SO almost completely.

Nevertheless, after execution we had a lot of chunks on disk:

![](./part-0.png)
![](./part-1.png)
![](./part-2.png)
![](./part-3.png)
![](./part-4.png)
![](./part-5.png)
![](./part-6.png)
![](./part-7.png)
![](./part-8.png)
![](./part-9.png)
![](./part-10.png)
![](./part-12.png)
![](./part-13.png)
![](./part-14.png)
![](./part-15.png)
![](./part-16.png)
![](./part-17.png)
![](./part-18.png)
![](./part-18.png)
![](./part-20.png)

(If you see only first chunk, that's because your browser rejects chunks with invalid CRC. Tell your browser to chill out).

And, with a bit of determination, we could just read a flag from them:

`ASIS{As_l0n9_4s_CTF_3x1sts_th3r3_w1ll_b3_ASIS_4nd_4s_l0n9_4s_ASIS_3x1sts_th3r3_w1ll_b3_PNG!}`

###PL version

Dostajemy w zadaniu ciekawy plik, który wygląda jak obrazek png:

![](p1ng.png)

Powinniście go zobaczyć, jeśli wasza przeglądarka go obsługuje, bo - niespodzianka - to nie jest zwykły plik png. Plik jest w formacie APNG (animated png). Kiedy to odkryliśmy (używając programu tweakpng), spróbowaliśmy go odpakować na poszczególne ramki, używajac gotowych narzędzi znalezionych w internecie. Niestety, wszystkie poległy - nie jestem pewien dlaczego. Dlatego napisaliśmy na szybko skrypt w PHP:

```php
<?php

function splitapng($data) {
  $parts = array();

  // Save the PNG signature   
  $signature = substr($data, 0, 8);
  $offset = 8;
  $size = strlen($data);
  while ($offset < $size) {
    // Read the chunk length
    $length = substr($data, $offset, 4);
    $offset += 4;

    // Read the chunk type
    $type = substr($data, $offset, 4);
    $offset += 4;

    // Unpack the length and read the chunk data including 4 byte CRC
    $ilength = unpack('Nlength', $length);
    $ilength = $ilength['length'];
    $chunk = substr($data, $offset, $ilength+4); 
    $offset += $ilength+4;

    if ($type == 'IHDR')
      $header = $length . $type . $chunk;  // save the header chunk
    else if ($type == 'IEND')
      $end = $length . $type . $chunk;     // save the end chunk
    else if ($type == 'IDAT') 
      $parts[] = $length . $type . $chunk; // save the first frame
    else if ($type == 'fdAT') {
      // Animation frames need a bit of tweaking.
      // We need to drop the first 4 bytes and set the correct type.
      $length = pack('N', $ilength-4);
      $type = 'IDAT';
      $chunk = substr($chunk,4);
      $parts[] = $length . $type . $chunk;
    }
  }

  // Now we just add the signature, header, and end chunks to every part.
  for ($i = 0; $i < count($parts); $i++) {
    $parts[$i] = $signature . $header . $parts[$i] . $end;
  }

  return $parts;
}

$filename = 'p1ng';

$handle = fopen($filename, 'rb');
$filesize = filesize($filename);
$data = fread($handle, $filesize);
fclose($handle);

$parts = splitapng($data);

for ($i = 0; $i < count($parts); $i++) {
  $handle = fopen("part-$i.png",'wb');
  fwrite($handle,$parts[$i]);
  fclose($handle);
}
```

Tak szczerze mówiąc, to bardziej ukradliśmy ten skrypt z SO niż `napisaliśmy`.

Tak czy inaczej, po wykonaniu tego skryptu otrzymaliśmy wiele chunków na dysku:

![](./part-0.png)
![](./part-1.png)
![](./part-2.png)
![](./part-3.png)
![](./part-4.png)
![](./part-5.png)
![](./part-6.png)
![](./part-7.png)
![](./part-8.png)
![](./part-9.png)
![](./part-10.png)
![](./part-12.png)
![](./part-13.png)
![](./part-14.png)
![](./part-15.png)
![](./part-16.png)
![](./part-17.png)
![](./part-18.png)
![](./part-18.png)
![](./part-20.png)

(Jeśli widzisz tylko jeden obrazek, to dlatego że Twoja przeglądarka odrzuca obrazy z nieprawidłowym CRC. Powiedz swojej przeglądarce żeby wyluzowała.)

I, z odpowiednią determinacją, byliśmy w stanie odczytać flagę:

`ASIS{As_l0n9_4s_CTF_3x1sts_th3r3_w1ll_b3_ASIS_4nd_4s_l0n9_4s_ASIS_3x1sts_th3r3_w1ll_b3_PNG!}`
