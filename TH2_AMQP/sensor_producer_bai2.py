import pika
import json
import time
import random
from datetime import datetime

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Tạo queue sensor_data_queue
    channel.queue_declare(queue='sensor_data_queue')

    print(" [*] Đang gửi dữ liệu cảm biến (mỗi 3 giây). Bấm CTRL+C để dừng.")
    
    try:
        while True:
            # Sinh dữ liệu ngẫu nhiên
            temp = round(random.uniform(25.0, 40.0), 1)
            humidity = round(random.uniform(30.0, 80.0), 1)
            
            payload = {
                "device_id": "sensor01",
                "temperature": temp,
                "humidity": humidity,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Chuyển dict thành chuỗi JSON
            message = json.dumps(payload)

            channel.basic_publish(exchange='', 
                                  routing_key='sensor_data_queue', 
                                  body=message)
            
            print(f" [x] Đã gửi: {message}")
            time.sleep(3) # Tạm dừng 3 giây trước khi gửi tiếp
            
    except KeyboardInterrupt:
        print("\nĐã dừng gửi dữ liệu.")
    finally:
        connection.close()

if __name__ == '__main__':
    main()