#!/usr/bin/python
# An Ansible local custom module

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: my_custom_module
version_added: "2.7.1"
author: "EOS+ CS (@mharista)"
short_description:
    A short description for my custom module.
description:
  - This module is an example module for developing local custom modules.
options:
  option_one:
    description:
      - Option 1.
    required: true
  option_two:
    description:
      - Option 2.
    default: None
  option_three:
    description:
      - Option 3.
    default: value
    choices: [value, othervalue]
notes:
requirements:
'''

EXAMPLES = '''
- name: Run with option_one
  my_custom_module:
    option_one: 1

- name: Run with all options.
  cv_server_provision:
    option_one: 1
    option_two: 2
    option_three: othervalue
'''

RETURN = '''
changed:
  description: Signifies if a change was made
  returned: success
  type: bool
  sample: false
return_value_one:
  description: A return value
  returned: when option_two provided
  type: string
  sample: value1
return_value_two:
  description: Another return value
  returned: when option_three is othervalue
  type: string
  sample: value2
'''

from ansible.module_utils.basic import AnsibleModule


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        option_one=dict(required=True),
        option_two=dict(required=False, default=None),
        option_three=dict(default='value', choices=['value', 'othervalue']))

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)
    result = dict(changed=False)

    if module.params['option_one'] == 'fail':
        module.fail_json(msg='option_one = fail. Fail module')
    if module.params['option_two'] is not None:
        result['return_value_one'] = 'value1'
    if module.params['option_three'] == 'othervalue':
        result['return_value_two'] = 'value2'
    module.exit_json(**result)


if __name__ == '__main__':
    main()
