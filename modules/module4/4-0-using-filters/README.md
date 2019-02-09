# Exercise 4.0 - Building and Using Custom Filters


Ansible has many filters built in that can be used for validating or transforming data. We have previously used one filter `dict2items` for transforming a dictionary of data into a list to be provided to the `loop` statement.

In this lab we will create a playbook that uses some of these built in filters in addition to developing our own filters.


#### Step 1

Create a new playbook called `networking_filters.yml` and add the following play definition with a task to run module `eos_facts`:


``` yaml
---
- name: NETWORKING FILTERS
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:
```

Now lets take note of some variables in the host_vars/ files for several of the devices. You'll notice in the host_vars/ directory spine1, spine2, leaf1 and leaf2 all have additional host variables defined.

View the contents of one of these files.

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/spine1
extra_variable: value
spine_description: value

extra_address: 10.0.0.1
extra_address_with_mask: 10.0.0.2/24
[arista@ansible ansible-training]$
```

Notice the `extra_address` and `extra_address_with_mask` variables. Let's use filters to do some validation and manipulation of these variables and give them a default value when they don't exist for a given device.

Let's add one more task to our playbook.

``` yaml
---
- name: NETWORKING FILTERS
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:

    -set_fact: extra_address='{{ extra_address | default("0.0.0.0") }}'

    - name: DISPLAY VARIABLE. DEFAULT IT IF IT DOESN'T EXIST
      debug:
        msg: 'Extra Address: {{ extra_address | default("0.0.0.0") }}'
```

Now let's run the playbook for all hosts.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts switch_report.yml

PLAY [GENERATE MODEL/VERSION REPORT FROM SWITCHES] ************************************************************************************

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [spine2]
ok: [leaf2]
ok: [leaf3]
ok: [leaf1]
ok: [spine1]
ok: [leaf4]
ok: [host1]
ok: [host2]

TASK [ENSURE REPORTS FOLDER] **********************************************************************************************************
changed: [spine1]

TASK [RENDER FACTS AS A REPORT] *******************************************************************************************************
changed: [spine1]
changed: [leaf1]
changed: [leaf2]
changed: [spine2]
changed: [leaf3]
changed: [host2]
changed: [host1]
changed: [leaf4]

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=2    changed=1    unreachable=0    failed=0
host2                      : ok=2    changed=1    unreachable=0    failed=0
leaf1                      : ok=2    changed=1    unreachable=0    failed=0
leaf2                      : ok=2    changed=1    unreachable=0    failed=0
leaf3                      : ok=2    changed=1    unreachable=0    failed=0
leaf4                      : ok=2    changed=1    unreachable=0    failed=0
spine1                     : ok=3    changed=2    unreachable=0    failed=0
spine2                     : ok=2    changed=1    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

# Complete

You have completed lab exercise 4.0

---
