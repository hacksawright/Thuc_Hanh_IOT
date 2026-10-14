import pika
import time

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Tạo một direct exchange tên iot_alert_exchange
    channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')

    # Danh sách các cảnh báo mẫu
    alerts = [
        {"level": "info", "message": "He thong khoi dong thanh cong info"},
        {"level": "warning", "message": "Nhiet do phong may vuot nguong warning"},
        {"level": "critical", "message": "Cam bien kho lanh mat ket noi critical"},
        {"level": "warning", "message": "CPU server hoat dong qua tai warning"}
    ]

    for alert in alerts:
        routing_key = alert["level"]
        message = alert["message"]
        
        channel.basic_publish(exchange='iot_alert_exchange', 
                              routing_key=routing_key, 
                              body=message)
                              
        print(f" [x] Đã gửi [{routing_key}]: '{message}'")
        time.sleep(1) # Nghỉ 1s giữa các lần gửi để dễ quan sát

    connection.close()

if __name__ == '__main__':
    main()