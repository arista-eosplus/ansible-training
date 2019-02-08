# Exercise 1.3 - when statement, loop statement & extra-vars on command line


Now that you have run a playbook that gathers facts, runs commands on the switch, and displays output, lets work with some control statements.

Control statements include when for checking some value before executing a play or task, and loop for repeating an action many times for a list or dictionary of data.


#### Step 1

Using your favorite text editor (`vim` and `nano` are available on the control host) create a new file called `show_interface_state.yml`.

>Alternately, you can create it using sublimetext or any GUI editor on your laptop and scp it over)

```
[arista@ansible ansible-training]$ vim show_interface_state.yml
```

Enter the following play and task definition into `show_interface_state.yml`:

>Press the letter "i" to enter insert mode*

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: DISPLAY EXTRA VARIABLE
      debug:
        msg: "User provided command line variable: {{ command_line_variable }}"
```

Notice that the variable we are referencing in the debug message hasn't been defined anywhere. The intention here is that we will pass this variable in via the `extra-vars` command line variable.

What happens if we run the playbook without adding the variable? Let's also limit the execution to `spine1` for now.

```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts show_interface_state.yml --limit spine1

PLAY [GATHER INFORMATION FROM SWITCHES] ***********************************************************************************************

TASK [DISPLAY EXTRA VARIABLE] *********************************************************************************************************
fatal: [spine1]: FAILED! => {"msg": "The task includes an option with an undefined variable. The error was: 'command_line_variable' is undefined\n\nThe error appears to have been in '/home/arista/ansible-training/show_interface_state.yml': line 8, column 7, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n  tasks:\n    - name: DISPLAY EXTRA VARIABLE\n      ^ here\n"}
	to retry, use: --limit @/home/arista/ansible-training/show_interface_state.retry

PLAY RECAP ****************************************************************************************************************************
spine1                     : ok=0    changed=0    unreachable=0    failed=1

[arista@ansible ansible-training]$

```

The execution failed with an error mentioning the undefined variable. Let's run the playbook again but this time make sure to provide the `command_line_variable` in the execution using the `extra-vars` flag.

```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts show_interface_state.yml --limit spine1 --extra-vars '{"command_line_variable":"value"}'

PLAY [GATHER INFORMATION FROM SWITCHES] ***********************************************************************************************

TASK [DISPLAY EXTRA VARIABLE] *********************************************************************************************************
ok: [spine1] => {
    "msg": "User provided command line variable: value"
}

PLAY RECAP ****************************************************************************************************************************
spine1                     : ok=1    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

This time the execution is successful and the message is displayed.


#### Step 2

What if we want our playbook to run without error even in the case where the user or automation executing the playbook does not provide the additional variable via `extra-vars`?

This is a scenario where we can use the `when` statement. The `when` statement is a conditional that allows the playbook to determine whether or not to skip a given play or task based on the state of some values/variables. It is similar to an if statement in programming.

Add a when statement to the playbook.

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: DISPLAY EXTRA VARIABLE
      debug:
        msg: "User provided command line variable: {{ command_line_variable }}"
      when: command_line_variable is defined
```

The `is defined` portion of the statement is the check that verifies the command_line_variable has been defined somewhere, whether it be in inventory, the playbook or commmand line, before executing the task. Also note that variables are referenced in the `when` statement without curly braces {{ }}.

Run the playbook again without `extra-vars`

```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts show_interface_state.yml --limit spine1

PLAY [GATHER INFORMATION FROM SWITCHES] ***********************************************************************************************

TASK [DISPLAY EXTRA VARIABLE] *********************************************************************************************************
skipping: [spine1]

PLAY RECAP ****************************************************************************************************************************
spine1                     : ok=0    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

Notice that in this execution the task was skipped instead of producing an error.


#### Step 3

Now that we've used the conditional `when` statement a bit lets try the `loop` statement for repetitive actions within a task. Add the following two tasks to the playbook.

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: DISPLAY EXTRA VARIABLE
      debug:
        msg: "User provided command line variable: {{ command_line_variable }}"
      when: command_line_variable is defined

    - name: GATHER SWITCH FACTS
      eos_facts:

    - name: DISPLAY IPv4 ADDRS
      debug:
        msg: "Found Addr: {{ item }}"
      loop: "{{ ansible_net_all_ipv4_addresses }}"
```

The first task is simply the `eos_facts` module that we've used several times already. We are using this to populate some information about the switch that we can then loop over for display.

The second task is using the `loop` statement in conjunction with the `debug` module to display each IPv4 address found on the device. The `ansible_net_all_ipv4_addresses` is a list data type. You can run the playbook with `-v` to verify this if you would like. Also notice that the variable name in the `debug` message is `item`. `item` is a keyword used to reference the current item being iterated over by the loop.

Let's run the updated playbook.

```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts show_interface_state.yml --limit spine1

