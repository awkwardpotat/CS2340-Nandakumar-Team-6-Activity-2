from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('restaurants', '0003_restaurant_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(upload_to='restaurant_images/', null=True, blank=True),
        ),
    ]
