# Generated by Django 5.0.3 on 2024-03-31 00:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_conversation_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='Conversation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='accounts.conversation'),
            preserve_default=False,
        ),
    ]
