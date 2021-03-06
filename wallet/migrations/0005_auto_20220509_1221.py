# Generated by Django 3.2.10 on 2022-05-09 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_auto_20220509_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='xpub_added_coin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wallet.addedcoinmnemonics'),
        ),
        migrations.AlterField(
            model_name='address',
            name='xpub',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wallet.bitcoinmnemonics'),
        ),
    ]
