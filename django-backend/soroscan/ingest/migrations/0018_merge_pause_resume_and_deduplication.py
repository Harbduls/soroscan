from django.db import migrations


class Migration(migrations.Migration):
    """
    Merge migration: combines 0016_trackedcontract_pause_resume and
    0017_eventdeduplicationlog into a single chain.
    """

    dependencies = [
        ("ingest", "0016_trackedcontract_pause_resume"),
        ("ingest", "0017_eventdeduplicationlog"),
    ]

    operations = []
