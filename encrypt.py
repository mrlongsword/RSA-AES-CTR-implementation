import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from base64 import b64encode

enc_aes_key = ""
aes_key = ""
plaintext = ""
ciphertext = ""

# send encrypted key to server
def send_to_server():
    global enc_aes_key
    try:
        requests.post('https://enzyhxpv9aau.x.pipedream.net', data={'encrypted_AES_key':enc_aes_key})
    except:
        print("Whoops...something went wrong.\nWriting key to file\n Check 'encrypted_AES_key.txt'")
        fout = open("encrypted_AES_key.txt", "w")
        fout.write(enc_aes_key)
        fout.close()

def aes_key_gen():
    global aes_key 
    aes_key = get_random_bytes(16)
def aes_encrypt():
    global aes_key,plaintext,ciphertext
    cipher = AES.new(aes_key, AES.MODE_CTR)
    ct_bytes = cipher.encrypt(bytes(plaintext,'utf-8'))
    nonce = b64encode(cipher.nonce).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    ciphertext = nonce +' '+ ct

def rsa_encrypt_aes_key():
    global aes_key,enc_aes_key
    try:
        public_key = RSA.import_key(open("public.pem").read())
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_aes_key = cipher_rsa.encrypt(aes_key)
        enc_aes_key = b64encode(enc_aes_key).decode('utf-8')
    except FileNotFoundError:
        print("[!ERROR!]RSA Public Key not found. Please generate a new pair with rsa_key_gen.py.")
        exit()
    
def get_message():
    global plaintext
    print("Enter your message. You can enter multiple lines.Ctrl-D or Ctrl-Z ( windows ) to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    plaintext = '\n'.join(contents)
def write_to_file():
    global ciphertext
    print("[+]Writing ciphertext to file")
    file_out = open("ciphertext.txt", "w")
    file_out.write(ciphertext)
    file_out.close()
    print("[+]Done")
def main():
    global plaintext,ciphertext
    get_message()
    aes_key_gen()
    aes_encrypt()
    rsa_encrypt_aes_key()
    send_to_server()
    write_to_file()
    

main()
