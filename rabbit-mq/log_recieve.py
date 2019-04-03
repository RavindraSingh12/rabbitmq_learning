#here we bind the exchange to the queue else all messages will be discarded. 

#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#declare channel incase we are not sure if the exchange exists or not
channel.exchange_declare(exchange='logs', exchange_type='fanout')

#declare a queue with no name in this case rabbitmq will automatically asign a random name to it.
#setting exclusive=True will once the consumer connection is closed, the queue should be deleted
result = channel.queue_declare('', exclusive=True)

#retrive random name of the queue
queue_name = result.method.queue

#bind queue to the exchange
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

#start the lool
channel.start_consuming()
