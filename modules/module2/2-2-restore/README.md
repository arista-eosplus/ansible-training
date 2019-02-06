# Exercise 2.2 - Using Ansible to restore the backed up configuration


In the previous lab you learned how to backup the configuration of the 8 Arista switches. In this lab you will learn how to restore the configuration. The backups had been saved into a local directory called `backup`.


``` shell
backup
total 72
-rw-rw-r-- 1 arista arista 2311 Feb  6 01:46 host1.config
-rw-rw-r-- 1 arista arista 2457 Feb  6 01:45 host1_config.2019-02-06@01:45:55
-rw-rw-r-- 1 arista arista 2162 Feb  6 01:46 host2.config
-rw-rw-r-- 1 arista arista 2308 Feb  6 01:45 host2_config.2019-02-06@01:45:55
-rw-rw-r-- 1 arista arista 2164 Feb  6 01:46 leaf1.config
-rw-rw-r-- 1 arista arista 2310 Feb  6 01:45 leaf1_config.2019-02-06@01:45:52
-rw-rw-r-- 1 arista arista 2164 Feb  6 01:46 leaf2.config
-rw-rw-r-- 1 arista arista 2310 Feb  6 01:45 leaf2_config.2019-02-06@01:45:52
-rw-rw-r-- 1 arista arista 2164 Feb  6 01:46 leaf3.config
-rw-rw-r-- 1 arista arista 2310 Feb  6 01:45 leaf3_config.2019-02-06@01:45:52
-rw-rw-r-- 1 arista arista 2164 Feb  6 01:46 leaf4.config
-rw-rw-r-- 1 arista arista 2310 Feb  6 01:45 leaf4_config.2019-02-06@01:45:55
-rw-rw-r-- 1 arista arista 2166 Feb  6 01:46 spine1.config
-rw-rw-r-- 1 arista arista 2312 Feb  6 01:45 spine1_config.2019-02-06@01:45:52
-rw-rw-r-- 1 arista arista 2166 Feb  6 01:46 spine2.config
-rw-rw-r-- 1 arista arista 2312 Feb  6 01:45 spine2_config.2019-02-06@01:45:52

```


Our objective is to apply this "last known good configuration backup" to the switches.

#### Step 1


On one of the switches (`spine1`) manually make a change. For instance add a new loopback interface.

Log into `spine1` using the `ssh arista@192.168.0.10` command and add the following:

```
spine1#config
spine1(config)#interface loopback 101
spine1(config-if-Lo101)#ip address 169.1.1.1 255.255.255.255
spine1(config-if-Lo101)#end
spine1#

```

Now verify the newly created Loopback Interface

```
spine1#sh run interface loopback 101
interface Loopback101
   ip address 169.1.1.1/32
spine1#

```
#### Step 2

Step 1 simulates our "Out of process/band" changes on the network. This change needs to be reverted. So let's write a new playbook to apply the backup we collected from our previous lab to achieve this.

Create a file called `restore_config.yml` using your favorite text editor and add the following play definition:

``` yaml
---
- name: RESTORE CONFIGURATION
  hosts: arista
  connection: network_cli
  gather_facts: no

```


#### Step 3

Write the task to copy over the previously backed up configuration file to the switches. To do this we will need the Management1 IP address from the switch. Create a task to gather the devices facts so we can reference the Management IP for the SCP command. Lets also add a conditional to only copy the config for switches that are not in the hosts group.

``` yaml
---
- name: RESTORE CONFIGURATION
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:

    - name: COPY RUNNING CONFIG TO SWITCH
      command: scp ./backup/{{inventory_hostname}}.config  arista@{{ansible_net_interfaces.Management1.ipv4.address}}:/mnt/flash/{{inventory_hostname}}.config
      when: "'hosts' not in group_names"

```

> Note the use of the **inventory_hostname** variable and the **ansible_net_interfaces.Management1.ipv4.address** variable from the gathered `eos_facts` command. For each device in the inventory file under the arista group, this task will secure copy (scp) over the file that corresponds to the device name onto the flash: of the devices.


#### Step 4

Go ahead and run the playbook.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts restore_config.yml

PLAY [RESTORE CONFIGURATION] **********************************************************************************************************

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [leaf3]
ok: [spine1]
ok: [spine2]
ok: [leaf1]
ok: [leaf2]
ok: [leaf4]
ok: [host1]
ok: [host2]

TASK [COPY RUNNING CONFIG TO SWITCH] **************************************************************************************************
changed: [leaf1]
changed: [spine2]
changed: [leaf2]
changed: [spine1]
skipping: [host1]
changed: [leaf3]
skipping: [host2]
changed: [leaf4]

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=1    changed=0    unreachable=0    failed=0
host2                      : ok=1    changed=0    unreachable=0    failed=0
leaf1                      : ok=2    changed=1    unreachable=0    failed=0
leaf2                      : ok=2    changed=1    unreachable=0    failed=0
leaf3                      : ok=2    changed=1    unreachable=0    failed=0
leaf4                      : ok=2    changed=1    unreachable=0    failed=0
spine1                     : ok=2    changed=1    unreachable=0    failed=0
spine2                     : ok=2    changed=1    unreachable=0    failed=0

