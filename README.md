# Telegram_Chats
Скрипт парсит дату обновления всех чатов, в которых присутствует бот. Для запуска скрипта требуется указать актуальный API ключ, доступы к MySQL базе данных.

Предварительно требуется создать следующие таблицы:
CREATE DATABASE telegram_client_chats;

CREATE TABLE data_chats (
chat_name TEXT,
date_message DATETIME,
message_from_user TEXT,
chat_id TEXT
)

CREATE TABLE update_id (
update_id TEXT
)
