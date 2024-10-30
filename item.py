class Item(object):
    def __init__(self):
        self.device_id = {}
        self.version = ''
        self.network_use = ''
        self.qr = ''
        self.indicator = ''
        self.network = ''
        
    def set_device_id(self, device_id) :
        self.device_id = device_id
        
    def set_version(self, ver_str) :
        self.version = ver_str
        
    def set_network_use(self, net_str) :
        self.network_use = net_str 
    
    def set_qr(self, yn) :
        self.qr = yn
        
    def set_indicator(self, yn) :
        self.indicator = yn
        
    def set_network(self, yn) :
        self.network = yn
        
    def get_device_id(self) :
        return self.device_id

    def get_version(self) :
        return self.version

    def get_network_use(self) :
        return self.network_use

    def get_qr(self) :
        return self.qr

    def get_indicator(self) :
        return self.indicator

    def get_network(self) :
        return self.network
    