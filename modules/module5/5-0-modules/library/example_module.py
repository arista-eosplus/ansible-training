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
