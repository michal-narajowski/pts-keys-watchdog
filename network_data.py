import xml.etree.ElementTree as ET

import time


class NetworkData:
    def __init__(self, index, network_key, iv_index):
        self.index = index
        self.network_key = network_key
        self.iv_index = iv_index

    def __str__(self):
        return "NetworkData(Index={0}, NetworkKey={1}, IVIndex={2})".format(self.index, self.network_key, self.iv_index)

    @staticmethod
    def parse(filepath):
        # Sleep to avoid reading the file while some other process is writing to it.
        # This issue caused f.read() to return empty string.
        time.sleep(0.5)

        with open(filepath, 'r') as f:
            contents = f.read()

        if not contents:
            return None

        root = ET.fromstring(contents)

        if root is None:
            print('Root is none')
            return None

        if root.tag != 'MeshNetworkData':
            print('Root.tag is none')
            return None

        network = root.find("MeshNetwork")
        if network is None:
            print('Network is none')
            return None

        index = network.find("Index")
        if index is None:
            print('Index is none')
            return None

        netkey = network.find("NetworkKey")
        if netkey is None:
            print('Netkey is none')
            return None

        ivindex = network.find("IVIndex")
        if ivindex is None:
            print('IVIndex is none')
            return None

        return NetworkData(index.text, netkey.text, ivindex.text)
