import os

env = os.environ.get

broker_url = env('FFIO_BROKER_URL', 'redis://localhost:6379')

result_backend = broker_url

task_track_started = True

SERIALIZATION_PROTOCOL = 'pickle'

accept_content = [SERIALIZATION_PROTOCOL]
task_serializer = SERIALIZATION_PROTOCOL
result_serializer = SERIALIZATION_PROTOCOL
