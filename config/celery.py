import os
from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

default_exchange = Exchange(name='default', type='direct')
media_exchange = Exchange(name='media', type='direct')
task_queues = (
    Queue(name='default', exchange=default_exchange, routing_key='default'),
    Queue(name='image', exchange=media_exchange, routing_key='image'),
    Queue(name='video', exchange=media_exchange, routing_key='video'),
)
task_default_queue = 'default'
task_default_exchange = 'default'
task_default_routing_key = 'default'

app.conf.task_routes = {
    # 'app_name.tasks.task_1': {'queue': 'default'},
}

app.autodiscover_tasks()
