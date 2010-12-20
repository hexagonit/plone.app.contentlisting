from zope.component import queryMultiAdapter
from interfaces import IContentListing, IContentListingObject
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from zope import interface
from zLOG import LOG, INFO
from plone.app.layout.icons.interfaces import IContentIcon
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import queryUtility


class ContentListing(object):
    """ An IContentListing implementation based on sequences of objects"""
    interface.implements(IContentListing)

    def __init__(self, sequence):
        self._basesequence = sequence

    def __getitem__(self, index):
        """`x.__getitem__(index)` <==> `x[index]`
        """
        return IContentListingObject(self._basesequence[index])

    def __len__(self):
        """ length of the resultset is equal to the length of the underlying
            sequence
        """
        return self._basesequence.__len__()

    def __iter__(self):
        """ let the sequence be iterable and whenever we look at an object, 
            it should be a ContentListingObject"""
        for obj in self._basesequence:
            yield IContentListingObject(obj)

    def __contains__(self, item):
        """`x.__contains__(item)` <==> `item in x`"""
        # It would be good if we could check this without waking all objects
        for i in self:
            if i == item:
                return True
        return False

    def __lt__(self, other):
        """`x.__lt__(other)` <==> `x < other`"""
        raise NotImplementedError

    def __le__(self, other):
        """`x.__le__(other)` <==> `x <= other`"""
        raise NotImplementedError

    def __eq__(self, other):
        """`x.__eq__(other)` <==> `x == other`"""
        raise NotImplementedError

    def __ne__(self, other):
        """`x.__ne__(other)` <==> `x != other`"""
        raise NotImplementedError

    def __gt__(self, other):
        """`x.__gt__(other)` <==> `x > other`"""
        raise NotImplementedError

    def __ge__(self, other):
        """`x.__ge__(other)` <==> `x >= other`"""
        raise NotImplementedError

    def __add__(self, other):
        """`x.__add__(other)` <==> `x + other`"""
        raise NotImplementedError

    def __mul__(self, n):
        """`x.__mul__(n)` <==> `x * n`"""
        raise NotImplementedError

    def __rmul__(self, n):
        """`x.__rmul__(n)` <==> `n * x`"""
        raise NotImplementedError

    def __getslice__(self, i, j):
        """`x.__getslice__(i, j)` <==> `x[i:j]`
        Use of negative indices is not supported.
        Deprecated since Python 2.0 but still a part of `UserList`.
        """
        return IContentListing(self._basesequence[i:j])



class BaseContentListingObject(object):
    """A baseclass for the different types of contentlistingobjects
        To avoid duplication of the stuff that is not implementation-specific
    """
    
    def __eq__(self, other):
        """For comparing two contentlistingobject"""
        other = IContentListingObject(other)
        return self.uniqueIdentifier() == other.uniqueIdentifier()

    def ContentTypeClass(self):
        """A normalised type name that identifies the object in listings.
        used for CSS styling"""
        return "contenttype-" + queryUtility(IIDNormalizer).normalize(
            self.Type())
            
    def ReviewStateClass(self):
        """A normalised review state string for CSS styling use in listings."""
        return "state-" + queryUtility(IIDNormalizer).normalize(
            self.review_state())

    def appendViewAction(self):
        """decide whether to produce a string /view to append to links
        in results listings"""
        try:
            types = self._brain.portal_properties.site_properties \
                        .typesUseViewActionInListings
        except AttributeError:
            return ''
        if self.Type() in types:
            return "/view"
        return ''




