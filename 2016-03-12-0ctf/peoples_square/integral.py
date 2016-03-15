##############################################################
# This is a utility file to help with laboratory exercises in
# the "Understanding Cryptology: Cryptanalysis" course offered
# by Dr. Kerry McKay
# Hosted at OpenSecurityTraining.info under a CC BY-SA license
# http://creativecommons.org/licenses/by-sa/3.0/
##############################################################

# Integral attack exercise
# This attack is on a 4-round variant of AES
# This code is written for understanding, not efficiency

ciphertexts = [
'd2e2579eee1fe0dd39458d5a3f4e9765', 'bba3808c6694c5b9c72b18ad8d9a1f78',
'46c756747a76d38a794a8c05de7e3cca', '59c6d4dfec3c316598a2d21d3307461b',
'd0b792fb87c20b8fb7935d7dd0dc2881', 'a32ca29fdd54ab75b7aa2097508f0004',
'07bf9d81e39e0e0e2adf0a32b514befd', '38104bcb762b7318db3e57fd5bf75d4c',
'24dce2f37526f111e177f39c40a523ba', '9e9b4181d109ae159c7ed10cc5bb0564',
'7336ac3c4d7dda2afb29e4083d0f1c8e', '0d1ea5c49482794f1b62f652b5015d34',
'4dddb99fa88362d8e0ca2c178a6f462b', '211dc2d04cf5662f6bde3f35d0315fa8',
'd079d71aa68dddf43bd192492f5fa910', '6de5c80099c0a7034c8551581de41d26',
'8fa472d951142efe169d8b1313b64ea4', '28e76d17c7fef6099ce59833add815c3',
'16beded41805822ec24a797b05c58540', 'db8ef6a8f40bdadc1babe57b2400483d',
'2ba2947dc5a11d21611731f0a6174cfa', '639eb88af8fae1c50098d424b89a7759',
'b11c880f9b7d213cd9d600f6d519af1f', '2ebaaf1b1492d16ba5d4c08d06d45f7c',
'27e56c9cf0c8d2ac33327a42afd8503e', '9a4a585f3d28a2886ca56da329d01759',
'c76831f7f9b88ffc349be7e1678c3353', '7923bccdd7d6bbd193b8a2ad7ed3b899',
'b4e5a0ba35b62bcd0d8b589556c868f9', '1cd0f626bad01ea46a62f014f2d24c7a',
'0e9ecc68638285e52de96cf62eaa1a7f', '6051de722122db40e04aa2ff0bf7446a',
'8501f988e37b68506746ee36a9191502', '5ad84b54645c87d9ce727ede715ab52a',
'94b16ad4b58345958621bc5c0e852bce', '9e7fb595d457b23bcf47b8670842c631',
'76f25e155b4762c9c31cf804956b0cad', 'fc4dcedc5ba15a554bdd6d44db5f1d8a',
'57042f538d4749506851546b12a57769', '40bb26c71a20cee9f9313cc0f89bd6b9',
'6a4d80b9a221287552c455d0ddde44b9', '4c944d5c5bb9eea0955d512ca8975e89',
'f5d3568aa57f1f3b0047070e20e7a15a', 'ee17e4dff8ef058000700ca28b50ee0a',
'5eb6159d62048ace8d2f8cf30fbd8e2f', '4d076e5a5c9c1586eba62a0ba120b82a',
'4845025a045f90d27e76afbca9e240a4', '6910fbbb4064bded3597f3b40177e844',
'a8e2dbca63387c989f98016bb5adbdcf', '8c4880a7aa26da3a0cba4e48d59439a0',
'f02ba82f05207879793f93baa2eee538', '9c601edb2f732de662cc533f9fee2ad2',
'bfadae3c642a81e180925ee639371044', '72d341e60da081add3e7be5af46828e3',
'15d29d375d5ae422c9060c8dd2b97b58', '367e1e18454c481919337900a392aef7',
'3ca6a6c39a0d6ccf349ab1872032cb81', '96817ac302ec824d73c227f5a3559304',
'0e5fd7f1ec6a910b4ff857f5012b6302', 'b9dde873b9703c43232890e9720c8ccd',
'c720bf79ef85dd10bef3149836f99895', '893e56c884a4a586c94b69c988c1e59e',
'813de149422c62261ff8ebdcd5ead962', '351c6cb07e490c93b9d4dc65d4d9cda8',
'68661ea5fb2ac2462dd515e1f3cdee59', 'a82019f9c55e7f419306592f40e0dbb0',
'78cecc405344cec1abc078129a802f02', '80cd98a1ae98cf058ac290d47da64dd8',
'f60f053fa90d84b6a70b3563125e924d', '7d49b1a134dcea7a54c0e15aa4c93f15',
'0cdeb7eae3b0b76533bcfd3b21c735ad', 'df4741395c4fd4c87fab473b87468c29',
'b24379fed496488c1735e912dae424e9', 'da218b3a232afdb40f9824d7f2f4fc62',
'2c8371ab9b2c00aaae39778dd48afc5c', '8e3d642a976c66674cae5d932ae3b9c6',
'608b88c42b949297db4e36b8c11c3151', '03cd8ad4d091cef0f7a9791045565027',
'eeb4b95ce3014bf243d504d765ba1a1b', '3bb95fc044485258f1bb9245b6316c51',
'a0af16bfb2f3e2fb37ca48c67de8af68', 'bebefa01d3a8b47244918b9e2f6cae30',
'986bfa7b48aa9167a71bbf9d77424790', '594c11718d6d73126066c0a1db153ce1',
'4f645779ad31bceee75eaa1e4737779a', '28fdd9c8ddd59a59f8721d72dc2bf1ac',
'cb6fcf3cc5cc8bfe39cdcd3ef0ac01c6', '15a24c14602b05b0e798292916b903d8',
'c61091776a03a37734cece7809748914', '894754fcc0897126766b4dffef4c7f6d',
'9a45820f77eb08ac35a5e0303191a9b1', '3334dd398240508fd498592784f6a219',
'600323397506794dc774090b6984c7e9', 'f75101a4dc353bb1e400b1693fbe38ee',
'7e64b2b004379c4d6a4485fac3709cdb', 'f787a1e99198437370c77b79fdea29b6',
'f5a0ab068978d94230f44439c7c8de80', '4ec1f7ee8a2fcdbd3b3149ea80dca93a',
'c27f38201668b87e9b22a3bef2150878', 'fc6bd3f1aeb2ab7b7335d1318ec22ae0',
'fd7bcbe36d120616011ccc5bd35e2e66', '859fdad75b5997e1bbb289c68b8da7b1',
'28711a2fbd3f834c0624c57bbfd6d9cb', '13562c7f1a774600c095ca941edff56a',
'563da100c32e0acc5bee435d3c276a25', '248c9e68c3732834d59eec369b2a7a01',
'f6b771761dde7146dcd1b271a6f745eb', 'fcaa3291675499315c8fd3e2a60c97fa',
'95e43eaed86473ffbba8828fb9bddbf5', 'ae60f76499f95f8317181f1c6b67825b',
'494af1a920878bc98a658b53807a4123', '95049028ceba7feda3761155ab26eddc',
'50ddb255399fa11678b0f752206dbb5e', '19d545375ad0045af88d1fcf5252bdfe',
'c493c3b01a172cbaf13171498a2d3d9a', '783c5c0d4c33ef356a8bc036bda4f1bc',
'f47f00421bdc03cc0a2deb2422c8a12d', '30f605767f74f3c033543b97246b4071',
'8751f348ab862d468bdde707e1189af1', 'ed00f6c796c53a8cce0758b48f6695e4',
'4293e6305e1c824c6a1a7dd7ed39d062', '63888ba7f2866013a45aa2f2982eb080',
'12410c0fe1db754289b47d2397298f29', '670e6a2bb48d5d5f6144a32ad7747027',
'6402a25c6b24889bef5d3ac99a8bf1b7', 'd95f7a3c36ab41f6fab2acea8ae17805',
'47a4e51b8a7902b6fc3eb27317398b13', '3a71a3854c2290f8f304518e0a767e07',
'1bc5c43a62713d0a6de36549a8578867', '53767bf22c52a57c9bf4786f386e175e',
'1b031788fdb8e623ba34fb4c2300d889', '624af405a57ec71c29f4546776877194',
'8f4d9ee8932d9cc992e50c41900ffb6c', 'e05254d61d8091221bb3536033105316',
'f0556188aea4e03a980ee9f4aa47d0a9', 'a1497d18796a4a83787e9c39d9b4e42c',
'51d16423473fd39eaaf50d5cb694cb1f', 'e8a849f16b95253c6e874d32e28d84e8',
'11a250981d047789dfd06db5e50b509e', 'fe8bba4c91bf31c0708281b3a49cca53',
'94755eea366755cdcbdc3c408ba55693', '034df3e83f4cdfb9dd8544fe859fd5fe',
'19ca93263c8ff4aad3447d546c5a84cd', 'f632c199d1ea1d18ce93581775876500',
'986dae3b6a25bec816fe61ba003e7888', '6e0a5659e6d0d249821f8982b0a42dc3',
'c61d2fa7edde7bb8f77b42d54b2a85a9', '615e9416ee6d3237e31204fe43b3792a',
'cb2b75790a6e00c977b7fd0dcac19d2d', 'd012fa94c7699ad70312ab236cce5aa5',
'd55d37fca3cbe59cf6ff89283bd6e0ba', '32cfb4aa3db0aa06e15f4a3274997361',
'27ac00d66c692dde172d6c486f075c32', '337b5e377b2f3c4405a786d2a990830e',
'c7ded36b8023a866afbdc5ad21f11e87', '61e22361c2eb8c1a9e3708483138fd6d',
'8a41495d3454080b20af7c0253ac796f', 'e1159cfc1d8351b410658626a9bedda2',
'3b4d7c30c20a46bb586fbf73de3c8aa3', '844c94bb452e1b1105e98194fcc9a372',
'28956b53e494ea22fb0ced08a2f3aa10', 'bb5da10d032c7425fba675ac7038dc04',
'39ef80dc8fb44fb095997bae308ad406', '0f85ca9ad4731ece44cd9c203778bdc1',
'2998733487cc999284f4963a02bb8fea', '68194e9a5d2a20464456c07b5958b839',
'c0f92afe59effe8f490993646a13d88f', 'b1ad2e33eb4c72a5819612a1b7a843f5',
'c5b7b4a28e26a7b3c2944f32952f1747', '5922540abf13bda1e67c27defa5b7e0a',
'ad983d034742856a5ed3d89c8b6e71d6', '0f7a02188cf53ec3c9a4788e2d3f0365',
'173958a0c6ae941bf1dc3d56d06068ab', '21eb6a57457ff21c6ea85a824ca9afdb',
'00470fd5ea50083c62ea8a73b3a1f81a', 'bbfd36b1098376d490b01d23c98f62de',
'b1ce6e00cf58c43809a7ea842166f5fd', 'ac1c4731702113212289792e93f9a4f2',
'a94eae502a4d416054a95b0be05a25ed', 'e71f031f5185d0411f7fdf897db0be6c',
'9a121751e844cfea7287888457978e4f', '710833ce83c0169d34b061c3c4585ec2',
'11b4e0b7eaea60db7a448dd4623613f8', '333e0691ed73925b3a37a92b9f1f4cc9',
'24161cb017d81454e7b5d5df47b1283e', 'fbf675a4c9866862dcc358b59dec7002',
'96d85ef181b32dcb983806e30adc53d4', '4303ce6ae615044dc3ffc0eaa5617786',
'28969c04a18ffd8c10656462c2cbabf0', 'eddd0ccbee18e89d2ec2252da4eeca58',
'8a6e66c7eef29bd0c33d4a15c6110e30', 'c51e70475564379d8b279476e22cce0d',
'0bcf00498d3bee625813ceb08639d70a', '6b7a451d5e023ffcad7cee92298d0439',
'0966ee2a6c0dfcaffdb0e7006cb80b78', '1af91667cc2c83fc1baa2507166cd731',
'd01a69b6374217664303026b42eaa3be', 'a1d19c7a27d983270bf8a25bdedd135a',
'54cad482cbf1a741ff0e91d8fb0ec6a6', '64354b72a39b132b0e1f9203aaa7e0be',
'6951c6b145e06a49e2e87f2e8aef10ce', '5c77789040446a608f8f316de83664b2',
'94daea57aba81b19de868e423be7cf51', '009a2116045b9a762f17505139e06e23',
'92b731fed4e27b0db5a68ce827998845', '0a4fe78a63ce9722b6bab7218038c418',
'f9117dab5d3070ceea302d47493ab11e', 'c96b432945664c87490a56147c017b05',
'1adeb43900c2bb2f4b72883e674b19dd', '587e43fcf2920fcf2d9533ddd33ffa0f',
'9ff6fa8bddbefd5bead7d7574131530a', '83f298db96474aa90b5f4339dbc5eac1',
'5ccbd456c4e71d86c16f45e506a2f579', 'cf0f60a069ec03b8fc4a3e6b8d61e7a1',
'b35779643517300bc32068bdaeb97721', '50f85e4eae2475fa6d0b84e95380a994',
'9a8fe142dcfeb682b728a220f0e087ad', '5f9b5d33b9e6123c8553b82bbd7c4354',
'f162849e666d691b031bc0eabdb6cb0a', 'e1c53f4fbe008ad498e7e891769647a3',
'59d854f4664316fe276e6a80cfbe2202', '5d033a81dff2a9ac88990432c8af50c5',
'3dd2e6d89db696c32c96a999dd6240ba', '93fadd94e4163b81aa44b2bb0502d32f',
'cb177cb822b71c0fdf6f5612d1c294f5', 'eddd3b0d0b602a7ccd7a0470a7d65676',
'056b048bc9516924c67b16665aacb467', 'fc3996f3c95df19d5686497e52825ed5',
'fa69257a5891558cb96c2fe5ce8976bf', 'f0b607e9c54e6270266322b6001d5391',
'b2b61c9ceb04e408e39e02331f41551b', 'e157ef915827e1b4e6b08a39689930e5',
'd74b8d8c11db47af023185a6390e1692', '8e646c32e894e206873fd5a0908a2249',
'773b3976a415c0f9eed1eff8c0b91be6', '5df1c29cf06c3a0498456ef664e48e80',
'4c429f6f9fa8a75b64b4ad2ac292f2d4', '1af8b79dff437b8a0d2ea9523e468712',
'b4eb0a344ce673a542c79d39956da4b6', '224e8082bb374652d25361e56d19ec88',
'bb7ff43454779adb1b160d8e7a12963f', '54e9082ed484c6a6ccd8c4b690cf697d',
'1b194681f6ef47a5ce49c20de0a08421', '1673503d55471f634d57e464ab39f557',
'a02edc8703816e5c70f2fa647292c39c', 'b569bc455248cabc754ab427f406dafc',
'62e2f2058133c157e134961107b9ee83', '6507a19f3f0725ad98a1c96a67d89237',
'45c67552632288c31f6c812df2f1a033', '71ae9cb8afcc54c1414fbd68dd3493c4',
'b745d1637383e808d01989d901c456a4', '6b9a575eb30a286571644053cab7d9ef',
'2a4674be0bb586645ac939b741a81450', '17d45682137f0e1a1d16cee83ac601a6',
'97c09c268d9b91c4e7c92479ecac6953', 'bf3e737e4f894737ffa148d75b840884' ]

