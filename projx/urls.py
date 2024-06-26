"""
URL configuration for projx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views import defaults as default_views
from django.views.generic import TemplateView

# from django_telethon.urls import django_telethon_urls

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .yasg_schema import BothHttpAndHttpsSchemaGenerator

admin.autodiscover()

schema_view = get_schema_view(
    openapi.Info(
        title="projectX",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    generator_class=BothHttpAndHttpsSchemaGenerator,
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "",
        TemplateView.as_view(
            template_name="index.html", extra_context={"next": "/dashboard/home/"}
        ),
        name="home",
    ),
    path("admin/", admin.site.urls),
    path("", include("user.urls")),
    path("", include("accounts.urls")),
    path("trade/", include("signalbot.urls")),
    path("subscription/", include("subscription.urls")),
    path(
        "api/list/v1/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "",
        TemplateView.as_view(
            template_name="index.html", extra_context={"next": "/dashboard/home/"}
        ),
        name="home",
    ),
    path("admin/", admin.site.urls),
    path("", include("user.urls")),
    path("binary/", include("binarytree.urls")),
    path("", include("accounts.urls")),
    path("a/", include("binarytree.urls")),
    # path("trade/", include("signalbot.urls")),
    # path('telegram/', django_telethon_urls()),
    # api
    path("api/account/", include("accountsapi.urls")),
    path("api/binary/", include("binarytreeapi.urls")),
    path("income/", include("signalbot.apiurls")),
    path("posts/", include("posts.urls")),
    path("projx-wallet/", include("projxwallet.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        print("debug toolbar is installed")
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
