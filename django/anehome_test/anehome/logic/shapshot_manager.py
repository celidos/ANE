from anehome_test.anehome.settings.settings import BASE_DIR
from anehome_test.anehome.logic.snapshot import Snapshot
from anehome_test.anehome.logic.avaiable_site_handlers import init_site_handlers, SITE_CODE_TO_HANDLER
import os
from anehome_test.anehome.global_status import GlobalStatus
from anehome_test.anehome.logic import standard_food_basket as sfb

import plotly.plotly as py
import plotly.offline as opy
import plotly.graph_objs as go

from matplotlib import pyplot as plt

from anehome_test.anehome.logic.avaiable_site_handlers import SITE_HANDLERS

from multiprocessing.pool import ThreadPool
from threading import Thread
import threading

ANE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))
SNAPSHOTS_DIR = os.path.join(ANE_DIR, 'snapshots')


class SnapshotManager:
    def __init__(self):
        self.snapshots = {}
        self.fresh_snapshot_date = None
        self.fresh_snapshot_ref = None
        self.can_make_snaps = True

    def add_snap(self, newsnap):
        if newsnap.is_valid():
            print('valid snapshot!')
            self.snapshots[newsnap.snap_date] = newsnap

            print('snapshot: {}'.format(newsnap.snap_date))

            if (self.fresh_snapshot_date and self.fresh_snapshot_date < newsnap.snap_date) or \
                    (self.fresh_snapshot_date is None):
                print('got fresh snapshot!')
                if set(newsnap.info['done']).issuperset(set(['globus', 'perekrestok', 'okey', 'utkonos'])):
                    self.fresh_snapshot_date = newsnap.snap_date
                    self.fresh_snapshot_ref = newsnap

    def scan_all_snapshots(self):
        snapshot_folder_list = next(os.walk(SNAPSHOTS_DIR))[1]

        for snapshot_folder_name in snapshot_folder_list:
            newsnap = Snapshot(snap_folder_name=snapshot_folder_name)
            print('newsnap.info', newsnap.info)

            self.add_snap(newsnap)

    def update_plot_pic(self):

        plt.figure(figsize=(12, 8))
        # to change
        for site_handler in SITE_HANDLERS:
            x = []
            y = []
            for date in sorted(self.snapshots.keys()):
                snap = self.snapshots[date]

                if snap.info['finished']:
                    x.append(date)
                    y.append(snap.basket[site_handler.site_code + '_total'].sum())


            plt.plot(x, y, marker='o', label=site_handler.description)
        plt.legend()
        plt.grid()
        plt.savefig('anehome/static/dynamics/fig.png')

    def update_plot_js(self):
        # plt.figure(figsize=(12, 8))
        # to change
        data = []
        for site_handler in SITE_HANDLERS:
            if site_handler.site_code == 'gks':
                continue

            x = []
            y = []
            for date in sorted(self.snapshots.keys()): # should be optimized!
                snap = self.snapshots[date]
                if snap.info['finished'] and snap.info['type'] == 'normal':
                    if site_handler.site_code + '_total' in snap.basket.columns:
                        x.append(date)
                        y.append(snap.basket[site_handler.site_code + '_total'].sum())

            # plt.plot(x, y, marker='o', label=site_handler.description)

            trace = go.Scatter(x=x,
                               y=y,
                               marker={'size': 8},
                               mode="lines+markers", name=site_handler.description
                               )

            data.append(trace)

        x = []
        y = []
        for date in sorted(self.snapshots.keys()):  # should be optimized!
            snap = self.snapshots[date]
            if snap.info['finished'] and snap.info['type'] == 'gks':
                x.append(date)
                y.append(snap.site_prices['gks']['gks_total'].sum())

        # plt.plot(x, y, marker='o', label=site_handler.description)

        trace = go.Scatter(x=x,
                           y=y,
                           marker={'size': 8},
                           mode="lines+markers", name='Госстатистика'
                           )

        data.append(trace)

        layout = dict(
            title='Динамика продуктовой корзины для разных магазинов',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        fig = go.Figure(data=data, layout=layout)
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    def update_product_plot_js(self, product_id):
        # plt.figure(figsize=(12, 8))
        # to change
        data = []
        for site_handler in SITE_HANDLERS:
            if site_handler.site_code == 'gks':
                continue

            x = []
            y = []
            for date in sorted(self.snapshots.keys()): # should be optimized!
                snap = self.snapshots[date]
                if snap.info['finished'] and snap.info['type'] == 'normal':
                    if site_handler.site_code + '_total' in snap.basket.columns:
                        value = snap.basket[site_handler.site_code + '_total'][snap.basket['id'] == product_id].iloc[0]
                        if value:
                            x.append(date)
                            y.append(value)

            # plt.plot(x, y, marker='o', label=site_handler.description)

            trace = go.Scatter(x=x,
                               y=y,
                               marker={'size': 8},
                               mode="lines+markers", name=site_handler.description
                               )

            data.append(trace)

        x = []
        y = []
        for date in sorted(self.snapshots.keys()):  # should be optimized!
            snap = self.snapshots[date]
            if snap.info['finished'] and snap.info['type'] == 'gks':
                x.append(date)
                y.append(snap.site_prices['gks'][snap.site_prices['gks']['product_id'] == product_id]['gks_total'].iloc[0])

        # plt.plot(x, y, marker='o', label=site_handler.description)

        trace = go.Scatter(x=x,
                           y=y,
                           marker={'size': 8},
                           mode="lines+markers", name='Госстатистика'
                           )

        data.append(trace)

        layout = dict(
            title='Динамика стоимости продукта {} для разных магазинов'.format(sfb.sfb.get_product_title(product_id)),
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        fig = go.Figure(data=data, layout=layout)
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    def get_snap_table(self):
        pass

        lst = []
        it = 1
        for date in sorted(self.snapshots.keys(), reverse=True):
            newsnap = {}
            snap = self.snapshots[date]
            newsnap['id'] = it
            it += 1
            newsnap['date'] = str(snap.snap_date)
            newsnap['status'] = 'OK'
            newsnap['code'] = snap.snap_folder_name

            newsnap['imagelink'] = r'../static/ok_sign.png'
            if 'warnings' in snap.info:
                if len(snap.info['warnings']) > 0:
                    newsnap['imagelink'] = r'../static/warning_sign.png'

            lst.append(newsnap)

        return lst

    def get_test_snap(self):

        newsnap = Snapshot()
        newsnap.get_snapshot(save_to_file=True,\
                             type='normal')#, handlers=[SITE_CODE_TO_HANDLER['globus']])
        self.snapshots[newsnap.snap_date] = newsnap


    def get_new_snap_threaded(self, handlers=None):
        if self.can_make_snaps:
            GlobalStatus().setstatus('Подготовка к снапшоту')
            self.can_make_snaps = False

            thread = BaseThread(
                name='test',
                target=get_snap_thread_job,
                callback=self.get_new_snap_callback,
                callback_args=tuple(),
            )

            thread.start()

    def get_new_snap_callback(self, newsnap):
        GlobalStatus().setstatus('Свободен')
        self.snapshots[newsnap.snap_date] = newsnap
        self.can_make_snaps = True


def get_snap_thread_job(handlers=None):
    newsnap = Snapshot()
    # GlobalStatus().setstatus('lollolllllllllllllllllllllllllll')
    print(GlobalStatus().status)
    newsnap.get_snapshot(save_to_file=True,
                         type='normal', handlers=[SITE_CODE_TO_HANDLER['utkonos']])
    return newsnap


class BaseThread(threading.Thread):
    def __init__(self, callback=None, callback_args=None, *args, **kwargs):
        target = kwargs.pop('target')
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.callback = callback
        self.method = target
        self.callback_args = callback_args

        self.newsnap = None

    def target_with_callback(self):
        self.newsnap = self.method()
        if self.callback is not None:
            self.callback(*self.callback_args + (self.newsnap, ))