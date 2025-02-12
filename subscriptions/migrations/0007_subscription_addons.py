# Generated by Django 4.2.16 on 2024-12-02 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_remove_subscription_addons'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='addons',
            field=models.ManyToManyField(blank=True, related_name='subscriptions', to='subscriptions.addon'),
        ),
    ]
