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

# Complete

You have completed lab exercise 4.0

---
