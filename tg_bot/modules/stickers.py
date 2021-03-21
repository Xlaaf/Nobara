#Credits to @meanii <https://github.com/meanii>
import os
import math
import urllib.request as urllib
from PIL import Image
from html import escape

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import TelegramError
from telegram.ext import run_async, CallbackQueryHandler
from telegram.utils.helpers import mention_html

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.alternate import typing_action
 

@typing_action
def addsticker(update, context):
    msg = update.effective_message
    user = update.effective_user
    args = context.args
    packnum = 0
    packname = "a" + str(user.id) + "_by_" + context.bot.username
    packname_found = 0
    max_stickers = 120
    waiting_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                        ]
                    ]
                    )
    
    while packname_found == 0:
        try:
            stickerset = context.bot.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = (
                    "a"
                    + str(packnum)
                    + "_"
                    + str(user.id)
                    + "_by_"
                    + context.bot.username
                )
            else:
                packname_found = 1
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                packname_found = 1
    kangsticker = "kangsticker.png"
    is_animated = False
    file_id = ""

    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            if msg.reply_to_message.sticker.is_animated:
                is_animated = True
            file_id = msg.reply_to_message.sticker.file_id

        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            file_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("Yea, I can't kang that.")

        kang_file = context.bot.get_file(file_id)
        if not is_animated:
            kang_file.download("kangsticker.png")
        else:
            kang_file.download("kangsticker.tgs")

        if args:
            sticker_emoji = str(args[0])
        elif msg.reply_to_message.sticker and msg.reply_to_message.sticker.emoji:
            sticker_emoji = msg.reply_to_message.sticker.emoji
        else:
            sticker_emoji = "💈"
        
        adding_process = msg.reply_text(
                    "<b>Your sticker will be added in few seconds, please wait...</b>",
                    reply_markup=waiting_keyboard,
                    parse_mode=ParseMode.HTML
                    )
        
        if not is_animated:
            try:
                im = Image.open(kangsticker)
                maxsize = (512, 512)
                if (im.width and im.height) < 512:
                    size1 = im.width
                    size2 = im.height
                    if im.width > im.height:
                        scale = 512 / size1
                        size1new = 512
                        size2new = size2 * scale
                    else:
                        scale = 512 / size2
                        size1new = size1 * scale
                        size2new = 512
                    size1new = math.floor(size1new)
                    size2new = math.floor(size2new)
                    sizenew = (size1new, size2new)
                    im = im.resize(sizenew)
                else:
                    im.thumbnail(maxsize)
                if not msg.reply_to_message.sticker:
                    im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                        ]
                    ]
                    )
                adding_process.edit_text(
                    "<b>Your sticker has been added!</b>"
                    "\n\n<code><i>if you don't see it, remove and re-add the Sticker Pack:</i></code>",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML
                    )

            except OSError as e:
                
                print(e)
                return

            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        png_sticker=open("kangsticker.png", "rb"),
                    )
                    adding_process.delete()
                elif e.message == "Sticker_png_dimensions":
                    im.save(kangsticker, "PNG")
                    adding_process = msg.reply_text(
                        "<b>Your sticker will be added in few seconds, please wait...</b>",
                        reply_markup=waiting_keyboard,
                        parse_mode=ParseMode.HTML
                        )
                    context.bot.add_sticker_to_set(
                        user_id=user.id,
                        name=packname,
                        png_sticker=open("kangsticker.png", "rb"),
                        emojis=sticker_emoji,
                    )
                    edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                        ]
                    ]
                    )
                    adding_process.edit_text(
                        "<b>Your sticker has been added!</b>"
                        "\n\n<code><i>if you don't see it, remove and re-add the Sticker Pack:</i></code>",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML
                        )
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Stickers_too_much":
                    msg.reply_text("Max packsize reached. Press F to pay respecc.")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                        ]
                    ]
                    )
                    msg.reply_text(
                        "<b>Your sticker has been added!</b>"
                        "\n\n<code><i>if you don't see it, remove and re-add the Sticker Pack:</i></code>",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML
                        )
                print(e)

        else:
            packname = "animated" + str(user.id) + "_by_" + context.bot.username
            packname_found = 0
            max_stickers = 50
            while packname_found == 0:
                try:
                    stickerset = context.bot.get_sticker_set(packname)
                    if len(stickerset.stickers) >= max_stickers:
                        packnum += 1
                        packname = (
                            "animated"
                            + str(packnum)
                            + "_"
                            + str(user.id)
                            + "_by_"
                            + context.bot.username
                        )
                    else:
                        packname_found = 1
                except TelegramError as e:
                    if e.message == "Stickerset_invalid":
                        packname_found = 1
            try:
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    tgs_sticker=open("kangsticker.tgs", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                        ]
                    ]
                    )
                adding_process.edit_text(
                        "<b>Your sticker has been added!</b>"
                        "\n\n<code><i>if you don't see it, remove and re-add the Sticker Pack:</i></code>",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML
                        ) 
            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        tgs_sticker=open("kangsticker.tgs", "rb"),
                    )
                    adding_process.delete()
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                        ]
                    ]
                    )
                    adding_process.edit_text(
                            "<b>Your sticker has been added!</b>"
                            "\n\n<code><i>if you don't see it, remove and re-add the Sticker Pack:</i></code>",
                            reply_markup=edited_keyboard,
                            parse_mode=ParseMode.HTML
                            )
                print(e)

    elif args:
        try:
            try:
                urlemoji = msg.text.split(" ")
                png_sticker = urlemoji[1]
                sticker_emoji = urlemoji[2]
            except IndexError:
                sticker_emoji = "💈"
            urllib.urlretrieve(png_sticker, kangsticker)
            im = Image.open(kangsticker)
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
            im.save(kangsticker, "PNG")
            msg.reply_photo(photo=open("kangsticker.png", "rb"))
            context.bot.add_sticker_to_set(
                user_id=user.id,
                name=packname,
                png_sticker=open("kangsticker.png", "rb"),
                emojis=sticker_emoji,
            )
            edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                        ]
                    ]
                    )
            adding_process.edit_text(
                        "<b>Your sticker has been added!</b>"
                        "\n\n<code><i>if you don't see it, remove and re-add the Sticker Pack:</i></code>",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML
                        )
        except OSError as e:
            msg.reply_text("I can only kang images m8.")
            print(e)
            return
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                makepack_internal(
                    update,
                    context,
                    msg,
                    user,
                    sticker_emoji,
                    packname,
                    packnum,
                    png_sticker=open("kangsticker.png", "rb"),
                )
                adding_process.delete()
            elif e.message == "Sticker_png_dimensions":
                im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                        ]
                    ]
                    )
                adding_process.edit_text(
                            "<b>Your sticker has been added!</b>"
                            "\n\n<code><i>if you don't see it, remove and re-add the Sticker Pack:</i></code>",
                            reply_markup=edited_keyboard,
                            parse_mode=ParseMode.HTML
                            )
            elif e.message == "Invalid sticker emojis":
                msg.reply_text("Invalid emoji(s).")
            elif e.message == "Stickers_too_much":
                msg.reply_text("Max packsize reached. Press F to pay respecc.")
            elif e.message == "Internal Server Error: sticker set not found (500)":
                msg.reply_text(
                    "<b>Your sticker has been added!</b>"
                    "\n\n<code><i>if you don't see it, remove and re-add the Sticker Pack:</i></code>",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML
                    )
            print(e)
    else:
        packs_text = "*Please reply to a sticker, or image to kang it!*\n*Oh, by the way. here are your packs:*\n"
        if packnum > 0:
            firstpackname = "a" + str(user.id) + "_by_" + context.bot.username
            for i in range(0, packnum + 1):
                if i == 0:
                    packs = f"t.me/addstickers/{firstpackname}"
                else:
                    packs = f"t.me/addstickers/{packname}"
        else:
            packs = f"t.me/addstickers/{packname}"
        
        edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"{packs}"
                                )
                        ],
                        [
                            InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                        ]
                    ]
                    )
        msg.reply_text(packs_text   ,
                       reply_markup=edited_keyboard,
                       parse_mode=ParseMode.MARKDOWN
                       )
    if os.path.isfile("kangsticker.png"):
        os.remove("kangsticker.png")
    elif os.path.isfile("kangsticker.tgs"):
        os.remove("kangsticker.tgs")


