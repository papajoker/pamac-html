import gi
gi.require_version('Pamac', '1.0')  # import xml /usr/share/gir-1.0/Pamac-1.0.gir
from gi.repository import GLib, Pamac

from PyQt5.QtCore import QObject



"""
    singleton 
"""

class Singleton:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

class Database(Singleton, QObject):
    
    def __init__(self):
        self.config = Pamac.Config(conf_path="/etc/pamac.conf")
        #self.config.set_enable_aur(True)  # is true
        self.db = Pamac.Database(config=self.config)
        self.db.enable_appstream()


print(Database().db.get_repos_names())
#help(Pamac.Database)
