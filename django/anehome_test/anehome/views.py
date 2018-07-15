from django.shortcuts import render
import django_tables2 as tables

class NameTable(tables.Table):
    name = tables.Column()
    age = tables.Column()

def main(request):
    table = NameTable([{'name': 'hui', 'age': 21}, {'name': 'pizda', 'age': 22}])

    return render(request, 'index.html', {'people': table})
