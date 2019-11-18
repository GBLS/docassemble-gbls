from docassemble.base.core import DAList, DAEmpty
from docassemble.base.util import Individual

__all__ = ['HouseholdList']

class HouseholdList(DAList):
    def init(self, *pargs, **kwargs):
        super(HouseholdList, self).init(*pargs, **kwargs)
        self.object_type = Individual
    
    @property
    def spouse(self):
        for person in self.elements:
            if person.relationship.lower() in ['spouse','husband', 'wife','partner','unmarried partner','spouse/domestic partner']:
                return person
        return DAEmpty()
    
    @property
    def children(self):
        """ Returns list of direct children/step/foster children (not grandchildren) based on the relationship attribute."""
        return self.has_relationship(['child','son','daughter','foster child','stepchild','step child'])

    @property
    def guardians(self):
        """Returns legal guardians or parents"""
        return self.has_relationship( ['parent','guardian','father','mother',
                'legal guardian','step father','step mother','stepparent','step parent'])

    @property
    def grandchildren(self):
        """Returns grandchildren"""
        return self.has_relationship(['grandchild','grand child','grandson','granddaughter',
                'grand son','grand daughter'])
    
    @property
    def coclients(self):
        """Return a list of coclients"""
        return self.has_relationship(['co-client','coclient'])

    @property
    def siblings(self):
        """Return a list of siblings"""
        return self.has_relationship(['sibling','brother','sister','step sister','step brother',
            'stepsister','stepbrother','half brother','half sister','half sibling','foster brother',
            'foster sister','foster sibling'])
    
    def has_relationship(self, relationships):
        """Return a list of household memberships with the specified relationship attribute. Relationship may be a string or list of strings."""
        related = DAList(object_type=Individual, auto_gather=False,gathered=True)
        for person in self.elements:
            if isinstance(relationships, list):
                if person.relationship.lower() in relationships:
                    related.append(person)
            else:
                if person.relationship.lower() == relationships:
                    related.append(person)
        return related 
