# Exercise 2.0 - Updating the switch configurations using Ansible

Using Ansible you can update the configuration of switches either by pushing a configuration file to the device or you can push configuration lines directly to the device.

#### Step 1

Create a new file called `switch_configs.yml` (use either `vim` or `nano` on the jumphost to do this or use a local editor on your laptop and copy the contents to the jumphost later). Add the following play definition to it:


``` yaml
---
- name: SNMP RO/RW STRING CONFIGURATION
  hosts: arista
  gather_facts: no
  connection: network_cli

```

#### Step 2

Add a task to ensure that the SNMP strings `ansible-public` and `ansible-private` are present on all the switches. Use the `eos_config` module for this task

> Note: For help on the **eos_config** module, use the **ansible-doc eos_config** command from the command line or check docs.ansible.com. This will list all possible options with usage examples.


``` yaml

---
- name: SNMP RO/RW STRING CONFIGURATION
  hosts: arista
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      eos_config:
        commands:
          - snmp-server community ansible-public ro
          - snmp-server community ansible-private rw

```

#### Step 3

Run the playbook:

```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts switch_configs.yml

PLAY [SNMP RO/RW STRING CONFIGURATION] ************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *******************************************************************************
changed: [spine2]
changed: [leaf1]
changed: [spine1]
changed: [leaf3]
changed: [leaf2]
changed: [leaf4]
changed: [host1]
changed: [host2]

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=1    changed=1    unreachable=0    failed=0
host2                      : ok=1    changed=1    unreachable=0    failed=0
leaf1                      : ok=1    changed=1    unreachable=0    failed=0
leaf2                      : ok=1    changed=1    unreachable=0    failed=0
leaf3                      : ok=1    changed=1    unreachable=0    failed=0
leaf4                      : ok=1    changed=1    unreachable=0    failed=0
spine1                     : ok=1    changed=1    unreachable=0    failed=0
spine2                     : ok=1    changed=1    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

Feel free to log in and check the configuration update.


#### Step 4

The `eos_config` module is idempotent. This means, a configuration change is  pushed to the device if and only if that configuration does not exist on the end hosts. To validate this, go ahead and re-run the playbook:


```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts switch_configs.yml  

PLAY [SNMP RO/RW STRING CONFIGURATION] ************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *******************************************************************************
ok: [leaf3]
ok: [spine1]
ok: [leaf2]
ok: [spine2]
ok: [leaf1]
ok: [leaf4]
ok: [host1]
ok: [host2]

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=1    changed=0    unreachable=0    failed=0
host2                      : ok=1    changed=0    unreachable=0    failed=0
leaf1                      : ok=1    changed=0    unreachable=0    failed=0
leaf2                      : ok=1    changed=0    unreachable=0    failed=0
leaf3                      : ok=1    changed=0    unreachable=0    failed=0
leaf4                      : ok=1    changed=0    unreachable=0    failed=0
spine1                     : ok=1    changed=0    unreachable=0    failed=0
spine2                     : ok=1    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$



```

> Note: See that the **changed** parameter in the **PLAY RECAP** indicates 0 changes.


#### Step 5

Now update the task to add one more SNMP RO community string:


``` yaml
---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: arista
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      eos_config:
        commands:
          - snmp-server community ansible-public ro
          - snmp-server community ansible-private rw
          - snmp-server community ansible-test ro

```



#### Step 6

This time however, instead of running the playbook to push the change to the device, execute it using the `--check` flag in combination with the `-v` or verbose mode flag:


```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts switch_configs.yml  --check -v
Using /home/arista/ansible-training/ansible.cfg as config file

PLAY [SNMP RO/RW STRING CONFIGURATION] ************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *******************************************************************************
changed: [spine1] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1549398023", "updates": ["snmp-server community ansible-test ro"]}
changed: [leaf1] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1549398023", "updates": ["snmp-server community ansible-test ro"]}
changed: [leaf3] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1549398023", "updates": ["snmp-server community ansible-test ro"]}
changed: [leaf2] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1549398023", "updates": ["snmp-server community ansible-test ro"]}
changed: [spine2] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1549398023", "updates": ["snmp-server community ansible-test ro"]}
changed: [leaf4] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1549398027", "updates": ["snmp-server community ansible-test ro"]}
changed: [host1] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1549398027", "updates": ["snmp-server community ansible-test ro"]}
changed: [host2] => {"changed": true, "commands": ["snmp-server community ansible-test ro"], "session": "ansible_1549398027", "updates": ["snmp-server community ansible-test ro"]}

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=1    changed=1    unreachable=0    failed=0
host2                      : ok=1    changed=1    unreachable=0    failed=0
leaf1                      : ok=1    changed=1    unreachable=0    failed=0
leaf2                      : ok=1    changed=1    unreachable=0    failed=0
leaf3                      : ok=1    changed=1    unreachable=0    failed=0
leaf4                      : ok=1    changed=1    unreachable=0    failed=0
spine1                     : ok=1    changed=1    unreachable=0    failed=0
spine2                     : ok=1    changed=1    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

