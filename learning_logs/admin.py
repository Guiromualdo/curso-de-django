from django.contrib import admin # type: ignore
from learning_logs.models import Topic
from learning_logs.models import Entry

admin.site.register(Topic)
admin.site.register(Entry)
