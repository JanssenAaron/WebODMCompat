from django.conf.urls import url, include
from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog

from .views import app as app_views, public as public_views, dev as dev_views
from .plugins.views import app_view_handler, root_url_patterns

from app.boot import boot
from webodm import settings
from app.plugins import sync_plugin_db

# Test cases call boot() independently
# Also don't execute boot with celery workers
if not settings.WORKER_RUNNING and not settings.TESTING:
    boot()

# During testing, boot() is not called (see above)
# but we need to know which plugins are available to mount the proper
# routes via urlpatterns.
if settings.TESTING:
    sync_plugin_db()

urlpatterns = [
    url(r'^$', app_views.index, name='index'),
    path('welcome/', app_views.welcome, name='welcome'),
    path('dashboard/', app_views.dashboard, name='dashboard'),
    path('map/project/<project_pk>/task/<task_pk>/', app_views.map, name='map'),
    path('map/project/<project_pk>/', app_views.map, name='map'),
    path('3d/project/<project_pk>/task/<task_pk>/', app_views.model_display, name='model_display'),

    path('public/task/<task_pk>/map/', public_views.map, name='public_map'),
    path('public/task/<task_pk>/iframe/map/', public_views.map_iframe, name='public_iframe_map'),
    path('public/task/<task_pk>/3d/', public_views.model_display, name='public_3d'),
    path('public/task/<task_pk>/iframe/3d/', public_views.model_display_iframe, name='public_iframe_3d'),
    path('public/task/<task_pk>/json/', public_views.task_json, name='public_json'),

    re_path(r'^processingnode/([\d]+)/$', app_views.processing_node, name='processing_node'),

    url(r'^api/', include("app.api.urls")),

    # Bit of a hacky fix but changes could be made so that resource path is used in the app_view_handler
    path('plugins/<plugin_name>/', app_view_handler, name="plugins"),
    path('plugins/<plugin_name>/<path:resource_path>', app_view_handler, name="plugins"),

    url(r'^about/$', app_views.about, name='about'),
    url(r'^dev-tools/(?P<action>.*)$', dev_views.dev_tools, name='dev_tools'),

    # TODO: add caching: https://docs.djangoproject.com/en/3.1/topics/i18n/translation/#note-on-performance
    url(r'^jsi18n/', JavaScriptCatalog.as_view(packages=['app']), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + root_url_patterns()

handler404 = app_views.handler404
handler500 = app_views.handler500

