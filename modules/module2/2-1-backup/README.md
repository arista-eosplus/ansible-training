# Exercise 2.1 - Backing up the switch configuration


In this realistic scenario,  you will create a playbook to back-up Arista switch configurations. In subsequent labs we will use this backed up configuration, to restore devices to their known good state.

> Note: Since this is a common day 2 operation for most network teams, you can pretty much re-use most of this content for your environment with minimum changes.

#### Step 1

Create a new file called `backup.yml` using your favorite text editor and add the following play definition:

``` yaml
---
- name: BACKUP SWITCH CONFIGURATIONS
  hosts: arista
  connection: network_cli
  gather_facts: no

```

#### Step 2

Use the `eos_config` Ansible module to write a new task. This task should back up the configuration of all devices defined in `arista` group.

The `backup` parameter automatically creates a directory called `backup` within the playbook root and saves a time-stamped backup of the running configuration.

> Note: Use **ansible-doc eos_config** or check out **docs.ansible.com** for help on the module usage.


``` yaml
---
- name: BACKUP SWITCH CONFIGURATIONS
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      eos_config:
        backup: yes
      register: config_output
```


Why are we capturing the output of this task into a variable called `config_output`? **Step 5** will reveal this.


#### Step 3

Go ahead and run the playbook:

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts backup.yml

PLAY [BACKUP SWITCH CONFIGURATIONS] ***************************************************************************************************

TASK [BACKUP THE CONFIG] **************************************************************************************************************
ok: [spine2]
ok: [leaf2]
ok: [leaf3]
ok: [spine1]
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


#### Step 4

The playbook should now have created a directory called `backup`. Now, list the contents of this directory:


``` shell
[arista@ansible ansible-training]$ ls -l backup
total 32
-rw-rw-r-- 1 arista arista 2457 Feb  5 20:43 host1_config.2019-02-05@20:43:05
-rw-rw-r-- 1 arista arista 2308 Feb  5 20:43 host2_config.2019-02-05@20:43:08
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:43 leaf1_config.2019-02-05@20:43:02
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:43 leaf2_config.2019-02-05@20:43:02
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:43 leaf3_config.2019-02-05@20:43:02
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:43 leaf4_config.2019-02-05@20:43:05
-rw-rw-r-- 1 arista arista 2312 Feb  5 20:43 spine1_config.2019-02-05@20:43:02
-rw-rw-r-- 1 arista arista 2312 Feb  5 20:43 spine2_config.2019-02-05@20:43:02
[arista@ansible ansible-training]$

```

Feel free to open up these files using a text editor (`vim` & `nano` work as well) to validate their content.

#### Step 5

Since we will be using the backed up configurations as a source to restore the configuration. Let's rename them to reflect the device name.

In **Step 2** you captured the output of the task into a variable called `config_output`. This variable contains the name of the backup file. Use the `copy` Ansible module to make a copy of this file.



``` yaml
---
- name: BACKUP SWITCH CONFIGURATIONS
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      eos_config:
        backup: yes
      register: config_output

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"
```


#### Step 6

Re-run the playbook.



``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts backup.yml

PLAY [BACKUP SWITCH CONFIGURATIONS] ***************************************************************************************************

TASK [BACKUP THE CONFIG] **************************************************************************************************************
ok: [spine1]
ok: [spine2]
ok: [leaf3]
ok: [leaf2]
ok: [leaf1]
ok: [leaf4]
ok: [host1]
ok: [host2]

TASK [RENAME BACKUP] ******************************************************************************************************************
changed: [spine1]
changed: [leaf3]
changed: [leaf1]
changed: [leaf2]
changed: [spine2]
changed: [leaf4]
changed: [host2]
changed: [host1]

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

#### Step 7

Once again list the contents of the `backup` directory:

