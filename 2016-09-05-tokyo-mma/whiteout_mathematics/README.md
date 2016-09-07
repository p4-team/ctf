## Whiteout Mathmatics (Reverse, PPC, 200p)
	tl;dr reverse the program, find the number that matches the problem



Our job is to run the included [whitespace program](program) with following arguments: `100 1000000000000`

After some fiddling with it, we've noticed it's hard to get the output in reasonable for anything bigger than a couple hundred. So we have to find out what exactly does it do.

Covert the source code to asm-like instructions, do some dynamic analysis and you get something like this:

```assembly



     push 1                                         
     iint              //load first input to 1  input1                        
     push 2                                         
     iint              //load second input to 2 input2                          
     push 3                                         
     push -1                                        
     set               //store -1 at 3                             
     push 1                                         
     get               //push input 1
part "A"                                            
     copy              //duplicate                             
     push 2                                         
     get               //push input 2
     push 1                                         
     add               //push (1 + input2)                            
     sub               //input1 - input2                            
     less "B"          //jump b if <0                             
     goto "D"          //jump d else                             
part "B"                                            
     copy                                         
     call "E"    // return sum of divisors for current input1 (on top of the stack)                                    
     copy                                           
     push 3                                         
     get          
     sub          
     less "C"    // generally, set value of variable_3 to max of variable_3 and returned value from "E"                                
     push 3                                         
     swap                                           
     set                                            
     push 0                                         
part "C"                                            
     away                                           
     push 1                                         
     add                                            
     goto "A"                                       
part "D"   //print TWCTF{variable_3}
     push 3                                         
     get                                            
     push 84                                        
     ochr                                           
     push 87                                        
     ochr                                           
     push 67                                        
     ochr                                           
     push 84                                        
     ochr                                           
     push 70                                        
     ochr                                           
     push 123                                       
     ochr                                           
     oint                                           
     push 125                                       
     ochr                                           
     push 10                                        
     ochr                                           
     exit                                           
part "E"     // set variable_5 to 0
     push 5                                         
     push 0                                         
     set            //store 0 at 5                                       
     push 1                                         
part "F"                                            
     copy 1         
     copy 1                                                                        
     mod            
     zero "G"       //jump if interator divides current input1                                
     goto "H"       

part "G"     //add current interator value to variable_5
     copy                                           
     push 5                                         
     get            //push from 5                                
     add            //add interator                                 
     push 5                                         
     swap                                           
     set            //store to 5

part "H"     // check if interator value is equal or bigger than current input1                                       
     push 1  
     add                                            
     copy                                           
     copy 2  //input1                                       
     sub                                            
     push 1                                         
     sub                                            
     less "F"                                       
     away                                           
     away                                           
     push 5                                         
     get                                            
     back                                           
```

It turns out, that the program searches for the biggest sum of divisors for numbers from `input1` to `input2` and it's complexity is O(n^2), which means, it wont return the answer for 10^12 before end of the ctf ;).

So we either have to calculate the outcome using a more sophisticated algorithm... or find the result on [google](https://oeis.org/A002093/b002093.txt)

Use wolframalpha to get the sum of divisors and your score magically increments by 200 points!

`TWCTF{5618427494400}`