ciphertexts = [[ord(c) for c in x.decode('hex')] for x in ciphertexts]

sbox = (0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
        0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 
        0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 
        0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 
        0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 
        0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 
        0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 
        0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 
        0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 
        0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 
        0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 
        0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 
        0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 
        0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 
        0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 
        0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 
        0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16)

invsbox = []
for i in range(256):
    invsbox.append(sbox.index(i))


def SubBytes(state):
    state = [list(c) for c in state]
    for i in range(len(state)):
        row = state[i]
        for j in range(len(row)):
            state[i][j] = sbox[state[i][j]]
    return state

def InvSubBytes(state):
    state = [list(c) for c in state]
    for i in range(len(state)):
        row = state[i]
        for j in range(len(row)):
            state[i][j] = invsbox[state[i][j]]
    return state


def rowsToCols(state):
    cols = []
    
    #convert from row representation to column representation
    cols.append([state[0][0], state[1][0], state[2][0], state[3][0]])
    cols.append([state[0][1], state[1][1], state[2][1], state[3][1]])
    cols.append([state[0][2], state[1][2], state[2][2], state[3][2]])
    cols.append([state[0][3], state[1][3], state[2][3], state[3][3]])
    
    return cols


def colsToRows(state):
    rows = []
    
    #convert from column representation to row representation 
    rows.append([state[0][0], state[1][0], state[2][0], state[3][0]])
    rows.append([state[0][1], state[1][1], state[2][1], state[3][1]])
    rows.append([state[0][2], state[1][2], state[2][2], state[3][2]])
    rows.append([state[0][3], state[1][3], state[2][3], state[3][3]])
    
    return rows