``` shell
[arista@ansible ansible-training]$ ls -l backup
total 64
-rw-rw-r-- 1 arista arista 2457 Feb  5 20:46 host1.config
-rw-rw-r-- 1 arista arista 2457 Feb  5 20:46 host1_config.2019-02-05@20:46:01
-rw-rw-r-- 1 arista arista 2308 Feb  5 20:46 host2.config
-rw-rw-r-- 1 arista arista 2308 Feb  5 20:46 host2_config.2019-02-05@20:46:01
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:46 leaf1.config
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:45 leaf1_config.2019-02-05@20:45:58
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:46 leaf2.config
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:45 leaf2_config.2019-02-05@20:45:58
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:46 leaf3.config
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:45 leaf3_config.2019-02-05@20:45:58
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:46 leaf4.config
-rw-rw-r-- 1 arista arista 2310 Feb  5 20:46 leaf4_config.2019-02-05@20:46:01
-rw-rw-r-- 1 arista arista 2312 Feb  5 20:46 spine1.config
-rw-rw-r-- 1 arista arista 2312 Feb  5 20:45 spine1_config.2019-02-05@20:45:58
-rw-rw-r-- 1 arista arista 2312 Feb  5 20:46 spine2.config
-rw-rw-r-- 1 arista arista 2312 Feb  5 20:45 spine2_config.2019-02-05@20:45:58
[arista@ansible ansible-training]$

```

Notice that the directory now has another backed-up configuration but one that reflects the device's name.



#### Step 8

If we were to try and manually restore the contents of this file to the respective device there are two lines in the configuration that will raise errors:

``` shell
Building configuration...

Current configuration with default configurations exposed : 393416 bytes

```
These lines have to be "cleaned up" to have a restorable configuration.

Write a new task using Ansible's `lineinfile` module to remove the first line.


``` yaml
---
- name: BACKUP SWITCH CONFIGURATIONS
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      eos_config:
        backup: yes
      register: config_output

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"

    - name: REMOVE NON CONFIG LINES
      lineinfile:
        path: "./backup/{{inventory_hostname}}.config"
        line: "Building configuration..."
        state: absent
```


> Note: The module parameter **line** is matching an exact line in the configuration file "Building configuration..."


#### Step 9

Before we run the playbook, we need to add one more task to remove the second line "Current configuration ...etc". Since this line has a variable entity (the number of bytes), we cannot use the `line` parameter of the `lineinfile` module. Instead, we'll use the `regexp` parameter to match on regular expressions and remove the line in the file:


``` yaml
---
- name: BACKUP SWITCH CONFIGURATIONS
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: BACKUP THE CONFIG
      eos_config:
        backup: yes
      register: config_output

    - name: RENAME BACKUP
      copy:
        src: "{{config_output.backup_path}}"
        dest: "./backup/{{inventory_hostname}}.config"

    - name: REMOVE NON CONFIG LINES
      lineinfile:
        path: "./backup/{{inventory_hostname}}.config"
        line: "Building configuration..."
        state: absent

    - name: REMOVE NON CONFIG LINES - REGEXP
      lineinfile:
        path: "./backup/{{inventory_hostname}}.config"
        regexp: 'Current configuration.*'
        state: absent
```


#### Step 10

Now run the playbook.


``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts backup.yml

PLAY [BACKUP SWITCH CONFIGURATIONS] *********************************************************************************************************************************************************

TASK [BACKUP THE CONFIG] ********************************************************************************************************************************************************************
ok: [rtr2]
ok: [rtr4]
ok: [rtr1]
ok: [rtr3]

TASK [RENAME BACKUP] ************************************************************************************************************************************************************************
changed: [rtr2]
changed: [rtr4]
changed: [rtr3]
changed: [rtr1]

TASK [REMOVE NON CONFIG LINES] **************************************************************************************************************************************************************
changed: [rtr4]
changed: [rtr1]
changed: [rtr2]
changed: [rtr3]

TASK [REMOVE NON CONFIG LINES - REGEXP] *****************************************************************************************************************************************************
changed: [rtr1]
changed: [rtr3]
changed: [rtr2]
changed: [rtr4]

PLAY RECAP **********************************************************************************************************************************************************************************
rtr1                       : ok=4    changed=3    unreachable=0    failed=0   
rtr2                       : ok=4    changed=3    unreachable=0    failed=0   
rtr3                       : ok=4    changed=3    unreachable=0    failed=0   
rtr4                       : ok=4    changed=3    unreachable=0    failed=0   

[arista@ansible ansible-training]$

```


#### Step 11

Use an editor to view the cleaned up files. The first 2 lines that we cleaned up in the earlier tasks should be absent:

``` shell
[arista@ansible ansible-training]$ head -n 10 backup/rtr1.config

!
! Last configuration change at 14:25:42 UTC Tue Jun 19 2018 by arista
!
version 16.8
downward-compatible-config 16.8
no service log backtrace
no service config
no service exec-callback
no service nagle
[arista@ansible ansible-training]$

```

> Note: The **head** unix command will display the first N lines specified as an argument.

# Complete

You have completed lab exercise 2.1

---
