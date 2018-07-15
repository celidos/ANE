from django.shortcuts import render
import django_tables2 as tables

from anehome.startup_routine import fresh_table_holder

class NameTable(tables.Table):
    name = tables.Column()
    age = tables.Column()

def main(request):
    # table = NameTable([{'name': 'hui', 'age': 21}, {'name': 'pizda', 'age': 22}])



    return render(request, 'index.html', {'mytable': fresh_table_holder.gks_table.to_html()})
