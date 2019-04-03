#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

#declare a queue
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

#binding key taken from cmd when this script is run
binding_keys = sys.argv[1:]

#if no binding key is given print uses of this script
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)


#whatever is given to the script as args will be bound to this queue here
#1.)ex: run it with "cron.warning cron.info" for saving it to a file or to directly dump to any location
#2.)then run it with other args for other solutions
for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
