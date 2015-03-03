Generate initial & very basic serializers and viewsets

Installation
------------

`pip install git+git://github.com/rapilabs/django-rest-framework-generator.git`

or in your requirements.txt:

`-e git+git://github.com/rapilabs/django-rest-framework-generator.git#egg=django-rest-framework-generator`

and in your settings.py add:

```python
INSTALLED_APPS = (
    # ...
    'django_rest_framework_generator',
)
```

Usage
-----

To generate serializers:

`python manage.py generate_serializers_views <app_name> > <app_dir>/serializers.py`

To generate viewsets:

`python manage.py generate_serializers_views <app_name> --viewsets > <app_dir>/views.py`
