import json

class Config(object):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __getitem__(self, key):
        return self.config[key]

    def load_from_file(self, path = 'config.json'):
        f = open(path, 'r')
        data = f.read()
        f.close()
        self.config = json.loads(data)


Config().load_from_file('/etc/scvrepo/config.json')
