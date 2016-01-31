import os
from subprocess import check_output, call

while(True):

	fileType = check_output(["file", "f100"])
	fileType = fileType[6:9]

	print(fileType)

	if(fileType=='ARC'):
		print('ARC')
		os.system("nomarch -p f100 > out")
		os.system("mv out f100")
	elif(fileType=='PPM'):
		print('PPMD')
		os.system("ppmd d f100")
		os.system("mv secret f100")
	elif(fileType=='Mic'):
		print('Cabinet')
		os.system("cabextract f100")
		os.system("mv secret f100")
	elif(fileType=='bzi'):
		print('Bzip2')
		os.system("bzip2 -d f100")
		os.system("mv f100.out f100")
	elif(fileType=='XZ'):
		print('XZ')
		os.system("unxz < f100 > out")
		os.system("mv out f100")
	elif(fileType=='7-z'):
		print('7-Z')
		os.system("7z e f100")
		os.system("mv secret f100")
	elif(fileType=='gzi'):
		print('gzip')
		os.system("mv f100 f100.gz")
		os.system("gzip -d f100.gz")
	elif(fileType=='POS'):
		print('POSIX')
		os.system("tar -xvf f100")
		os.system("mv secret f100")
	elif(fileType=='Zip'):
		print('ZIP')
		os.system("unzip f100")
		os.system("mv secret f100")
	elif(fileType=='ARJ'):
		print('ARJ')
		os.system("mv f100 f100.arj")
		os.system("arj e f100")
		os.system("mv secret f100")
	elif(fileType=='rzi'):
		print('fzip')
		os.system("mv f100 f100.rz")
		os.system("rzip -d f100.rz")
		os.system("mv secret f100")
	elif(fileType=='Zoo'):
		print('zoo')
		os.system("mv f100 f100.zoo")
		os.system("zoo -extract f100")
		os.system("mv secret f100")
	elif(fileType=='RAR'):
		print('RAR')
		os.system("unrar e f100")
		os.system("mv secret f100")			
	else :
		exit();
