# This Python file uses the following encoding: utf-8

import json
import requests
import phue
import os

from PySide2.QtCore import QObject
from PySide2.QtCore import Slot
from PySide2.QtCore import QStandardPaths


class AppConfig(QObject):
    config_file = os.path.join(
        QStandardPaths.writableLocation(QStandardPaths.ConfigLocation),
        'candela.json')

    paired_bridges = []
    reachable_bridges = []
    all_bridges = []

    def __init__(self, parent=None):
        super(AppConfig, self).__init__(parent)
        print()
              
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as cfg:
                print("Configuration file found")
                try:
                    config = json.load(cfg)
                except:
                    print('Corrupted configuration')
                    config = []
        else:
            config = []

        if len(config) > 0:
            for bridge in config:
                if 'ip' in bridge and 'user' in bridge:
                    self.paired_bridges.append({
                        'ip':   bridge['ip'],
                        'user': bridge['user']
                        })

        self.detect_bridges()

    def detect_bridges(self):
        # Populate reachable_bridges with default values
        self.reachable_bridges = []

        for bridge in self.paired_bridges:
            self.reachable_bridges.append({
                'ip': bridge['ip'],
                'user': bridge['user'],
                'in_reach': False,
                'accepted': False
                })

        # Detect which bridges are in reach and paired to
        discovered_bridges = requests.get('https://discovery.meethue.com/').json()
        self.all_bridges = []

        for remote_bridge in discovered_bridges:
            current_bridge = {'ip': remote_bridge['internalipaddress']}
            configured = False
            user = ''

            for known_bridge in self.reachable_bridges:
                if known_bridge['ip'] == remote_bridge['internalipaddress']:
                    # In reach bridge
                    known_bridge['in_reach'] = True

                    # Attempt to connect
                    try:
                        bridge = phue.Bridge(
                            known_bridge['ip'],
                            known_bridge['user'])
                    except phue.PhueRegistrationException:
                        # Connection failed
                        known_bridge['accepted'] = False
                        continue

                    # Connection success, add it to the known configured bridge
                    known_bridge['accepted'] = True
                    configured = True
                    user = known_bridge['user']
                else:
                    # Configured out of reach bridge
                    # Sanity, not necessary, just in case
                    known_bridge['in_reach'] = False
                    known_bridge['accepted'] = False
                    configured = True

            current_bridge['configured'] = configured
            current_bridge['user'] = user

            self.all_bridges.append(current_bridge)

    @Slot(str, str)
    def add_bridge(self, ip, user):
        self.paired_bridges.append({
            'ip': ip,
            'user': user
            })

        self.save()

        # Update paired and reachable bridges
        self.detect_bridges()

    @Slot(str)
    @Slot(str, str)
    def remove_bridge(self, ip, user=None):
        temp_bridges = []

        for b in self.paired_bridges:
            if ip != b['ip']:
                temp_bridges.append(b)
            elif user is not None and user != b['user']:
                temp_bridges.append(b)

        self.paired_bridges = temp_bridges
        self.detect_bridges()

    def save(self):
        with open(self.config_file, 'w') as cfg:
            json.dump(self.paired_bridges, cfg)