###########
# Key schedule functions
###########
# key schedule helper function
def RotWord(word):
    r = []
    r.append(word[1])
    r.append(word[2])
    r.append(word[3])
    r.append(word[0])
    return r


# key schedule helper function
def SubWord(word):
    r = []
    r.append(sbox[word[0]])
    r.append(sbox[word[1]])
    r.append(sbox[word[2]])
    r.append(sbox[word[3]])
    return r

# key schedule helper function
def XorWords(word1, word2):
    r = []
    for i in range(len(word1)):
        r.append(word1[i] ^ word2[i])
    return r

def printWord(word):
    str = ""
    for i in range(len(word)):
        str += "{0:02x}".format(word[i])
    print str
        
    
Rcon = [[0x01,0x00,0x00,0x00], [0x02,0x00,0x00,0x00], [0x04,0x00,0x00,0x00],
    [0x08,0x00,0x00,0x00], [0x10,0x00,0x00,0x00], [0x20,0x00,0x00,0x00], 
    [0x40,0x00,0x00,0x00], [0x80,0x00,0x00,0x00],[0x1B,0x00,0x00,0x00], 
    [0x36,0x00,0x00,0x00]]


# key is a 4*Nk list of bytes, w is a Nb*(Nr+1) list of words
# since we're doing 4 rounds of AES-128, this means that
# key is 16 bytes and w is 4*(4+1) words
def KeyExpansion(key):
    Nk = 4
    Nb = 4
    Nr = 4
    
    temp = [0,0,0,0]
    w=[]
    for i in range(Nb*(Nr+1)):
        w.append([0,0,0,0])
    
    i = 0
    
    #the first word is the master key
    while i<Nk:
        w[i] = [key[4*i],key[4*i+1], key[4*i+2], key[4*i+3]]
        
        #printWord(w[i])
        i = i+1
    
    i=Nk
    
    
    while i < (Nb*(Nr+1)):
        #print "Round ", i
        temp = w[i-1]
        #printWord(temp)
        if (i % Nk) == 0:
            #print "Rcon: ", printWord(Rcon[i/Nk-1])
            #printWord(RotWord(temp))
            #printWord(SubWord(RotWord(temp)))
            temp = XorWords(SubWord(RotWord(temp)), Rcon[i/Nk-1])
            #print "After XOR with Rcon:"
            #printWord(temp)
        #printWord(temp)
        #printWord(w[i-Nk])
        w[i] = XorWords(w[i-Nk], temp)
        i = i+ 1
        
    return w



