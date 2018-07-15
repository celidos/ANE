from anehome.settings.settings import BASE_DIR
import re
import os

ANE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))
SNAPSHOTS_DIR = os.path.join(ANE_DIR, 'snapshots')

def scan_all_snapshots():
    snapshot_folder_list = next(os.walk('.'))[1]
    fresh_snapshot_name = None

    print(SNAPSHOTS_DIR)

    # for snapshot_folder_name in snapshot_folder_list:
    #     re.match()


    pass

def startup_routine():
    scan_all_snapshots()

    pass
