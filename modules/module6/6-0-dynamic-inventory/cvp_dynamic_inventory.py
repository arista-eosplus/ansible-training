#!/usr/bin/python
# Ansible Dynamic Inventory Script with CVP

import json
import sys
from cvprac.cvp_client import CvpClient
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    client = CvpClient()
    client.connect(['52.53.222.131'], 'arista', 'arista')
    inventory = client.api.get_inventory()
    all_hosts = []
    for dev in inventory:
        all_hosts.append(dev['ipAddress'])
    formatted_inventory = dict(arista=dict(hosts=all_hosts))
    output = json.dumps(formatted_inventory, indent=2)
    print output
    sys.exit(0)



if __name__ == '__main__':
    main()
