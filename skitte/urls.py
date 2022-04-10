from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls import handler404

from graphene_django.views import GraphQLView
from .graphql.authClass import AuthenticatedGraphQLView
from django.views.decorators.csrf import csrf_exempt
from skitte.graphql.schema import schema

handler404 = 'helpers.views.handle_not_found'


from accounts.views import (
    login_view,
    logout_view,
    register_view,
    activate,
    credit_view
)

from skit.views import (
    home_view,
    feed_view,
    notify_view,
    skits_list_view,
    skits_detail_view,
    base_layout,
    skitte_serviceworker,
    skitte_offline,
    result
)
from django.views.generic import TemplateView

UUID_CHANNEL_REGEX = r'channel/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})'

urlpatterns = [
    # Expo
    path('ex/', include('expo.urls'), name="ex"),
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),
    path('', home_view, name="home"),
    path("defaultsite", home_view, name="default-home"),
    path('feed/', feed_view, name="feeds"),
    re_path(r'notification?s/', notify_view, name="notify"),
    path('base_layout/', base_layout),
    path('global/', skits_list_view),

    path('activate/<uidb64>/<token>', activate, name='activate'),
    re_path(r'^skt-serviceworker(.*.js)$', skitte_serviceworker),
    re_path(r'^offline(.*.html)$', skitte_offline),

    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="signup"),
    path('credit', credit_view, name="credit"),
    path('post/₦/<skit_url>', skits_detail_view),

    re_path(r'profiles?/', include('profiles.urls')),

    path('api/skits/', include('skit.api.urls')),
    path('api/auth/', AuthenticatedGraphQLView.as_view(graphiql=True, schema=schema)),
    path('api/profiles/', include('profiles.api.urls')),
    # path('api/chat/', include('skitte_chat.api.urls')),


    # Chat
    # path('chat/', include('skitte_chat.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('result/', result, name='result'),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        # GraphQL
        path("api/graphql/",
             AuthenticatedGraphQLView.as_view(graphiql=True, schema=schema)),
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
else:
    urlpatterns += [
        # GraphQL
        path("api/graphql/",
             csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    ]
