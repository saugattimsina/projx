from django.urls import path
from .views import GetMYParentandChildren

urlpatterns = [path("my/child/parent/", GetMYParentandChildren.as_view())]
