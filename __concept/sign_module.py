#!/usr/bin/python
#-*- coding: utf-8 -*-

def main():
    import Crypto.PublicKey.RSA as RSA
    import sys
    
    if sys.argv[1] == 'generate':
        try:
            open('scoville_prv.pem')
        except IOError:
            pass
        else:
            print "Key Already exists. Are you sure you want to overwrite it? (yes)"
            if raw_input() != "yes":
                print "Aborted"
                sys.exit(1)
        import os
        key = RSA.generate(1024, os.urandom)
        pubkey = key.publickey()
        file_private = open('scoville_prv.pem','w')
        file_private.write(key.exportKey())
        file_private.close()
        file_public  = open('scoville_pub.pem','w')
        file_public.write(pubkey.exportKey())
        file_public.close()
        print "Keys successfully generated"
        
    elif sys.argv[1] == 'sign':
        try:
            filename=sys.argv[2]
        except IndexError:
            print "Second parameter must be the package"
            sys.exit(1)
        try:
            moduleData = open(filename,'r').read()
        except IOError:
            print "Could not open Scoville Module "+filename
            sys.exit(1)
        
        try:
            keyraw = open('scoville_prv.pem','r').read()
        except IOError:
            print "Need a private Key 'scoville_prv.pem' to sign packet."+\
                  "Generate Key using sign_module.py generate"
            sys.exit(1)
        import Crypto.Hash.SHA256 as SHA256
        import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5
        import json
        key = RSA.importKey(keyraw)
        hash = SHA256.new(moduleData)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(hash)
        print type(signature)
        import base64
        signature = base64.encodestring(signature)
        
        sigFile = open(filename+'.sig','w')
        sigFile.write(signature)
        sigFile.close()
        print "Generated Signature"
        
    elif sys.argv[1] == 'verify':
        try:
            filename=sys.argv[2]
        except IndexError:
            print "Second parameter must be the package"
            sys.exit(1)
        try:
            moduleData = open(filename,'r').read()
        except IOError:
            print "Could not open Scoville Module "+filename
            sys.exit(1)
        
        try:
            keyraw = open('scoville_pub.pem','r').read()
        except IOError:
            print "Need a private Key 'scoville_prv.pem' to sign packet."+\
                  "Generate Key using sign_module.py generate"
            sys.exit(1)
        import json
        try:
            import base64
            signature = base64.decodestring(open(filename+'.sig','r').read())
        except IOError:
            print "Could not load signature"
            sys.exit(1)
        import Crypto.Hash.SHA256 as SHA256
        import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5
        key = RSA.importKey(keyraw)
        verifier = PKCS1_v1_5.new(key)
        hash = SHA256.new(moduleData)
        print "key: "+keyraw
        print "hash: "+hash.hexdigest()

        if verifier.verify(hash,signature):
            print "This Module is safe"
        else:
            print "Someone fucked around with this Module"
        
    else:
        print """Dumb Command.
                 
         Smart Commands are:
           - generate          Generates RSA-Keys
           - sign <package>    Generates Signature for a Package
           - verify <package>  Verifies a package from .sig file"""
             
if __name__ == '__main__':
    main()