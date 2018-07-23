from __future__ import absolute_import, unicode_literals

# This ensures that the app is loaded when Django starts so that
# the @shared_task decorator (mentioned later) will use it:

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)

# Note that this example project layout is suitable for larger projects,
# for simple projects you may use a single contained module that defines both the app and tasks,
# like in the First Steps with Celery tutorial.