def Shiftrows(state):
    state = colsToRows(state)

    #move 1
    state[1].append(state[1].pop(0))
    
    #move 2
    state[2].append(state[2].pop(0))
    state[2].append(state[2].pop(0))
    
    #move 3
    state[3].append(state[3].pop(0))
    state[3].append(state[3].pop(0))
    state[3].append(state[3].pop(0))
    
    return rowsToCols(state)   



def InvShiftrows(state):
    state = colsToRows(state)

    #move 1
    state[1].insert(0,state[1].pop())
    
    #move 2
    state[2].insert(0,state[2].pop())
    state[2].insert(0,state[2].pop())
    
    #move 3
    state[3].insert(0,state[3].pop())
    state[3].insert(0,state[3].pop())
    state[3].insert(0,state[3].pop())
    
    return rowsToCols(state)    
    

#converts integer x into a list of bits
#least significant bit is in index 0
def byteToBits(x):
    r = []
    while x>0:
        if (x%2):
            r.append(1)
        else:
            r.append(0)
        x = x>>1

    #the result should have 8 bits, so pad if necessary
    while len(r) < 8:
        r.append(0)
        
    return r


#inverse of byteToBits
def bitsToByte(x):
    r = 0
    for i in range(8):
        if x[i] == 1:
            r += 2**i
            
    return r


