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
            if person.relationship.lower() == 'spouse':
                return person
            elif person.relationship.lower() == 'husband':
                return person
            elif person.relationship.lower() == 'wife':
                return person
            elif person.relationship.lower() == 'partner':
                return person
        return DAEmpty()
    
    @property
    def children(self):
        """ Returns list of direct children/step/foster children (not grandchildren) based on the relationship attribute."""
        children = DAList(object_type=Individual, auto_gather=False, gathered=True)
        for person in self.elements:
            if (person.relationship.lower() == 'child' or 
                person.relationship.lower() == 'son' or 
                person.relationship.lower() == 'daughter' or
                person.relationship.lower() == 'foster child' or
                person.relationship.lower() == 'stepchild' or
                person.relationship.lower() == 'step child'):
                x = children.appendObject()
                x = person
        return children