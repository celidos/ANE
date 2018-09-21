from django.shortcuts import render
import django_tables2 as tables
import anehome_test.anehome as anehome
from django.http import HttpResponse
import pandas as pd
import json
import datetime
from anehome_test.anehome.settings.forms import ProductChooseForm, SiteChooseForm
from anehome_test.anehome import startup_routine
from anehome_test.anehome.global_status import GlobalStatus
from anehome_test.anehome.logic import standard_food_basket as sfb
import math

class BasketTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    title = tables.Column(verbose_name='Название продукта', footer='Суммарно:')
    globus_unit = tables.Column(verbose_name='Глобус (цена)')
    globus_total = tables.Column(verbose_name='Глобус (стоимость)',
                                 footer=lambda table: round(sum(x['globus_total'] for x in table.data if not pd.isna(x)), 2))
    okey_unit = tables.Column(verbose_name='Окей (цена)')
    okey_total = tables.Column(verbose_name='Окей (стоимость)',
                               footer=lambda table: round(sum(x['okey_total'] for x in table.data if not pd.isna(x)), 2))
    perekrestok_unit = tables.Column(verbose_name='Перекресток (цена)')
    perekrestok_total = tables.Column(verbose_name='Перекресток (стоимость)',
                                      footer=lambda table: round(sum(x['perekrestok_total'] for x in table.data if not pd.isna(x)), 2))
    utkonos_unit = tables.Column(verbose_name='Утконос (цена)')
    utkonos_total = tables.Column(verbose_name='Утконос (стоимость)',
                                  footer=lambda table: round(sum([x['utkonos_total'] for x in table.data if not pd.isna(x['utkonos_total'])]), 2),
                                  attrs={'td': {'font-weight': 'bold'}})

class GksTable(tables.Table):
    product_id = tables.Column(verbose_name='ID')
    site_title = tables.Column(verbose_name='Название продукта', footer='Суммарно:')
    gks_unit = tables.Column(verbose_name='Госстатистика (цена)')
    gks_total = tables.Column(verbose_name='Госстатистика (стоимость)',
                                  footer=lambda table: round(sum(x['gks_total'] for x in table.data if not pd.isna(x)), 2),
                                  attrs={'td': {'font-weight': 'bold'}})


class SnapsTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    date = tables.TemplateColumn('<a href="/snaps/{{record.code}}">{{record.date}}</a>', verbose_name='Дата снапшота')
    status = tables.TemplateColumn('<img src="{{record.imagelink}}" height="16" width="16">', verbose_name='')


class SnapErrorMessagesTable(tables.Table):
    status = tables.TemplateColumn('<img src="./../../static/warning_sign.png" height="16" width="16">',
                                   verbose_name='')
    reason = tables.Column(verbose_name='Описание')



class PriceTable(tables.Table):
    site_title = tables.Column(verbose_name='Название')
    link = tables.TemplateColumn('<a href="{{record.site_link}}"><img src="./../../static/link_sign.png" '+\
                                 ' height="16" width="16"></a>', verbose_name='Ссылка')
    site_cost = tables.Column(verbose_name='Цена (маг.)')
    site_unit = tables.Column(verbose_name='Ед.')
    unitcost = tables.Column(verbose_name='Цена за единицу')


class ExpTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    text = tables.Column(verbose_name='Текст')


def main(request):
    # global snapshot_manager
    # global snapshot_manager
    bsk = startup_routine.snapshot_manager.fresh_snapshot_ref.basket

    print(bsk.drop(bsk[bsk['id'] == 0].index).to_dict('records'))

    # return render(request, 'index.html', {'mytable': fresh_table_holder.gks_table.to_html()})
    return render(request, 'index.html',
                  {'mytable': BasketTable(bsk.drop(bsk[bsk['id'] == 0].index).to_dict('records')),
                   'last_succ_snap_date' : anehome.startup_routine.snapshot_manager.fresh_snapshot_date})


