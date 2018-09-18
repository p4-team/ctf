# DeepDive (forensics, 200p)

In the challenge we get a [pcap](DeepDive.pcap).
Once we analyse it with NetworkMiner we are able to extract some files.
One is interesting because it's supposed to be a picture, and in fact it's a [binary](mausoleum.exe).

It's a pyinstaller exe so we can unpack it via https://github.com/countercept/python-exe-unpacker

For some reason we were unable to decompile the [pyc file](mausoleum.pyc) but there is no real need for that, since the flag is just a string there: `TMCTF{the_s3cr3t_i$_unE@rth3d}`
