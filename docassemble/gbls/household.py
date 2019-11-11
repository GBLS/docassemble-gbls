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
            if person.relationship.lower() in ['spouse','husband', 'wife','partner']:
                return person
        return DAEmpty()
    
    @property
    def children(self):
        """ Returns list of direct children/step/foster children (not grandchildren) based on the relationship attribute."""
        children = DAList(object_type=Individual, auto_gather=False, gathered=True)
        for person in self.elements:
            if person.relationship.lower() in ['child','son','daughter','foster child','stepchild','step child']:
                children.append(person)
        return children

    @property
    def guardians(self):
        """Returns legal guardians or parents"""
        guardians = DAList(object_type=Individual, auto_gather=False,gathered=True)
        for person in self.elements:
            if person.relationship.lower() in ['guardian','father','mother',
                'legal guardian','step father','step mother','stepparent','step parent']:
                guardians.append(person)
        return guardians

    