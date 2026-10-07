import logging
import time

from app.services.notification_service import send_notification

logger = logging.getLogger(__name__)


def process_notification(submission_id: int, max_retries: int = 3) -> bool:
    """
    Send a notification with retries.

    Returns True when successful.
    Returns False after all retry attempts fail.
    """

    for attempt in range(1, max_retries + 1):
        try:
            send_notification(submission_id)

            logger.info(
                "Notification completed for submission %s on attempt %s",
                submission_id,
                attempt,
            )

            return True

        except Exception as exc:
            logger.error(
                "Notification attempt %s/%s failed for submission %s: %s",
                attempt,
                max_retries,
                submission_id,
                exc,
            )

            if attempt < max_retries:
                time.sleep(1)

    logger.critical(
        "ALERT: notification permanently failed for submission %s",
        submission_id,
    )

    return False
