#!/usr/bin/python
import os
import sys
import time

import winreg
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from app_data import AppData
from network_data import NetworkData


def prepare_mesh_options(net_data, app_data):
    lines = []
    lines.append("[mesh]")
    lines.append("")
    lines.append("{IVindex}")
    if not net_data.iv_index:
        lines.append('0'*8)
    lines.append("{0}".format(net_data.iv_index))
    lines.append("")
    lines.append("{NetKey}")
    if not net_data.network_key:
        lines.append('0'*32)
    lines.append("{0}".format(net_data.network_key))
    lines.append("")
    lines.append("{AppKey}")
    if not app_data.app_keys:
        lines.append('0'*32)
    for appkey in app_data.app_keys:
        lines.append("{0}".format(appkey.appkey))
    lines.append("")
    lines.append("{DevKey}")
    if not app_data.dev_key:
        lines.append('0'*32)
    lines.append("{0}".format(app_data.dev_key))
    lines.append("")

    return "\n".join(lines)


def file_modified():
    network_data = NetworkData.parse(os.path.join(mesh_keys_path, network_file))
    print(network_data)

    app_data = AppData.parse(os.path.join(mesh_keys_path, app_file))
    print(app_data)

    mesh_options_text = prepare_mesh_options(network_data, app_data)
    print(mesh_options_text)

    with open(os.path.join(my_decoders_path, mesh_options_filename), "w") as f:
        f.write(mesh_options_text)


class MeshKeysFileEventHandler(PatternMatchingEventHandler):

    def __init__(self, patterns=None, ignore_patterns=None,
                 ignore_directories=False, case_sensitive=False):
        super(MeshKeysFileEventHandler, self).__init__(patterns, ignore_patterns,
                                                       ignore_directories, case_sensitive)

    def on_modified(self, event):
        print("{} modified!".format(event.src_path))
        file_modified()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Specify path to workspace!")
        exit(1)

    mesh_keys_path = os.path.expanduser(sys.argv[1])
    network_file = 'mesh_network_data.txt'
    app_file = 'mesh_app_data.txt'
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Frontline Test Equipment\User Data')
    my_decoders_path = winreg.QueryValueEx(key, "My Decoders")[0]
    mesh_options_filename = 'MeshOptions.ini'

    file_modified()

    mesh_keys_file_event_handler = MeshKeysFileEventHandler(patterns=[os.path.join(mesh_keys_path, network_file),
                                                                      os.path.join(mesh_keys_path, app_file)])
    observer = Observer()
    observer.schedule(mesh_keys_file_event_handler, path=mesh_keys_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
