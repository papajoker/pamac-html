"""
sur-class for Pamac packages
"""

import gi, sys
from gi.repository import GObject
gi.require_version('Pamac', '1.0')
from gi.repository import Pamac
# import xml /usr/share/gir-1.0/Pamac-1.0.gir

class PackageGObject(GObject.Object):
    """use GObject.Object.props as attibutes"""
    
    TO_NOTHING, TO_ADD, TO_REMOVE = range(3)

    def __init__(self):
        self.commit = self.TO_NOTHING

    def __dir__(self):
        return dir(self.props) + ['commit']

    def __getattr__(self, key):
        #print('__getattr__',key)
        try:
            return self.get_property(key)
        except TypeError as err:
            #raise err
            return ""

    def __call__(self, arg):
        """use for auto-format in text ?"""
        return self.get_property(arg) 

    def __iter__(self):
        for p in self.props:
            yield p.name, self.get_property(p.name)

    def __len__(self):
        return len(self.props)

    def __bool__(self) ->bool:
        """test if object:"""
        return self.name != ""

    def __eq__(self, pkg) ->bool:
        return self.props.size == pkg.props.size

    def __lt__(self, pkg) ->bool:
        return self.props.size < pkg.props.size

    def __le__(self, pkg) ->bool:
        return self.props.size <= pkg.props.size

    def __gt__(self, pkg) ->bool:
        return self.props.size > pkg.props.size

    def __ge__(self, pkg) ->bool:
        return self.props.size >= pkg.props.size

    def __neg__(self):
        self.commit = self.TO_REMOVE
        return self;

    def __pos__(self):
        print(f"+: {self.commit} ...")
        self.commit = self.TO_ADD
        return self

    def __invert__(self):
        print(f"invert: {self.commit} ...")
        if self.commit == self.TO_ADD:
            self.commit = self.TO_REMOVE
        else:
            if self.commit == self.TO_REMOVE:
                self.commit = self.TO_ADD
        return self

    def __repr__(self):
        result = "{"
        for attr, val in self:
            if val:
                result += f"({attr}=\"{val}\"),"
        result = result[:-1] + "}"
        return result

    @classmethod
    def surClass(cls, package_pamac: GObject.Object):
        """Change type of Pamac.Package for sur-class"""
        package_pamac.__class__ = cls
        package_pamac.commit = cls.TO_NOTHING
        return package_pamac

class PackageSearch(Pamac.Package, PackageGObject):
    """ package after search"""
    '''
    @classmethod
    def surClass(cls, package_pamac: Pamac.Package):
        """Change type of Pamac.Package for sur-class"""
        package_pamac.__class__ = cls
        return package_pamac'''

    '''def __dir__(self):
        return dir(self.props) + ['installed']'''

    @property
    def size(self) ->str:
        """ humain size"""
        return self.to_humain_size(self.get_size())

    '''@property
    def version(self) ->bool:
        print('get_version')
        try:
            return self.props.version
        except AttributeError:
            return self.props.installed_version'''

    @property
    def is_installed(self) ->bool:
        try:
            return self.props.installed_version != ""
        except AttributeError:
            return False

    @property
    def download_size(self) ->str:
        """ humain size"""
        return self.to_humain_size(self.get_download_size())

    @classmethod
    def to_humain_size(cls, size: int) ->str:
        """ humain sizes"""
        if size < 1:
            return ""
        power = 1000
        n = 1
        dic_powern = {1:'ko', 2:'Mo', 3:'Go', 4:'To'}

        if size <= power**2:
            size /= power
            return f"{float(round(size*10))/10}{dic_powern[n]}"
        else:
            while size > power:
                n  += 1
                size /= power**n
            return f"{float(round(size*10))/10}{dic_powern[n]}"

class PackageDetail(Pamac.PackageDetails, PackageSearch):
    """ package with details"""
    pass

class PackageAURSearch(Pamac.AURPackage, PackageGObject):
    """ 
    package aur search details
        #['desc', 'installed_version', 'name', 'popularity', 'version']
    """

    @property
    def is_installed(self) ->bool:
        return self.props.installed_version

    @property
    def popularity(self):
        return float(round(self.props.popularity*10))/10
