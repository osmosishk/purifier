# Generated by Django 3.1.4 on 2021-03-17 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OneToOne', '0002_auto_20210317_1729'),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productcode', models.CharField(max_length=30)),
                ('producttype', models.CharField(choices=[('WPU', 'Water Purifier'), ('U', 'Under Sink'), ('F', 'Filter')], max_length=3)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='machine',
            name='main_pack',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='price',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='producttype',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='user',
        ),
        migrations.AddField(
            model_name='case',
            name='customer',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='OneToOne.customer'),
        ),
        migrations.AddField(
            model_name='machine',
            name='customer',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='OneToOne.customer'),
        ),
        migrations.AddField(
            model_name='machine',
            name='maintenance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.mainpack'),
        ),
        migrations.AlterField(
            model_name='case',
            name='handledby',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='management.technician'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='installdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='mac',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name='MainPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField(null=True)),
                ('enddate', models.DateField(null=True)),
                ('Price', models.CharField(max_length=30)),
                ('isrenewed', models.BooleanField(default=False)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.machine')),
            ],
        ),
        migrations.AddField(
            model_name='machine',
            name='machinetype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.product'),
        ),
    ]