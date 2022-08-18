# Generated by Django 3.2.14 on 2022-08-11 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_info_consultant_thematique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partenaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('logo', models.ImageField(blank=True, upload_to='media')),
                ('thematique_metier', models.ManyToManyField(related_name='partenaire', to='api.Thematique_metier')),
            ],
        ),
    ]
