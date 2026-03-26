"""
Webhook utilities for contract-related notifications.
"""
import hashlib
import hmac
import json
import logging
from django.db import models
from django.utils import timezone
from .models import WebhookSubscription

logger = logging.getLogger(__name__)

def notify_contract_status_change(contract, status):
    """
    Trigger webhooks when a contract's indexing status changes (paused/resumed).
    """
    from .tasks import dispatch_webhook_data  # Lazy import to avoid circular dependency
    
    # We use a special event type for status changes
    event_type = f"contract.{status}"
    
    # Payload as specified in requirements
    payload = {
        "contract_id": contract.contract_id,
        "status": status,
        "timestamp": timezone.now().isoformat(),
    }
    if status == "paused":
        payload["reason"] = contract.pause_reason

    # Find webhooks subscribed to this contract
    # (or all events for this contract if event_type is blank)
    webhooks = WebhookSubscription.objects.filter(
        contract=contract,
        is_active=True,
    ).filter(models.Q(event_type=event_type) | models.Q(event_type=""))

    for webhook in webhooks:
        # Dispatch asynchronously via Celery
        dispatch_webhook_data.delay(webhook.id, event_type, payload)

    logger.info(
        "Status change notification (%s) queued for contract %s",
        status,
        contract.contract_id
    )
