

# https://www.ncbi.nlm.nih.gov/nuccore/HW306977.1/

s = """
atggagaaaa tagtrcttct tcttgcaata gtcagtcttg ttaaaagtga tcagatttgc
attggttacc atgcaaacaa ttcaacagag caggttgaca caatcatgga aaagaacgtt
actgttacac atgcccaaga catactggaa aagacacaca acgggaagct ctgcgatcta
gatggagtga agcctctaat tttaagagat tgtagtgtag ctggatggct cctcgggaac
ccaatgtgtg acgaattcat caatgtaccg gaatggtctt acatagtgga gaaggccaat
ccaaccaatg acctctgtta cccagggagt ttcaacgact atgaagaact gaaacatcta
ttgagcagaa taaaccattt tgagaaaatt caaatcatcc ccaaaagttc ttggtccgat
catgaagcct catcaggagt gagctcagca tgtccatacc tgggaagtcc ctcctttttt
agaaatgtgg tatggcttat caaaaagaac agtacatacc caacaataaa gaaaagctac
aataatacca accaagaaga tcttttggta ctgtggggaa ttcaccatcc taatgatgcg
gcagagcaga caaggctata tcaaaaccca accacctata tttccattgg gacatcaaca
ctaaaccaga gattggtacc aaaaatagct actagatcca aagtaaacgg gcaaagtgga
aggatggagt tcttctgggc aattttaaaa cctaatgatg caatcaactt cgagagtaat
ggaaatttca ttgctccaga atatgcatac aaaattgtca agaaagggga ctcagcaatt
atgaaaagtg aattggaata tggtaactgc aacaccaagt gtcaaactcc aatgggggcg
ataaactcta gtatgccatt ccacaacata caccctctca ccatcgggga atgccccaaa
tatgtgaaat caaacagatt agtccttgca acagggctca gaaatagccc tcaaagagag
agcagaagaa aaaagagagg actatttgga gctatagcag gttttataga gggaggatgg
cagggaatgg tagatggctg gtatgggtac caccatagca atgagcaggg gagtgggtac
gctgcagaca aagaatccac tcaaaaggca atagatggag tcaccaataa ggtcaactca
attattgaca aaatgaacac tcagtttgag gctgttggaa gggaatttaa taacttagaa
aggagaatag agaatttaaa caagaagatg gaagacgggt ttctagatgt ttggacttat
aatgccgaac ttctggttct catggaaaat gagagaactc tagactttca tgactcaaat
gttaagaacc tctacgacaa ggtccgacta cagcttaggg ataatgcaaa agagctgggt
aacggttgtt tcgagttcta tcacaaatgt gataatgaat gtatggaaag tataagaaac
ggaacgtaca actatccgca gtattcagaa gaagcaagat taaaaagaga ggaaataagt
ggggtaaaat tggaatcaat aggaacttac caaatactgt caatttattc aacagtagcg
agttccctag cactggcaat catgatagct ggtctatctt tatggatgtg ctccaatgga
tcgttacaat gcagaatttg catttaa
"""

s = s.replace(" ", "").replace("\n", "").upper()

data = {}
datas = {}
mx = 0
for line in open("mars_dna_samples.txt").readlines():
    num = int(line.split(",")[0])
    q = line.split(",")[1].strip()
    data[num] = q
    datas[q] = num
    if len(q) > mx:
        mx = len(q)


solutions = {}

for ln in range(1, len(s) + 1):
    print ln, len(s)
    for off in range(len(s) - ln + 1):
        q = s[off:off+ln]
        if q in datas:
            solutions[(ln, off)] = [q]
            continue

        bl = 9999
        bsol = None
        for div in range(1, mx + 5)[::-1]:
            if q[:div] not in datas:
                continue
            if (ln-div, off+div) not in solutions:
                continue
            sol = [q[:div]] + solutions[(ln-div, off+div)]
            if len(sol) < bl:
                bl, bsol = len(sol), sol

        if bsol:
            solutions[(ln, off)] = bsol

res = solutions[(len(s), 0)]
print res
ress = ",".join(str(datas[q]) for q in res)
print ress

import hashlib
print "ctfzone{" + hashlib.md5(ress).hexdigest() + "}"
