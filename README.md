# GBLS Module

This package is the beginning of a collection of standard includes for Greater
Boston Legal Services.

It provides `basic-questions-gbls.yml` and `legal_server.py`, which
creates some standard objects and fills in their variables with data from
Legal Server, when launched from Legal Server.

Attributes that are filled in include name, address, email, and phone number, using the
standard Individual attribute names.

To use (and add the objects `client`, `advocate`, and `adverse_parties`) 
include `docassemble.gbls:basic-questions-gbls.yml`

E.g., when you include `docassemble.gbls:basic-questions-gbls.yml`, you will have
the following attributes available to you:

* client
* client.full_name()
* client.name.first / client.name.middle / client.name.last / client.name.suffix
* client.address.address, client.address.zip, etc / client.address_block()
* client.phone_number
* client.mobile_number
* client.email
* client.birth_date

Name fields and email will also be available for `advocate`. adverse_parties will
be a DAList of Persons, with adverse_party[i].name.text and adverse_party[i].full_name()
available. Address of adverse parties is not parsed.

# Integrating with Legal Server

After you install this package on your Docassemble Server, create a new instruction
block on the case page with the contents below.

Replace both instances of MYDOCASSEMBLESERVER with the name of your Docassemble server (e.g., `docs.legalaid.org`)
and replace the text MYAPIKEY with an [API key](https://docassemble.org/docs/api.html#manage_api) that you generate on your Docassemble
profile. Get the API key by clicking on your email address, select Profile, and then 
Other Settings | API key.

You will see a new block on the page with the same interviews that you see when you visit
/list on your Docassemble server.

```
<input type="hidden" id="da_api_url" value="https://MYDOCASSEMBLESERVER/api/list?key="/>
<input type="hidden" id="da_api_key" value="MYAPIKEY" />
<script type="text/javascript" src="https://MYDOCASSEMBLESERVER/packagestatic/docassemble.gbls/docassemble-ls.js">
</script>

<div class="book book_large" id="docassemble_container">
    <div class="bookTabRow">
        <ul class="tab_start_here htabs">
        <li class="bookTabItem dynamicBookTabItem selected_book_tab">
        <a class="select">Docassemble Interviews</a>
        </li>
        </ul>
    </div>
    <div class="bookPage">
        <div class="dynamicBookContents tabs">
                <div style="border: 0px; padding: 0px; margin: 0px;"><div class="form_container"><div class="listview_outer">
                    <div id="interviews" class="datatable">
                    </div>
                </div></div></div>
        </div>
    </div>
</div>
```
# Sending fields to Docassemble without displaying in Legal Server
You can create a whole tab block of fields that won't display in Legal Server but are still available to Docassemble,
by creating an instruction with the contents:
```
<div id="docassemble-fields"></div>
```
Somewhere in the tab block that you want to hide.

# Listviews
As of version .30, this module supports Legal Server Listviews. 
Please check the ListView option "Show list title" in order to get labeled data into Docassemble. Every listview
in the form section needs to be labeled for the module to be able to guess which label corresponds to which list view.

# Filtering

By default, interviews will be filtered to match the metadata tag equalling the program name.
Any interview tagged "everyone" will also be displayed.

