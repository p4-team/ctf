const FLAG_SIZE: usize = 56;
const FLAG_DATA_SIZE: usize = FLAG_SIZE * 2;

#[derive(Debug, Copy, Clone)]
struct Unit {
    letter: u8,
    size: u8,
}

fn deserialize(data: &Vec<u8>) -> Vec<Unit> {
    let mut secret = Vec::new();
    for (letter, size) in data.iter().tuples() {
        secret.push(Unit {
            letter: *letter,
            size: *size,
        });
    }
    secret
}

fn decode(data: &Vec<Unit>) -> Vec<u8> {
    let mut res = Vec::new();
    for &Unit { letter, size } in data.iter() {
        res.extend(vec![letter; size as usize + 1].iter())
    }
    res
}

fn decrypt(data: &Vec<u8>) -> Vec<u8> {
    key = get_key();
    iv = get_iv();
    openssl::symm::decrypt(
        openssl::symm::Cipher::aes_256_ctr(),
        &key,
        Some(&iv),
        data
    ).unwrap()
}

fn store(data: &Vec<u8>) -> String {
    assert!(
        data.len() == FLAG_DATA_SIZE,
        "Wrong data size ({} vs {})",
        data.len(),
        FLAG_DATA_SIZE
    );
    let decrypted = decrypt(data);
    let secret = deserialize(&decrypted);
    let expanded = decode(&secret);
    base64::encode(&compute_sha3(&expanded)[..])
}

