from Crypto.Cipher import AES

# 加密函数
def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return nonce + ciphertext

# 解密函数
def decrypt(ciphertext, key):
    nonce = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext[16:])
    return plaintext


