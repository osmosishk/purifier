from django.contrib import admin

from .models import Machine, MainPack , Case,Technician ,Filter , jobsheet

admin.site.register(Machine)
admin.site.register(MainPack)
admin.site.register(Case)
admin.site.register(Technician)
admin.site.register(Filter)
admin.site.register(jobsheet)



