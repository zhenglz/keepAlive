from keep_alive import KeepAlive
import time
import os
#import psutil

def main():

    ka = KeepAlive()
    ka.params = ka.read_params("./parameters.dat")
	
    print("Backup now")

    while True:
        gamefolder = "dontstarve"
        bkp_loc = os.path.join(ka.params["BACKUP_LOCATION"], gamefolder)

        if os.path.isdir(bkp_loc):
            prev = os.path.join(ka.params["BACKUP_LOCATION"], gamefolder+"_prev")
            if os.path.isdir(prev):
                ka.delete_backups(prev)
                time.sleep(5)
                print("Backup/%s_prev exists, delete it."%gamefolder)

            ka.copy_files(bkp_loc, prev)
            time.sleep(5)
            ka.delete_backups(bkp_loc)
            time.sleep(5)
            
        print("Working: backup files now... ")
        ka.copy_files(ka.params["ORIGIN_LOCATION"], bkp_loc)

        print("Sleep here ... ")
        time.sleep(ka.params["TIME_GAP"])

main()

