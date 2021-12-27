from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
key = ""

def menu():
    print('''
    
    ''')
def decrypt_aes_key():
    global key
    private_key = RSA.import_key(open("private.pem").read())
    input_key = input('Enter the encrypted key\n')
    enc_session_key = b64decode(input_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    key = cipher_rsa.decrypt(enc_session_key)
def decrypt_ciphertext():
    global key
    try:
        ciphertext = open("ciphertext.txt").read()
        data = ciphertext.split(' ')
        nonce = data[0]
        message = data[1]
        nonce = b64decode(nonce)
        message = b64decode(message)
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        pt = cipher.decrypt(message)
        plaintext = pt.decode("utf-8")
        print(plaintext)
        f = open("decrypted.txt","w")
        f.write(plaintext)
        f.close()
    except FileNotFoundError:
        print("[!ERROR!]Could not find 'ciphertext.txt'\n Quitting...")
        exit()
def main():
    decrypt_aes_key()
    decrypt_ciphertext()
main()