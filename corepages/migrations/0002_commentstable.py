# Generated by Django 4.2.7 on 2024-05-05 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corepages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentsTable',
            fields=[
                ('id_student', models.OneToOneField(db_column='id_student', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='corepages.studentstable')),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'comments_table',
                'managed': False,
            },
        ),
    ]
