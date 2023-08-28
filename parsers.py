from bs4 import BeautifulSoup


def parser_chats(username):
    with open(f'chats/{username}_chats.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    ul_element = soup.find('ul')

    chat_data_list = []

    for li_element in ul_element.find_all('li', class_='styles_menu-conversation-item__xRVEN'):
        conversation_id = li_element.find('div', class_='styles_sides-block__QJXBM')['data-conversation-id']

        sender_name_element = li_element.find('p', class_='styles_right-side__top-name__520T1')
        sender_name = sender_name_element.text.strip() if sender_name_element else ""

        timestamp_element = li_element.find('span', class_='styles_right-side__top-time__lcbOS')
        timestamp = timestamp_element.text.strip() if timestamp_element else ""

        message_element = li_element.find('span', class_='styles_preview__v8Q7r')
        message = message_element.text.strip() if message_element else ""

        unseen_messages_element = li_element.find('span', class_='styles_unseen-message-badge__mU2mu')
        unseen_messages = unseen_messages_element.text.strip() if unseen_messages_element else ""

        chat_data = {
            'chat_id': conversation_id,
            'sender_name': sender_name,
            'timestamp': timestamp,
            'message': message,
            'unseen_messages': unseen_messages
        }
        chat_data_list.append(chat_data)

    return chat_data_list


# parsed_chats = parser_chats()
# for chat in parsed_chats:
#     print(chat)
