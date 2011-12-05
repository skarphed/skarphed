import Crypto.Cipher.AES
from Crypto.Cipher import AES

class Application:
    STATE_LOGGEDIN = 1
    STATE_LOGGEDOUT = 0
    def __init__(self):
        self.state = STATE_LOGGEDIN
        
        
application = Application()
def App():
    return application

        