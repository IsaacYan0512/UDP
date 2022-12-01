# UDP
UDP-based authentication and encrypted communication protocol

This authentication and message encryption method starts by matching the incoming and outgoing port numbers of the host (Alice) and the client (Bob).
And generates an RSA key pair in the host folder and stores the public key fingerprint (i.e., H(pk)) in the client directory.

Client login requires username and password, and allows the client to send the first message of the authentication protocol when the username and password match. i.e. (Bob, NB (128-bit random string)). 

After the host verifies the first authentication message, the host sends the second authentication message to the client (Alice, pk, Na).

After the client verifies that the second authentication message is correct and sends the third authentication message to the host (C1 = PKE_pk(PW, K (a 128-bit random key chosen for the client))).

After all the above three authentication messages are passed, the host returns a normal connection prompt, otherwise it returns a failed connection.


After successful authentication, every message communicated between the host and the client is encrypted by the RC4 stream cipher. 

And the checksum appended to the authentication message is required.
