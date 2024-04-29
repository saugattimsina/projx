from django.contrib import admin

# Register your models here.
from .models import MLMMember, MLMBinary, MLMRank, UserRank, BinaryParents

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
#
# admin.site.register(ForcedMatrix, MyAdmin2)

admin.site.register(MLMRank)
admin.site.register(BinaryParents)


@admin.register(UserRank)
class UserRankAdmin(admin.ModelAdmin):
    list_display = ("user", "rank")
    list_filter = ("rank",)
