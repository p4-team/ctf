# lol (Crypto, 233p, 16 solved)

In the task we get [encryption code](encrypt.cpp) and [encrypted flag](flag.txt.enc).
This task turned out to be "broken" and solvable with an unintended solution, so another version was released at some point with a fix.

The code here is pretty straighforward.
Core part is:

```c
    string input;
    in >> input;
    Vector plaintext(input.size());
    copy(input.begin(), input.end(), begin(plaintext));

    // Generate deterministic helper matrix A
    Matrix A(key_size, plaintext.size());
    {
        RNG rng(0);
        A.fill(&rng);
    }

    // Generate random key
    Vector key(key_size);
    {
        RNG rng;
        for (auto& x : key)
            x = rng.next_qword_safe();
    }

    Vector cipher = A * plaintext + key;
```

The flag is treated as integer vector and multiplied by a fixed matrix, and the a random key vector is added to the result.

```
ciphertext = M*flag + key
```

In order to recover the flag we would have to figure out the random key vector, subtract it from the ciphertext we have and then solve the matrix equation.

The random number generator is:

```c
struct RNG {
    random_device dev;
    mt19937_64 rng;
    RNG() : dev(), rng(dev()) {}
    RNG(uint64_t seed) : rng(seed) {}

    bool next_bit() { return rng() & 1; }

    // For when we want to hide the RNG state
    uint64_t next_qword_safe() {
        uint64_t res = 0;
        for (int i = 0; i < 64; ++i)
            res |= next_bit() << i;
        return res;
    }

    // For when we don't care about security
    uint64_t next_qword_fast() {
        return rng();
    }
};
```

It might seem pretty strong - the `next_qword_safe` function generates 64 bit uint one bit at a time from `mt19937_64`, so untwisting the generator state is pretty much impossible.
There are two strange things to notice here:

- A single bit from the generator is extracted via function `bool next_bit() { return rng() & 1; }`, which means it's treated as `bool`. It's interesting because we later do a bitshift of this value, and boolean is promoted to a `signed int`, which means the bitshift will cause a sign extension, making the high bits not-so-random.
- Random number generator is seeded with a call to `random_device` and if we check the signature of the `operator()` we will see `result_type operator()();` and we can read that `result_type is a member type, defined as an alias of unsigned int.`

The second remark is a key to solve this version of the task - the seed is an `unsigned int` so a 32 bit value - we can simply brute-force all possible seeds!

Not the remaining part is to solve the matrix equation for a given `random key` and check if it's the flag, but we need to do this reasonably fast.
Since the matrix `M` is constant, we can calculate inverse matrix and multiply it by the `ciphertext - random_key` to get the result candidate flag.
This is much easier and faster than using some Gauss elimitation to solve the equation.
Even more if we realise that we need to perform all calculations in a ring modulo 2**64, because in the original code all computations are wrapping around uint_64.

A small difficulty here is that the matrix is not square - random key is 64 bytes long and the flag is only 37 bytes long, therefore the matrix `M` is 37x64 and we can't invert such matrix.
We can, however, select a subset of matrix rows and use only those.
This is due to the fact that when doing a multiplication `M * flag` each element of the resulting vector is a linear combination of all of the elements of the flag vector.
So we really need only as many elements of this vector as the uknown variables.
We can't select those rows randomly, because some of the matrix rows might not be independent, and we need 37 independent rows (not `independent` here means that a certain row `M[i]` is equal to `k * M[j]` where `k` is some integer and `M[j]` is another matrix row).

We used `sage` to check 37-elements combinations of the matrix `M` rows and find a set of independent rows.
It turned out that if we take rows `[4:41]` we will be fine.

```python
R = IntegerModRing(2**64)
coefficients = load() # matrix rows generated with the original source code
M = Matrix(R, coefficients[4:37+4]) 
M.inverse()
```

Once we have the inverse matrix, we can do:

```c
Vector load_result(string path){
    ifstream in(path.c_str(), ios::binary);
    char buffer[8];
    in.read(buffer, 8);
    uint64_t size = *reinterpret_cast<uint64_t*>(buffer);
    Vector all(64);
    for(int i=0;i<64;i++){
        in.read(buffer, 8);
        uint64_t element = *reinterpret_cast<uint64_t*>(buffer);
        all[i] = element;
    }
    Vector res(size);
    for(int i=0;i<size;i++){
        res[i] = all[i+4];
    }
    return res;
}

int main(int argc, const char **argv) {
    if(argc < 4){
        cerr<<"./binary start end encrypted_file"<<endl;
        exit(-1);
    }
    unsigned int start = atoi(argv[1]);
    unsigned int end = atoi(argv[2]);
    Vector result = load_result(string(argv[3]));

    Matrix A_inv(37, 37);
    uint64_t data[] = {...}; # list of inverse matrix coefficients
    A_inv.fill(data);

    // Generate random key
    for(unsigned int i=start;i<end;i++){
        if((i & 0xFFFFF) == 0){
            cout<<i<<endl;
        }
        Vector key(key_size);
        {
            RNG rng(i);
            for (auto& x : key)
                x = rng.next_qword_safe();
        }
        Vector cut_key(37);
        for(int j=0;j<37;j++){
            cut_key[j] = key[j+4];
        }
        Vector clean = (result - cut_key);
        Vector solution = A_inv * clean;
        if(solution[0] == 51) {
            cout<<"match at seed = "<<i<<endl;
            for (int k=0;k<37;k++) {
                cout << solution[k]<<" ";
            }
        }
    }
}
```

And with such code we can test all seed ranges from `start` till `end`.
It takes a while, but we can run this in paralell on as many cores as we have available and at some point we get a match and the result flag `34C3_l3nstra_w0uld_h4ve_b33n_s0_proud`, which indicates that the author expected this to be solved via `LLL`.

The complete solver code available [here](brute.cpp)
