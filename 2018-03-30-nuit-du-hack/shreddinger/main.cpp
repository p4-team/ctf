#include <cstdio>
#include <cstdlib>
#include <cmath>

float weights[128][128][2][2];
int perm[128];
int rots[128];

int newperm[128];
int newrots[128];

int rnd(int l, int r) {
	return l + rand() % (r - l + 1);
}

double rnd() {
	return rand() / (float(RAND_MAX));
}

int main() {
	freopen("/tmp/spec", "r", stdin);
	int n;
	scanf("%d", &n);
	fprintf(stderr, "Started\n");
	for (int i = 0; i < n; i++)
		for (int j = 0; j < n; j++)
			for (int ri = 0; ri < 2; ri++)
				for (int rj = 0; rj < 2; rj++)
					scanf("%f", &weights[i][j][ri][rj]);

	fprintf(stderr, "Scanned\n");
	for (int i = 0; i < n; i++) {
		perm[i] = i;
		rots[i] = 0;
	}
	int ITER = 30000000;
	for (int i = 0; i < ITER; i++) {
		if (i % 2 == 0) {
			int indices[4];
			for (int j = 0; j < 3; j++) {
				indices[j] = rnd(1, n-2);
			}
			indices[3] = indices[2] + indices[1] - indices[0];
            if (indices[3] < 1 or indices[3] > n-2) continue;
            if (indices[0] >= indices[1]) continue;
            if (indices[2] >= indices[3]) continue;
            if (indices[0] <= indices[3] and indices[1] >= indices[2]) continue;

			int val = 0;
            val += weights[perm[indices[0]-1]][perm[indices[0]]][rots[indices[0]-1]][rots[indices[0]]];
            val += weights[perm[indices[1]]][perm[indices[1]+1]][rots[indices[1]]][rots[indices[1]+1]];
            val += weights[perm[indices[2]-1]][perm[indices[2]]][rots[indices[2]-1]][rots[indices[2]]];
            val += weights[perm[indices[3]]][perm[indices[3]+1]][rots[indices[3]]][rots[indices[3]+1]];

			int nex = 0;
            nex += weights[perm[indices[0]-1]][perm[indices[2]]][rots[indices[0]-1]][rots[indices[2]]];
            nex += weights[perm[indices[1]]][perm[indices[3]+1]][rots[indices[1]]][rots[indices[3]+1]];
            nex += weights[perm[indices[2]-1]][perm[indices[0]]][rots[indices[2]-1]][rots[indices[0]]];
            nex += weights[perm[indices[3]]][perm[indices[1]+1]][rots[indices[3]]][rots[indices[1]+1]];

			int r = rnd() < exp(-i / (ITER/20.0));
			if (nex < val or r) {
				//fprintf(stderr, "OK %d %d\n", i, r);
				for (int i = 0; i < n; i++) {
					newperm[i] = perm[i];
					newrots[i] = rots[i];
				}
                for (int i = 0; i < indices[1] + 1 - indices[0]; i++) {
					newperm[indices[0] + i] = perm[indices[2] + i];
					newperm[indices[2] + i] = perm[indices[0] + i];
					newrots[indices[0] + i] = rots[indices[2] + i];
					newrots[indices[2] + i] = rots[indices[0] + i];
				}
				for (int i = 0; i < n; i++) {
					perm[i] = newperm[i];
					rots[i] = newrots[i];
				}
			}
		}
		else {
			int indices[2];
			for (int j = 0; j < 2; j++) {
				indices[j] = rnd(1, n - 2);
			}
			if (indices[0] > indices[1]) continue;
            int val = 0;
            val += weights[perm[indices[0]-1]][perm[indices[0]]][rots[indices[0]-1]][rots[indices[0]]];
            val += weights[perm[indices[1]]][perm[indices[1]+1]][rots[indices[1]]][rots[indices[1]+1]];

            int nex = 0;
            nex += weights[perm[indices[0]-1]][perm[indices[1]]][rots[indices[0]-1]][1-rots[indices[1]]];
            nex += weights[perm[indices[0]]][perm[indices[1]+1]][1-rots[indices[0]]][rots[indices[1]+1]];

			int r = rnd() < exp(-i / (ITER/20.0));
			if (nex < val or r) {
				//fprintf(stderr, "OK2 %d %d\n", i, r);
				for (int i = 0; i < n; i++) {
					newperm[i] = perm[i];
					newrots[i] = rots[i];
				}
				for (int i = 0; i < indices[1] + 1 - indices[0]; i++) {
                    newperm[indices[0] + i] = perm[indices[1] - i];
                    newrots[indices[0] + i] = 1 - rots[indices[1] - i];
				}
				for (int i = 0; i < n; i++) {
					perm[i] = newperm[i];
					rots[i] = newrots[i];
				}
			}
		}
	}
	for (int i = 0; i < n; i++) {
		printf("%d\n", perm[i]);
	}
	for (int i = 0; i < n; i++) {
		printf("%d\n", rots[i]);
	}
}

