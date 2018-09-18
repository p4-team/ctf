# This code is written in SageMath, which is powerfull math system based on Python
#
# You can download the interpreter here: http://www.sagemath.org
#
# You can use online interpreter here: https://cocalc.com/app (I recommend this option)
#
# Or you can use this file like a "pseudo-code" template to rewrite functions you need into another programming language - the advantage of Python code is, that it's really easy to understand what it should do. 


def text2int(text):
    chars = [ord(c) for c in text]
    result  = 0
    for c in chars:
        result *= 256
        result += c
    return result

def int2text(message):
    result=""
    while message>0:
        result = chr(int(message)%int(256))+ result
        message=int(message)/int(256)
    return result

	
	
def encrypt(text, e, N):
    text_int = text2int(text)
    encrypted = pow(text_int, e, N)
    return encrypted

def decrypt(x_int, d, N):
    decrypted = pow(x_int, d, N)
    text = int2text(decrypted)
    return text

e  =  65537