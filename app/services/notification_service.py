import logging
import os

logger = logging.getLogger(__name__)


def send_notification(submission_id: int) -> None:
    """
    Simulated notification side effect.

    In production this could send an email or webhook.
    For the capstone, failure can be forced with:
    NOTIFICATION_FORCE_FAILURE=true
    """

    force_failure = os.getenv("NOTIFICATION_FORCE_FAILURE", "false").lower() == "true"

    if force_failure:
        raise RuntimeError("Notification service is unavailable")

    logger.info(
        "Notification sent successfully for submission %s",
        submission_id,
    )
