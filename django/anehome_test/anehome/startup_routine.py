from anehome_test.anehome.settings.settings import BASE_DIR
from anehome_test.anehome.logic.shapshot_manager import SnapshotManager
from anehome_test.anehome.logic.avaiable_site_handlers import init_site_handlers, SITE_CODE_TO_HANDLER
import sys
import plotly.plotly as py
from anehome_test.anehome.global_status import GlobalStatus

snapshot_manager = 123

def startup_routine():
    print('startup_routine runned!')

    global snapshot_manager

    GlobalStatus()

    init_site_handlers()
    snapshot_manager = SnapshotManager()
    snapshot_manager.scan_all_snapshots()
    print('snapshot manager:', snapshot_manager)

    GlobalStatus().setstatus('Свободен')

    # snapshot_manager.get_test_snap()

    snapshot_manager.get_new_snap_threaded()

    # snapshot_manager.update_plot_pic()
