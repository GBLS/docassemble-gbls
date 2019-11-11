from docassemble.base.core import DAObject, DAList, DADict, DAOrderedDict
from docassemble.base.util import as_datetime, Individual, Person, from_b64_json
import docassemble.base.functions
from nameparser import HumanName
import re
import usaddress
from email.utils import parseaddr # parse email addresses
from decimal import Decimal

class LegalServerFields(DADict):
    """Class to handle Legal Server fields passed with JavaScript as a base64 encoded JSON object into the URL argument 'args'.
    Constructor may be called with url_args=url_args or .using(url_args=url_args). Optionally specify client(Individual), advocate(Individual), pbadvocate(Individual), initiator(Individual) and adverse_parties (DAList.using(object_type=Person))"""
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
            ls_args = from_b64_json(url_args.get('args',None)+'===') # Add padding that might get stripped away
        
        #if ls_args is None:
            # self.elements = dict()
        #    return # Don't do anything if we didn't get a URL args argument
        self.elements = ls_args

        if ls_args.get('case_email'):
            self.case_email = ls_args.get('case_email')
        if ls_args.get('id'):
            self.casenumber = ls_args.get('id')
        if ls_args.get('legal_problem_code'):
            self.legal_problem_code = ls_args.get('legal_problem_code')
        if ls_args.get('special_legal_problem_code'):
            self.special_legal_problem_code = ls_args.get('special_legal_problem_code')
        if ls_args.get('name',False):
            self.client_name_parts = HumanName(ls_args.get('name',''))
        if ls_args.get('sidebar_advocate',False):
            self.advocate_name_parts = HumanName(ls_args.get('sidebar_advocate',''))
        if ls_args.get('initiating_user',False):
            self.initiator_name_parts = HumanName(ls_args.get('initiating_user',''))
        if ls_args.get('pro_bono_attorney_s_name',False):
            self.pbadvocate_name_parts = HumanName(ls_args.get('pro_bono_attorney_s_name',''))
        if hasattr(self,'client'):
            self.load_client(self.client)
        if hasattr(self,'advocate'):
            self.load_advocate(self.advocate)
        if hasattr(self,'initiator'):
            self.load_initiator(self.initiator)
        if hasattr(self, 'adverse_parties'):
            self.load_adverse_parties(self.adverse_parties)
        if hasattr(self, 'pbadvocate'):
            self.load_pbadvocate(self.pbadvocate)
        if hasattr(self, 'household'):
            self.load_household(self.household)
        if hasattr(self, 'income'):
            self.load_income(self.income)

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
                    client.address.state = address_parts[0].get('StateName')
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
        if self.elements.get('social_security',False):
            client.ssn = self.elements.get('social_security','')
        if self.elements.get('social_security',False) and client.ssn != '':
            client.ssn_last_4 = client.ssn[-4:]
        if self.elements.get('language',False):
            if self.elements.get('language','') == 'English':
                client.language = 'en'
            if self.elements.get('language','') == 'Spanish':
                client.language = 'es'
            if self.elements.get('language','') == 'Vietnamese':
                client.language = 'vi'
            if self.elements.get('language','') == 'Chinese':
                client.language = 'zo'
        client.gender = self.elements.get('gender','').lower()
                
    def load_advocate(self, advocate):
        """Loads up the Individual object (e.g., advocate) with fields from Legal Server. Fills in name and email address attributes"""
        try:
            advocate.name.first = self.advocate_name_parts['first']
            advocate.name.last = self.advocate_name_parts['last']
            advocate.name.middle = self.advocate_name_parts['middle']
            advocate.name.suffix = self.advocate_name_parts['suffix']
            advocate.program = self.elements.get('sidebar_assignment_program','')
        except:
            pass
        try:
            email = parseaddr(self.elements.get('initiating_user_email_address'))
            advocate.email  = email[1]
        except:
            advocate.email = self.elements.get('initiating_user_email_address')

    def load_initiator(self, initiator):
        """Loads up the Individual object (e.g., initiator) with fields from Legal Server. Fills in name and email address attributes"""
        try:
            initiator.name.first = self.initiator_name_parts['first']
            initiator.name.last = self.initiator_name_parts['last']
            initiator.name.middle = self.initiator_name_parts['middle']
            initiator.name.suffix = self.initiator_name_parts['suffix']
            initiator.program = self.elements.get('sidebar_assignment_program','')
            initiator.email = self.elements.get('initiating_user_email_address','')
        except:
            pass
        
    def load_pbadvocate(self, pbadvocate):
        """Loads up the Individual objection (e.g., pbadvocate) with fields from Legal Server. Fills in name, firm, address, phone, and email attributes"""
        if self.elements.get('pro_bono_attorney_s_name',False):
            try: 
                pbadvocate.name.first = self.pbadvocate_name_parts['first']
                pbadvocate.name.last = self.pbadvocate_name_parts['last']
                pbadvocate.name.middle = self.pbadvocate_name_parts['middle']
                pbadvocate.name.suffix = self.pbadvocate_name_parts['suffix']
            except:
                pass
        if self.elements.get('pro_bono_attorney_s_email',False):
            pbadvocate.email = self.elements.get('pro_bono_attorney_s_email')
        if self.elements.get('pro_bono_attorney_s_phone',False):
            pbadvocate.phone_number = self.elements.get('pro_bono_attorney_s_phone')
        if self.elements.get('pro_bono_attorney_s_firm',False):
            pbadvocate.firm = self.elements.get('pro_bono_attorney_s_firm')
        if self.elements.get('pro_bono_attorney_s_salutation',False):
            pbadvocate.salutation = self.elements.get('pro_bono_attorney_s_salutation')
        
        if self.elements.get('pro_bono_attorney_s_address',False):
            pbaddress_parts = usaddress.tag(self.elements.get('pro_bono_attorney_s_address'))
            try:
                if pbaddress_parts[1].lower() == 'street address':
                    pbadvocate.address.address = pbaddress_parts[0].get('AddressNumber','') + ' ' + pbaddress_parts[0].get('StreetName','')  + ' ' + pbaddress_parts[0].get('StreetNamePostType', '')
                    pbadvocate.address.unit = pbaddress_parts[0].get('OccupancyType', '') + ' ' + pbaddress_parts[0].get('OccupancyIdentifier')
                    pbadvocate.address.city = pbaddress_parts[0].get('PlaceName')
                    pbadvocate.address.zip = pbaddress_parts[0].get('ZipCode')
                    pbadvocate.address.state = pbaddress_parts[0].get('StateName')
                else:
                    raise Exception('We expected a Street Address. Fall back to Google Geolocation')
            except:
                pbadvocate.address.address = self.elements.get('pro_bono_attorney_s_address','')
                pbadvocate.address.geolocate(self.elements.get('pro_bono_attorney_s_address',''))

    def load_adverse_parties(self,adverse_parties):
        """Try to set the provided object to the corresponding Legal Server listview"""
        adverse_list = self.elements.get('Adverse Parties')
        if not adverse_parties:
            return self.fallback_load_adverse_parties(adverse_parties)
        for person in adverse_list:
            ap = adverse_parties.appendObject() # Person()
            ap.name.text = person.get('Adverse Party Name')
            ap.birthdate = as_datetime(person.get('Date of Birth')) if not person.get('Date of Birth') == 'N/A' else None
            ap.gender = person.get('Gender').lower() if not person.get('Gender') == 'N/A' else None
            ap.race = person.get('Race') if not person.get('Race') == 'N/A' else None
            try:
                self.parse_address(person.get('Adverse Party Address'),ap.address)
            except:
                ap.address.address = person.get('Adverse Party Address')
                ap.address.geolocate(person.get('Adverse Party Address'))
            # adverse_parties.add(ap)

    def load_income(self,income):
        """Load income from the Financial Information listview"""
        income_list = self.elements.get('Income',[])
        for source in income_list:
            inc = income.appendObject()
            inc.type = source.get('Type of Income')
            # The conversion below could be made more robust (internationally), but this is fine for GBLS's site
            # For alternative, add dependency to price-parser and Python 3.6+
            inc.value = Decimal(source.get('Amount','').strip(' $'))
            freq = source.get('Frequency')
            inc.owner = source.get('Family Member')

            if freq == 'Annually':
                inc.period = 1
            elif freq == 'Monthly':
                inc.period = 12
            elif freq == 'Quarterly':
                inc.period = 4
            elif freq == 'Semi-Monthly':
                inc.period = 6
            elif freq == 'Biweekly':
                inc.period = 26
            elif freq == 'Weekly':
                inc.period = 52
            else:
                inc.value = Decimal(source.get('Monthly Amount').strip(' $'))
                inc.period = 12 # Default to monthly income if something goes wrong

    def load_household(self, household):
        """Try to set the provided object to the corresponding Legal Server listview"""
        household_list = self.elements.get('Family Members',[])
        for person in household_list:
            hh = household.appendObject()
            name_parts = HumanName(person.get('Name'))
            hh.name.first = name_parts.first
            hh.name.last = name_parts.last
            hh.name.middle = name_parts.middle
            hh.name.suffix = name_parts.suffix

            hh.name.text = person.get('Adverse Party Name')
            hh.birthdate = as_datetime(person.get('Date of Birth')) if not person.get('Date of Birth') == 'N/A' else None
            hh.gender = person.get('Gender').lower() if not person.get('Gender') == 'N/A' else None
            hh.race = person.get('Race') if not person.get('Race') == 'N/A' else None
            hh.relationship = person.get('Relationship')

            # household.add(hh)

    @staticmethod
    def parse_address(address_text, address_obj):
        """Convert a text address like '123 Main St, Boston, MA' to a Docassemble Address object. Will throw an exception if not given a valid street address."""
        address_parts = usaddress.tag(address_text)
        if address_parts[1].lower() == 'street address':
            address_obj.address = address_parts[0].get('AddressNumber','') + ' ' + address_parts[0].get('StreetName','')  + ' ' + address_parts[0].get('StreetNamePostType', '')
            address_obj.unit = address_parts[0].get('OccupancyType', '') + ' ' + address_parts[0].get('OccupancyIdentifier')
            address_obj.city = address_parts[0].get('PlaceName')
            address_obj.zip = address_parts[0].get('ZipCode')
            address_obj.state = address_parts[0].get('StateName')
        else:
            raise Exception("Not a valid street address")

    def fallback_load_adverse_parties(self, adverse_parties):
        """If there is not a listview labeled 'Adverse Parties', fall back on parsing the adverse_parties (display only) field."""

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
