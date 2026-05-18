import django.contrib.gis.db.models.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('category', models.IntegerField(choices=[(10, 'Library'), (20, 'Bookshop'), (30, 'Cultural Centre'), (40, 'Café'), (50, 'Museum'), (60, 'Other')], default=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
