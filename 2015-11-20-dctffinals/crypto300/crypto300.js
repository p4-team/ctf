function goToHex(input)
{
    var result = input.split('').map(function(c){ var t = c.charCodeAt(0).toString(16); return t.length == 1 ? "0" + t:t});

    return result.join('');
}

function backFromHex(input)
{
    var result = '';

    for (var i = 0; i < input.length; i += 2) {
		  result += String.fromCharCode(parseInt(input[i] + input[i+1], 16));
    }

    return result;
}

function algo350(input, key)
{																				     
    var dc = [];
	var j = 0;

    for (var i = 0; i < 128; i++) {
		dc[i] = i;
    }
																						  
    for (i = 0; i < Math.max(128, input.length); i++) {
		var k = key.charCodeAt(i);
		key += String.fromCharCode((k << 1 | k >> 7) & 255);
    }
     console.log(key.charCodeAt(4))

    for (i = 0; i < 128; i++) {
		j = (j + dc[i] + key.charCodeAt(i)) % 128;
		dc[i] ^= dc[j];
		dc[j] ^= dc[i];
		dc[i] ^= dc[j];
    }

    i = j = 0;
    result = "";

    for (var l = 0; l < input.length; l++) {																	   
		i = (i + 1) % 128;
		j = (j + dc[i]) % 128;

		dc[i] ^= dc[j];
		dc[j] ^= dc[i];
		dc[i] ^= dc[j];

		var x1 = dc[(dc[i] + dc[j]) % 128];
		var x2 = key.charCodeAt(l);	
    
      
		result = result + String.fromCharCode(x1 ^ input.charCodeAt(l) ^ x2);

    }

	return result
}

    function proceed(input, key, mode)
	{
		if (mode == 'encrypt') {
			cipherText = algo350(input, key);

			return goToHex(cipherText);
		} else if (mode == 'decrypt') {
			plainText = algo350(backFromHex(input), key);

			return plainText;
		}

		return "Make up your mind!"
    }

