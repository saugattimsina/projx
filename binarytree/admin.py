from django.contrib import admin

# Register your models here.
from .models import MLMMember,MLMBinary

# admin.site.register(MLMMember)


# from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
# from myproject.models import MyNode

class MyAdmin(TreeAdmin):
    form = movenodeform_factory(MLMMember)

class MyAdmin1(TreeAdmin):
    form = movenodeform_factory(MLMBinary)

admin.site.register(MLMMember, MyAdmin)

admin.site.register(MLMBinary, MyAdmin1)