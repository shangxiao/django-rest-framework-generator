from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
try:
    from django.apps import apps
    get_app = apps.get_app_config
    from django.apps.registry import AppConfig
    get_models = AppConfig.get_models
except ImportError:
    from django.db.models.loading import get_app, get_models

serializers = """\
from rest_framework import serializers
%(model_imports)s
%(classes)s
"""

serializer_class_def = """\


class %(model)sSerializer(serializers.ModelSerializer):
    class Meta:
        model = %(model)s
"""

viewsets = """\
from rest_framework import viewsets
%(model_imports)s
%(serializer_imports)s
%(classes)s
"""

viewset_class_def = """\


class %(model)sViewSet(viewsets.ModelViewSet):
    queryset = %(model)s.objects.all()
    serializer_class = %(model)sSerializer
"""

urls = """\
from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
%(router_defs)s

urlpatterns = [
    url(r'^', include(router.urls)),
]
"""

router_def = "router.register(r'%(model_api_name)s', views.%(model)sViewSet)\n"

class Command(BaseCommand):
    args = '<app_name>'
    help = 'Generates serializers and viewsets (with --viewsets) for DRF'
    option_list = BaseCommand.option_list + (
        make_option('--viewsets',
            action='store_true',
            dest='viewsets',
            default=False,
            help='Generate viewsets'),
        make_option('--urls',
            action='store_true',
            dest='urls',
            default=False,
            help='Generate urls'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please supply an app name')

        app_name = args[0]
        app = get_app(app_name)
        model_names = [model.__name__ for model in get_models(app)]

        if options['viewsets']:
            serializer_names = [model_name + 'Serializer' for model_name in model_names]
            class_defs = [
                viewset_class_def % {
                    'model': name,
                }
                for name in model_names
            ]

            print(viewsets % {
                'model_imports': 'from ' + app_name + '.models import ' + (', '.join(model_names)),
                'serializer_imports': 'from ' + app_name + '.serializers import ' + (', '.join(serializer_names)),
                'classes': ''.join(class_defs),
            })

        elif options['urls']:
            view_names = [model_name + 'ViewSet' for model_name in model_names]
            router_defs = [
                router_def % {
                    'model_api_name': model_name.lower() + 's',
                    'model': model_name,
                }
                for model_name in model_names
            ]

            print(urls % {
                'view_imports': 'from ' + app_name + '.views import ' + (', '.join(view_names)),
                'router_defs': ''.join(router_defs),
            })

        else:
            class_defs = [
                serializer_class_def % {
                    'model': name,
                }
                for name in model_names
            ]

            print(serializers % {
                'model_imports': 'from ' + app_name + '.models import ' + (', '.join(model_names)),
                'classes': ''.join(class_defs),
            })
