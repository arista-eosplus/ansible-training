# Exercise 3.1 - Building dynamic documentation using the command parser

Most CLI based network devices support `show` commands. The output of the commands are "pretty" formatted, in the sense that they are very human readable. However, in the context of automation, where the objective is for a machine(code) to interpret this output, it needs to be transformed into "structured" data. In other words data-types that the code/machine can interpret and navigate. Examples would be lists, dictionaries, arrays and so on.

The Ansible [network-engine](https://github.com/ansible-network/network-engine) is a [role](https://docs.ansible.com/ansible/2.5/user_guide/playbooks_reuse_roles.html) that supports 2 such "translators" - `command_parser` and `textfsm_parser`. These are modules built into the `network-engine` role that takes a raw text input (pretty formatted) and converts it into structured data. You will work with each of these to generate dynamic reports in the following sections:


# Unstructured command output from network devices

Here is how the output of a `show interfaces` command looks like on a Arista EOS device:

``` shell
spine1#show interfaces
Ethernet1 is up, line protocol is up (connected)
  Hardware is Ethernet, address is aeca.6e66.78e8 (bia aeca.6e66.78e8)
  Ethernet MTU 9214 bytes
  Full-duplex, Unconfigured, auto negotiation: off, uni-link: n/a
  Up 1 hour, 8 minutes, 40 seconds
  Loopback Mode : None
  1 link status changes since last clear
  Last clearing of "show interface" counters never
  5 minutes input rate 0 bps (- with framing overhead), 0 packets/sec
  5 minutes output rate 0 bps (- with framing overhead), 0 packets/sec
     174 packets input, 29864 bytes
     Received 0 broadcasts, 174 multicast
     0 runts, 0 giants
     0 input errors, 0 CRC, 0 alignment, 0 symbol, 0 input discards
     0 PAUSE input
     2220 packets output, 281522 bytes
     Sent 0 broadcasts, 2220 multicast
     0 output errors, 0 collisions
     0 late collision, 0 deferred, 0 output discards
     0 PAUSE output
Ethernet2 is up, line protocol is up (connected)
  Hardware is Ethernet, address is 722f.201a.45b4 (bia 722f.201a.45b4)
  Ethernet MTU 9214 bytes
  Full-duplex, Unconfigured, auto negotiation: off, uni-link: n/a
  Up 1 hour, 8 minutes, 40 seconds
  Loopback Mode : None
  1 link status changes since last clear
.
.
.
.
.
<output omitted for brevity>
```


Let's say your task is to prepare a list of interfaces that are currently **up**, the MTU setting, the type and description on the interface. You could log into each device, execute the above command and collect this information. Now imagine if you had to repeat this for 150 devices in your network. That would require a lot of time on a relatively boring task!

In this lab, we will learn how to automate this exact scenario using Ansible.

#### Step 1

Start by creating a new playbook called `interface_report.yml` and add the following play definition:

``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: arista
  gather_facts: no
  connection: network_cli


```

#### Step 2

Next add the `ansible-network.network-engine` role into the playbook. Roles are nothing but a higher level playbook abstraction. Think of them as pre-written playbooks that handle repeated, specific tasks. For this we will need to first install the role. Execute the following command on the control node to install this role:

``` bash
[arista@ansible ansible-training]$ ansible-galaxy install ansible-network.network-engine
- downloading role 'network-engine', owned by ansible-network
- downloading role from https://github.com/ansible-network/network-engine/archive/v2.7.3.tar.gz
- extracting ansible-network.network-engine to /home/arista/.ansible/roles/ansible-network.network-engine
- ansible-network.network-engine (v2.7.3) was installed successfully
[arista@ansible ansible-training]$

```

The `ansible-network.network-engine` role specifically makes available the `command_parser` module, among other things, which you can then use in subsequent tasks inside your own playbook.


``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: arista
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine
```


#### Step 3

Now we can begin adding our tasks. Add the first task to run the `show interfaces` command against all the switches and register the output into a variable.



``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: arista
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      eos_command:
        commands:
          - show interfaces
      register: output



```
> Feel free to run this playbook in verbose mode to view the output returned from the devices.

#### Step 4

The next task is to send the raw data returned in the previous task to the `command_parser` module. This module takes the raw content as one of the inputs along with the name of the parser file.

> Note: The parser file is a YAML file that has a similar structure to Ansible playbooks.


Add this to your playbook:


``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: arista
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      eos_command:
        commands:
          - show interfaces
      register: output

    - name: PARSE THE RAW OUTPUT
      command_parser:
        file: "parsers/show_interfaces.yaml"
        content: "{{ output.stdout[0] }}"

```

Let's understand this task in a little more depth. The `command_parser` is referencing a file called `show_interfaces.yaml` within the `parsers` directory. For this lab, the parser has been pre-populated for you. The parsers are written to handle the output from standard show commands on various network platforms.


> More parsers are being made available in the public domain so you will only have to build them if a specific use case has not been handled.

Feel free to view the contents of the parser file. You will notice how it uses regular expressions to capture relevant data from the show command and return it as a variable called `interface_facts`



#### Step 5

Add a new task to view the contents being returned by the `command_parser`

``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: arista
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      eos_command:
        commands:
          - show interfaces
      register: output

    - name: PARSE THE RAW OUTPUT
      command_parser:
        file: "parsers/show_interfaces.yaml"
        content: "{{ output.stdout[0] }}"

    - name: DISPLAY THE PARSED DATA
      debug:
        var: interface_facts
```


#### Step 6

Go ahead and run this playbook. Since our objective is to simply view the returned data, limit your playbook run to a single switch.


``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts interface_report.yml --limit spine1

PLAY [GENERATE INTERFACE REPORT] ******************************************************************************************************

TASK [CAPTURE SHOW INTERFACES] ********************************************************************************************************
ok: [spine1]

TASK [PARSE THE RAW OUTPUT] ***********************************************************************************************************
ok: [spine1]

TASK [DISPLAY THE PARSED DATA] ********************************************************************************************************
ok: [spine1] => {
    "interface_facts": [
        {
            "Ethernet1": {
                "config": {
                    "description": null,
                    "mtu": "9214",
                    "name": "Ethernet1",
                    "type": "Ethernet,"
                }
            }
        },
        {
            "Ethernet2": {
                "config": {
                    "description": null,
                    "mtu": "9214",
                    "name": "Ethernet2",
                    "type": "Ethernet,"
                }
            }
        },
        {
            "Ethernet3": {
                "config": {
                    "description": null,
                    "mtu": "9214",
                    "name": "Ethernet3",
                    "type": "Ethernet,"
                }
            }
        },
        {
            "Ethernet4": {
                "config": {
                    "description": null,
                    "mtu": "9214",
                    "name": "Ethernet4",
                    "type": "Ethernet,"
                }
            }
        },
        .
        .
        .
        .
        .
        <output omitted for brevity>
    ]
}

PLAY RECAP ****************************************************************************************************************************
spine1                     : ok=3    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$
```


How cool is that! Your playbook now converted all that raw text output into structured data: a list of dictionaries where each dictionary describes the elements you need to build your report.









#### Step 7
Next create a directory to hold the per device report:

``` shell

[arista@ansible ansible-training]$ mkdir intf_reports
[arista@ansible ansible-training]$

```

#### Step 8
Our next step is to use the template module to generate a report from the above data. Use the same technique you learned in the previous lab to generate the reports per device and then consolidate them using the assemble module.


``` yaml
---
- name: GENERATE INTERFACE REPORT
  hosts: arista
  gather_facts: no
  connection: network_cli

  roles:
    - ansible-network.network-engine

  tasks:
    - name: CAPTURE SHOW INTERFACES
      eos_command:
        commands:
          - show interfaces
      register: output

    - name: PARSE THE RAW OUTPUT
      command_parser:
        file: "parsers/show_interfaces.yaml"
        content: "{{ output.stdout[0] }}"

    #- name: DISPLAY THE PARSED DATA
    #  debug:
    #    var: interface_facts

    - name: GENERATE REPORT FRAGMENTS
      template:
        src: interface_facts.j2
        dest: intf_reports/{{inventory_hostname}}_intf_report.md

    - name: GENERATE A CONSOLIDATED REPORT
      assemble:
        src: intf_reports/
        dest: interfaces_report.md
      delegate_to: localhost
      run_once: yes

```

> Note: For this lab the Jinja2 template has been pre-populated for you. Feel free to look at the file **interface_facts.j2** in the **templates** directory.

> Note: The debug task has been commented out so that display is concise

#### Step 9

Run the playbook:



``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts interface_report.yml

PLAY [GENERATE INTERFACE REPORT] ******************************************************************************************************

TASK [CAPTURE SHOW INTERFACES] ********************************************************************************************************
ok: [leaf2]
ok: [leaf4]
ok: [spine1]
ok: [leaf1]
ok: [leaf3]
ok: [spine2]
ok: [host1]
ok: [host2]

TASK [PARSE THE RAW OUTPUT] ***********************************************************************************************************
ok: [leaf4]
ok: [spine1]
ok: [leaf3]
ok: [leaf1]
ok: [leaf2]
ok: [spine2]
ok: [host2]
ok: [host1]

TASK [GENERATE REPORT FRAGMENTS] ******************************************************************************************************
changed: [leaf4]
changed: [leaf2]
changed: [leaf3]
changed: [spine1]
changed: [leaf1]
changed: [host2]
changed: [host1]
changed: [spine2]

TASK [GENERATE A CONSOLIDATED REPORT] *************************************************************************************************
changed: [leaf1 -> localhost]

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=3    changed=1    unreachable=0    failed=0
host2                      : ok=3    changed=1    unreachable=0    failed=0
leaf1                      : ok=4    changed=2    unreachable=0    failed=0
leaf2                      : ok=3    changed=1    unreachable=0    failed=0
leaf3                      : ok=3    changed=1    unreachable=0    failed=0
leaf4                      : ok=3    changed=1    unreachable=0    failed=0
spine1                     : ok=3    changed=1    unreachable=0    failed=0
spine2                     : ok=3    changed=1    unreachable=0    failed=0

[arista@ansible ansible-training]$

```


#### Step 10


Use the `cat` command to view the contents of the final report:


``` shell
[arista@ansible ansible-training]$ cat interfaces_report.md
SPINE1
-----
Ethernet1:
  Description:
  Name: Ethernet1
  MTU: 9214

Ethernet2:
  Description:
  Name: Ethernet2
  MTU: 9214

Ethernet3:
  Description:
  Name: Ethernet3
  MTU: 9214

Ethernet4:
  Description:
  Name: Ethernet4
  MTU: 9214
.
.
.
.
.
<output omitted for brevity>

SPINE2
-----
Ethernet1:
  Description:
  Name: Ethernet1
  MTU: 9214

Ethernet2:
  Description:
  Name: Ethernet2
  MTU: 9214

Ethernet3:
  Description:
  Name: Ethernet3
  MTU: 9214

Ethernet4:
  Description:
  Name: Ethernet4
  MTU: 9214
.
.
.
.
.
<output omitted for brevity>
```

# Complete

You have completed lab exercise 3.1

---
