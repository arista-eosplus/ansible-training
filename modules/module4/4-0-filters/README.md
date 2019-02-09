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
extra_route: 10.10.0.0/24
[arista@ansible ansible-training]$
```

Notice the `extra_address` and `extra_route` variables. Let's use filters to do some validation and manipulation of these variables and give them a default value when they don't exist for a given device.

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

    - name: DISPLAY EXTRA ADDRESS AND EXTRA ROUTE
      debug:
        msg: 'Extra Address: {{ extra_address | default("None") }} Extra Route: {{ extra_route | default("None") }}'
```

The task is simply going to display the extra variables when they exist for a device and will print None when they do not exist.

Now let's run the playbook for all hosts.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts networking_filters.yml

PLAY [NETWORKING FILTERS] *************************************************************************************************************

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [leaf1]
ok: [spine1]
ok: [leaf4]
ok: [leaf3]
ok: [leaf2]
ok: [spine2]
ok: [host2]
ok: [host1]

TASK [DISPLAY EXTRA ADDRESS AND EXTRA ROUTE] ******************************************************************************************
ok: [leaf1] => {
    "msg": "Extra Address: 10.0.0.11 Extra Route: 10.0.100.0/24"
}
ok: [leaf3] => {
    "msg": "Extra Address: None Extra Route: None"
}
ok: [leaf4] => {
    "msg": "Extra Address: None Extra Route: None"
}
ok: [leaf2] => {
    "msg": "Extra Address: 10.0.0.12 Extra Route: 10.0.200.0/24"
}
ok: [spine1] => {
    "msg": "Extra Address: 10.0.0.1 Extra Route: 10.10.0.0/24"
}
ok: [spine2] => {
    "msg": "Extra Address: 10.0.0.2 Extra Route: 10.11.0.0/24"
}
ok: [host2] => {
    "msg": "Extra Address: None Extra Route: None"
}
ok: [host1] => {
    "msg": "Extra Address: None Extra Route: None"
}

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=2    changed=0    unreachable=0    failed=0
host2                      : ok=2    changed=0    unreachable=0    failed=0
leaf1                      : ok=2    changed=0    unreachable=0    failed=0
leaf2                      : ok=2    changed=0    unreachable=0    failed=0
leaf3                      : ok=2    changed=0    unreachable=0    failed=0
leaf4                      : ok=2    changed=0    unreachable=0    failed=0
spine1                     : ok=2    changed=0    unreachable=0    failed=0
spine2                     : ok=2    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

One other item to note here is that the default value printed for devices that do not have the extra variables defined is limited to the current task. The value `None` is not set in `extra_address` or `extra_route` for other tasks in this playbook.


#### Step 2

Now let's add a couple more tasks for validating the `extra_address`  and `extra_route` variables are the types we expect because it is possible a user put some bogus value into our host_vars/.

``` yaml
---
- name: NETWORKING FILTERS
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:

    - name: DISPLAY EXTRA ADDRESS AND EXTRA ROUTE
      debug:
        msg: 'Extra Address: {{ extra_address | default("None") }} Extra Route: {{ extra_route | default("None") }}'

    - name: VALIDATE EACH EXTRA ADDRESS
      debug:
        msg: "{{ extra_address }} is IP: {{ extra_address | ipv4 }}"
      when: extra_address is defined
      tags: validate

    - name: VALIDATE EACH EXTRA ROUTE
      debug:
        msg: "{{ extra_route }} is network range: {{ extra_route | ipaddr('net') }}"
      when: extra_route is defined
      tags: validate
```

The first task will use the `ipv4` filter to verify `extra_address` is a valid IPv4 address and the second task will use the `ipaddr` filter with parameter `net` to verify that `extra_route` is a valid network range. Let's run the updated playbook but with `--tags validate` so we only run our newest validation tasks.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts networking_filters.yml --tags validate

PLAY [NETWORKING FILTERS] *************************************************************************************************************

TASK [VALIDATE EACH EXTRA ADDRESS] ****************************************************************************************************
skipping: [leaf3]
skipping: [leaf4]
skipping: [host1]
skipping: [host2]
ok: [spine1] => {
    "msg": "10.0.0.111111 is IP: False"
}
ok: [leaf1] => {
    "msg": "10.0.0.11 is IP: 10.0.0.11"
}
ok: [spine2] => {
    "msg": "10.0.0.2 is IP: 10.0.0.2"
}
ok: [leaf2] => {
    "msg": "10.0.0.12 is IP: 10.0.0.12"
}

TASK [VALIDATE EACH EXTRA ROUTE] ******************************************************************************************************
skipping: [leaf3]
skipping: [leaf4]
skipping: [host1]
skipping: [host2]
ok: [spine1] => {
    "msg": "10.10.0.0/24 is network range: 10.10.0.0/24"
}
ok: [leaf1] => {
    "msg": "10.0.100.0/24 is network range: 10.0.100.0/24"
}
ok: [spine2] => {
    "msg": "10.11.0.0/24 is network range: 10.11.0.0/24"
}
ok: [leaf2] => {
    "msg": "10.0.200.0/24 is network range: 10.0.200.0/24"
}

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=0    changed=0    unreachable=0    failed=0
host2                      : ok=0    changed=0    unreachable=0    failed=0
leaf1                      : ok=2    changed=0    unreachable=0    failed=0
leaf2                      : ok=2    changed=0    unreachable=0    failed=0
leaf3                      : ok=0    changed=0    unreachable=0    failed=0
leaf4                      : ok=0    changed=0    unreachable=0    failed=0
spine1                     : ok=2    changed=0    unreachable=0    failed=0
spine2                     : ok=2    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$