# Galois Multiplication
def galoisMult(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256


#single column multiplication
def mixColumn(column):
    temp = []
    for i in range(len(column)):
        temp.append(column[i])
    
    column[0] = galoisMult(temp[0],2) ^ galoisMult(temp[3],1) ^ \
                galoisMult(temp[2],1) ^ galoisMult(temp[1],3)
    column[1] = galoisMult(temp[1],2) ^ galoisMult(temp[0],1) ^ \
                galoisMult(temp[3],1) ^ galoisMult(temp[2],3)
    column[2] = galoisMult(temp[2],2) ^ galoisMult(temp[1],1) ^ \
                galoisMult(temp[0],1) ^ galoisMult(temp[3],3)
    column[3] = galoisMult(temp[3],2) ^ galoisMult(temp[2],1) ^ \
                galoisMult(temp[1],1) ^ galoisMult(temp[0],3)    
                
    return column


def MixColumns(cols):
    #cols = rowsToCols(state)
    
    r = [0,0,0,0]
    for i in range(len(cols)):
        r[i] = mixColumn(cols[i])
                    
         
    return r

def mixColumnInv(column):
    temp = []
    for i in range(len(column)):
        temp.append(column[i])
    
    column[0] = galoisMult(temp[0],0xE) ^ galoisMult(temp[3],0x9) ^ galoisMult(temp[2],0xD) ^ galoisMult(temp[1],0xB)
    column[1] = galoisMult(temp[1],0xE) ^ galoisMult(temp[0],0x9) ^ galoisMult(temp[3],0xD) ^ galoisMult(temp[2],0xB)
    column[2] = galoisMult(temp[2],0xE) ^ galoisMult(temp[1],0x9) ^ galoisMult(temp[0],0xD) ^ galoisMult(temp[3],0xB)
    column[3] = galoisMult(temp[3],0xE) ^ galoisMult(temp[2],0x9) ^ galoisMult(temp[1],0xD) ^ galoisMult(temp[0],0xB)    
                
    return column

def InvMixColumns(cols):
    #cols = rowsToCols(state)
    
    r = [0,0,0,0]
    for i in range(len(cols)):
        r[i] = mixColumnInv(cols[i])
                    
         
    return r


#state s, key schedule ks, round r
def AddRoundKey(s,ks,r):

    for i in range(len(s)):
        for j in range(len(s[i])):
            s[i][j] = s[i][j] ^ ks[r*4+i][j]

    return s



########
# Encrypt functions
#########
# for rounds 1-3
def oneRound(s, ks, r):
    s = SubBytes(s)
    s = Shiftrows(s)
    s = MixColumns(s)
    s = AddRoundKey(s,ks,r)
    return s

def oneRoundDecrypt(s, ks, r):
    s = AddRoundKey(s,ks,r)
    s = InvMixColumns(s)
    s = InvShiftrows(s)
    s = InvSubBytes(s)
    return s


# round 4 (no MixColumn operation)
def finalRound(s, ks, r):
    s = SubBytes(s)
    s = Shiftrows(s)
    s = AddRoundKey(s,ks,r)
    return s

def finalRoundDecrypt(s, ks, r):
    s = AddRoundKey(s,ks,r)
    s = InvShiftrows(s)
    s = InvSubBytes(s)
    return s

# Put it all together
def encrypt4rounds(message, key):
    s = []
    
    #convert plaintext to state
    s.append(message[:4])
    s.append(message[4:8])
    s.append(message[8:12])
    s.append(message[12:16])
    #printState(s)
    
    #compute key schedule
    ks = KeyExpansion(key)
    
    #apply whitening key
    s = AddRoundKey(s,ks,0)
    #printState(s)
    
    c = oneRound(s, ks, 1)
    c = oneRound(c, ks, 2)
    c = oneRound(c, ks, 3)
    #printState(c)
    c = finalRound(c, ks, 4)
    #printState(c)
    
    #convert back to 1d list
    output = []
    for i in range(len(c)):
        for j in range(len(c[i])):
            output.append(c[i][j])
    
    return output

def swapRows(rows):
    result = []
    for i in range(4):
        for j in range(4):
            result.append(rows[j*4+i])
    return result

def decrypt4rounds(message, key):
    #message = swapRows(message)

    s = []
    
    #convert plaintext to state
    s.append(message[:4])
    s.append(message[4:8])
    s.append(message[8:12])
    s.append(message[12:16])
    #printState(s)
    
    #compute key schedule
    ks = KeyExpansion(key)
    
    #apply whitening key
    #printState(s)
    s = finalRoundDecrypt(s, ks, 4)
    
    c = oneRoundDecrypt(s, ks, 3)
    c = oneRoundDecrypt(c, ks, 2)
    c = oneRoundDecrypt(c, ks, 1)
    c = AddRoundKey(c,ks,0)
    #printState(c)
    #printState(c)
    
    #convert back to 1d list
    output = []
    for i in range(len(c)):
        for j in range(len(c[i])):
            output.append(c[i][j])
    
    return output

testCt = range(16)
testState = []
testState.append(testCt[:4])
testState.append(testCt[4:8])
testState.append(testCt[8:12])
testState.append(testCt[12:16])

key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 
        0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]


