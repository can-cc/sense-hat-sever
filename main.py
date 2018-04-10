from crontabs import Cron, Tab
from datetime import datetime


def my_job(*args, **kwargs):
    print('args={} kwargs={} running at {}'.format(args, kwargs, datetime.now()))


# Will run with a 5 second interval synced to the top of the minute
Cron().schedule(
    Tab(name='run_my_job').every(minute=1).run(my_job, 'my_arg', my_kwarg='hello')
).go()
