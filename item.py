class Item(object):
    def __init__(self):
        self.version = ''
        self.qr = '0'
        self.indicator = '0'
        self.network = '0'
        
    def set_version(self, version) :
        self.version = version
        
    def set_qr(self, yn) :
        self.qr = yn
        
    def set_indicator(self, yn) :
        self.indicator = yn
        
    def set_network(self, yn) :
        self.network = yn