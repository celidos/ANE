from anehome.settings.settings import BASE_DIR
import re
import os
import datetime
import pandas as pd

ANE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))
SNAPSHOTS_DIR = os.path.join(ANE_DIR, 'snapshots')

class FreshTablesHolder():
    def __init__(self):
        self.fresh_snapshot_name = None
        self.fresh_snapshot_date = None
        self.fresh_snapshot_dir = None
        self.snapshot_folder_list = None

        self.gks_table = None

    def scan_all_snapshots(self):

        print(SNAPSHOTS_DIR)

        self.snapshot_folder_list = next(os.walk(SNAPSHOTS_DIR))[1]

        for snapshot_folder_name in self.snapshot_folder_list:
            print(snapshot_folder_name)
            sr = re.search('\Asnap_(?P<year>\d+)_(?P<month>\d+)_(?P<day>\d+)__(?P<hour>\d+)_(?P<minute>\d+)_(?P<second>\d+)$',
                           snapshot_folder_name)
            if sr:
                snapdate = datetime.datetime(year=int(sr.group('year')),
                                             month=int(sr.group('month')),
                                             day=int(sr.group('day')),
                                             hour=int(sr.group('hour')),
                                             minute=int(sr.group('minute')),
                                             second=int(sr.group('second')))
                if (self.fresh_snapshot_date and self.fresh_snapshot_date < snapdate) or\
                        (self.fresh_snapshot_date is None):
                    self.fresh_snapshot_date = snapdate
                    self.fresh_snapshot_name = snapshot_folder_name

        print('fresh name =', self.fresh_snapshot_name)

        if self.fresh_snapshot_name:
            self.fresh_snapshot_dir = os.path.join(SNAPSHOTS_DIR, self.fresh_snapshot_name)

            self.gks_table = pd.read_csv(os.path.join(self.fresh_snapshot_dir,
                                                      'gks_acc.csv'))

            print(self.gks_table)




        #     re.match()

        pass

fresh_table_holder = FreshTablesHolder()

def startup_routine():
    fresh_table_holder.scan_all_snapshots()

    pass
