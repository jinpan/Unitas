# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='datetime',
            new_name='endtime',
        ),
        migrations.AddField(
            model_name='event',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 22, 21, 50, 34, 460255, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