ks = KeyExpansion(key)

textData = [0]*16
assert AddRoundKey(AddRoundKey(testState, ks, 1), ks, 1) == testState
assert InvMixColumns(MixColumns(testState)) == testState
assert InvShiftrows(Shiftrows(testState)) == testState
assert InvSubBytes(SubBytes(testState)) == testState
assert oneRoundDecrypt(oneRound(testState, ks, 1), ks, 1) == testState
assert finalRoundDecrypt(finalRound(testState, ks, 1), ks, 1) == testState
assert decrypt4rounds(encrypt4rounds(textData, key), key) == textData

#########################
# Attack code goes here #
#########################

def backup(ct, byteGuess, byteIndex):
    # We just need to check sums
    # There is no mixColumns in the last round, so skip it.
    # shiftRows just changes the byte's position. We don't care, so skip it.
    # All we need is a single xor for the guessed byte, and InvSubBytes

    t = ct[byteIndex] ^ byteGuess
    return invsbox[t]


def integrate(index):
    if len(ciphertexts) != 256:
        print "ERROR"
    potential = []

    for candidateByte in range(256):
        sum = 0
        for ciph in ciphertexts:
            oneRoundDecr = backup(ciph, candidateByte, index)
            sum ^= oneRoundDecr
        if sum == 0:
            potential.append(candidateByte)
    return potential


