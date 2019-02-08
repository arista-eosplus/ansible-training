# Custom Filters for Ansible

class FilterModule(object):

    def filters(self):
        return {
            'valid_eos_version': self.valid_eos_version,
        }

    def valid_eos_version(self, version_string):
        import re
        version_search = re.search(r'4.\d+.\d+[A-Za-z]+)', version_string)
        if not version_search:
            raise EOSVersionFormatError("{} isn't a valid EOS version string.".format(version_string))
        return True

class EOSVersionFormatError(Exception):
    pass
