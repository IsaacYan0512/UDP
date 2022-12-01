import rsa
import hashlib
import os

current_path = os.path.abspath(__file__)

father_path1 = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
father_path2 = os.path.abspath(os.path.dirname(father_path1) + os.path.sep + ".")



(pubkey, privkey) = rsa.newkeys(2048)
 
with open(father_path1 + '\\public.pem','wb+') as f:
    f.write(pubkey.save_pkcs1())
    f.close()
 
with open(father_path1 + '\\private.pem','wb+') as f:
    f.write(privkey.save_pkcs1())
    f.close()



with open(father_path1 + "\\public.pem", 'r') as f:
    public = f.read() 
    f.close()

public = public.encode()
fp1 = hashlib.sha1(public).hexdigest()
fp = str(fp1)

with open (father_path2 + "\\Bob\\finger_print.txt", 'w+') as sha1_file:
    sha1_file.write(fp)
    f.close 




 