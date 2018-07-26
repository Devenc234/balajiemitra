from __future__ import absolute_import, unicode_literals
import os
import django
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
django.setup()

app = Celery('myshop')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# The uppercase name-space means that all Celery configuration options must be specified
# in uppercase instead of lowercase, and start with CELERY_,
# so for example the task_always_eager setting becomes CELERY_TASK_ALWAYS_EAGER,
# and the broker_url setting becomes CELERY_BROKER_URL.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# a common practice for reusable apps is to define all tasks in a separate tasks.py module,
# and Celery does have a way to auto-discover these modules
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# With the line above Celery will automatically discover tasks from all of your installed apps,
# following the tasks.py convention
# - app1/
#     - tasks.py
#     - models.py
# - app2/
#     - tasks.py
#     - models.py


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
