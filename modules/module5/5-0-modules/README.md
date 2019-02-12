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





#### Step 5





#### Step 6





# Complete

You have completed lab exercise 5.0

---
