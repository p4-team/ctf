/* 
 * Fast, portable, and easy-to-use Twofish implementation,  
 * Version 0.3. 
 * Copyright (c) 2002 by Niels Ferguson. 
 * 
 * See the twofish.c file for the details of the how and why of this code. 
 * 
 * The author hereby grants a perpetual license to everybody to 
 * use this code for any purpose as long as the copyright message is included 
 * in the source code of this or any derived work. 
 */ 
 
 
/* 
 * PLATFORM FIXES 
 * ============== 
 * 
 * The following definitions have to be fixed for each particular platform  
 * you work on. If you have a multi-platform program, you no doubt have  
 * portable definitions that you can substitute here without changing  
 * the rest of the code. 
 * 
 * The defaults provided here should work on most PC compilers. 
 */ 
 
 
/*  
 * A Twofish_Byte must be an unsigned 8-bit integer. 
 * It must also be the elementary data size of your C platform, 
 * i.e. sizeof( Twofish_Byte ) == 1. 
 */ 
typedef unsigned char   Twofish_Byte; 
 
/*  
 * A Twofish_UInt32 must be an unsigned integer of at least 32 bits.  
 *  
 * This type is used only internally in the implementation, so ideally it 
 * would not appear in the header file, but it is used inside the 
 * Twofish_key structure which means it has to be included here. 
 */ 
typedef unsigned int    Twofish_UInt32; 
 
/*  
 * Select data type for q-table entries.   
 *  
 * Larger entry types cost more memory (1.5 kB), and might be faster   
 * or slower depending on the CPU and compiler details.  
 *  
 * This choice only affects the static data size and the key setup speed.  
 * Functionality, expanded key size, or encryption speed are not affected.  
 * Define to 1 to get large q-table entries.  
 */   
#define LARGE_Q_TABLE   0    /* default = 0 */   

/*  
 * The q-boxes are only used during the key schedule computations.   
 * These are 8->8 bit lookup tables. Some CPUs prefer to have 8->32 bit   
 * lookup tables as it is faster to load a 32-bit value than to load an   
 * 8-bit value and zero the rest of the register.  
 * The LARGE_Q_TABLE switch allows you to choose 32-bit entries in   
 * the q-tables. Here we just define the Qtype which is used to store   
 * the entries of the q-tables.  
 */   
#if LARGE_Q_TABLE   
typedef Twofish_UInt32      Qtype;   
#else   
typedef Twofish_Byte        Qtype;   
#endif   

/* 
 * END OF PLATFORM FIXES 
 * ===================== 
 *  
 * You should not have to touch the rest of this file, but the code 
 * in twofish.c has a few things you need to fix too. 
 */  
 
/* 
 * Structure that contains a prepared Twofish key. 
 * A cipher key is used in two stages. In the first stage it is converted 
 * from the original form to an internal representation.  
 * This internal form is then used to encrypt and decrypt data.  
 * This structure contains the internal form. It is rather large: 4256 bytes 
 * on a platform with 32-bit unsigned values. 
 * 
 * Treat this as an opague structure, and don't try to manipulate the 
 * elements in it. I wish I could hide the inside of the structure, 
 * but C doesn't allow that. 
 */ 
class TwofishKey
    {
    public: 
    TwofishKey()
        {
        Clear();
        }
    void Clear();

    Twofish_UInt32 s[4][256];   /* pre-computed S-boxes */ 
    Twofish_UInt32 K[40];       /* Round key words */ 
    };
 
class Twofish
    {
    public:

    /** 
    Construct and test the Twofish object.

    Apart from constructing the object it performs a self test. 
    If assert() or the Twofish_fatal function is not called, the code passed the test. 
    (See the twofish.c file for details on the Twofish_fatal function.) 
    */ 
    Twofish();

    /** 
    Convert a cipher key to the internal form used for  
    encryption and decryption. 
     
    The cipher key is an array of bytes; the Twofish_Byte type is  
    defined above to a type suitable on your platform.  
    
    Any key must be converted to an internal form in the TwoFishKey structure 
    before it can be used. 
    The encryption and decryption functions only work with the internal form. 
    The conversion to internal form need only be done once for each key value. 
    
    Be sure to wipe all key storage, including the TwoFishKey structure,  
    once you are done with the key data.  
    A call to TwofishKey::Clear() will do just fine. 
    
    Unlike most implementations, this one allows any key size from 0 bytes  
    to 32 bytes. According to the Twofish specifications,  
    irregular key sizes are handled by padding the key with zeroes at the end  
    until the key size is 16, 24, or 32 bytes, whichever 
    comes first. Note that each key of irregular size is equivalent to exactly 
    one key of 16, 24, or 32 bytes. 
    
    WARNING: Short keys have low entropy, and result in low security. 
    Anything less than 8 bytes is utterly insecure. For good security 
    use at least 16 bytes. I prefer to use 32-byte keys to prevent 
    any collision attacks on the key. 
    
    The key length argument key_len must be in the proper range. 
    If key_len is not in the range 0,...,32 this routine attempts to generate  
    a fatal error (depending on the code environment),  
    and at best (or worst) returns without having done anything. 
    
    Arguments: 
    aKeyBytes   Array of key bytes 
    aKeyLength  Number of key bytes, must be in the range 0,1,...,32.  
    aKey        Pointer to a TwofishKey object that will be filled  
                with the internal form of the cipher key. 
    */ 
    void PrepareKey(const Twofish_Byte aKeyBytes[],int aKeyLength,TwofishKey* aKey);

    /* 
    Encrypt a single block of data. 
    
    This function encrypts a single block of 16 bytes of data. 
    If you want to encrypt a larger or variable-length message,  
    you will have to use a cipher mode, such as CBC or CTR.  
    These are outside the scope of this implementation. 
    
    The key structure is not modified by this routine, and can be 
    used for further encryption and decryption operations. 
    
    Arguments: 
    aKey            the key
    aPlainText      plain text to be encrypted 
    aCipherText     place to store the cyphertext 
    */ 
    void Encrypt(const TwofishKey* aKey,const Twofish_Byte aPlainText[16],Twofish_Byte aCipherText[16]); 
 
    /* 
    Decrypt a single block of data. 
    
    This function decrypts a single block of 16 bytes of data. 
    If you want to decrypt a larger or variable-length message,  
    you will have to use a cipher mode, such as CBC or CTR.  
    These are outside the scope of this implementation. 
    
    The key structure is not modified by this routine, and can be 
    used for further encryption and decryption operations. 
    
    Arguments: 
    aKey            the key 
    aCipherText     cyphertext to be decrypted
    aPlainText      place to store the plain text 
    */ 
    void Decrypt(const TwofishKey* aKey,const Twofish_Byte aCipherText[16],Twofish_Byte aPlainText[16]); 

    private:
    void test_vector(Twofish_Byte key[],int key_len,Twofish_Byte p[16],Twofish_Byte c[16]);   
    void test_vectors();
    void test_sequence(int key_len,Twofish_Byte final_value[]);
    void test_sequences();   
    void test_odd_sized_keys();
    void self_test();
    void initialise_q_boxes();
    void initialise_mds_tables();
    Twofish_UInt32 h(int k,Twofish_Byte L[],int kCycles);
    void fill_keyed_sboxes(Twofish_Byte S[],int kCycles,TwofishKey* xkey);   

    /*   
    The q-box tables.   
    There are two q-boxes, each having 256 entries.  
    */   
    Qtype q_table[2][256];   

    /* The MDS tables. */   
    Twofish_UInt32 MDS_table[4][256];   
    };
 
