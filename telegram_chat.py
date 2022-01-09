#!/usr/bin/env python3
import requests
from config import *
import datetime, time
import pymysql
from datetime import timedelta

telegram_url = 'https://api.telegram.org/bot' + api_bot
get_updates_url = telegram_url + '/getUpdates?'
db = pymysql.connect(host=host, user=user, password=password, database=name)


def get_updates():
    r = requests.get(get_updates_url)
    print(r.json())
    return r.json()


def get_update_id_from_bd(chat_id):
    try:
        cursor = db.cursor()
        sql_update = chat_id
        sql = "SELECT date_message FROM data_chats WHERE chat_id = %s"
        cursor.execute(sql, sql_update)
        data_db = cursor.fetchone()
        if data_db:
            return data_db
    except Exception as e:
        print(e)


def insert_data_base(chat_id, message_from_user, date_message, chat_name, update_id):
    try:
        cursor = db.cursor()
        sql = "INSERT INTO update_id(update_id) VALUES (%s)"
        cursor.execute(sql, update_id)
        db.commit()
        cursor = db.cursor()
        sql = "INSERT INTO data_chats(chat_name, date_message, message_from_user, chat_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (chat_name, date_message, message_from_user, chat_id))
        db.commit()
        cursor.close()
    except Exception as e:
        print(e)


def update_data_base(chat_id, message_from_user, date_message, chat_name, update_id):
    try:
        cursor = db.cursor()
        sql = "INSERT INTO update_id(update_id) VALUES (%s)"
        cursor.execute(sql, update_id)
        db.commit()
        cursor.close()
        cursor = db.cursor()
        sql = "UPDATE data_chats SET chat_name = %s, date_message = %s, message_from_user = %s, chat_id = %s WHERE " \
              "chat_id = %s "
        cursor.execute(sql, (chat_name, date_message, message_from_user, chat_id, chat_id))
        db.commit()
        cursor.close()

    except Exception as e:
        print(e)


def get_data_chat_member(json_data_request):
    try:
        chat_id = json_data_request['my_chat_member']['chat']['id']
        message_from_user = json_data_request['my_chat_member']['from']['first_name']
        date_message = json_data_request['my_chat_member']['date']
        date_message = datetime.datetime.utcfromtimestamp(date_message) + timedelta(hours=3)
        chat_name = json_data_request['my_chat_member']['chat']['title']
        update_id = json_data_request['update_id']
        dict_data = {
            'chat_id': chat_id,
            'message_from_user': message_from_user,
            'date_message': date_message,
            'chat_name': chat_name,
            'update_id': update_id
        }
        return dict_data
    except:
        print("ERROR CHAT")


def get_data_edited_message_telegram(json_data_request):
    try:
        chat_id = json_data_request['edited_message']['chat']['id']
        message_from_user = json_data_request['edited_message']['from']['first_name']
        date_message = json_data_request['edited_message']['date']
        date_message = datetime.datetime.utcfromtimestamp(date_message) + timedelta(hours=3)
        chat_name = json_data_request['edited_message']['chat']['title']
        update_id = json_data_request['update_id']
        dict_data = {
            'chat_id': chat_id,
            'message_from_user': message_from_user,
            'date_message': date_message,
            'chat_name': chat_name,
            'update_id': update_id
        }
        return dict_data
    except KeyError as e:
        print(f"ERROR MESSAGE JS: {e}")
        if str(e) == "'message'":
            return get_data_chat_member(json_data_request)
        else:
            return get_data_chat_member(json_data_request)


def get_data_json_telegram(json_data_request):
    try:
        chat_id = json_data_request['message']['chat']['id']
        message_from_user = json_data_request['message']['from']['first_name']
        date_message = json_data_request['message']['date']
        date_message = datetime.datetime.utcfromtimestamp(date_message) + timedelta(hours=3)
        chat_name = json_data_request['message']['chat']['title']
        update_id = json_data_request['update_id']
        dict_data = {
            'chat_id': chat_id,
            'message_from_user': message_from_user,
            'date_message': date_message,
            'chat_name': chat_name,
            'update_id': update_id
        }
        return dict_data

    except KeyError as e:
        print(f"ERROR MESSAGE: {e}")
        if str(e) == "'message'":
            return get_data_edited_message_telegram(json_data_request)
        else:
            return "Error"


if __name__ == '__main__':
    json_result = get_updates()
    if json_result['ok']:
        for i in json_result['result']:
            # print(i)
            data_request = get_data_json_telegram(i)
            if data_request != "Error":
                # up_id = data_request['update_id']
                chat_id = data_request['chat_id']
                date_time_message = data_request['date_message']
                # data_sql = (get_update_id_from_bd(up_id))
                data_sql = (get_update_id_from_bd(chat_id))

                if not data_sql:
                    # print("Dannyx Net")
                    insert_data_base(data_request['chat_id'], data_request['message_from_user'],
                                     data_request['date_message'], data_request['chat_name'],
                                     data_request['update_id'])
                else:
                    if date_time_message > data_sql[0]:
                        # print("Dannye EST")
                        update_data_base(data_request['chat_id'], data_request['message_from_user'],
                                         data_request['date_message'], data_request['chat_name'],
                                         data_request['update_id'])
