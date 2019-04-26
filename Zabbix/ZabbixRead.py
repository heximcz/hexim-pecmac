from Zabbix import ZabbixFile


class ZabbixRead:

    def __init__(self):
        zbx = ZabbixFile()
        self.data = zbx.read()

    def get_current(self, phase):
        # 'F1': {'ampere': '0.00', 'watt': '0.00'},
        # 'F2': {'ampere': '0.00', 'watt': '0.00'},
        # 'F3': {'ampere': '0.00', 'watt': '0.00'}}}
        return self.data['F'+str(phase)]['ampere']

    def get_watts(self, phase):
        # 'F1': {'ampere': '0.00', 'watt': '0.00'},
        # 'F2': {'ampere': '0.00', 'watt': '0.00'},
        # 'F3': {'ampere': '0.00', 'watt': '0.00'}}}
        return self.data['F'+str(phase)]['watt']
