#include <bits/stdc++.h>
using namespace std;

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

using Vector = valarray<uint64_t>;

struct Matrix {
    vector<Vector> elements;
    Matrix(int rows, int cols)
        : elements(rows, Vector(cols)) {}

    auto rows() const { return elements.size(); }
    auto cols() const { return elements[0].size(); }

    auto operator*(const Vector& v) const {
        assert(v.size() == cols());
        Vector res(rows());
        for (size_t i = 0; i < rows(); ++i) {
            Vector mul = elements[i] * v;
            res[i] = accumulate(begin(mul), end(mul), uint64_t{0});
        }
        return res;
    }

    void fill(RNG* rng) {
        for (auto& row : elements)
            for (auto& x : row)
                x = rng->next_qword_fast();
    }
};

constexpr int key_size = 64;

void write64(ofstream& o, uint64_t x) {
    o.write(reinterpret_cast<const char*>(&x), sizeof x);
}

int main(int argc, const char **argv) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " filename" << endl;
        return EXIT_FAILURE;
    }

    string filename(argv[1]);
    ifstream in(filename, ios::binary);

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

    // Write ciphertext
    ofstream out(filename + ".enc", ios::binary);
    write64(out, plaintext.size());
    for (auto x : cipher)
        write64(out, x);

    // TODO Store key somewhere
}
