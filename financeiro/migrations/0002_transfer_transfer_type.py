# Generated by Django 4.2.4 on 2023-09-22 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='transfer_type',
            field=models.CharField(choices=[('Recebimento', 'Recebimento'), ('Pagamento', 'Pagamento'), ('Transferência', 'Transferência')], default='1', max_length=13),
            preserve_default=False,
        ),
    ]