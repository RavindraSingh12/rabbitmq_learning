#We will use a direct exchange instead. The routing algorithm behind a direct exchange is simple - a message goes to the queues whose binding key exactly matches the routing key of the message.
#In such a setup a message published to the exchange with a routing key
#and gets deliverd to the queue having excatly same binding key 

#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#declaring exchange with direct type exchange
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

#taking serverity from commnad line if the severity is from error,warning,info then we will write to one queue
#and in case of error we will write to disk and print it too so we will send that to multiple queue
#here first arg from cmd is severity and the other arguement is message else hello world
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

#publish message or send message to exchange with the routing key 
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)

print(" [x] Sent %r:%r" % (severity, message))
connection.close()
