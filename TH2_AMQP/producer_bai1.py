import pika

def main():
    #Kết nối tới RabbitMQ broker
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    #Tạo queue có tên iot_lab_queue
    channel.queue_declare(queue='iot_lab_queue')

    student_id = "B23DCCN494"
    student_name = "Vu Thanh Loc"
    message = f"Xin chao tu ung dung Python AMQP - {student_id} - {student_name}"

    #Gửi message vào queue
    channel.basic_publish(exchange='', 
                          routing_key='iot_lab_queue', 
                          body=message)
    
    print(f"Đã gửi message: '{message}'")

    connection.close()

if __name__ == '__main__':
    main()