PLAY [GATHER INFORMATION FROM SWITCHES] ***********************************************************************************************

TASK [DISPLAY EXTRA VARIABLE] *********************************************************************************************************
skipping: [spine1]

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [spine1]

TASK [DISPLAY IPv4 ADDRS] *************************************************************************************************************
ok: [spine1] => (item=192.168.0.10) => {
    "msg": "Found Addr: 192.168.0.10"
}

PLAY RECAP ****************************************************************************************************************************
spine1                     : ok=2    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

Turns out there is only one IP address currently configured on the device. Not the most interesting case for demonstrating the `loop` statement.

Let's add another task.

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: DISPLAY EXTRA VARIABLE
      debug:
        msg: "User provided command line variable: {{ command_line_variable }}"
      when: command_line_variable is defined

    - name: GATHER SWITCH FACTS
      eos_facts:

    - name: DISPLAY IPv4 ADDRS
      debug:
        msg: "Found Addr: {{ item }}"
      loop: "{{ ansible_net_all_ipv4_addresses }}"

      - name: DISPLAY INTERFACES
        debug:
          msg: "Found Interface: {{ item.key }}"
        loop: "{{ ansible_net_interfaces|dict2items }}"
```

This task is very similar to the previous one but notice a few additions. The variable being iterated over `ansible_net_interfaces` is following by a `|` and `dict2items`. This is a Jinja2 filter and it is being applied to the `ansible_net_interfaces` variable. We will discuss filters in more detail later, but this is needed now because the `ansible_net_interfaces` variable is not a list. It is a dictionary or data structure representing interface information. Using the `dict2items` filter we can now reference the dictionary variable by its key and/or value. Notice the `debug` message references `item.key`. In our case the key will be the interface name. If you run the playbook with a `-v` you can see the structure of the `ansible_net_interfaces` data. Let's run the playbook.

```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts show_interface_state.yml --limit spine1

PLAY [GATHER INFORMATION FROM SWITCHES] ***********************************************************************************************

TASK [DISPLAY EXTRA VARIABLE] *********************************************************************************************************
skipping: [spine1]

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [spine1]

TASK [DISPLAY IPv4 ADDRS] *************************************************************************************************************
ok: [spine1] => (item=192.168.0.10) => {
    "msg": "Found Addr: 192.168.0.10"
}

TASK [DISPLAY INTERFACES] *************************************************************************************************************
ok: [spine1] => (item={'key': u'Ethernet8', 'value': {u'macaddress': u'f6:62:e1:20:11:f5', u'lineprotocol': u'up', u'description': u'', u'operstatus': u'connected', u'mtu': 9214, u'duplex': u'duplexFull', u'bandwidth': 0, u'ipv4': {}, u'type': u'bridged'}}) => {
    "msg": "Found Interface: Ethernet8"
}
ok: [spine1] => (item={'key': u'Ethernet9', 'value': {u'macaddress': u'f2:30:d5:08:38:6b', u'lineprotocol': u'up', u'description': u'', u'operstatus': u'connected', u'mtu': 9214, u'duplex': u'duplexFull', u'bandwidth': 0, u'ipv4': {}, u'type': u'bridged'}}) => {
    "msg": "Found Interface: Ethernet9"
}
ok: [spine1] => (item={'key': u'Ethernet2', 'value': {u'macaddress': u'46:d2:a4:9e:0e:f8', u'lineprotocol': u'up', u'description': u'', u'operstatus': u'connected', u'mtu': 9214, u'duplex': u'duplexFull', u'bandwidth': 0, u'ipv4': {}, u'type': u'bridged'}}) => {
    "msg": "Found Interface: Ethernet2"
}
ok: [spine1] => (item={'key': u'Ethernet3', 'value': {u'macaddress': u'02:32:4f:94:f4:27', u'lineprotocol': u'up', u'description': u'', u'operstatus': u'connected', u'mtu': 9214, u'duplex': u'duplexFull', u'bandwidth': 0, u'ipv4': {}, u'type': u'bridged'}}) => {
    "msg": "Found Interface: Ethernet3"
}
.
.
.
.
.
<output omitted for brevity>

PLAY RECAP ****************************************************************************************************************************
spine1                     : ok=3    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$

