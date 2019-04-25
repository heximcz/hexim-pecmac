import yaml


class ZabbixFile:

    def __init__(self):
        self.file_path = "/opt/ramdisk/current.txt"

    def write(self, data):
        try:
            with open(self.file_path, 'w') as stream:
                try:
                    stream.write(yaml.dump(data, default_flow_style=False))
                except yaml.YAMLError:
                    pass
        except IOError:
            pass
