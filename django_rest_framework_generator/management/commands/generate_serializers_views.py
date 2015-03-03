from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
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

class Command(BaseCommand):
    args = '<app_name>'
    help = 'Generates serializers and viewsets (with --viewsets) for DRF'
    option_list = BaseCommand.option_list + (
        make_option('--viewsets',
            action='store_true',
            dest='viewsets',
            default=False,
            help='Generate viewsets'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please supply an app name')

        app_name = args[0]
        app = get_app(app_name)
        class_defs = []
        model_names = [model.__name__ for model in get_models(app)]

        if options['viewsets']:
            serializer_names = [model_name + 'Serializer' for model_name in model_names]

            for model in get_models(app):
                class_defs.append(viewset_class_def % {
                    'model': model.__name__
                })

            print viewsets % {
                'model_imports': 'from ' + app_name + '.models import ' + (', '.join(model_names)),
                'serializer_imports': 'from ' + app_name + '.serializers import ' + (', '.join(serializer_names)),
                'classes': ''.join(class_defs),
            }
        else:
            for model in get_models(app):
                class_defs.append(serializer_class_def % {
                    'model': model.__name__
                })

            print serializers % {
                'model_imports': 'from ' + app_name + '.models import ' + (', '.join(model_names)),
                'classes': ''.join(class_defs),
            }
