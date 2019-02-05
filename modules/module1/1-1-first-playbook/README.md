# Exercise 1.1 - Writing your first playbook

Now that you have a fundamental grasp of the inventory file and the group/host variables, this section will walk you through building a playbook.

> This section will help you understand the components of a playbook while giving you an immediate baseline for using it within your own production environment!

#### Step 1:

Using your favorite text editor (`vim` and `nano` are available on the control host) create a new file called `gather_eos_data.yml`.

>Alternately, you can create it using sublimetext or any GUI editor on your laptop and scp it over)


>Ansible playbooks are **YAML** files. YAML is a structured encoding format that is also extremely human readable (unlike it's subset - the JSON format)

#### Step 2:
```
[arista@ansible ansible-training]$ vim gather_eos_data.yml
```

Enter the following play definition into `gather_eos_data.yml`:

>Press the letter "i" to enter insert mode*

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no
```

`---` indicates that this is a YAML file. We are running this playbook against the group `arista`, that was defined earlier in the inventory file. Playbooks related to network devices should use the connection plugin called `network_cli`. Ansible has different connection plugins that handle different connection interfaces. The `network_cli` plugin is written specifically for network equipment and handles things like ensuring a persistent SSH connection across multiple tasks. We have previously defined the `network_cli` variable in our host/variable files so it is not mandatory in the playbook.


#### Step 3

Next, add the first `task`. This task will use the `eos_facts` module to gather facts about each device in the group `arista`.


``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:
```

>A play is a list of tasks. Modules are pre-written code that perform the task.



#### Step 4

Run the playbook - exit back into the command line of the control host and execute the following:

>Use the write/quit method in vim to save your playbook, i.e. Esc :wq!


```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts gather_eos_data.yml

```

The output should look as follows.

```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts gather_eos_data.yml

PLAY [GATHER INFORMATION FROM SWITCHES] ******************************************************************

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [spine1]
ok: [leaf3]
ok: [spine2]
ok: [leaf2]
ok: [leaf1]
ok: [leaf4]
ok: [host1]
ok: [host2]

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=3    changed=0    unreachable=0    failed=0
host2                      : ok=3    changed=0    unreachable=0    failed=0
leaf1                      : ok=3    changed=0    unreachable=0    failed=0
leaf2                      : ok=3    changed=0    unreachable=0    failed=0
leaf3                      : ok=3    changed=0    unreachable=0    failed=0
leaf4                      : ok=3    changed=0    unreachable=0    failed=0
spine1                     : ok=3    changed=0    unreachable=0    failed=0
spine2                     : ok=3    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$


```


#### Step 5


The play ran successfully and executed against the 8 switches. But where is the output?! Re-run the playbook using the `-v` flag.

> Note: Ansible has increasing level of verbosity. You can use up to 4 "v's", -vvvv.


```
arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts gather_eos_data.yml  -v
Using /home/arista/ansible-training/ansible.cfg as config file

PLAY [GATHER INFORMATION FROM SWITCHES] ******************************************************************

TASK [GATHER SWITCH FACTS] ******************************************************************************
ok: [spine1] => {"ansible_facts": {"ansible_net_all_ipv4_addresses": ["192.168.0.10"], "ansible_net_all_ipv6_addresses": [], "ansible_net_filesystems": ["file:", "flash:", "system:"], "ansible_net_fqdn": "spine1.arista.test", "ansible_net_gather_subset": ["hardware", "default", "interfaces"], "ansible_net_hostname": "spine1", "ansible_net_image": null, "ansible_net_interfaces": {"Ethernet1": {"bandwidth": 0, "description": "", "duplex": "duplexFull", "ipv4": {}, "lineprotocol": "up", "macaddress": "5e:f4:4c:c2:c5:92", "mtu": 9214, "operstatus": "connected", "type": "bridged"}, "Ethernet10": {"bandwidth": 0, "description": "", "duplex": "duplexFull", "ipv4": {}, "lineprotocol": "up", "macaddress": "3a:af:f4:e0:f7:e0", "mtu": 9214, "operstatus": "connected", "type": "bridged"}, "Ethernet11": {"bandwidth": 0, "description": "", "duplex": "duplexFull", "ipv4": {}, "lineprotocol": "up", "macaddress": "62:78:4b:c6:a3:4b", "mtu": 9214, "operstatus": "connected", "type": "bridged"}, "Management1": {"bandwidth": 0, "description": "", "duplex": "duplexUnknown", "ipv4": {"address": "192.168.0.10", "masklen": 24}, "lineprotocol": "notPresent", "macaddress": "16:04:97:ff:0d:a7", "mtu": 1500, "operstatus": "notconnect", "type": "routed"}}, "ansible_net_memfree_mb": 3117, "ansible_net_memtotal_mb": 3884, "ansible_net_model": "vEOS", "ansible_net_neighbors": {"Ethernet1": [{"host": "spine2.arista.test", "port": "Ethernet1"}], "Ethernet2": [{"host": "leaf1.arista.test", "port": "Ethernet2"}], "Ethernet3": [{"host": "leaf2.arista.test", "port": "Ethernet2"}], "Ethernet4": [{"host": "leaf3.arista.test", "port": "Ethernet2"}], "Ethernet5": [{"host": "leaf4.arista.test", "port": "Ethernet2"}]}, "ansible_net_serialnum": "spine1", "ansible_net_version": "4.21.2F"}, "changed": false}

.
.
.
.
.
<output truncated for readability>
```


> Note: The output returns key-value pairs that can then be used within the playbook for subsequent tasks. Also note that all variables that start with **ansible_** are automatically available for subsequent tasks within the play.


#### Step 6

Ansible allows you to limit the playbook execution to a subset of the devices declared in the group, against which the play is running against. This can be done using the `--limit` flag. Rerun the above task, limiting it first to `spine1` and then to both `spine1` and `leaf1`


```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts gather_eos_data.yml  -v --limit spine1
```


```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts gather_eos_data.yml  -v --limit spine1,leaf1

```





#### Step 7

Running a playbook in verbose mode is a good option to validate the output from a task. To work with the variables within a playbook you can use the `debug` module.

Write 2 tasks that display the switches' OS version and hostname.

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:

    - name: DISPLAY VERSION
      debug:
        msg: "The EOS version is: {{ ansible_net_version }}"

    - name: DISPLAY HOSTNAME
      debug:
        msg: "The hostname is: {{ ansible_net_hostname }}"
```


#### Step 8

Now re-run the playbook but this time do not use the `verbose` flag and run it against all hosts.

```

[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts gather_eos_data.yml

PLAY [GATHER INFORMATION FROM SWITCHES] ***********************************************************************************************

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [leaf2]
ok: [leaf1]
ok: [spine1]
ok: [leaf3]
ok: [spine2]
ok: [host1]
ok: [leaf4]
ok: [host2]

TASK [DISPLAY VERSION] ****************************************************************************************************************
ok: [spine1] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [spine2] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [leaf2] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [leaf1] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [leaf3] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [leaf4] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [host2] => {
    "msg": "The EOS version is: 4.21.2F"
}
ok: [host1] => {
    "msg": "The EOS version is: 4.21.2F"
}

TASK [DISPLAY HOSTNAME] ***************************************************************************************************************
ok: [spine2] => {
    "msg": "The hostname is:spine2"
}
ok: [spine1] => {
    "msg": "The hostname is:spine1"
}
ok: [leaf3] => {
    "msg": "The hostname is:leaf3"
}
ok: [leaf2] => {
    "msg": "The hostname is:leaf2"
}
ok: [leaf1] => {
    "msg": "The hostname is:leaf1"
}
ok: [host2] => {
    "msg": "The hostname is:host2"
}
ok: [leaf4] => {
    "msg": "The hostname is:leaf4"
}
ok: [host1] => {
    "msg": "The hostname is:host1"
}

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=3    changed=0    unreachable=0    failed=0
host2                      : ok=3    changed=0    unreachable=0    failed=0
leaf1                      : ok=3    changed=0    unreachable=0    failed=0
leaf2                      : ok=3    changed=0    unreachable=0    failed=0
leaf3                      : ok=3    changed=0    unreachable=0    failed=0
leaf4                      : ok=3    changed=0    unreachable=0    failed=0
spine1                     : ok=3    changed=0    unreachable=0    failed=0
spine2                     : ok=3    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$

```


Using less than 20 lines of "code" you have just automated version and hostname collection. Imagine if you were running this against your production network! You have actionable data in hand that does not go out of date.

# Complete

You have completed lab exercise 1.1

---