def dynamics(request):
    if request.method == "GET":
        print('penis!')
        product_id = request.GET.get('product_name', '')
        if product_id:
            return HttpResponse(anehome.startup_routine.snapshot_manager.update_product_plot_js(int(product_id)))
        else:
            product_form = ProductChooseForm()
            product_form.fields["product"].choices = sfb.sfb.get_products()

            return render(request, 'dynamics.html',
                          {'graph': anehome.startup_routine.snapshot_manager.update_plot_js(),
                           'form_product' : product_form})



def list_snaps(request):
    return render(request, 'list_snaps.html',
                  {'snapstable': SnapsTable(anehome.startup_routine.snapshot_manager.get_snap_table())})


def display_snap(request, year, month, day, hour, minute, second):
    snap_date = datetime.datetime(year=int(year),
                                  month=int(month),
                                  day=int(day),
                                  hour=int(hour),
                                  minute=int(minute),
                                  second=int(second))

    if request.method == "GET":
        print('penis!')
        product_id = request.GET.get('product_name', '')
        site_name = request.GET.get('site_name', '')
        if product_id and site_name:
            if snap_date in anehome.startup_routine.snapshot_manager.snapshots.keys():
                snap = anehome.startup_routine.snapshot_manager.snapshots[snap_date]
                if site_name != 'gks':
                    response = PriceTable(snap.get_by_site_and_product(site_name, product_id))
                else:
                    response = GksTable(snap.get_by_site_and_product(site_name, product_id))
                return render(request, 'rendertable.html', {'pricetable': response})
            else:
                return render(request, 'no_data.html')
        else:
            product_form = ProductChooseForm()
            product_form.initwith(anehome.startup_routine.snapshot_manager.snapshots[snap_date])
            site_form = SiteChooseForm()
            site_form.initwith(anehome.startup_routine.snapshot_manager.snapshots[snap_date])

            snap = anehome.startup_routine.snapshot_manager.snapshots[snap_date]

            if 'warnings' in snap.info:
                error_list = [{'reason': x} for x in snap.info['warnings']]
            else:
                error_list = []

            return render(request, 'snap_page.html',
                          {'form_product': product_form,
                           'form_site': site_form,
                           'error_messages' : SnapErrorMessagesTable(error_list)})


def experiment(request):
    newtable = ExpTable([{'id' : 0, 'text': 'heil'}, {'id': 1, 'text' : 'Masha'}])
    if request.method == "POST":
        form = ExperimentForm(request.POST)
        if form.is_valid():
            if form.is_valid():  # All validation rules pass
                # Process the data in form.cleaned_data
                # ...

                opt = form.cleaned_data['my_option']

                newtable = generate_shit(opt)
                return render(request, 'maindata.html',
                          {'exptable': newtable})

    # return HttpResponse(json.dumps({'a': 1, 'bbbb' : 4}), content_type="application/json")
    form = ProductForm()
    return render(request, 'experiment.html',
                  {'exptable': newtable, 'form' : form}) #ExpTable([{'id' : 0, 'text': 'heil'}, {'id': 1, 'text' : 'Masha'}])})


def render_form(request):
    return render(request, 'radio_form.html')


def generate_shit(option):
    if option == 'firefox':
        return ExpTable([{'id' : 0, 'text': 'heil'}, {'id': 1, 'text' : 'FIREFOX!!!!!1'}])
    elif option == 'opera':
        return ExpTable([{'id' : 1110, 'text': 'zeig'}, {'id': 2, 'text' : 'OPERA'}])
    else:
        return ExpTable([{'id' : -123, 'text': '!!!!'}, {'id': 2, 'text' : 'IE'}])


def display_price_table(request):
    if request.method == 'GET':
        # queryset = PhoneNumber.objects.filter(is_deleted=False)
        product = request.GET.get('product_name')
        site = request.GET.get('site_name')
        response = HttpResponse('Нет данных')
        if product and site:
            response = PriceTable(anehome.startup_routine.snapshot_manager.\
                fresh_snapshot_ref.basket.to_dict('records'))


        return response

def display_cp(request):
    return render(request, 'cp.html',
           {'current_status': GlobalStatus().status})