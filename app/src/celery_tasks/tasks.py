import json
import smtplib

import pika

from .celery import celery_app
from .. import dependencies, models, schemas, token
from fastapi import APIRouter, Depends

get_db = dependencies.get_db


@celery_app.task(name="send_email")
def send_email(message):
    email = "minhha10c8@gmail.com"
    password = "mgolqbczagtknjlv"  # mật khẩu ứng dụng
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    # message_body = f'Title: {message["title"]}\n\n{message["description"]}' --> thêm \n trước title để tránh mất thông tin title
    if message["status"] == "Finished":
        message_body = f'\n\nAnnouncement: todo with:\nTitle: {message["title"]}\nDescription: {message["description"]}\nhas been marked complete!'
    else:
        message_body = f'\n\nAnnouncement: todo with:\nTitle: {message["title"]}\nDescription: {message["description"]}\nhas been marked as incomplete!'
    # recipients = ["minhha10c8@gmail.com", "trinhduchoang625dora@gmail.com"]
    recipients = [message["receiver"]]
    server.sendmail(email, recipients, message_body)
    server.quit()
    return "Email sent successfully."


# celery -A app.src.celery_tasks.celery worker --loglevel=INFO


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMiwiZXhwIjoxNjgyMzQyOTA5fQ.spdgnbZ83n3hKnMfN0hmQ5-kK0gNEa7jtwrXzysIHeI
# id: 11
@celery_app.task(name="process_email_queue")
def process_email_queue():
    parameters = pika.URLParameters(
        "amqp://roegjsyb:GLm6HM5YrT0XlJY34oJxPcyKFyftBv9-@armadillo.rmq.cloudamqp.com/roegjsyb"
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="email_queue")

    def callback(ch, method, properties, body):
        message = json.loads(body)
        send_email(message)
        print("Sent email:", message)

    channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)
    print("Listening for emails...")
    channel.start_consuming()
