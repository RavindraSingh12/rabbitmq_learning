#!/usr/bin/env python

#make connection with the rabbitmq server

import pika

connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel=connection.channel()


#create queue for reception of messages, without this rabbitmq will drop the messages.
#this is a named queue
channel.queue_declare(queue='hello')

#In RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
#specifying '' in exchange var tells rabbitmq to use default exchange.

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='I am loving it!')

print(" [x] Sent 'Ravindra Singh just started loving his job!'")

connection.close()

