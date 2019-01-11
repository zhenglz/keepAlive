from .keep_alive import KeepAlive
import time
import os

if __name__ == "__main__":

    ka = KeepAlive()
    ka.params = ka.read_params("./parameters.dat")

    while True:
        gamefolder = "dontstarve"
        bkp_loc = os.path.join(ka.params["BACKUP_LOCATION"], gamefolder)

        if os.path.isdir(bkp_loc):
            if os.path.isdir(os.path.join(bkp_loc, "_prev")):
                ka.delete_backups(os.path.join(bkp_loc, "_prev"))

            ka.copy_files(bkp_loc, os.path.join(bkp_loc, "_prev"))
            ka.delete_backups(bkp_loc)

        ka.copy_files(ka.params["ORIGIN_LOCATION"], bkp_loc)

        time.sleep(ka.params["TIME_GAP"])