The `--check` mode in combination with the `-v` flag will display the exact changes that will be deployed to the end device without actually pushing the change. This is a great technique to validate the changes you are about to push to a device before pushing it.

> Go ahead and log into a couple of devices to validate that the change has not been pushed.


Also note that even though 3 commands are being sent to the device as part of the task, only the one command that is missing on the devices will be pushed.


#### Step 7

Finally re-run this playbook again without the `-v` or `--check` flag to push the changes.

```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts switch_configs.yml  

PLAY [SNMP RO/RW STRING CONFIGURATION] ************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *******************************************************************************
changed: [spine1]
changed: [leaf3]
changed: [leaf1]
changed: [spine2]
changed: [leaf2]
changed: [host1]
changed: [leaf4]
changed: [host2]

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=1    changed=1    unreachable=0    failed=0
host2                      : ok=1    changed=1    unreachable=0    failed=0
leaf1                      : ok=1    changed=1    unreachable=0    failed=0
leaf2                      : ok=1    changed=1    unreachable=0    failed=0
leaf3                      : ok=1    changed=1    unreachable=0    failed=0
leaf4                      : ok=1    changed=1    unreachable=0    failed=0
spine1                     : ok=1    changed=1    unreachable=0    failed=0
spine2                     : ok=1    changed=1    unreachable=0    failed=0

[arista@ansible ansible-training]$
```


#### Step 8

Rather than push individual lines of configuration, an entire configuration snippet can be pushed to the devices. Create a file called `general_switch.cfg` in the same directory as your playbook and add the following lines of configuration into it:

```
ip domain-name ansible.test

logging host 192.168.0.200

ntp server ansible-nettime prefer
ntp server 192.168.0.100

```


#### Step 9

Remember that a playbook contains a list of plays. Add a new play called `GENERAL ENVIRONMENT CONFIGS FOR EOS SWITCHES` to the `switch_configs.yml` playbook.

``` yaml

---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: arista
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      eos_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO


- name: GENERAL ENVIRONMENT CONFIGS FOR EOS SWITCHES
  hosts: arista
  gather_facts: no
  connection: network_cli



```

#### Step 10

Add a task to this new play to push the configurations in the `general_switch.cfg` file you created in **STEP 8**


``` yaml
---
- name: UPDATE THE SNMP RO/RW STRINGS
  hosts: arista
  gather_facts: no
  connection: network_cli

  tasks:

    - name: ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT
      eos_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO


- name: GENERAL ENVIRONMENT CONFIGS FOR EOS SWITCHES
  hosts: arista
  gather_facts: no
  connection: network_cli

  tasks:

    - name: PUSH GENERAL SWITCH CONFIGS
      eos_config:
        src: general_switch.cfg
```


#### Step 11

Go ahead and run the playbook.

```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts switch_configs.yml  

PLAY [SNMP RO/RW STRING CONFIGURATION] ************************************************************************************************

TASK [ENSURE THAT THE DESIRED SNMP STRINGS ARE PRESENT] *******************************************************************************
ok: [spine2]
ok: [leaf3]
ok: [spine1]
ok: [leaf2]
ok: [leaf1]
ok: [leaf4]
ok: [host1]
ok: [host2]

PLAY [GENERAL ENVIRONMENT CONFIGS FOR EOS SWITCHES] ***********************************************************************************

TASK [PUSH GENERAL SWITCH CONFIGS] ****************************************************************************************************
changed: [spine1]
changed: [spine2]
changed: [leaf1]
changed: [leaf3]
changed: [leaf2]
changed: [leaf4]
changed: [host1]
changed: [host2]

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=2    changed=1    unreachable=0    failed=0
host2                      : ok=2    changed=1    unreachable=0    failed=0
leaf1                      : ok=2    changed=1    unreachable=0    failed=0
leaf2                      : ok=2    changed=1    unreachable=0    failed=0
leaf3                      : ok=2    changed=1    unreachable=0    failed=0
leaf4                      : ok=2    changed=1    unreachable=0    failed=0
spine1                     : ok=2    changed=1    unreachable=0    failed=0
spine2                     : ok=2    changed=1    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

# Complete

You have completed lab exercise 2.0

---