/*
        for i in range(n):
            for j in range(n):
                for ri in range(2):
                    for rj in range(2):
                        f.write(str(weights[(i, j, ri, rj)])+"\n")
    perm = range(n)
    rots = [0] * n
    print "Loaded"
    ITER = 10000000
    for i in range(ITER):
        if i % 2 == 0:
            indices = []
            for j in range(3):
                indices.append(random.randint(1, n-2))
            indices.append(indices[2] + indices[1] - indices[0])
            if indices[3] < 1 or indices[3] > n-2: continue
            if indices[0] >= indices[1]: continue
            if indices[2] >= indices[3]: continue
            if indices[0] <= indices[3] and indices[1] >= indices[2]: continue

            val = 0
            val += weights[(perm[indices[0]-1], perm[indices[0]], rots[indices[0]-1], rots[indices[0]])]
            val += weights[(perm[indices[1]], perm[indices[1]+1], rots[indices[1]], rots[indices[1]+1])]
            val += weights[(perm[indices[2]-1], perm[indices[2]], rots[indices[2]-1], rots[indices[2]])]
            val += weights[(perm[indices[3]], perm[indices[3]+1], rots[indices[3]], rots[indices[3]+1])]

            nex = 0
            nex += weights[(perm[indices[0]-1], perm[indices[2]], rots[indices[0]-1], rots[indices[2]])]
            nex += weights[(perm[indices[1]], perm[indices[3]+1], rots[indices[1]], rots[indices[3]+1])]
            nex += weights[(perm[indices[2]-1], perm[indices[0]], rots[indices[2]-1], rots[indices[0]])]
            nex += weights[(perm[indices[3]], perm[indices[1]+1], rots[indices[3]], rots[indices[1]+1])]

            rnd = random.random() < math.exp(-i / (ITER/20.0))
            if nex < val or rnd:
                print "Ok", i, rnd
                newperm = perm[:]
                newrots = rots[:]
                for i in range(indices[1] + 1 - indices[0]):
                    newperm[indices[0] + i] = perm[indices[2] + i]
                    newperm[indices[2] + i] = perm[indices[0] + i]
                    newrots[indices[0] + i] = rots[indices[2] + i]
                    newrots[indices[2] + i] = rots[indices[0] + i]
                perm = newperm
                rots = newrots
        else:
            indices = []
            for j in range(2):
                indices.append(random.randint(1, n-2))
            if indices[0] > indices[1]: continue

            val = 0
            val += weights[(perm[indices[0]-1], perm[indices[0]], rots[indices[0]-1], rots[indices[0]])]
            val += weights[(perm[indices[1]], perm[indices[1]+1], rots[indices[1]], rots[indices[1]+1])]

            nex = 0
            nex += weights[(perm[indices[0]-1], perm[indices[1]], rots[indices[0]-1], 1-rots[indices[1]])]
            nex += weights[(perm[indices[0]], perm[indices[1]+1], 1-rots[indices[0]], rots[indices[1]+1])]

            rnd = random.random() < math.exp(-i / (ITER/20.0))
            if nex < val or rnd:
                print "Ok2", i, rnd
                newperm = perm[:]
                newrots = rots[:]
                for i in range(indices[1] + 1 - indices[0]):
                    newperm[indices[0] + i] = perm[indices[1] - i]
                    newrots[indices[0] + i] = 1 - rots[indices[1] - i]
                perm = newperm
                rots = newrots

*/
