# Exercise 5.0 - Building and Using Custom Modules


Ansible has many built in modules but there will be cases when existing or combinations of existing module functionality will not meet all of the needs of your automation environment. In these cases you can develop your own custom Ansible modules to fill in whatever gaps exist.

There are many ways of extending Ansible, from plugins (for example the filter_plugins we have seen in a previous lab), to modules.


#### Step 1


We will first create a new module that will only be usable by our playbooks within `~/ansible-training` directory. To do this create a new directory `library/` (if it doesn't already exist) within the `ansible-training/` directory.

The `library/` directory is where Ansible will look when loading custom modules for playbooks sourced in the current directory. We will later look at moving the module to the `~/.ansible/plugins/modules` directory so it will be globally available to all playbooks.

Create a new Python file within the `library/` directory called `example_module.py` and add the following skeleton module content.

``` Python
#!/usr/bin/python
# An Ansible local custom module

from ansible.module_utils.basic import AnsibleModule


def main():
    """ main entry point for custom module execution
    """
    argument_spec = dict()

    module = AnsibleModule(argument_spec=argument_spec)
    result = dict(changed=False)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
```

This skeleton framework for our custom Ansible module doesn't do anything currently, but it provides the building blocks for our module.

- It is importing `AnsibleModule`, which is an Ansible built in Python object used for simplifying argument handling and return data within modules.
- It creates an empty argument specification as `argument_spec` that is being used during `AnsibleModule` instantiation.
- It shows the usage of the `exit_json()` method associated with the `AnsibleModule` object for returning our data in the proper format.


#### Step 2


Let's try running `ansible-doc` for our new module. Make sure to use the `-M` option and add the local `library/` path otherwise `ansible-doc` won't be able to find our new module. This won't be required later when we move the module to `~/.ansible/plugins/modules`

``` shell
[arista@ansible ansible-training]$ ansible-doc -t module example_module -M library
ERROR! module example_module missing documentation (or could not parse documentation): 'NoneType' object has no attribute 'get'
```

The command returns an error, which is expected, because we haven't added our documentation strings yet. Let's do that now. Add some empty doc strings to `library/example_module.py`

``` Python
#!/usr/bin/python
# An Ansible local custom module

DOCUMENTATION = '''
---
module: example_module
version_added: "2.7.1"
author: "me"
short_description:
    A short description for my custom module.
description:
  - This module is an example module for developing local custom modules.
options:
notes:
requirements:
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule


def main():
    """ main entry point for custom module execution
    """
    argument_spec = dict()

    module = AnsibleModule(argument_spec=argument_spec)
    result = dict(changed=False)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
```

Now rerun the `ansible-doc` command:

``` shell
[arista@ansible ansible-training]$ ansible-doc -t module example_module -M library
> EXAMPLE_MODULE    (/home/arista/ansible-training/library/example_module.py)

        This module is an example module for developing local custom modules.

AUTHOR: me

EXAMPLES:


RETURN VALUES:


```

Much better. You can also try running the `ansible-doc` command without the previously dicsuccsed `-M` option to see Ansible won't find our custom module within the standard paths it loads extra modules from.

``` shell
[arista@ansible ansible-training]$ ansible-doc -t module example_module
[WARNING]: module example_module not found in:
/home/arista/.ansible/plugins/modules:/usr/share/ansible/plugins/modules:/usr/local/lib/python2.7/dist-packages/ansible/modules

```


#### Step 3


Now that we know our empty custom module can be found by Ansible, let's try adding it to a playbook. Create a new playbook called `test_example_module.yml` and add the following content:

``` yaml
---
- name: TEST EXAMPLE MODULE
  hosts: arista
  gather_facts: no
  connection: network_cli

  tasks:
    - name: RUN EXAMPLE MODULE
      example_module:
      register: result

    - name: DISPLAY EXAMPLE MODULE RESULT
      debug:
        var: result
```

The playbook will be running our custom `example_module` and registering the output into a variable `result` that we will print with the built in `debug` module.

Now let's run the new playbook.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts test_example_module.yml --limit spine1

PLAY [TEST EXAMPLE MODULE] ************************************************************************************************************

TASK [RUN EXAMPLE MODULE] *************************************************************************************************************
ok: [spine1]

TASK [DISPLAY EXAMPLE MODULE RESULT] **************************************************************************************************
ok: [spine1] => {
    "result": {
        "changed": false,
        "failed": false
    }
}

PLAY RECAP ****************************************************************************************************************************
spine1                     : ok=2    changed=0    unreachable=0    failed=0

```

In three simple steps we have created a custom module and used it within a playbook. Let's continue by updating our module to do something more useful than the nothing it currently does.


#### Step 4


For our next step we will add some more internal Ansible helping methods, use them to execute a command on the switch, and add the output to the return data. This portion is not as straight forward as developing a standard module and will require us to dig into the Ansible core code for examples.

Let's say we want to add the execution of `show run | include ip route` to our module so we can gather all static routes configured on the system. How would we do this? Since Ansible's core code is open for us to view we can see how Ansible is currently doing things by viewing the Python code for module `eos_command`.

Let's look at the code at https://github.com/ansible/ansible/blob/stable-2.7/lib/ansible/modules/network/eos/eos_command.py

> Note: It is important to know your Ansible version when looking through core code modules and make sure you are looking at the core module that corresponds to the Ansible verison you have running. In this example the link is for stable-2.7 Ansible code since we are running version 2.7.1.


#### Step 5


Let's update `example_module.py` with some of the contents from `eos_command.py`:

``` Python
#!/usr/bin/python
# An Ansible local custom module

DOCUMENTATION = '''
---
module: example_module
version_added: "2.7.1"
author: "me"
short_description:
    A short description for my custom module.
description:
  - This module is an example module for developing local custom modules.
options:
notes:
requirements:
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import string_types
from ansible.module_utils.network.common.utils import ComplexList
from ansible.module_utils.network.eos.eos import run_commands
from ansible.module_utils.network.eos.eos import eos_argument_spec, check_args

def to_lines(stdout):
    lines = list()
    for item in stdout:
        if isinstance(item, string_types):
            item = str(item).split('\n')
        lines.append(item)
    return lines


def parse_commands(module, warnings):
    spec = dict(
        command=dict(key=True),
        output=dict(),
        prompt=dict(),
        answer=dict()
    )

    transform = ComplexList(spec, module)
    commands = transform(module.params['commands'])

    if module.check_mode:
        for item in list(commands):
            if not item['command'].startswith('show'):
                warnings.append(
                    'Only show commands are supported when using check_mode, not '
                    'executing %s' % item['command']
                )
                commands.remove(item)

    return commands

def main():
    """ main entry point for custom module execution
    """
    argument_spec = dict()
    argument_spec.update(eos_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    module.params['commands'] = ['show run | include ip route']
    result = dict(changed=False)
    warnings = list()
    check_args(module, warnings)
    commands = parse_commands(module, warnings)
    if warnings:
        restul['warnings'] = warnings
    responses = run_commands(module, commands)
    result['static_routes'] = responses
    result['static_routes_lines'] = to_lines(responses)
    module.exit_json(**result)


if __name__ == '__main__':
    main()

```

Here we've added a group of additional functions imported from core Ansible that we see used in `eos_command` and replicated their usage. We also added in the parse_commands method which will transform our string commands into a format Ansible expects using the imported`ComplexList` object. We've also replicated the `parse_commands` and `to_lines` functions that were used in `eos_command`.

Another important addition is that we imported the `eos_arugment_spec` and added that to our `argument_spec`. This is an Ansible built in helper for making sure we have all variables necessary for connecting to our networking devices.

We've also added support to run our module in check mode, even though currently no changes are being made to the switch and the user will still not be providing any input parameters.

We will use the imported `run_commands` method to run our formatted commands and return the collected output in our results with the keys `static_routes` and `static_routes_lines`.

Let's run our playbook again.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts test_example_module.yml --limit spine1

PLAY [TEST EXAMPLE MODULE] ************************************************************************************************************

TASK [RUN EXAMPLE MODULE] *************************************************************************************************************
ok: [spine1]

TASK [DISPLAY EXAMPLE MODULE RESULT] **************************************************************************************************
ok: [spine1] => {
    "result": {
        "changed": false,
        "failed": false,
        "static_routes": [
            "ip route 0.0.0.0/0 192.168.0.254"
        ],
        "static_routes_lines": [
            [
                "ip route 0.0.0.0/0 192.168.0.254"
            ]
        ]
    }
}

PLAY RECAP ****************************************************************************************************************************
spine1                     : ok=2    changed=0    unreachable=0    failed=0

```

With these additions we've added some interaction with our EOS device and some additional return output that we could register into a variable and use if desired.


#### Step 6





# Complete

You have completed lab exercise 5.0

---