def makepack_internal(
    update,
    context,
    msg,
    user,
    emoji,
    packname,
    packnum,
    png_sticker=None,
    tgs_sticker=None,
):
    name = user.first_name
    name = name[:50]
    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                                text="View Pack", url=f"{packname}"
                                ),
                    [
                        InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                    ]
                ]
            ]
            )
    try:
        extra_version = ""
        if packnum > 0:
            extra_version = " " + str(packnum)
        if png_sticker:
            sticker_pack_name = f"{name}'s stic-pack (@{context.bot.username})" + extra_version
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                sticker_pack_name,
                png_sticker=png_sticker,
                emojis=emoji,
            )
        if tgs_sticker:
            sticker_pack_name = f"{name}'s ani-pack (@{context.bot.username})" + extra_version
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                sticker_pack_name,
                tgs_sticker=tgs_sticker,
                emojis=emoji,
            )

    except TelegramError as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            msg.reply_text(
                "<b>Your Sticker Pack is already created!</b>"
                "\n\nYou can now reply to images, stickers and animated sticker with /addsticker to add them to your pack"
                "\n\n<b>Send /stickers to see all commands and info.</b>",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML
            )
        elif e.message == "Peer_id_invalid" or "bot was blocked by the user":
            msg.reply_text(
                f"</b>{context.bot.first_name}</b> was blocked by you.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="What Is This?", url=f"t.me/spookyanii/58"
                            )
                        ]
                    ]
                ),
            )
        elif e.message == "Internal Server Error: created sticker set not found (500)":
            msg.reply_text(
                "<b>Your Sticker Pack has been created!</b>"
                "\n\nYou can now reply to images, stickers and animated sticker with /addsticker to add them to your pack"
                "\n\n<b>Send /stickers to see all commands and info.</b>",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML
            )
        return

    if success:
        msg.reply_text(
                "<b>Your Sticker Pack has been created!</b>"
                "\n\nYou can now reply to images, stickers and animated sticker with /addsticker to add them to your pack"
                "\n\n<b>Send /stickers to see all commands and info.</b>",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML
            )
    else:
        msg.reply_text("Failed to create sticker pack. Possibly due to blek mejik.")

