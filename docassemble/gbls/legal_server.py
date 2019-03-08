from docassemble.base.core import DAObject, DAList, DADict, DAOrderedDict
from docassemble.base.util import as_datetime, Individual, Person, from_b64_json
import docassemble.base.functions
from nameparser import HumanName
import re
import usaddress

class LegalServerFields(DADict):
    """Class to handle Legal Server fields passed with JavaScript as a base64 encoded JSON object into the URL argument 'args'.
    Constructor may be called with url_args=url_args or .using(url_args=url_args). Optionally specify client(Individual), advocate(Individual), and adverse_parties (DAList.using(object_type=Person))"""
    def init(self, *pargs, **kwargs):
        super(LegalServerFields, self).init(*pargs, **kwargs) 
        self.auto_gather = False
        self.gathered = True
        if hasattr(self, 'url_args') and self.url_args.get('args',False):
            self.initialize(self.url_args)
        else:
            self.empty_args = True

    def initialize(self, url_args):
        """Load URL args and any objects that may have been passed to .using or set as attributes on the LegalServerFields object"""
        # We expect that the 'args' URL parameter will be a base64 encoded JSON object
        if not url_args.get('args',False):
            return
        else:
            ls_args = from_b64_json(url_args.get('args',None))
        
        #if ls_args is None:
            # self.elements = dict()
        #    return # Don't do anything if we didn't get a URL args argument
        self.elements = ls_args

        if ls_args.get('case_email'):
            self.case_email = ls_args.get('case_email')
        if ls_args.get('name',False):
            self.client_name_parts = HumanName(ls_args.get('name',''))
        if ls_args.get('sidebar_advocate',False):
            self.advocate_name_parts = HumanName(ls_args.get('sidebar_advocate',''))
        if hasattr(self,'client'):
            self.load_client(self.client)
        if hasattr(self,'advocate'):
            self.load_advocate(self.advocate)
        if hasattr(self, 'adverse_parties'):
            self.load_adverse_parties(self.adverse_parties)

    def load_client(self,client):
        """Loads up the Individual object (e.g., client) with fields from Legal Server. Fills in birthdate, name, email, and address attributes"""
        try:
            client.name.first = self.client_name_parts['first']
            client.name.last = self.client_name_parts['last']
            client.name.suffix = self.client_name_parts['suffix']
            client.name.middle = self.client_name_parts['middle']

            address_parts = usaddress.tag(self.elements.get('full_address'))
            try:
                if address_parts[1].lower() == 'street address':
                    client.address.address = address_parts[0].get('AddressNumber','') + ' ' + address_parts[0].get('StreetName','')  + ' ' + address_parts[0].get('StreetNamePostType', '')
                    client.address.unit = address_parts[0].get('OccupancyType', '') + ' ' + address_parts[0].get('OccupancyIdentifier')
                    client.address.city = address_parts[0].get('PlaceName')
                    client.address.zip = address_parts[0].get('ZipCode')
                else:
                    raise Exception('We expected a Street Address. Fall back to Google Geolocation')
            except:
                client.address.address = self.elements.get('full_address','')
                client.address.geolocate(self.elements.get('full_address',''))
        except:
            pass
        if self.elements.get('date_of_birth', False):
            client.birthdate = as_datetime(self.elements.get('date_of_birth'))
        client.email = self.elements.get('sidebar_email','')
        client.mobile_number = self.elements.get('sidebar_mobile_phone','')
        client.phone_number = self.elements.get('sidebar_home_phone','')

    def load_advocate(self, advocate):
        """Loads up the Individual object (e.g., advocate) with fields from Legal Server. Fills in name and email address attributes"""
        try:
            advocate.name.first = self.advocate_name_parts['first']
            advocate.name.last = self.advocate_name_parts['last']
            advocate.name.middle = self.advocate_name_parts['middle']
            advocate.name.suffix = self.advocate_name_parts['suffix']
        except:
            pass
        advocate.email = self.elements.get('initiating_user_email_address')

    def load_adverse_parties(self,adverse_parties):
        """Loads up the Person object (e.g., adverse_party) with fields from Legal Server. Fills in name"""
        adverse_text = self.elements.get('adverse_parties','')
        if adverse_text == '' or adverse_text is None:
            return

        # This regex will match one or more Adverse Parties from Legal Server
        # To help avoid a "read only" regex
        # Group 0 (the outermost parens) should be a single Adverse party, with the + letting us match multiples. Further parsed inside in groups 1,2,3
        # Group 1 matches the text AP:
        # Group 2 is the actual party name
        # Group 3 matches the remaining address info for the AP, which is often left blank and we won't parse for now
        party_regex = r"((AP:)(.*?)(,.*?,.*?))+" 

        matches = re.findall(party_regex, self.elements.get('adverse_parties',''))

        for match in matches:
            ap = Person()
            ap.name.text = match[2] # Index 2 of each match will be the actual name of the AP
            # adverse_parties.appendObject(name.text=match[2])
            adverse_parties.append(ap)