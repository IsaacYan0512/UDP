from socket import *
import string
from threading import Thread
import random
import rsa
import hashlib
import string
import base64
from Crypto.Cipher import ARC4
from binascii import a2b_hex


NA = ''.join(random.choices(string.ascii_letters + string.digits, k=128))
soc = socket(AF_INET, SOCK_DGRAM)
soc.bind(('127.0.0.1',5555))  


def verify():
    data1=soc.recvfrom(1024)   #收用户名密码
    data1 = data1[0].decode('utf-8')
    global NB
    NB = data1[5:]

    with open("public.pem", 'r') as f:
            public = f.read()
    pub = str(public)
    msg1 = 'Alice, ' + pub + ', ' + NA
    soc.sendto(msg1.encode('utf-8'), ("127.0.0.1", 3333))


    with open("private.pem", 'r') as f:
        private = f.read()
    private = rsa.PrivateKey.load_pkcs1(private)
    data2 = soc.recvfrom(1024)
    msg2 = data2[0]
    msg3 = base64.b64decode(msg2)
    msg_2 = rsa.decrypt(msg3, private)
    
    pswd = str(msg_2, 'utf-8')
    pswd1 = pswd[0:8]
    global K
    K = pswd[10:]
    pswd1 = pswd1.encode()
    h_pswd = hashlib.sha1(pswd1).hexdigest()
    
    with open('pswd.txt', 'rb') as f:
        ha = f.read()
    ha = str(ha, 'utf-8') 
    if ha != h_pswd:     #比对用户名密码
        wor = 'Connection Failed'
        soc.sendto(wor.encode('utf-8'), ("127.0.0.1", 3333))
    else:
        wor = 'Connection Okay'
        soc.sendto(wor.encode('utf-8'), ("127.0.0.1", 3333))
    
def SSk():
    ssk1 = K+NA+NB
    ssk2 = ssk1.encode()
    ssk = hashlib.sha1(ssk2).hexdigest()
    ssk = ssk.encode('utf-8')
    return ssk
        
def RC4_decrypt(info):
    cipher = ARC4.new(SSk())
    msg = cipher.decrypt(info)
    return msg

def RC4_encrypt(info):
    cipher = ARC4.new(SSk())
    msg = cipher.encrypt(info)
    return msg

def recveData():
    while True:
        recevinfoa=soc.recvfrom(1024)
        info = recevinfoa[0]
        msg = RC4_decrypt(info)
        msg = msg.decode('utf-8')
        h = msg[-40:]
        msg1 = msg[:-40]
        h1 = SSk().decode('utf-8')+msg1
        h1 = h1.encode()
        h1 = hashlib.sha1(h1).hexdigest()
        if h == h1:
            print(msg1)
        else:
            print("The ciphertext is rejected")
    
def sendData():
    while True:
        info=input()
        h = SSk().decode('utf-8')+info
        h = h.encode()
        h = hashlib.sha1(h).hexdigest()
        info = info + h
        msg = RC4_encrypt(info.encode('utf-8'))
        soc.sendto(msg,("127.0.0.1",3333))



def main():
    
    verify()
   
    t1=Thread(target=recveData)
    t2=Thread(target=sendData)
                
    t1.start()
    t2.start()
        
    t1.join()
    t2.join()
   
    


if __name__ == '__main__':
    main()