def getsticker(update, context):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        context.bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text(
            "Hello"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please check the file you requested below."
            "\nPlease use this feature wisely!",
            parse_mode=ParseMode.HTML,
        )
        context.bot.sendChatAction(chat_id, "upload_document")
        file_id = msg.reply_to_message.sticker.file_id
        newFile = context.bot.get_file(file_id)
        newFile.download("sticker.png")
        context.bot.sendDocument(chat_id, document=open("sticker.png", "rb"))
        context.bot.sendChatAction(chat_id, "upload_photo")
        context.bot.send_photo(chat_id, photo=open("sticker.png", "rb"))

    else:
        context.bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text(
            "Hello"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get sticker image",
            parse_mode=ParseMode.HTML,
        )


@typing_action
def stickerid(update, context):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", The sticker id you are replying is :\n <code>"
            + escape(msg.reply_to_message.sticker.file_id)
            + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get id sticker",
            parse_mode=ParseMode.HTML,
        )

@typing_action
def delsticker(update, context):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        context.bot.delete_sticker_from_set(file_id)
        msg.reply_text(
            "Deleted!"
        )
    else:
        update.effective_message.reply_text(
            "Please reply to sticker message to del sticker"
        )
    

__mod_name__ = "Stickers"
KANG_HANDLER = DisableAbleCommandHandler("addsticker", addsticker, pass_args=True)
DEL_HANDLER = DisableAbleCommandHandler("delsticker", delsticker)
STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker)

dispatcher.add_handler(KANG_HANDLER)
dispatcher.add_handler(DEL_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
