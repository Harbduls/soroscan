from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Add pause/resume fields to TrackedContract (PR #175).
    """

    dependencies = [
        ("ingest", "0015_merge_notification_and_teams"),
    ]

    operations = [
        migrations.AddField(
            model_name="trackedcontract",
            name="is_paused",
            field=models.BooleanField(default=False, help_text="Whether indexing is temporarily paused"),
        ),
        migrations.AddField(
            model_name="trackedcontract",
            name="paused_at",
            field=models.DateTimeField(blank=True, null=True, help_text="When indexing was paused"),
        ),
        migrations.AddField(
            model_name="trackedcontract",
            name="pause_reason",
            field=models.TextField(blank=True, help_text="Reason for horizontal suspension/pausing"),
        ),
        migrations.AddField(
            model_name="trackedcontract",
            name="resume_at",
            field=models.DateTimeField(
                blank=True,
                null=True,
                help_text="Scheduled time to automatically resume indexing",
            ),
        ),
        migrations.RemoveIndex(
            model_name="trackedcontract",
            name="ingest_trac_contrac_7989b1_idx",
        ),
        migrations.AddIndex(
            model_name="trackedcontract",
            index=models.Index(
                fields=["contract_id", "is_active", "is_paused"],
                name="ingest_trac_contrac_7989b1_idx",
            ),
        ),
    ]
