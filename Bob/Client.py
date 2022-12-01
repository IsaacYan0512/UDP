from socket import *
from threading import Thread
from sys import exit
import random
from unicodedata import name
import rsa
import string
import hashlib
import base64
from Crypto.Cipher import ARC4


NB = ''.join(random.choices(string.ascii_letters + string.digits, k=128))
K = ''.join(random.choices(string.ascii_letters + string.digits, k=128))


soc = socket(AF_INET, SOCK_DGRAM)
soc.bind(('127.0.0.1',3333))   
    
def verify():
    
    msg = input("Please input Username and password:") #用户名密码
    pswd1 = msg[5:]
    
    msg1 = 'Bob, '+ NB
    soc.sendto(msg1.encode('utf-8'),("127.0.0.1",5555))

    data1 = soc.recvfrom(1024) #收 Alice
    receive1 = data1[0].decode('utf-8')
    pub1 = receive1[7:433]
    global  NA
    NA = receive1[-128:]
    pub = pub1.encode()   
    pubkey = hashlib.sha1(pub).hexdigest()

    with open ('finger_print.txt', 'r') as f:              #判断指纹
        public = f.read()
    public = str(public)

    if public != pubkey:
        soc.close()
    else:
        pubkey1 = bytes(pub1, encoding="utf8")
        pubkey2 = rsa.PublicKey.load_pkcs1(pubkey1)
        msg2 = pswd1 + ', ' +K
        msg3 = msg2.encode('ascii')
        en_msg2 = rsa.encrypt(msg3, pubkey2)
        en_msg = base64.b64encode(en_msg2).decode()
        soc.sendto(en_msg.encode('utf-8'),("127.0.0.1",5555))
        wor=soc.recvfrom(1024)
        wor = wor[0].decode('utf-8')
        print(wor)
        if wor == 'Connection Failed':
            soc.close()

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
        if info == "exit":
            soc.close()
        else:
            h = SSk().decode('utf-8')+info
            h = h.encode()
            h = hashlib.sha1(h).hexdigest()
            info = info + h
            msg = RC4_encrypt(info.encode('utf-8'))
            soc.sendto(msg,("127.0.0.1",5555))



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
