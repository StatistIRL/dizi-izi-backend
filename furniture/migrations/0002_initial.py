# Generated by Django 4.1.7 on 2024-03-04 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('furniture', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='powersocket',
            name='north_east',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='furniture.coordinate', verbose_name='Координата north-east'),
        ),
        migrations.AddField(
            model_name='powersocket',
            name='north_west',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='furniture.coordinate', verbose_name='Координата north-west'),
        ),
        migrations.AddField(
            model_name='powersocket',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='furniture.room', verbose_name='Комната'),
        ),
        migrations.AddField(
            model_name='powersocket',
            name='south_east',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='furniture.coordinate', verbose_name='Координата south-east'),
        ),
        migrations.AddField(
            model_name='powersocket',
            name='south_west',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='furniture.coordinate', verbose_name='Координата south-west'),
        ),
        migrations.AddField(
            model_name='placement',
            name='furniture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placements', to='furniture.furniture', verbose_name='Мебель'),
        ),
        migrations.AddField(
            model_name='placement',
            name='north_east',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='furniture.coordinate', verbose_name='Координата north-east'),
        ),
        migrations.AddField(
            model_name='placement',
            name='north_west',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='furniture.coordinate', verbose_name='Координата north-west'),
        ),
        migrations.AddField(
            model_name='placement',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='furniture.room', verbose_name='Комната'),
        ),
        migrations.AddField(
            model_name='placement',
            name='south_east',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='furniture.coordinate', verbose_name='Координата south-east'),
        ),
        migrations.AddField(
            model_name='placement',
            name='south_west',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='furniture.coordinate', verbose_name='Координата south-west'),
        ),
        migrations.AddField(
            model_name='furniture',
            name='type_of_rooms',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='furniture', to='furniture.typeofroom', verbose_name='Комната'),
        ),
        migrations.AddField(
            model_name='door',
            name='north_east',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='furniture.coordinate', verbose_name='Координата north-east'),
        ),
        migrations.AddField(
            model_name='door',
            name='north_west',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='furniture.coordinate', verbose_name='Координата north-west'),
        ),
        migrations.AddField(
            model_name='door',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='furniture.room', verbose_name='Комната'),
        ),
        migrations.AddField(
            model_name='door',
            name='south_east',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='furniture.coordinate', verbose_name='Координата south-east'),
        ),
        migrations.AddField(
            model_name='door',
            name='south_west',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='furniture.coordinate', verbose_name='Координата south-west'),
        ),
    ]