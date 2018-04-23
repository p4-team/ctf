#include <cstdio>
#include <vector>
#include <map>
#include <set>
#include <cassert>
#include <algorithm>

#define N 8
#define LEN 4
//#define X 0
//#define Y 20

int X, Y;

enum type {
	ADD, ROL, XOR,
};

struct operation {
	type t;
	unsigned char arg;
};

struct four {
	operation ops[LEN];
};

std::vector<four> generate_sequences(int n) {
	if (n == 0) {
		return {{}};
	}
	auto prev = generate_sequences(n - 1);
	int cnt = 0;
	for (auto& seq: prev) {
		//type tx[] = {ADD, ROL, XOR, ADD};
		//type t = tx[n-1];
		for (auto t: {ADD, ROL, XOR}) {
			if (n > 1 && seq.ops[n-2].t == t) continue;
			if (n == 1 && t != ADD) continue;
			if (n == 2 && t != ROL) continue;
			if (n == 3 && t != XOR) continue;
			if (n == 4 && t != ADD) continue;
			for (int arg = 0; arg < (1<<N); arg++) {
				if (t == ROL && arg == N) break;
				if (t == ROL && arg == 0) continue;
				cnt++;
			}
		}
	}
	std::vector<four> ret;
	ret.reserve(cnt);
	for (auto& seq: prev) {
		//type tx[] = {ADD, ROL, XOR, ADD};
		//type t = tx[n-1];
		for (auto t: {ADD, ROL, XOR}) {
			if (n > 1 && seq.ops[n-2].t == t) continue;
			if (n == 1 && t != ADD) continue;
			if (n == 2 && t != ROL) continue;
			if (n == 3 && t != XOR) continue;
			if (n == 4 && t != ADD) continue;
			for (int arg = 0; arg < (1<<N); arg++) {
				if (t == ROL && arg == N) break;
				if (t == ROL && arg == 0) continue;
				ret.push_back(seq);
				ret.back().ops[n-1] = {t, (unsigned char)arg};
			}
		}
	}
	return ret;
}

void print_seq(const four& ops) {
	printf("[");
	for (auto op: ops.ops) {
		//printf("%s %d\n", (op.t == ADD ? "ADD" : op.t == ROL ? "ROL" : "XOR"), op.arg);
		printf("(%d, %d), ", op.t, op.arg);
	}
	printf("],\n");
}

int apply(int n, const four& ops) {
	for (auto op: ops.ops) {
		if (op.t == ADD) { n += op.arg; }
		if (op.t == ROL) { n = (n << op.arg) | (n >> (N - op.arg)); }
		if (op.t == XOR) { n ^= op.arg; }
		n &= (1<<N) - 1;
	}
	return n;
}

bool correct(const four& ops) {
	if (apply(0, ops) != Y || apply(Y, ops) != 0) return false;
	for (int i = 1; i < (1<<N); i++) {
		if (i == Y) continue;
		if (apply(i, ops) != i) return false;
	}
	return true;
}

bool correct2(const four& ops) {
	return apply(X, ops) == 0 && apply(Y, ops) == 1;
}

int main() {
	auto seqs = generate_sequences(LEN);
	std::random_shuffle(seqs.begin(), seqs.end());
	printf("tab = {\n");
	for (X = 0; X < (1<<N); X++) {
		for (Y = X+1; Y < (1<<N); Y++) {
			printf("    (%d, %d): ", X, Y);
			bool any = false;
			//printf("  y=%d\n", Y);
			for (const auto& s: seqs) {
				if (correct2(s)) {
					print_seq(s);
					any = true;
					break;
				}
			}
			assert(any);
		}
	}
	printf("}\n");
}
