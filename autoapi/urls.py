from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    # Django Admin -> not important
    path('admin/', admin.site.urls),
    # API URLs
    path('', include('App.urls')),
    # API DOCS
    path('', include_docs_urls(title="AUTO API")),
    path('schema', get_schema_view(
        title="AUTO API",
        description="API FOR AUTO ANALYTICS PROJECT",
        version="1.0.0"
    ), name='openapi-schema'),
    # serves static files for api docs
    path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]