```


#### Step 3

Now that we have seen some examples of using Ansible's built in filters let's build our own custom filters for validating and formatting our specific EOS data.

First create a new directory `filter_plugins`. This directory is where our Python code for our custom filters will live.

Within the `filter_plugins` directory create a new Python file `some_custom_filters.py` with the following skeleton content.

''' Python

#!/usr/bin/python
# Custom Filters for Ansible

class FilterModule(object):

    def filters(self):


'''

Custom filters must be built within the class `FilterModule` and returned via the `filters` function within this class. Our current module has no filter functions defined to be returned by the `filters` function.

Let's add our first filter that we can use to validate our EOS version.

''' Python

#!/usr/bin/python
# Custom Filters for Ansible

class FilterModule(object):

    def filters(self):
        return {
            'valid_eos_version': self.valid_eos_version,
        }

    def valid_eos_version(self, version_string):
        import re
        match = re.match(r'4\.\d+\.\d+[A-Za-z]+', version_string)
        if not match:
            raise EOSVersionFormatError("%s isn't a valid EOS version string." % version_string)
        return True

class EOSVersionFormatError(Exception):
    pass

'''

We now have an additional filter function defined named `valid_eos_version`. This new function accepts one variable, which will be our EOS version, and uses a regular expression to validate it is a 4.X.X version. If the version is not a 4.X.X version an Exception will be raised. This is essentially an error in Python. If the version is a valid 4.X.X version our function will return True. The last item added is that we had to make sure our new filter function `valid_eos_version` is being returned by the `filters` function within our `FilterModule`.

> Note: within python the **self** variable is a variable that refers to the class object itself.


#### Step 4

Now that we have our new `valid_eos_version` filter, let's use it in our playbook. Add a new task for validating our EOS version to the playbook.

``` yaml
---
- name: NETWORKING FILTERS
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:
      tags: validate

    - name: DISPLAY EXTRA ADDRESS AND EXTRA ROUTE
      debug:
        msg: 'Extra Address: {{ extra_address | default("None") }} Extra Route: {{ extra_route | default("None") }}'

    - name: VALIDATE EACH EXTRA ADDRESS
      debug:
        msg: "{{ extra_address }} is IP: {{ extra_address | ipv4 }}"
      when: extra_address is defined
      tags: validate

    - name: VALIDATE EACH EXTRA ROUTE
      debug:
        msg: "{{ extra_route }} is network range: {{ extra_route | ipaddr('net') }}"
      when: extra_route is defined
      tags: validate

    - name: DISPLAY WHETHER VERSION IS VALID USING CUSTOM FILTER
      debug:
        msg: "VERSION VALID: {{ ansible_net_version | valid_eos_version }}"
      tags: validate
```

Make sure to notice in addition to the new task we've also added the `tags: validate` statement to our initial `eos_facts` task. This is necessary to populate our `ansible_net_version` variable.

New run the playbook.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts networking_filters.yml --tags validate

PLAY [NETWORKING FILTERS] *************************************************************************************************************

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [leaf1]
ok: [leaf3]
ok: [spine1]
ok: [leaf2]
ok: [leaf4]
ok: [spine2]
ok: [host1]
ok: [host2]

TASK [VALIDATE EACH EXTRA ADDRESS] ****************************************************************************************************
.
.
<output omitted for brevity>

TASK [VALIDATE EACH EXTRA ROUTE] ******************************************************************************************************
.
.
<output omitted for brevity>

TASK [DISPLAY WHETHER VERSION IS VALID USING CUSTOM FILTER] ***************************************************************************
ok: [spine1] => {
    "msg": "VERSION VALID: True"
}
ok: [leaf2] => {
    "msg": "VERSION VALID: True"
}
ok: [leaf1] => {
    "msg": "VERSION VALID: True"
}
ok: [leaf3] => {
    "msg": "VERSION VALID: True"
}
ok: [leaf4] => {
    "msg": "VERSION VALID: True"
}
ok: [host1] => {
    "msg": "VERSION VALID: True"
}
ok: [host2] => {
    "msg": "VERSION VALID: True"
}
ok: [spine2] => {
    "msg": "VERSION VALID: True"
}

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=2    changed=0    unreachable=0    failed=0
host2                      : ok=2    changed=0    unreachable=0    failed=0
leaf1                      : ok=4    changed=0    unreachable=0    failed=0
leaf2                      : ok=4    changed=0    unreachable=0    failed=0
leaf3                      : ok=2    changed=0    unreachable=0    failed=0
leaf4                      : ok=2    changed=0    unreachable=0    failed=0
spine1                     : ok=4    changed=0    unreachable=0    failed=0
spine2                     : ok=4    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

And just like that we have created our first custom filter and used it within a playbook with information pulled from the device under test.


#### Step 4

# Complete

You have completed lab exercise 4.0

---
