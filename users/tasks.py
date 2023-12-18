from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def task_send_code(code):
    logger.info(f'user.verification_code {code}')
    print('user.verification_code', code)
