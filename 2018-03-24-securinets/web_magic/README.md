# Magic test (Web)

In the task we get a very simple webpage where we can input a name and birthday.
We get source code of the server part as well:

```javascript
const express = require('express')
const app = express()

function getTimestamp(date) {
    try{
        var x = Math.floor((new Date(date)) / 1000);
        return x;
    } catch( e ){
        return  Math.floor((new Date()) / 1000);
    }
}

function getAsciiCode(str)
{
    var arr1 = [];
    for (var n = 0; n < str.length; n ++) 
     {
        var ascii = Number(str.charCodeAt(n));
        arr1.push(ascii);
     }
    return arr1.join('');
}

app.get('/:username/:birth_day', (req, res) => {
    flag = '************';
    username = req.params.username || '';
    birthDay = req.params.birth_day || '';

    console.log(username);
    console.log(birthDay);
    
    var priority = Math.pow(2, getAsciiCode(username) + getTimestamp(birthDay));
    
    if(priority >= 0) {
        res.send('Hey peasent, no flag for you !!');
    }
    else {
        res.send('Your magical powers have been proven, here is your flag: ' + flag );
    }
});

app.listen(3000, () => console.log('Node Task app listening on port 3000!'));
```

It's clear we need to bypass the check and therefore the value of `Math.pow(2, getAsciiCode(username) + getTimestamp(birthDay))` needs to be `< 0`.
Initially we simply wanted to send a non-date string as birthday (eg. some text), causing the result of `getTimestamp` to be `NaN`, but there must have been some validation of the input format.
In the end it worked as we wanted for string `2018-01-32` and we got `Flag{PhP_H4s_seCuriTY_issues_THEY-Said!!!}`
