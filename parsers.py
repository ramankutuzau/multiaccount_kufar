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


    for chat in chat_data_list:
        print(chat)
    return chat_data_list



def parser_single_chat():

    with open(f'chats/single-chat/aebb4612-1bce-4862-bd58-c2917f2a27a5_chats(main).html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')


    message_blocks = soup.select('div.styles_sender-bubble__UOAuv, div.styles_receiver-bubble__Q6j5A')

    result_dict = []

    for block in message_blocks:

        content_element = block.find('p', class_='styles_sender-bubble-message__content__J7ilo') or block.find(
            'p', class_='styles_receiver-bubble-message__content__xQpe9')

        time_element = content_element.find('span', class_='styles_sender-bubble-message__content_info__SlsBo') or block.find(
            'span',
            class_='styles_receiver-bubble-message__content_info__zAGtw')

        g_elements = time_element.find_all('g')

        g_result = []

        for g_element in g_elements:
            path_element = g_element.find('path')
            if path_element and 'stroke-dashoffset' in path_element.get('style', ''):
                g_result.append("Не Прочитано")
            else:
                g_result.append("Прочитано")

        if time_element:
            time_element.extract()

        content = content_element.get_text().strip()

        time_text = time_element.get_text().strip()

        result_dict.append({
            "content": content,
            "time_text": time_text,
            "g_results": g_result
        })
    for el in result_dict:
        print(el)

parser_single_chat()