class A(object):
    def __init__(self,parent):
        self.p = parent
    
    def getroot(self):
        return self.p.getroot()
    
class B(A):
    def __init__(self):
        pass
    def getroot(self):
        return 1
    
c = B()    
a = A(c)
b = A(a)

print b.getroot()

