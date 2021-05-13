from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from tracer.services import get_and_cache_lastest_currency


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        get_and_cache_lastest_currency, 'interval', hours=2
    )
