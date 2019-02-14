# Exercise 6.0 - Dynamic Inventory with CVP


Ansible has the ability to dynamically populate its inventory using a Python script in place of an inventory file.

In this module we will develop a simple Python script to pull the inventory from CVP to be used as the hosts for executing a playbook.


#### Step 1


First we will need to determine our CVP IP address for our lab environment.

This can be found by clicking on CVP on the left side of your lab splash page. Take of note of the CVP address.


#### Step 2


We will also need to install a helpful python package for interacting with CVP via its API.

execute the following command:

``` shell
[arista@ansible ansible-training]$ sudo pip install cvprac
[sudo] password for arista:
The directory '/home/arista/.cache/pip/http' or its parent directory is not owned by the current user and the cache has been disabled. Please check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
The directory '/home/arista/.cache/pip' or its parent directory is not owned by the current user and caching wheels has been disabled. check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
Collecting cvprac
Requirement already satisfied: requests>=1.0.0 in /usr/local/lib/python2.7/dist-packages (from cvprac) (2.20.0)
Requirement already satisfied: urllib3<1.25,>=1.21.1 in /usr/local/lib/python2.7/dist-packages (from requests>=1.0.0->cvprac) (1.24)
Requirement already satisfied: chardet<3.1.0,>=3.0.2 in /usr/local/lib/python2.7/dist-packages (from requests>=1.0.0->cvprac) (3.0.4)
Requirement already satisfied: idna<2.8,>=2.5 in /usr/local/lib/python2.7/dist-packages (from requests>=1.0.0->cvprac) (2.7)
Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python2.7/dist-packages (from requests>=1.0.0->cvprac) (2018.10.15)
Installing collected packages: cvprac
Successfully installed cvprac-1.0.1
You are using pip version 18.1, however version 19.0.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```


#### Step 3


Now we will create a new file in the `inventory/` directory called `cvp_dynamic_inventory.py` and provide the following content:

``` Python
#!/usr/bin/python
# Ansible Dynamic Inventory Script with CVP

import json
import sys
from cvprac.cvp_client import CvpClient
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    client = CvpClient()
    client.connect(['<YOUR CVP IP ADDRESS>'], 'arista', 'arista')
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
```

This is a simple Python script that is first making a connection to CVP using the cvprac  CvpClient object. Then it is using the clients get_inventory() method and using it to create a list of the devices management ip addresses. This list is then formatted into a JSON string to resemble the inventory and printed to the screen before exiting.


#### Step 4


Run the script alone to see the output:

``` shell
[arista@ansible ansible-training]$ python inventory/cvp_dynamic_inventory.py
{
  "arista": {
    "hosts": [
      "192.168.0.10",
      "192.168.0.11",
      "192.168.0.44",
      "192.168.0.14",
      "192.168.0.16",
      "192.168.0.15",
      "192.168.0.17"
    ]
  }
}
```


#### Step 5


Now before we attempt to run an Ansible playbook using the script to populate the inventory we need to make sure Ansible is able to use it. Change the scripts permissions so that it can be run by any user. We will simply by change the permissions to 777 level.

``` shell
[arista@ansible ansible-training]$ chmod 777 inventory/cvp_dynamic_inventory.py
[arista@ansible ansible-training]$ ls -alrt inventory/cvp_dynamic_inventory.py
-rwxrwxrwx 1 arista arista 1185 Feb 14 04:48 inventory/cvp_dynamic_inventory.py
```


#### Step 6

Now let's try running playbook `gather_eos_data.yml.yml` from a previous lab.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/cvp_dynamic_inventory.py gather_eos_data.yml

PLAY [GATHER INFORMATION FROM SWITCHES] ***********************************************************************************************

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [192.168.0.44]
ok: [192.168.0.17]
ok: [192.168.0.16]
ok: [192.168.0.11]
ok: [192.168.0.15]
ok: [192.168.0.10]
ok: [192.168.0.14]

TASK [DISPLAY VERSION] ****************************************************************************************************************
ok: [192.168.0.15] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [192.168.0.11] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [192.168.0.16] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [192.168.0.44] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [192.168.0.17] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [192.168.0.14] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [192.168.0.10] => {
    "msg": "The EOS version is: 4.21.2F"
}

TASK [DISPLAY HOSTNAME] ***************************************************************************************************************
ok: [192.168.0.17] => {
    "msg": "The hostname is: leaf4"
}
ok: [192.168.0.16] => {
    "msg": "The hostname is: leaf3"
}
ok: [192.168.0.44] => {
    "msg": "The hostname is: cvx01"
}
ok: [192.168.0.11] => {
    "msg": "The hostname is: spine2"
}
ok: [192.168.0.15] => {
    "msg": "The hostname is: leaf2"
}
ok: [192.168.0.14] => {
    "msg": "The hostname is: leaf1"
}
ok: [192.168.0.10] => {
    "msg": "The hostname is: spine1"
}