```


#### Step 4

Displaying every interface is an interesting way to demonstrate looping over a dictionary object in an Ansible playbook, but a more practical usage would be to only display interfaces that meet some criteria. Lets add one last task to our playbook to only display interface names that do not have their `lineprotocol` in an `up` state.

To do this we will combine both the `loop` and `when` statement in a single task.

``` yaml
---
- name: GATHER INFORMATION FROM SWITCHES
  hosts: arista
  connection: network_cli
  gather_facts: no

  tasks:
    - name: DISPLAY EXTRA VARIABLE
      debug:
        msg: "User provided command line variable: {{ command_line_variable }}"
      when: command_line_variable is defined

    - name: GATHER SWITCH FACTS
      eos_facts:

    - name: DISPLAY IPv4 ADDRS
      debug:
        msg: "Found Addr: {{ item }}"
      loop: "{{ ansible_net_all_ipv4_addresses }}"

    - name: DISPLAY INTERFACES
      debug:
        msg: "Found Interface: {{ item.key }}"
      loop: "{{ ansible_net_interfaces|dict2items }}"

    - name: DISPLAY INTERFACES WITH LINE PROTOCOL NOT UP
      debug:
        msg: "Found Interface: {{ item.key }}"
      loop: "{{ ansible_net_interfaces|dict2items }}"
      when: item.value.lineprotocol != "up"
```

This final task looks very similar to our previous task except it adds a `when` statement that references our `item.value`. Because the data stored in `item.value` is also a data structure, we can reference its parameters for our check using the standard variable dot notation.

Let's run our final playbook one last time.

```
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts show_interface_state.yml --limit spine1

PLAY [GATHER INFORMATION FROM SWITCHES] ***********************************************************************************************

TASK [DISPLAY EXTRA VARIABLE] *********************************************************************************************************
skipping: [spine1]

TASK [GATHER SWITCH FACTS] ************************************************************************************************************
ok: [spine1]

TASK [DISPLAY IPv4 ADDRS] *************************************************************************************************************
ok: [spine1] => (item=192.168.0.10) => {
    "msg": "Found Addr: 192.168.0.10"
}

TASK [DISPLAY INTERFACES] *************************************************************************************************************
ok: [spine1] => (item={'key': u'Ethernet8', 'value': {u'macaddress': u'f6:62:e1:20:11:f5', u'lineprotocol': u'up', u'description': u'', u'operstatus': u'connected', u'mtu': 9214, u'duplex': u'duplexFull', u'bandwidth': 0, u'ipv4': {}, u'type': u'bridged'}}) => {
    "msg": "Found Interface: Ethernet8"
}
ok: [spine1] => (item={'key': u'Ethernet9', 'value': {u'macaddress': u'f2:30:d5:08:38:6b', u'lineprotocol': u'up', u'description': u'', u'operstatus': u'connected', u'mtu': 9214, u'duplex': u'duplexFull', u'bandwidth': 0, u'ipv4': {}, u'type': u'bridged'}}) => {
    "msg": "Found Interface: Ethernet9"
}
.
.
.
.
.
<output omitted for brevity>

TASK [DISPLAY INTERFACES WITH LINE PROTOCOL NOT UP] ***********************************************************************************
ok: [spine1] => (item={'key': u'Management1', 'value': {u'macaddress': u'92:9c:13:7d:f1:f6', u'lineprotocol': u'notPresent', u'description': u'', u'operstatus': u'notconnect', u'mtu': 1500, u'duplex': u'duplexUnknown', u'bandwidth': 0, u'ipv4': {u'masklen': 24, u'address': u'192.168.0.10'}, u'type': u'routed'}}) => {
    "msg": "Found Interface: Management1"
}
skipping: [spine1] => (item={'key': u'Ethernet31', 'value': {u'macaddress': u'92:9d:1d:66:77:75', u'lineprotocol': u'up', u'description': u'', u'operstatus': u'connected', u'mtu': 9214, u'duplex': u'duplexFull', u'bandwidth': 0, u'ipv4': {}, u'type': u'bridged'}})
skipping: [spine1] => (item={'key': u'Ethernet29', 'value': {u'macaddress': u'96:95:fb:03:d0:11', u'lineprotocol': u'up', u'description': u'', u'operstatus': u'connected', u'mtu': 9214, u'duplex': u'duplexFull', u'bandwidth': 0, u'ipv4': {}, u'type': u'bridged'}})
.
.
.
.
.
<output omitted for brevity>

PLAY RECAP ****************************************************************************************************************************
spine1                     : ok=4    changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

Our final result shows that only Management1 interface `lineprotocol` is not in an `up` state. The remainder of the interface items were skipped. One thing to notice here is that when the `when` statement is combined with the `loop` statement the `when` clause is run for each item iterated over by the `loop` statement.

> Note don't worry about the state of the Management1 interface. This is simply a result of our virtual lab environment.


# Complete

You have completed lab exercise 1.3

---
