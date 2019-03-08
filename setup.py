import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.py', '*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.gbls',
      version='0.0.10',
      description=('Contains Legal Server integration, basic skeleton for interviews used at Greater Boston Legal Services'),
      long_description=u'# GBLS Module\r\n\r\nThis package is the beginning of a collection of standard includes for Greater\r\nBoston Legal Services.\r\n\r\nIt provides `basic-questions-gbls.yml` and `legal_server.py`, which\r\ncreates some standard objects and fills in their variables with data from\r\nLegal Server, when launched from Legal Server.\r\n\r\nAttributes that are filled in include name, address, email, and phone number, using the\r\nstandard Individual attribute names.\r\n\r\nTo use (and add the objects `client`, `advocate`, and `adverse_parties`) \r\ninclude `docassemble.gbls:basic-questions-gbls.yml`\r\n\r\nE.g., when you include `docassemble.gbls:basic-questions-gbls.yml`, you will have\r\nthe following attributes available to you:\r\n\r\n* client\r\n* client.full_name()\r\n* client.name.first / client.name.middle / client.name.last / client.name.suffix\r\n* client.address.address, client.address.zip, etc / client.address_block()\r\n* client.phone_number\r\n* client.mobile_number\r\n* client.email\r\n* client.birth_date\r\n\r\nName fields and email will also be available for `advocate`. adverse_parties will\r\nbe a DAList of Persons, with adverse_party[i].name.text and adverse_party[i].full_name()\r\navailable. Address of adverse parties is not parsed.',
      long_description_content_type='text/markdown',
      author='Quinten Steenhuis',
      author_email='admin@admin.com',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=['usaddress'],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/gbls/', package='docassemble.gbls'),
     )

