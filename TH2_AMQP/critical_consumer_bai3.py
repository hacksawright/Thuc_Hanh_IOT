import pika
import sys
import os

def callback(ch, method, properties, body):
    print(f"[critical_queue] Da nhan: {body.decode()}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')

    # Tạo queue
    channel.queue_declare(queue='critical_queue')
    
    # Bind queue với exchange bằng routing key 'critical'
    channel.queue_bind(exchange='iot_alert_exchange', 
                       queue='critical_queue', 
                       routing_key='critical')

    channel.basic_consume(queue='critical_queue', 
                          on_message_callback=callback, 
                          auto_ack=True)

    print(' [*] Đang chờ cảnh báo CRITICAL.')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nĐã dừng.")
        sys.exit(0)

if __name__ == '__main__':
    main()