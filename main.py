from telethon import TelegramClient, errors
import asyncio

# Функция для загрузки списка из файла
def load_list(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

# Функция для загрузки сообщения из файла
def load_message(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Функция для отправки сообщения в чаты
async def send_messages(api_id, api_hash, phone, chats, message):
    client = TelegramClient(phone, api_id, api_hash)
    
    await client.connect()

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            code = input(f'Enter the code for {phone}: ')
            await client.sign_in(phone, code)
        except errors.SessionPasswordNeededError:
            password = input(f'Enter the password for {phone}: ')
            await client.sign_in(password=password)

    for chat in chats:
        try:
            await client.send_message(chat, message)
            print(f'Message sent to {chat}')
        except Exception as e:
            print(f'Failed to send message to {chat}: {e}')
    
    await client.disconnect()

# Главная функция
async def main():
    # Загрузка аккаунтов и чатов
    accounts = load_list('accounts.txt')
    chats = load_list('chats.txt')
    message = load_message('message.txt')

    while True:
        # Отправка сообщений от каждого аккаунта
        tasks = []
        for account in accounts:
            api_id, api_hash, phone = account.split(':')
            tasks.append(send_messages(api_id, api_hash, phone, chats, message))

        await asyncio.gather(*tasks)
        print("All messages sent, waiting for 20 seconds...")
        await asyncio.sleep(20)

if __name__ == '__main__':
    asyncio.run(main())