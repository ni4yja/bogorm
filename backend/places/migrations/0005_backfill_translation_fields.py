from django.core.management import call_command
from django.db import migrations


def backfill_translation_fields(apps, schema_editor):
    call_command("update_translation_fields")


class Migration(migrations.Migration):
    dependencies = [
        ("places", "0004_place_description_en_place_description_pl_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill_translation_fields, migrations.RunPython.noop),
    ]
