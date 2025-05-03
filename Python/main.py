from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

        keyPair = RSA.generate(bits=1024)
        pubKey = keyPair.publickey()

        msg = b'Message for RSA signing'
        hash = SHA256.new(msg)
        signer = PKCS115_SigScheme(keyPair)
        signature = signer.sign(hash)
        print("Signature:", binascii.hexlify(signature))

        msg = b'Message for RSA signing'
        hash = SHA256.new(msg)
        verifier = PKCS115_SigScheme(pubKey)
        try:
        verifier.verify(hash, signature)
        print("Signature is valid.")
        except:
        print("Signature is invalid.")

        msg = b'A tampered message'
        hash = SHA256.new(msg)
        verifier = PKCS115_SigScheme(pubKey)
        try:
        verifier.verify(hash, signature)
        print("Signature is valid.")
        except:
        print("Signature is invalid.")