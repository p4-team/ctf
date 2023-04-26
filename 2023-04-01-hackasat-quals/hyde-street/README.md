# Hyde Street [146 points] (23 solves)

> Top of the hill, at the source.
>
> But the sky still beckons.

In this task we got a Docker container. However, unlike with previous tasks in the same category, there were no Crystal executables. Instead we got some weird Ruby code that, at a glance, seemed to generate and compile C source code into executable programs. The C source code consisted of a number of steps transforming a number received from the user before finally checking the transformed value against expected result. This is similar to what we have seen earlier in the As Below challenge, but this time we had access to the source code. So we decided to extract the operations and operands from the code and then execute the transformations in reverse starting with the expected result.

The challenging part was correctly parsing the C source code, but we decided to just slap a regex onto it and deal with any potential consequences later. After some code tinkering, we came up with the following:

```typescript
const decoder = new TextDecoder("utf-8");
let file_data = await Deno.readFile("/chall/challs/generated.c")
let source = decoder.decode(file_data)
source = source.split('{')[1].split('}')[0].split('\n')
    .filter(Boolean)
    .map(line => line.match(/(.) (\d+)/).slice(1))
    .map(([oper, num]) => [ oper, parseInt(num) ])

source.reverse()

let result = source.find(([ oper, num ]) => oper === '=')[1]
for (let [ oper, num ] of source.slice(1)) {
    switch (oper) {
        case '+':
            result -= num
            break
        case '-':
            result += num
            break
        case '/':
            result *= num
            break
    }
}

console.log(result)
```
