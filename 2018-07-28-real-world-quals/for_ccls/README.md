# CCLS (forensics, 31 solved, 146p)

```
Ray said that the challenge "Leaf-Similar Trees" from last LeetCode Weekly was really same-fringe problem and wrote it in the form of coroutine which he learned from a Stanford friend. 
Can you decrypt the cache file dumped from a language server without reading the source code? 
The flag is not in the form of rwctf{} because special characters cannot be used. 
```

In the task we get some [binary data](fringe.cc.blob) which turns out to be an index file from CCLS language server, generated for some source code.
In short, this is an index file used to provide code-completion in some compatible code editors.
As a result this file contains some meta-information about the source code it was generated for.
Reading the blob is hard, so we used a short code to transcribe this to a `json` format, which is also supported in CCLS:

```c
int main(int argc, char** argv) {
    std::ifstream input("fringe.cc.blob");
    std::string data;
    input.seekg(0, std::ios::end);
    int size = input.tellg();
    data.reserve(size);
    input.seekg(0, std::ios::beg);
    data.assign((std::istreambuf_iterator<char>(input)),
                 std::istreambuf_iterator<char>());
    auto ptr = Deserialize(SerializeFormat::Binary, "bleh.cc", data, "<empty>", std::nullopt);
    if (ptr.get() == nullptr) {
        std::cerr << "Error! Deserialize";
        return -1;
    }
    std::cout << ptr->ToString();
    return 0;
}
```

As a result we got a nice [json file](fringe.json).
This file was much easier to read, but still flag was no-where to be seen.
Initially we were afraid that the goal is to reconstruct the source code, based on the index information (eg. where certain functions and variables appear), and flag will be provided as `result` of the code.
This was even more probable when one of variables had:

```json
    {
      "usr": 7704954053858737267,
      "detailed_name": "int b",
      "qual_name_offset": 4,
      "short_name_offset": 4,
      "short_name_size": 1,
      "hover": "",
      "comments": "flag is here",
      "declarations": [],
      "spell": "16:80-16:81|1935187987660993811|3|2",
      "extent": "16:76-16:81|1935187987660993811|3|0",
      "type": 52,
      "uses": [],
      "kind": 13,
      "storage": 0
    },
```

We honestly thought that value of this variable after execution might be the flag...
Fortunately one of our players said that it's curious that there are so many single-letter integer variables in the code, especially ones with unlikely names like `int o`.

We decided to extract all those variables, and then to order them based on where they appear in the code:

```
7704954053858737267, b
6003530916780244609, l
16409791255353764606,e
6774343172775664959, s
9373165262205917908, s
4461895420097840245, w
4956677364806259883, o
8339831579497412465, d
14097758609443653436,w
5793038454202862564, h
11799706060736637558,o
2689251791356110509, i
9707098551059601229, s
8289061585496345026, i
9726294037205706468, n
6655996420844398086, h
168502829666687781   k
```

Then we spend next half an hour trying to figure out how to order this to get the `real` flag.
Finally we tried to submit just this: `blesswodwhoisinhk` and it turned out to be the flag.
