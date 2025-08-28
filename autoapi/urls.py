from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.schemas import get_schema_view
from django.conf import settings

urlpatterns = [
    # Django Admin -> not important
    path('admin/', admin.site.urls),
    # API URLs
    path('', include('App.urls')),
    # serves static files for api docs
    # re_path -> regular exp. path
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path("schema/", get_schema_view(
        title="AUTO API",
        description="API schema",
        version="1.0.0"
    ), name="openapi-schema"),
]