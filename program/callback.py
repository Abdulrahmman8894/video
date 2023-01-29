# Copyright (C) 2021 By VeezMusicProject

from driver.queues import QUEUE
from pyrogram import Client, filters
from program.utils.inline import menu_markup
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.answer("home start")
    await query.edit_message_text(
        f"""✨ **مرحبا [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) يتيح لك تشغيل القرآن والفيديو في مجموعات من خلال محادثات الفيديو الجديدة في Telegram!**

💡 **لمعرفة جميع اوامر البوت اضغط علي » 📚 زرار الاوامر!**

🔖** لمعرفه طريقه استخدام اضغط علي كلمه  » ❓ زرار الدليل الاساسي!""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ اضفني الي مجموعتك ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ الدليل الاساسي", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 الاوامر", callback_data="cbcmds"),
                    InlineKeyboardButton("❤ المالك", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "🪐︙جروب الدعم", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 قناة السورس", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🌐 مبرمج السورس", url="https://t.me/QطMR_X_N"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.answer("user guide")
    await query.edit_message_text(
        f"""❓ **Basic Guide for using this bot:**

1.) **اولا اضفني الى المجموعه.**
2.) **ثانيا ارفعني ادمن .الي المجموعه ثم رقيني ادمن .**
3.) **بعد الترقيه اكتب reloadلاعادة تشغيل البوت بشكل جيد.**
3.) **ضيف @{ASSISTANT_NAME} حساب المساعد او اكتب انضم علشان يدخل .**
4.) **بعد لما تضيفه اكتب شغل لتشغيل اغاني او اكتب فيديو لتشغيل فيديو او لايغ .**
5.) **كل فتره اعمل reload علشان لو في خطا يتصلح.**

📌 **لو واجهت مشكله مع الحساب المساعد اكتب 『اخرج』 وبعدين  اكتب 『انضم』**

💡 **لو محتاج ااي مساعده تواصل مع المطور م شات الدعم: @{GROUP_SUPPORT}**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.answer("commands menu")
    await query.edit_message_text(
        f"""✨ **مرحبا عزيزي [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» **اتبع الازرار التاليه للوصول الي اوامر استخدام البوت !**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👷🏻 اوامر ادمن الجروب", callback_data="cbadmin"),
                    InlineKeyboardButton("🧙🏻 اوامر المطور ", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("📚 الاوامر الاساسيه", callback_data="cbbasic")
                ],[
                    InlineKeyboardButton("🔙 رجوع", callback_data="cbstart")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.answer("basic commands")
    await query.edit_message_text(
        f"""🏮 here is the basic commands:

» شغل - (اسم الاغنيه او اللينك) لتشغيل الاغاني ف المحادثات
» فيديو - (اسم الفديو او اللينك) - لتشغيل الفديو في المحادثات الصوتيه
» لايف - لتشغيل البث المباشر
» كلمات - العثور علي كلمات الاغنيه
» فيد - (اسم او لينك) لتحميل فيديو
» اغنيه (اسم او لينك) - لتحميل اغنيه 
» بحث - (لينك) - للبحث ف اليوتيوب
» بينج - اظهار حاله البوت

⚡️ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.answer("admin commands")
    await query.edit_message_text(
        f"""🏮 here is the admin commands:

» وقف - ايقاف التشغيل مؤقتا
» كمل - استئناف التشغيل 
» تخطي - تشغيل الاغنيه التاليه
»  ايقاف - ايقاف تشغيل الموسيقى
» كتم - كتم البوت في الدردشه الصوتيه
» الغاء كتم - الغاء كتم البوت في الدردشه الصوتيه
» الصوت - `1-200` - ضبط مستوي الصوت
» ريلود - اعاده تشغيل البوت وتحديث قائمه الادمنيه
» انضم - انضمام الحساب المساعد إلي مجموعتك
» اخرج - خروج الحساب المساعد من المجموعه

⚡️ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.answer("sudo commands")
    await query.edit_message_text(
        f"""🏮 here is the sudo commands:

» /rmw - تنظيف الملفات
» /rmd - حذف جميع الملفات المحمله 
» /sysinfo - إظهار معلومات النظام
» /update - تحديث بوتك الي اخر اصدار
» /restart - عمل ريستارت للبوت
» /leaveall - عمل ريستارت للبوت

⚡ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.message.from_user.id
    buttons = menu_markup(user_id)
    chat = query.message.chat.title
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **Settings of** {chat}\n\n⏸ : pause stream\n▶️ : resume stream\n🔇 : mute userbot\n🔊 : unmute userbot\n⏹ : stop stream",
              reply_markup=InlineKeyboardMarkup(buttons),
          )
    else:
        await query.answer("❌ nothing is currently streaming", show_alert=True)


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Only admin with manage video chat permission that can tap this button !", show_alert=True)
    await query.message.delete()