[arista@ansible ansible-training]$



```


#### Step 5

Log into the switches to check that the file has been copied over

> Note **spine1.config** at the bottom of the flash:/ directory

```
[arista@ansible ansible-training]$ ssh arista@192.168.0.10

spine1#dir
Directory of flash:/

       -rw-          77            Feb 6 00:44  SsuRestore.log
       -rw-         801           Jan 15 18:48  awsdhclientscript
       drwx        4096            Feb 6 00:45  debug
       -rwx         971           Jan 15 18:48  dhcpintf
       -rwx      268444           Jan 15 18:48  dropbear
       -rwx         917           Jan 15 18:48  eosdhclientscript
       -rw-          12           Jan 15 18:59  imm.1547578781.92
       -rw-          12           Jan 15 19:04  imm.1547579045.06
       -rw-          12            Feb 4 16:01  imm.1549296099.61
       -rw-          12            Feb 5 14:04  imm.1549375446.21
       -rw-          12            Feb 6 00:44  imm.1549413847.44
       -rw-         391            Feb 6 00:43  key.pub
       drwx        4096           Jan 15 18:48  non-vxlan
       -rw-      140952            Feb 6 00:45  ovs.db
       -rw-      441182           Jan 15 18:48  ovs.db.100
       -rw-      105063           Jan 15 18:48  ovs.db.32
       -rw-       33882           Jan 15 18:48  ovs.db.8
       drwx        4096            Feb 6 01:06  persist
       drwx        4096            Feb 4 16:05  schedule
       -rw-        2166            Feb 6 02:29  spine1.config
       -rw-        2140            Feb 5 19:46  startup-config
       -rw-          49            Feb 4 16:03  veos-config
       -rwx        1716            Feb 4 16:03  vxlan_config
       -rw-           0            Feb 4 16:04  vxlan_config_success

4159373312 bytes total (2066505728 bytes free)
spine1#

```




#### Step 6

Now that the known good configuration is on the destination devices, add a new task to the playbook to replace the running configuration with the one we copied over. Add the same conditional to skip devices in the group hosts.



``` yaml
---
- name: RESTORE CONFIGURATION
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:

    - name: COPY RUNNING CONFIG TO SWITCH
      command: scp ./backup/{{inventory_hostname}}.config  arista@{{ansible_net_interfaces.Management1.ipv4.address}}:/mnt/flash/{{inventory_hostname}}.config
      when: "'hosts' not in group_names"

    - name: CONFIG REPLACE
      eos_command:
        commands:
          - config replace flash:{{inventory_hostname}}.config force
      when: "'hosts' not in group_names"

```


#### Step 7

Let's run the updated playbook:

``` shell

[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts restore_config.yml

PLAY [RESTORE CONFIGURATION] **********************************************************************************************************

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [leaf1]
ok: [spine1]
ok: [leaf2]
ok: [leaf3]
ok: [spine2]
ok: [leaf4]
ok: [host1]
ok: [host2]

TASK [COPY RUNNING CONFIG TO SWITCH] **************************************************************************************************
changed: [leaf1]
changed: [spine2]
skipping: [host1]
skipping: [host2]
changed: [leaf3]
changed: [spine1]
changed: [leaf2]
changed: [leaf4]

TASK [CONFIG REPLACE] *****************************************************************************************************************
ok: [leaf1]
ok: [leaf3]
skipping: [host1]
skipping: [host2]
ok: [spine1]
ok: [spine2]
ok: [leaf2]
ok: [leaf4]

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=1    changed=0    unreachable=0    failed=0
host2                      : ok=1    changed=0    unreachable=0    failed=0
leaf1                      : ok=3    changed=1    unreachable=0    failed=0
leaf2                      : ok=3    changed=1    unreachable=0    failed=0
leaf3                      : ok=3    changed=1    unreachable=0    failed=0
leaf4                      : ok=3    changed=1    unreachable=0    failed=0
spine1                     : ok=3    changed=1    unreachable=0    failed=0
spine2                     : ok=3    changed=1    unreachable=0    failed=0

[arista@ansible ansible-training]$


```


#### Step 8



Validate that the new loopback interface we added in **Step 1**  is no longer on the device.


```
[arista@ansible ansible-training]$ ssh arista@192.168.0.10



spine1#sh ip int br
Interface              IP Address         Status     Protocol         MTU
Management1            192.168.0.10/24    down       notpresent      1500
spine1#
spine1#sh run interfaces Loopback 101
spine1#

```

The output above shows that the Loopback 101 interface is no longer present, you have successfully backed up and restored configurations on your Arista switches!

# Complete

You have completed lab exercise 2.2

---
