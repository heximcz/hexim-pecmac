from Zabbix import ZabbixFile


class ZabbixRead:

    def __init__(self):
        zbx = ZabbixFile()
        self.data = zbx.read()
        self.sensors = len(self.data)

    def get_current(self, phase):
        # 'F1': {'ampere': '0.00', 'watt': '0.00'},
        # 'F2': {'ampere': '0.00', 'watt': '0.00'},
        # 'F3': {'ampere': '0.00', 'watt': '0.00'}}}
        # "No. of channel is over range."
        if phase <= self.sensors:
            return self.data['F'+str(phase)]['ampere']
        return "Phase number is over the range."

    def get_watts(self, phase):
        # 'F1': {'ampere': '0.00', 'watt': '0.00'},
        # 'F2': {'ampere': '0.00', 'watt': '0.00'},
        # 'F3': {'ampere': '0.00', 'watt': '0.00'}}}
        if phase <= self.sensors:
            return self.data['F'+str(phase)]['watt']
