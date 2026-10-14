import pika
from datetime import datetime
import sys
import os

def callback(ch, method, properties, body):
    current_time = datetime.now().strftime("%H:%M:%S")
    
    print(f"Da nhan message: {body.decode()}")
    print(f"Thoi gian nhan: {current_time}\n")

def main():
    #Kết nối tới RabbitMQ broker
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    #Đảm bảo queue iot_lab_queue tồn tại
    channel.queue_declare(queue='iot_lab_queue')

    #Lắng nghe queue
    channel.basic_consume(queue='iot_lab_queue', 
                          on_message_callback=callback, 
                          auto_ack=True)

    print('Đang chờ message.')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nĐã dừng consumer.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == '__main__':
    main()