TASK [COLLECT OUTPUT OF SHOW COMMANDS] ************************************************************************************************
ok: [192.168.0.16]
ok: [192.168.0.11]
ok: [192.168.0.15]
ok: [192.168.0.44]
ok: [192.168.0.17]
ok: [192.168.0.14]
ok: [192.168.0.10]

TASK [DISPLAY THE COMMAND OUTPUT] *****************************************************************************************************
ok: [192.168.0.11] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
            "hostname spine2",
            "Interface              IP Address         Status     Protocol         MTU\nManagement1            192.168.0.11/24    down       notpresent      1500"
        ],
        "stdout_lines": [
            [
                "hostname spine2"
            ],
            [
                "Interface              IP Address         Status     Protocol         MTU",
                "Management1            192.168.0.11/24    down       notpresent      1500"
            ]
        ]
    }
}
ok: [192.168.0.15] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
            "hostname leaf2",
            "Interface              IP Address         Status     Protocol         MTU\nManagement1            192.168.0.15/24    down       notpresent      1500"
        ],
        "stdout_lines": [
            [
                "hostname leaf2"
            ],
            [
                "Interface              IP Address         Status     Protocol         MTU",
                "Management1            192.168.0.15/24    down       notpresent      1500"
            ]
        ]
    }
}
ok: [192.168.0.17] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
            "hostname leaf4",
            "Interface              IP Address         Status     Protocol         MTU\nManagement1            192.168.0.17/24    down       notpresent      1500"
        ],
        "stdout_lines": [
            [
                "hostname leaf4"
            ],
            [
                "Interface              IP Address         Status     Protocol         MTU",
                "Management1            192.168.0.17/24    down       notpresent      1500"
            ]
        ]
    }
}
ok: [192.168.0.16] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
            "hostname leaf3",
            "Interface              IP Address         Status     Protocol         MTU\nManagement1            192.168.0.16/24    down       notpresent      1500"
        ],
        "stdout_lines": [
            [
                "hostname leaf3"
            ],
            [
                "Interface              IP Address         Status     Protocol         MTU",
                "Management1            192.168.0.16/24    down       notpresent      1500"
            ]
        ]
    }
}
ok: [192.168.0.44] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
            "hostname cvx01",
            "Interface              IP Address         Status     Protocol         MTU\nManagement1            192.168.0.44/24    down       notpresent      1500"
        ],
        "stdout_lines": [
            [
                "hostname cvx01"
            ],
            [
                "Interface              IP Address         Status     Protocol         MTU",
                "Management1            192.168.0.44/24    down       notpresent      1500"
            ]
        ]
    }
}
ok: [192.168.0.10] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
            "hostname spine1",
            "Interface              IP Address         Status     Protocol         MTU\nManagement1            192.168.0.10/24    down       notpresent      1500"
        ],
        "stdout_lines": [
            [
                "hostname spine1"
            ],
            [
                "Interface              IP Address         Status     Protocol         MTU",
                "Management1            192.168.0.10/24    down       notpresent      1500"
            ]
        ]
    }
}
ok: [192.168.0.14] => {
    "show_output": {
        "changed": false,
        "failed": false,
        "stdout": [
            "hostname leaf1",
            "Interface              IP Address         Status     Protocol         MTU\nManagement1            192.168.0.14/24    down       notpresent      1500"
        ],
        "stdout_lines": [
            [
                "hostname leaf1"
            ],
            [
                "Interface              IP Address         Status     Protocol         MTU",
                "Management1            192.168.0.14/24    down       notpresent      1500"
            ]
        ]
    }
}

TASK [DISPLAY THE HOSTNAME AGAIN] *****************************************************************************************************
ok: [192.168.0.17] => {
    "msg": "The hostname is hostname leaf4"
}
ok: [192.168.0.15] => {
    "msg": "The hostname is hostname leaf2"
}
ok: [192.168.0.16] => {
    "msg": "The hostname is hostname leaf3"
}
ok: [192.168.0.11] => {
    "msg": "The hostname is hostname spine2"
}
ok: [192.168.0.44] => {
    "msg": "The hostname is hostname cvx01"
}
ok: [192.168.0.14] => {
    "msg": "The hostname is hostname leaf1"
}
ok: [192.168.0.10] => {
    "msg": "The hostname is hostname spine1"
}

PLAY RECAP ****************************************************************************************************************************
192.168.0.10               : ok=6    changed=0    unreachable=0    failed=0
192.168.0.11               : ok=6    changed=0    unreachable=0    failed=0
192.168.0.14               : ok=6    changed=0    unreachable=0    failed=0
192.168.0.15               : ok=6    changed=0    unreachable=0    failed=0
192.168.0.16               : ok=6    changed=0    unreachable=0    failed=0
192.168.0.17               : ok=6    changed=0    unreachable=0    failed=0
192.168.0.44               : ok=6    changed=0    unreachable=0    failed=0
```

Simple as that we have used CVP to populate a dynamic inventory to execute our Ansible playbook against. If we were to add additional Arista devices to the inventory of CVP and rerun the ansible-playbook command, it would find these additional devices and run the plays/tasks against them as well.


# Complete

You have completed lab exercise 6.0

---
