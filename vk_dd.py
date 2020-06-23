import random
import threading
import time
import datetime
import asyncio
import traceback

from threading import Thread

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

def main(vkToken, myId, triggerWord):
    while True:
        try:
            vk_session = vk_api.VkApi(token=vkToken)
            longpoll = VkLongPoll(vk_session)
            vk = vk_session.get_api()

            toDeleteCount = None
            toDelete = []

            def delete():
                try:
                    vk.messages.delete(message_ids=str(toDelete),
                                       delete_for_all=1)
                except vk_api.exceptions.ApiError:
                    vk.messages.delete(message_ids=str(toDelete), delete_for_all=0)
                toDelete.clear()


            async def msgDelete():
                for n in vk.messages.getHistory(peer_id=event.peer_id, count=200).get('items'):
                    if n['from_id'] == myId and len(toDelete) < toDeleteCount:
                        toDelete.append(n['id'])
                toDelete.append(event.message_id)
                delete()

            async def msgReplaceDelete():
                for n in vk.messages.getHistory(peer_id=event.peer_id, count=200).get('items'):
                    if n['from_id'] == myId and len(toDelete) < toDeleteCount:
                        toDelete.append(n['id'])
                toDelete.append(event.message_id)
                for h in toDelete[::-1]:
                    if not h == event.message_id:
                        try:
                            vk.messages.edit(peer_id=event.peer_id, message_id=h, message='.')
                        except vk_api.exceptions.Captcha:
                            break
                        except vk_api.exceptions.ApiError:
                            pass
                delete()

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.text.lower().startswith(triggerWord) and event.from_me and len(
                        event.text.split()) is 1:
                    if len(event.text) > len(triggerWord):
                        if event.text[len(triggerWord):] is '1':
                            toDeleteCount = 2
                            asyncio.run(msgDelete())
                        else:
                            if event.text[len(triggerWord):].isdigit() is True:
                                toDeleteCount = int(event.text[len(triggerWord):]) + 1
                                asyncio.run(msgDelete())
                    else:
                        toDeleteCount = 2
                        asyncio.run(msgDelete())
                if event.type == VkEventType.MESSAGE_NEW and event.text.lower().startswith(triggerWord + '-') and event.from_me \
                        and len(event.text.split()) is 1:
                    if len(event.text) > (len(triggerWord) + 1):
                        if event.text[(len(triggerWord) + 1):] is '1':
                            toDeleteCount = 2
                            asyncio.run(msgReplaceDelete())
                        else:
                            if event.text[(len(triggerWord) + 1):].isdigit() is True:
                                toDeleteCount = int(event.text[(len(triggerWord) + 1):]) + 1
                                asyncio.run(msgReplaceDelete())
                    else:
                        toDeleteCount = 2
                        asyncio.run(msgReplaceDelete())
                if event.type == VkEventType.MESSAGE_NEW and event.text.lower().endswith('//') and event.from_me:
                    toDeleteCount = 1
                    asyncio.run(msgReplaceDelete())

                # elif event.type == VkEventType.MESSAGE_NEW and event.text.lower().endswith('//') and event.from_me:
                    # toDeleteCount = 1
                    # asyncio.run(msgDelete())
        except:
            print(traceback.format_exc())
            pass
Thread(target=main, args=('a3348696e516d0f9a51ad802f48ebdf5f4f0f2220b89c3757a672872911c22d777bd7144c5073b5d26ecc',590083098, 'lena')).start()
Thread(target=main, args=('token',id, 'дд')).start()

