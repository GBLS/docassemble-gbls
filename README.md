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