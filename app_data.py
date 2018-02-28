import xml.etree.ElementTree as ET


class AppKey:
    def __init__(self, index, netindex, appkey):
        self.index = index
        self.netindex = netindex
        self.appkey = appkey

    def __str__(self):
        return "AppKey(Index={0}, NetIndex={1}, AppKey={2})".format(self.index, self.netindex, self.appkey)

    def __repr__(self):
        return self.__str__()


class AppData:
    def __init__(self, app_keys, dev_key):
        self.app_keys = app_keys
        self.dev_key = dev_key

    def __str__(self):
        return "AppData(AppKeys={0}, DeviceKey={1})".format(self.app_keys, self.dev_key)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def parse(filepath):
        with open(filepath, 'r') as f:
            contents = f.read()

        root = ET.fromstring(contents)

        if root is None:
            print('Root is none')
            return None

        if root.tag != 'MeshApplicationData':
            print('Root.tag is none')
            return None

        appkeylist = []

        appkeylist_element = root.find("MeshAppKeyList")
        if appkeylist_element is not None:
            for appkey_element in appkeylist_element.iter("MeshAppKey"):
                if appkey_element is None:
                    print("appkey_element is none")
                    continue

                index = appkey_element.find("Index")
                if index is None:
                    print("index is none")
                    continue

                netindex = appkey_element.find("NetIndex")
                if netindex is None:
                    print("netindex is none")
                    continue

                appkey = appkey_element.find("AppKey")
                if appkey is None:
                    print("appkey is none")
                    continue

                appkeylist.append(AppKey(index.text, netindex.text, appkey.text))

        node = root.find("Node")
        if node is None:
            print('Node is none')
            return None

        devkey = node.find("DeviceKey")
        devkey_text = devkey.text if devkey is not None else None

        return AppData(appkeylist, devkey_text)
