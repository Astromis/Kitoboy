from telethon.sync import TelegramClient
import pandas as pd
from argparse import ArgumentParser

API_ID=8105340
API_HASH='8ee632a43aff7c01c56833d3eadcd1d1'

CLIENT = TelegramClient('session_id', API_ID, API_HASH)
CLIENT.start()

def parse_messages(messages:list):
    mj = {"user_tag":[], "text":[], "date":[], "nickname": [], "is_retweeted": []}
    for m in messages:
        try:
            mj["user_tag"].append(m.input_sender.user_id)
        except AttributeError:
            continue
        text =  m.text
        if text == "":
            text = "<mediafile>"
        mj["text"].append(text)
        mj["date"].append(str(m.date))
        
        if m.fwd_from != None:
            mj["is_retweeted"].append(True)
        else:
            mj["is_retweeted"].append(False)
        mj["nickname"].append("-")
    return mj

async def get_messages_from(client, url,  limit=None,):
    
    messages = []
    c = 0
    async with client:
        try:
            async for msg in client.iter_messages(url, limit=limit, ): #wait_time=0.5
                messages.append(msg)
                print(f"{c}", end="\r")
                c += 1
                if c > 100:
                    break
        except ValueError:
            print(f"Ending {url}")
            return messages
    print("\n")
    return messages



async def main(chat_url):

    #try:
    messages = await get_messages_from(CLIENT, chat_url, )
    #except:
    #    pass
    messages = parse_messages(messages)
    pd.DataFrame(messages).to_csv(f"data/telegram_chat_{chat_url}", sep="|")

if __name__ == '__main__':
    parser = ArgumentParser(description='')
    parser.add_argument(
        'chat_url',
        type=str,
    )
    args = parser.parse_args()
    with CLIENT:
        CLIENT.loop.run_until_complete(main(args.chat_url))
