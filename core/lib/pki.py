#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# © 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU Affero General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

import os
import Crypto.PublicKey.RSA as RSA
from StringIO import StringIO

class Pki(object):
    """
    Skarphed Instances need a PublicKey/PrivateKey-Pair
    to ensure that code, that is being transmitted from
    instance to the admininterface (e.g. the code used 
    for module- and widgetconfiguration) has not been 
    altered by third parties. Otherwise it would be possible
    to inject code and thereby threatening the integrity
    of the administrators system.
    """
    @classmethod
    def set_core(cls, core):
        """
        Sets the core
        """
        cls._core = core

    @classmethod
    def initialize(cls):
        """
        """
        cls._pki_is_present = False
        cls._public_key = None
        cls._private_key = None

        db = cls._core.get_db()
        stmnt = "SELECT PKI_HAS_PKI FROM PKI WHERE PKI_ID = 3 ;"
        cur = db.query(cls._core, stmnt)
        row = cur.fetchonemap()
        if row is not None:
            cls._pki_is_present = bool(row["PKI_HAS_PKI"])

        if cls._pki_is_present:
            cls._load_keys()

    @classmethod
    def _load_keys(cls):
        """
        Load the keys
        """
        db = cls._core.get_db()
        stmnt = "SELECT PKI_ID, PKI_KEY FROM PKI WHERE PKI_ID IN (1,2) ;"
        cur = db.query(cls._core, stmnt)
        for row in cur.fetchallmap():
            if row["PKI_ID"] == 1:
                cls._private_key = RSA.importKey(row["PKI_KEY"])
            elif row["PKI_ID"] == 2:
                cls._public_key = RSA.importKey(row["PKI_KEY"])

    @classmethod
    def _generate_pki(cls):
        """
        generates a public/private keypair and stores it in the
        database
        """
        key = RSA.generate(1024, os.urandom)
        pubkey = key.publickey()
        key_io = StringIO(key.exportKey())
        pubkey_io = StringIO(pubkey.exportKey())

        db = cls._core.get_db()
        stmnt = "INSERT INTO PKI (PKI_ID, PKI_KEY, PKI_HAS_PKI) VALUES (?,?, NULL) ;"
        db.query(cls._core, stmnt, (1, key_io), commit=True)
        db.query(cls._core, stmnt, (2, pubkey_io), commit=True)
        stmnt = "INSERT INTO PKI (PKI_ID, PKI_KEY, PKI_HAS_PKI) VALUES (3, NULL, 1) ;"
        db.query(cls._core, stmnt, commit=True)
        cls._pki_is_present = True

    @classmethod
    def get_public_key(cls, as_string=False):
        """
        returns the public key of this instance 
        """
        if not cls._pki_is_present:
            cls._generate_pki()
            cls._load_keys()
        
        if as_string:
            return cls._public_key.exportKey()
        else:
            return cls._public_key

    @classmethod
    def get_private_key(cls, as_string=False):
        """
        returns the private key of this instance
        """
        if not cls._pki_is_present:
            cls._generate_pki()
            cls._load_keys()

        if as_string:
            return cls._private_key.exportKey()
        else:
            return cls._private_key

    @classmethod
    def sign(cls, data):
        if not cls._pki_is_present:
            cls._generate_pki()
            cls._load_keys()
        
        import Crypto.Hash.SHA256 as SHA256
        import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5
        hashed = SHA256.new(data)
        signer = PKCS1_v1_5.new(cls._private_key)
        signature = signer.sign(hashed)
        return signature




class PkiManager(object):
    def __init__(self, core):
        Pki.set_core(core)
        Pki.initialize()

        self.get_public_key = Pki.get_public_key
        self.get_private_key = Pki.get_private_key
        self.sign = Pki.sign