from itertools import product
def integral():
    candidates = []
    for i in range(16):
        candidates.append(integrate(i))
    print 'candidates', candidates
    for roundKey in product(*candidates):
        masterKey = round2master(roundKey)
        plain = ''.join(chr(c) for c in decrypt4rounds(ciphertexts[1], masterKey))
        if '\0\0\0\0' in plain:
            print 'solved', masterKey
            return masterKey

# Calculate the master key candidate from the final round key candidate
def round2master(rk):
    Nr=4
    Nk=4
    Nb=4
    w = []
    for i in range(Nb*(Nr+1)):
        w.append([0,0,0,0])
        
    i=0
    while i<Nk:
        w[i] = [rk[4*i],rk[4*i+1], rk[4*i+2], rk[4*i+3]]
        
        #printWord(w[i])
        i = i+1

    j = Nk
    while j < Nb*(Nr+1):
        if (j%Nk) == 0:
            #print w[j-1],w[j-2]
            #tmp = SubWord(XorWords(w[j-1], w[j-2]))
            #w[j] = XorWords(XorWords(w[j-Nk], tmp), Rcon[Nr+1-j/Nk])
            #print "rcon: ", printWord(Rcon[Nr + 1 - j/Nk])
            w[j][0] = w[j-Nk][0] ^ sbox[w[j-1][1] ^ w[j-2][1]] ^ Rcon[Nr - j/Nk][0]
            for i in range(1,4):
                w[j][i] = w[j-Nk][i] ^ sbox[w[j-1][(i+1) % 4] ^ w[j-2][(i+1) % 4]]
        else:
            w[j] = XorWords(w[j-Nk], w[j-Nk-1])
        j = j+1
    
#    for i in range(20):
#        printWord(w[i])
    
    m = []
    for i in range(16,20):
        for j in range(4):
            m.append(w[i][j])
            

    return m
    
######################
# Printing functions #
######################
def printState(s):
    print "State:"
    for i in range(len(s)):
        row = s[i]
        rowstring = ""
        for j in range(len(row)):
            rowstring += "{0:02x} ".format(row[j])
        print rowstring
    print "\n"


def printKey(ks):
    for i in range(len(ks)):
        row = ks[i]
        rowstring = ""
        for j in range(len(row)):
            #rowstring += "{0:02x} ".format(row[j])
            rowstring += "{0:4} ".format(row[j])
        print rowstring
    print "\n"


###
# Main - attack code goes here
###    

key = integral()

flag1 = 'af93ceae1f1e7a1326d60551973c461b'.decode('hex')
flag2 = 'c9b1569c2cdfd55ac6ca334631fb1973'.decode('hex')

flag1 = [ord(c) for c in flag1]
flag2 = [ord(c) for c in flag2]

flag = decrypt4rounds(flag1, key) + decrypt4rounds(flag2, key)
print ''.join(chr(c) for c in flag)
