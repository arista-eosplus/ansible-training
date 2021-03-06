# Exercise 3.0 - An introduction to templating with Jinja2


Generally speaking, when one talks about network automation the focus is specifically around configuration management of devices. In this lab you will learn how to use Ansible as a tool to generate living, dynamic documentation.

This allows the ability to generate reports and documents, using the same information and can cater to the needs of a hands-on-keyboard network engineer to a manager who needs to understand the state of the network with a glance of a web-page!


[Jinja2](http://jinja.pocoo.org/docs/2.10/) is a powerful templating engine for Python. There is native integration of Jinja2 with Ansible. Jinja2 allows for manipulating variables and implementing logical constructs. In combination with the Ansible `template` module, the automation engineer has a powerful tool at their disposal to generate live or dynamic reports.


In this lab you will learn how to use the `template` module to pass collected data from devices to a Jinja2 template. The template module then renders the output as a `markdown` file.



#### Step 1

Create a new playbook called `switch_report.yml` and add the following play definition to it:


``` yaml
---
- name: GENERATE MODEL/VERSION REPORT FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no
```


#### Step 2

Add a task that collects the facts using the `eos_facts` module. Recollect that we used this module in an earlier lab.


``` yaml
---
- name: GENERATE MODEL/VERSION REPORT FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:

```

> Recall that the **facts** modules automatically populates device specific variables such as **ansible_net_version**, **ansible_net_model**, and **ansible_net_hostname** within the play. You can validate this by running the playbook in verbose mode.




#### Step 3

Rather than using debug or verbose mode to display the output on the screen, go ahead and add a new task using the template module as follows:


``` yaml
---
- name: GENERATE MODEL/VERSION REPORT FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:

    - name: ENSURE REPORTS FOLDER
      run_once: true
      file:
        name: reports
        state: directory

    - name: RENDER FACTS AS A REPORT
      template:
        src: switch_info_report.j2
        dest: reports/{{ inventory_hostname }}.md
```



Let's break this task down a bit. The `template` module has a `src` parameter that has a value of `switch_info_report.j2`. In the next few steps, we will create this file. This will be the Jinja2 template,  used to generate the desired report. The `dest` parameter specifies the destination file name to render the report into.


#### Step 4


The next step is to create a Jinja2 template. Ansible will look for the template file in the current working directory and within a directory called `templates` automatically. Convention/best-practice is to create the template file within the templates directory.

Using `vi`, `nano` or another text editor, go ahead and create the file called `switch_info_report.j2` under the `templates` directory. Add the following into the template file:


``` python


{{ inventory_hostname.upper() }}
---
hostname: {{ ansible_net_hostname }}
version: {{ ansible_net_version }}
model: {{ ansible_net_model }}
managementIP: {{ ansible_net_interfaces.Management1.ipv4.address }}


```

This file simply contains some of the variables we have been using in our playbooks until now.

> Note: Python build in methods for datatypes are available natively in Jinja2 making it very easy to manipulate the formatting etc.


#### Step 5

With this in place, go ahead and run the playbook:

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


#### Step 6

After the playbook run, you should see the following files appear in the reports directory:


``` shell
[arista@ansible ansible-training]$ ls -l reports
total 32
-rw-rw-r-- 1 arista arista 82 Feb  6 14:33 host1.md
-rw-rw-r-- 1 arista arista 82 Feb  6 14:33 host2.md
-rw-rw-r-- 1 arista arista 82 Feb  6 14:33 leaf1.md
-rw-rw-r-- 1 arista arista 82 Feb  6 14:33 leaf2.md
-rw-rw-r-- 1 arista arista 82 Feb  6 14:33 leaf3.md
-rw-rw-r-- 1 arista arista 82 Feb  6 14:33 leaf4.md
-rw-rw-r-- 1 arista arista 84 Feb  6 14:33 spine1.md
-rw-rw-r-- 1 arista arista 84 Feb  6 14:33 spine2.md
[arista@ansible ansible-training]$

```

The contents of one of them for example:

``` shell
[arista@ansible ansible-training]$ cat reports/spine1.md
SPINE1
---
hostname: spine1
version: 4.21.2F
model: vEOS
managementIP: 192.168.0.10

[arista@ansible ansible-training]$
```


#### Step 7


While it is nice to have the data, it would be even better to consolidate all these individual switch reports into a single document. Let's add a new task to do that



``` yaml
---
- name: GENERATE MODEL/VERSION REPORT FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: GATHER SWITCH FACTS
      eos_facts:

    - name: ENSURE REPORTS FOLDER
      run_once: true
      file:
        name: reports
        state: directory

    - name: RENDER FACTS AS A REPORT
      template:
        src: switch_info_report.j2
        dest: reports/{{ inventory_hostname }}.md

    - name: CONSOLIDATE THE EOS DATA
      assemble:
        src: reports/
        dest: switches_info_report.md
      delegate_to: localhost
      run_once: yes
```


Here we are using the `assemble` module. The `src` parameter specifies the directory that contain file fragments that need to be consolidated and the `dest` parameter provides the file to render the fragments into.

> Note: The **delegate_to** can be used to specify tasks that need to be executed locally. The **run_once** directive will ensure that the given task is executed only once.




#### Step 8

Go ahead and run the playbook.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts switch_report.yml

PLAY [GENERATE MODEL/VERSION REPORT FROM SWITCHES] ************************************************************************************

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [spine1]
ok: [leaf2]
ok: [leaf1]
ok: [spine2]
ok: [leaf3]
ok: [leaf4]
ok: [host2]
ok: [host1]

TASK [ENSURE REPORTS FOLDER] **********************************************************************************************************
ok: [spine1]

TASK [RENDER FACTS AS A REPORT] *******************************************************************************************************
ok: [leaf1]
ok: [spine2]
ok: [leaf2]
ok: [spine1]
ok: [leaf3]
ok: [leaf4]
ok: [host1]
ok: [host2]

TASK [CONSOLIDATE THE EOS DATA] *******************************************************************************************************
changed: [spine1 -> localhost]

PLAY RECAP ****************************************************************************************************************************
host1                      : ok=2    changed=0    unreachable=0    failed=0
host2                      : ok=2    changed=0    unreachable=0    failed=0
leaf1                      : ok=2    changed=0    unreachable=0    failed=0
leaf2                      : ok=2    changed=0    unreachable=0    failed=0
leaf3                      : ok=2    changed=0    unreachable=0    failed=0
leaf4                      : ok=2    changed=0    unreachable=0    failed=0
spine1                     : ok=4    changed=1    unreachable=0    failed=0
spine2                     : ok=2    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$

```



#### Step 9

A new file called `switches_info_report.md` will now be available in the playbook root. Use the `cat` command to view it's contents:


``` shell
[arista@ansible ansible-training]$ cat switches_info_report.md
HOST1
---
hostname: host1
version: 4.21.2F
model: vEOS
managementIP: 192.168.0.31

HOST2
---
hostname: host2
version: 4.21.2F
model: vEOS
managementIP: 192.168.0.32

LEAF1
---
hostname: leaf1
version: 4.21.2F
model: vEOS
managementIP: 192.168.0.14

LEAF2
---
hostname: leaf2
version: 4.21.2F
model: vEOS
managementIP: 192.168.0.15

LEAF3
---
hostname: leaf3
version: 4.21.2F
model: vEOS
managementIP: 192.168.0.16

LEAF4
---
hostname: leaf4
version: 4.21.2F
model: vEOS
managementIP: 192.168.0.17

SPINE1
---
hostname: spine1
version: 4.21.2F
model: vEOS
managementIP: 192.168.0.10

SPINE2
---
hostname: spine2
version: 4.21.2F
model: vEOS
managementIP: 192.168.0.11

[arista@ansible ansible-training]$

```

> Note: Markdown files can be rendered visually as HTML

At this point, with 3 small tasks, you have a report on all the EOS devices in your network. This is a simple example but the principle remains as you expand upon the capabilities.  For example, you can build status reports and dashboards that rely on the output of device show commands.

Ansible provides the tools and methods to extend network automation beyond configuration management to more robust capabilities, such as, generating documentation and or reports.

# Complete

You have completed lab exercise 3.0

---
