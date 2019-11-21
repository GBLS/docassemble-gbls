import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
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
      version='0.0.58',
      description=('Contains Legal Server integration, basic skeleton for interviews used at Greater Boston Legal Services'),
      long_description='# GBLS Module\r\n\r\nThis package is the beginning of a collection of standard includes for Greater\r\nBoston Legal Services.\r\n\r\nIt provides `basic-questions-gbls.yml` and `legal_server.py`, which\r\ncreates some standard objects and fills in their variables with data from\r\nLegal Server, when launched from Legal Server.\r\n\r\nAttributes that are filled in include name, address, email, and phone number, using the\r\nstandard Individual attribute names.\r\n\r\nTo use (and add the objects `client`, `advocate`, and `adverse_parties`) \r\ninclude `docassemble.gbls:basic-questions-gbls.yml`\r\n\r\nE.g., when you include `docassemble.gbls:basic-questions-gbls.yml`, you will have\r\nthe following attributes available to you:\r\n\r\n* client\r\n* client.full_name()\r\n* client.name.first / client.name.middle / client.name.last / client.name.suffix\r\n* client.address.address, client.address.zip, etc / client.address_block()\r\n* client.phone_number\r\n* client.mobile_number\r\n* client.email\r\n* client.birth_date\r\n\r\nName fields and email will also be available for `advocate`. adverse_parties will\r\nbe a DAList of Persons, with adverse_party[i].name.text and adverse_party[i].full_name()\r\navailable. Address of adverse parties is not parsed.\r\n\r\n# Integrating with Legal Server\r\n\r\nAfter you install this package on your Docassemble Server, create a new instruction\r\nblock on the case page with the contents below.\r\n\r\nReplace both instances of MYDOCASSEMBLESERVER with the name of your Docassemble server (e.g., `docs.legalaid.org`)\r\nand replace the text MYAPIKEY with an [API key](https://docassemble.org/docs/api.html#manage_api) that you generate on your Docassemble\r\nprofile. Get the API key by clicking on your email address, select Profile, and then \r\nOther Settings | API key.\r\n\r\nYou will see a new block on the page with the same interviews that you see when you visit\r\n/list on your Docassemble server.\r\n\r\n```\r\n<input type="hidden" id="da_api_url" value="https://MYDOCASSEMBLESERVER/api/list?key="/>\r\n<input type="hidden" id="da_api_key" value="MYAPIKEY" />\r\n<script type="text/javascript" src="https://MYDOCASSEMBLESERVER/packagestatic/docassemble.gbls/docassemble-ls.js">\r\n</script>\r\n\r\n<div class="book book_large" id="docassemble_container">\r\n    <div class="bookTabRow">\r\n        <ul class="tab_start_here htabs">\r\n        <li class="bookTabItem dynamicBookTabItem selected_book_tab">\r\n        <a class="select">Docassemble Interviews</a>\r\n        </li>\r\n        </ul>\r\n    </div>\r\n    <div class="bookPage">\r\n        <div class="dynamicBookContents tabs">\r\n                <div style="border: 0px; padding: 0px; margin: 0px;"><div class="form_container"><div class="listview_outer">\r\n                    <div id="interviews" class="datatable">\r\n                    </div>\r\n                </div></div></div>\r\n        </div>\r\n    </div>\r\n</div>\r\n```\r\n# Sending fields to Docassemble without displaying in Legal Server\r\nYou can create a whole tab block of fields that won\'t display in Legal Server but are still available to Docassemble,\r\nby creating an instruction with the contents:\r\n```\r\n<div id="docassemble-fields"></div>\r\n```\r\nSomewhere in the tab block that you want to hide.\r\n\r\n# Listviews\r\nAs of version .30, this module supports Legal Server Listviews. \r\nPlease check the ListView option "Show list title" in order to get labeled data into Docassemble. Every listview\r\nin the form section needs to be labeled for the module to be able to guess which label corresponds to which list view.\r\n\r\n# Filtering\r\n\r\nBy default, interviews will be filtered to match the metadata tag equalling the program name.\r\nAny interview tagged "everyone" will also be displayed.\r\n\r\n',
      long_description_content_type='text/markdown',
      author='Quinten Steenhuis',
      author_email='admin@admin.com',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=['docassemble.income', 'nameparser', 'usaddress'],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/gbls/', package='docassemble.gbls'),
     )

