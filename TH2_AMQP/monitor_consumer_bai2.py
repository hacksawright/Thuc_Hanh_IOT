import pika
import json
import sys
import os

def callback(ch, method, properties, body):
    try:
        # Parse chuỗi JSON thành Python dict
        data = json.loads(body.decode())
        
        device_id = data.get("device_id")
        temp = data.get("temperature")
        humidity = data.get("humidity")
        
        print("-----------------------------")
        print(f"Device: {device_id}")
        print(f"Temperature: {temp}")
        print(f"Humidity: {humidity}")
        
        # Kiểm tra ngưỡng và in cảnh báo
        if temp > 35:
            print("CANH BAO: Nhiet do cao")
        if humidity < 40:
            print("CANH BAO: Do am thap")
            
    except json.JSONDecodeError:
        print(f"Lỗi: Không thể parse JSON từ payload - {body}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='sensor_data_queue')
    channel.basic_consume(queue='sensor_data_queue', 
                          on_message_callback=callback, 
                          auto_ack=True)

    print(' [*] Đang lắng nghe dữ liệu từ cảm biến.')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nĐã dừng giám sát.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == '__main__':
    main()