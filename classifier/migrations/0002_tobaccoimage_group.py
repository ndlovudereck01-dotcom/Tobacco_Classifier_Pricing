from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tobaccoimage',
            name='group',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
