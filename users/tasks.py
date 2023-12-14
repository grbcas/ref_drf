from celery import shared_task
import logging


@shared_task
def task_send_code(code):
    logging.info(f'user.verification_code {code}')
    print('user.verification_code', code)
