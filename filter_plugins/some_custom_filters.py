#!/usr/bin/python
# Custom Filters for Ansible

class FilterModule(object):

    def filters(self):
        return {
            'valid_eos_version': self.valid_eos_version,
            'a_simple_filter': self.a_simple_filter,
        }

    def valid_eos_version(self, version_string):
        import re
        match = re.match(r'4\.\d+\.\d+[A-Za-z]+)', version_string)
        if not match:
            raise EOSVersionFormatError("%s isn't a valid EOS version string." % version_string)
        return True

    def a_simple_filter(self, string):
        updated_string = string + ' String Modified'
        return updated_string

class EOSVersionFormatError(Exception):
    pass
