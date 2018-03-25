# Tic Tac Toe (Web/misc)

A bit of a WTF challenge.
You can play Tic Tac Toe against a computer player, but since he starts and plays well, you can't win.
To get the flag you need to win 100 times in a row.

There was a ton of obfuscated JS, and fortunately we were too lazy to analyse it, because it turned out to be useless.
The point of the task was to notice that once you perform a selected sequence of moves the game "breaks" and allows you to make a move for the computer player.

Once we noticed this we simply automated the task:

```javascript
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

window.alert = function() {
    // Do nothing.
};

    

for(var i=0; i<100; i++){
    document.getElementById("button_11").click()
    await sleep(500);
    document.getElementById("button_10").click()
    await sleep(500);
    document.getElementById("button_02").click()
    await sleep(500);
    document.getElementById("button_01").click()
    await sleep(500);
    document.getElementById("button_20").click()
    await sleep(1000);
}
````

And run this via Chrome console, and after a while we got `Flag{S9ck3t_I0_set_by_Th3_EMPIRE_NIAHAHAHAHAHAHA_xD}`
