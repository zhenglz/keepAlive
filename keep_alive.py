#!/usr/bin/env python

import os, sys
import psutil
import glob
import time
import platform
import subprocess as sp
from distutils.dir_util import copy_tree, remove_tree, mkpath


class KeepAlive(object):

    def __init__(self):

        self.params = {
          "TIME_GAP" : 600,
          "ORIGIN_LOCATION" : "C:/Program Files/Steam/game/dontstarve/data/DLC0001",
          "BACKUP_LOCATION" : "./",
          "MAXNUM_BACKUP"   : 10,
        }

        self.game_on_ = False
        self.game_last_state_ = False
        self.current_bkp_num_ = 0
        self.bkp_prefix_ = "Backup_"
        self.system_ = "Windows"
        self.restore_now_ = False
        self.backup_folders_ = []
        self.game_folder_empty_ = False

        try:
            self.system_ = platform.system()
        except OSError:
            print("*WARNING*" * 50)

    def read_params(self, fn="./parameters.dat"):
        if not os.path.exists(fn):
            print("*ERROR*"*50)
            print("The parameter file %s is not existed! Exit now!"%fn)
            print("You may close this window. Otherwise it will be closed in 20s. ")
            print("*ERROR*" * 50)
            time.sleep(20)

            #sys.exit(0)

        with open(fn) as lines:
            lines = [x for x in lines if "#" not in x]

            for s in lines:
                if s.split("=")[0] in self.params.keys():
                    self.params[s.strip("=")[0]] = \
                        s.strip("=")[-1].split("#")[0].strip("\"")

            self.params["TIME_GAP"] = int(self.params["TIME_GAP"])
            self.params["MAXNUM_BACKUP"] = int(self.params["MAXNUM_BACKUP"])

        return self

    def delete_backups(self, folder):

        remove_tree(folder)

        return self

    def detect_backups(self):

        """self.current_bkp_num_ = len(backups)

        if self.system_ in ["MacOS", "Linux"]:
            cmd = "ls -rt %s" % self.params["BACKUP_LOCATION"]
        elif self.system_ in ["Windows"]:
            cmd = "dir %s /O:D /T:C" % self.params["BACKUP_LOCATION"]
        else:
            cmd = "ls %s" % self.params["BACKUP_LOCATION"]"""

        self.backup_folders_ = os.listdir(self.params["ORIGIN_LOCATION"])

        return self

    def copy_files(self, source_folder, write_loc):

        copy_tree(source_folder, write_loc, preserve_symlinks=1)

        """if self.system_ in ["Linux", "MacOS"]:
            try:
                job = sp.Popen("cp -R %s %s"%(source_folder, write_loc), shell=True)
                job.communicate()
            except:
                pass
        elif self.system_ == "Windows":
            try:
                job = sp.Popen("xcopy %s %s /O /X /E /H /K /Y" %
                               (source_folder, write_loc),
                               shell=True)
                job.communicate()
            except:
                pass
        else:
            print("*WARNING*" * 50)
            print("OS is not detected. Will assume it is a Linux machine. ")
            print("*WARNING*" * 50)

            self.system_ = "Linux"
            self.copy_files(source_folder, write_loc)"""

        return self

    def write_backup(self):

        if len(self.backup_folders_):
            indexer = int(self.backup_folders_[-1].split("_")[-1]) + 1
        else:
            indexer = 0

        source_folder = self.params["ORIGIN_LOCATION"]
        write_loc = os.path.join(self.params["BACKUP_LOCATION"],
                                 self.bkp_prefix_, str(indexer))

        if write_loc not in os.listdir(self.params["BACKUP_LOCATION"]):
            mkpath(write_loc)

        self.copy_files(source_folder, write_loc)
        return self

    def restore_backup(self):

        write_loc     = self.params["ORIGIN_LOCATION"]
        source_folder = os.path.join(self.params["BACKUP_LOCATION"],
                                     self.bkp_prefix_,
                                     str(self.current_bkp_num_ + 1))

        self.copy_files(source_folder, write_loc)
        return self

    def detect_game_state(self):
        # TODO: this requires more work to do
        self.game_on_ = False
        self.restore_now_ = False

        if self.system_ in ["Windows"]:
            game_name = "dontstarve.exe"
        else:
            game_name = "dontstarve"

        procesess = [x.name() for x in psutil.process_iter()]
        if game_name in procesess:
            self.game_on_ = True
        else:
            self.game_on_ = False

        if self.game_last_state_ and self.game_on_:
            self.restore_now_ = True

        self.game_folder_empty_ = False
        if len(os.listdir(self.params["BACKUP_LOCATION"])) < 10:
            self.game_folder_empty_ = True

        return self

    def run_keep_alive(self):

        while True:
            self.game_last_state_ = self.game_on_
            # check game state
            self.detect_game_state()
            # read parameter files
            self.read_params()
            self.detect_backups()

            if self.game_on_:
                if self.current_bkp_num_ == self.params["MAXNUM_BACKUP"]:
                    self.delete_backups(self.backup_folders_[0])

                self.write_backup()

            if self.restore_now_ and self.game_folder_empty_:
                self.restore_backup()

            time.sleep(self.params["TIME_GAP"])


if __name__ == "__main__":

    print("Backup files now ... ... ")
    ka = KeepAlive()
    ka.run_keep_alive()

