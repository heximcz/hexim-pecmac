from Zabbix import ZabbixFile


class ZabbixRead:

    def __init__(self):
        zbx = ZabbixFile()
        self.data = zbx.read()
        print(self.data)