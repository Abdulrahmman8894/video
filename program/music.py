# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

# important things
import re
import asyncio
# pyrogram stuff
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
# pytgcalls stuff
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
# repository stuff
from program.utils.inline import stream_markup
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
from driver.utils import bash
from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
# youtube-dl stuff
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'youtube-dl -g -f "{format}" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr


@Client.on_message(command(["شغل","تشغيل","play"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text("**انت مشرف مجهول.!\n\n» من فضلك ارجع الي المالك واطلب منه الغاء صلاحيه البقاء مختفيا**")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 **🎧 لاستخدامي ، أحتاج ان اكون مشرفا في المجموعه مع اعطائي الصلاحيات التاليه:\n\n» ❌ __حذف الرسائل__\n» ❌ __اضافه اعضاء__\n» ❌ __اضافه مستخدمين__\n» ❌ __اداره المحادثات الصوتيه__\n\nيتم تحديث البيانات تلقائيًا بعد ترقيتي‌‌**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
        "💡 يــرجـي مـنــح البــوت الصــلاحــيـه التــالـيــه:"
        + "\n» ❌ __**اداره المــحـادثــات الصــوتـيه**__")
        return
    if not a.can_delete_messages:
        await m.reply_text(
        "💡 يــرجـي مـنــح البــوت الصــلاحــيـه التــالـيــه:"
        + "\n» ❌ __**حــذف الـرســائــل**__")
        return
    if not a.can_invite_users:
        await m.reply_text(
        "💡 يــرجـي مـنــح البــوت الصــلاحــيـه التــالـيــه:"
        + "\n» ❌ __**اضــافــه مســتخـدمــيـن**__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot) 
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **فشل في الانضمام**\n\n**السبب**: `{e}`"
            )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **جاري التحميل...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **تـم الاضافه الي القـائـمه »** `{pos}`\n\n🗂 **الاســم:** [{songname}]({link}) | `music`\n💭 **المــجــمـوعــه:** `{chat_id}`\n🧸 **مـطـلوب بــواســطـه:** {requester}",
                )
            else:
             try:
                await suhu.edit("🔄 ** ويـــت  🎸..**")
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                buttons = stream_markup(user_id)
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"🗂 **الاســم:** [{songname}]({link}) | `music`\n💭 **المــجــمـوعــه:** `{chat_id}`\n🧸 **مـطـلوب بــواســطـه:** {requester}",
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫 error:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "»قم بالرد على ملف صوتي أو إعطاء شيء للبحث."
                )
            else:
                suhu = await c.send_message(chat_id, "🔍 **جاري البحث...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("❌ **لا توجد نتائج.**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await thumb(thumbnail, title, userid, ctitle)
                    format = "bestaudio[ext=m4a]"
                    veez, ytlink = await ytdl(format, url)
                    if veez == 0:
                        await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            buttons = stream_markup(user_id)
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"💡 **تـم اضـافـه الاضافه الي القـائـمه »** `{pos}`\n\n🗂 **الاســم:** [{songname}]({url}) | `music`\n**⏱ الوقـــت:** `{duration}`\n🧸 **مـطـلوب بــواســطـه:** {requester}",
                            )
                        else:
                            try:
                                await suhu.edit("🔄 ** ويـــت 🎸...**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                buttons = stream_markup(user_id)
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=InlineKeyboardMarkup(buttons),
                                    caption=f"🗂 **الاســم:** [{songname}]({url}) | `music`\n**⏱ الوقـــت:** `{duration}`\n🧸 **مـطـلوب بــواســطـه:** {requester}",
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» قــم بالرد عـلــي **مـلــف صــوتـي** او **اعـطائــي اسم للبــحث.**"
            )
        else:
            suhu = await c.send_message(chat_id, "🔍 **جاري البحث...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("❌ **لا توجد نتائج.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await thumb(thumbnail, title, userid, ctitle)
                format = "bestaudio[ext=m4a]"
                veez, ytlink = await ytdl(format, url)
                if veez == 0:
                    await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=image,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"💡 **تـم اضـافـه الاضافه الي القـائـمه »** `{pos}`\n\n🗂 **الاســم:** [{songname}]({url}) | `music`\n**⏱ الوقـــت:** `{duration}`\n🧸 **مـطـلوب بــواســطـه:** {requester}",
                        )
                    else:
                        try:
                            await suhu.edit("🔄 ** ويـــت  🎸...**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"🗂 **الاســم:** [{songname}]({url}) | `music`\n**⏱ الوقـــت :** `{duration}`\n🧸 **مـطـلوب بــواســطـه:** {requester}",
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")
