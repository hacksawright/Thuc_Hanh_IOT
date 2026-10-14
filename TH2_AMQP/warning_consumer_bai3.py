import pika
import sys
import os

def callback(ch, method, properties, body):
    print(f"[warning_queue] Da nhan: {body.decode()}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')

    # Tạo queue
    channel.queue_declare(queue='warning_queue')
    
    # Bind queue với exchange bằng routing key 'warning'
    channel.queue_bind(exchange='iot_alert_exchange', 
                       queue='warning_queue', 
                       routing_key='warning')

    channel.basic_consume(queue='warning_queue', 
                          on_message_callback=callback, 
                          auto_ack=True)

    print(' [*] Đang chờ cảnh báo WARNING.')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nĐã dừng.")
        sys.exit(0)

if __name__ == '__main__':
    main()