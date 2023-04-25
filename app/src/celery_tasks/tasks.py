from ..db.session import Base, SessionLocal
import json

import smtplib

import pika

from .celery import celery_app
from .. import dependencies, models, schemas, token
from fastapi import APIRouter, Depends
import datetime
from typing import List


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
    if "status" in message:
        if message["status"] == "Finished":
            message_body = f'\n\nAnnouncement: todo with:\nTitle: {message["title"]}\nDescription: {message["description"]}\nhas been marked complete!'
        else:
            message_body = f'\n\nAnnouncement: todo with:\nTitle: {message["title"]}\nDescription: {message["description"]}\nhas been marked as incomplete!'
    if "notify_due_date" in message:
        message_body = f'\n\nAnnouncement: todo with:\nTitle: {message["title"]}\nDescription: {message["description"]}\nis about to expire!'
    if "notify_morning" in message:
        message_body = f'\n\nAnnouncement at 8.00 AM:\nThe number of todos to complete today is: {message["todo_to_complete"]}\nAmount of todos due but not completed is: {message["todo_overdue"]}!'
    recipients = [message["receiver"]]
    # recipients = ["minhha10c8@gmail.com"]
    server.sendmail(email, recipients, message_body)
    server.quit()
    return "Email sent successfully."


# celery -A app.src.celery_tasks.celery beat --loglevel=INFO
# celery -A app.src.celery_tasks.celery worker --loglevel=INFO


# 2023-04-25T09:51:02.340598


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


@celery_app.task(name="check_due_date")
def check_due_date():
    db = SessionLocal()
    todos = db.query(models.ToDo).filter(models.ToDo.status == "Unfinished").all()
    for todo in todos:
        create_at = todo.created_at
        due_date = todo.due_date
        min_time = (due_date - create_at).total_seconds() / 60.0
        # thời điểm tạo và hạn lớn hơn 15 phút
        current_time = datetime.datetime.now().replace(second=0, microsecond=0)
        # 2023-04-25 12: 34: 56.789 - ->2023-04-25 12:34:00
        time_diff = (due_date - current_time).total_seconds() / 60.0
        # if time_diff <= 15 and time_diff > 0:
        if time_diff <= 15 and time_diff > 0 and min_time >= 15:
            list_todo = db.query(models.ToDoList).filter(models.ToDoList.id == todo.list_id).first()
            user = db.query(models.User).filter(models.User.id == list_todo.owner_id).first()
            message = {
                "receiver": user.email,
                "title": todo.title,
                "description": todo.description,
                "notify_due_date": True,
            }
            # print("check meesage: ", message)
            send_email.delay(message)
            # send_email.apply_async(args=[message], queue="email_queue")
    db.close()


@celery_app.task(name="morning")
def morning():
    db = SessionLocal()
    users = db.query(models.User).all()
    for user in users:
        todo_to_complete = 0
        todo_overdue = 0
        lists = db.query(models.ToDoList).filter(models.ToDoList.owner_id == user.id).all()
        for list_todo in lists:
            todos = (
                db.query(models.ToDo)
                .filter(models.ToDo.status == "Unfinished", models.ToDo.list_id == list_todo.id)
                .all()
            )
            for todo in todos:
                due_date = todo.due_date
                current_time = datetime.datetime.now().replace(second=0, microsecond=0)
                time_diff = (due_date - current_time).total_seconds() / 60.0
                if time_diff < 0:
                    todo_overdue += 1
                todo_to_complete += 1
        message = {
            "receiver": user.email,
            "todo_overdue": todo_overdue,
            "todo_to_complete": todo_to_complete,
            "notify_morning": True,
        }
        # print("check messsage: ", message)
        # print("todo_overdue: ", todo_overdue)
        # print("todo_to_complete: ", todo_to_complete)

        # send_email.apply_async(args=[message], queue="email_queue")
        send_email(message)
    db.close()
