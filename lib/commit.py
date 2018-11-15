#!/usr/bin/env python

import gi
gi.require_version('Pamac', '1.0')  # import xml /usr/share/gir-1.0/Pamac-1.0.gir
from gi.repository import GLib, Pamac


#import sys
#import re

class Commit:

    def __init__(self, db, post_message):
        self.data = None
        self.loop = None
        self.post_message = post_message

        self.transaction = self.transaction = Pamac.Transaction(database=db)

        self.transaction.connect("emit-action", self.on_emit_action, self.data)
        self.transaction.connect("emit-action-progress", self.on_emit_action_progress, self.data)
        self.transaction.connect("emit-hook-progress", self.on_emit_hook_progress, self.data)
        self.transaction.connect("emit-error", self.on_emit_error, self.data)
        self.transaction.connect("emit-warning", self.on_emit_warning, self.data)
        self.transaction.connect("finished", self.on_trans_finished, self.data)

    def __enter__(self):
        if not self.transaction.get_lock():
            raise Exception("pamac-system-daemon running")
        self.loop = GLib.MainLoop()
        return self

    def __exit__(self, type, value, traceback):
        try:
            self.loop.quit()
            self.transaction.unlock()
            self.transaction.quit_daemon()
        except:
            pass

    def run(self, to_install=[], to_remove=[], to_load=[]):
        if self.transaction.get_lock():
            self.transaction.start(to_install, to_remove, to_load, [], [], [])
            # launch a loop to wait for finished signal to be emitted
            self.loop.run()

    def on_trans_finished(self, transaction, success, data):
        print(success)
        self.post_message('END.', 6)
        self.loop.quit()

    def on_emit_error(self, transaction, message, details, details_length, data):
        #print("------")
        if details_length > 0:
            print(f"{message}:")
            for detail in details:
                print(detail)
                self.post_message(detail, 4)
        else:
            self.post_message(message, 4)
            print(message)
        self.loop.quit()
        '''sans doute supp 2 lignes suivantes car dans __exit__()
        A tester ...'''
        #transaction.unlock()
        #transaction.quit_daemon()

    def on_emit_action(self, transaction, action, data):
        print("on_emit_action", action)
        self.post_message(action, 1)

    def on_emit_hook_progress(self, transaction, action, details, status, progress, data):
        #print(f"{action} {details} {status}")
        self.post_message(f"{action} {details} {status}", 3)


    def on_emit_action_progress(self, transaction, action, status, progress, data):
        print("on_emit_action_progress", f"{action} {status}")
        if not status.startswith("0"):
            self.post_message(f"::{action} {status}", 3)

    def on_emit_warning(self, transaction, message, data):
        print("on_emit_warning", message)
        self.post_message(message, 5)




'''
    def post_message(self, msg: str, status):
        switcher = {
            1: "-> ",
            2: ":: ",
            3: "   ",
            4: "!!! ",
            5: "! ",
            6: "",
        }   
        self.text.append(f"{switcher.get(status, '')}{msg}")
        self.statusBar().showMessage(msg, 2000)
        if status == 4:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, "pamac", msg)

    def commit(self):
        """pacman commit"""
        self.parse_edit()
        self.text.setReadOnly(True)
        try:
            with Commit(self.db, self.post_message) as mycommit:
                mycommit.run(to_install=self.to_install, to_remove=self.to_remove, to_load=self.to_load  )
        except Exception as ex:
            print("transaction.get_lock(): False", "\nwait "+ex.args[0])
            QMessageBox.critical(self, "pamac", "ERROR: "+ex.args[0])
        self.text.setReadOnly(False)

 '''
