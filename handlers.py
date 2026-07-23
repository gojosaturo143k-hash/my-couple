import random
import logging
from telegram import Update, BotCommand
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import config
import database

logger = logging.getLogger(__name__)

def format_mention(user: dict) -> str:
    """Create an HTML clickable mention for a user."""
    name = user.get("first_name") or "Unknown User"
    user_id = user.get("user_id")
    username = user.get("username")
    
    # If username exists, display @username, but keep it as an HTML link for clickability
    if username:
        display_name = f"@{username}"
    else:
        display_name = name
        
    return f'<a href="tg://user?id={user_id}">{display_name}</a>'


async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Background task: Save every human user who sends a message to the DB."""
    user = update.effective_user
    chat = update.effective_chat
    
    # Only track in groups and supergroups
    if chat and chat.type in ["group", "supergroup"] and user and not user.is_bot:
        database.save_user(
            chat_id=chat.id,
            user_id=user.id,
            username=user.username,
            first_name=user.first_name
        )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    await update.message.reply_text(
        "👋 Hi! I'm the Random Relationship Bot.\n\n"
        "Add me to a group and use /help to see what I can do!",
        parse_mode=ParseMode.HTML
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    await update.message.reply_text(
        config.HELP_TEXT,
        parse_mode=ParseMode.HTML
    )


async def husband_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /husband command."""
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text(config.ERR_PRIVATE_CHAT)
        return

    user = update.effective_user
    random_member = None

    # MUMMY KA SPECIAL RULE
    if user.id == config.MUMMY_ID and config.FIXED_PAPA_ID:
        random_member = database.get_user_by_id(chat.id, config.FIXED_PAPA_ID)
    
    # CHECK FOR OTHER FIXED HUSBAND USERS
    elif user.id in config.FIXED_HUSBAND_USERS:
        fixed_husband_id = config.FIXED_HUSBAND_USERS[user.id]
        random_member = database.get_user_by_id(chat.id, fixed_husband_id)

    # NORMAL RANDOM SYSTEM
    if not random_member:
        if database.get_member_count(chat.id) < 2:
            await update.message.reply_text(config.ERR_NOT_ENOUGH_MEMBERS)
            return
        random_member = database.get_random_user(chat.id, exclude_user_id=user.id)
        
    if not random_member:
        await update.message.reply_text(config.ERR_NOT_ENOUGH_MEMBERS)
        return

    caption = (
        f"💍 <b>Today's Husband</b> 💍\n"
        f"👤 Husband:\n{format_mention(random_member)}\n"
        f"❤️ Selected by:\n{format_mention({'user_id': user.id, 'username': user.username, 'first_name': user.first_name})}\n"
        f"{random.choice(config.FUNNY_LINES)}"
    )

    await context.bot.send_photo(
        chat_id=chat.id,
        photo=config.HUSBAND_IMAGE,
        caption=caption,
        parse_mode=ParseMode.HTML
    )


async def wife_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /wife command."""
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text(config.ERR_PRIVATE_CHAT)
        return

    user = update.effective_user
    random_member = None

    # CHECK FOR FIXED WIFE USERS (Dost + Bhai)
    if user.id in config.FIXED_WIFE_USERS:
        fixed_wife_id = config.FIXED_WIFE_USERS[user.id]
        random_member = database.get_user_by_id(chat.id, fixed_wife_id)

    # NORMAL RANDOM SYSTEM
    if not random_member:
        if database.get_member_count(chat.id) < 2:
            await update.message.reply_text(config.ERR_NOT_ENOUGH_MEMBERS)
            return
        random_member = database.get_random_user(chat.id, exclude_user_id=user.id)
        
    if not random_member:
        await update.message.reply_text(config.ERR_NOT_ENOUGH_MEMBERS)
        return

    caption = (
        f"👰 <b>Today's Wife</b> 👰\n"
        f"💖 Wife:\n{format_mention(random_member)}\n"
        f"Chosen by:\n{format_mention({'user_id': user.id, 'username': user.username, 'first_name': user.first_name})}\n"
        f"{random.choice(config.FUNNY_LINES)}"
    )

    await context.bot.send_photo(
        chat_id=chat.id,
        photo=config.WIFE_IMAGE,
        caption=caption,
        parse_mode=ParseMode.HTML
    )


async def son_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /son command."""
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text(config.ERR_PRIVATE_CHAT)
        return

    user = update.effective_user
    random_member = None

    # CHECK FOR FIXED SON USERS
    if user.id in config.FIXED_SON_USERS:
        fixed_son_id = config.FIXED_SON_USERS[user.id]
        random_member = database.get_user_by_id(chat.id, fixed_son_id)

    # NORMAL RANDOM SYSTEM
    if not random_member:
        if database.get_member_count(chat.id) < 2:
            await update.message.reply_text(config.ERR_NOT_ENOUGH_MEMBERS)
            return
        random_member = database.get_random_user(chat.id, exclude_user_id=user.id)
        
    if not random_member:
        await update.message.reply_text(config.ERR_NOT_ENOUGH_MEMBERS)
        return

    caption = (
        f"👦 <b>Today's Son</b>\n"
        f"👦 Son:\n{format_mention(random_member)}\n"
        f"👨‍👧 Parent:\n{format_mention({'user_id': user.id, 'username': user.username, 'first_name': user.first_name})}\n"
        f"{random.choice(config.FUNNY_LINES)}"
    )

    await context.bot.send_photo(
        chat_id=chat.id,
        photo=config.SON_IMAGE,
        caption=caption,
        parse_mode=ParseMode.HTML
    )


async def daughter_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /daughter command."""
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text(config.ERR_PRIVATE_CHAT)
        return

    if database.get_member_count(chat.id) < 2:
        await update.message.reply_text(config.ERR_NOT_ENOUGH_MEMBERS)
        return

    user = update.effective_user
    random_member = database.get_random_user(chat.id, exclude_user_id=user.id)
    
    if not random_member:
        await update.message.reply_text(config.ERR_NOT_ENOUGH_MEMBERS)
        return

    caption = (
        f"👧 <b>Today's Daughter</b>\n"
        f"👧 Daughter:\n{format_mention(random_member)}\n"
        f"👩‍👧 Parent:\n{format_mention({'user_id': user.id, 'username': user.username, 'first_name': user.first_name})}\n"
        f"{random.choice(config.FUNNY_LINES)}"
    )

    await context.bot.send_photo(
        chat_id=chat.id,
        photo=config.DAUGHTER_IMAGE,
        caption=caption,
        parse_mode=ParseMode.HTML
    )


async def couple_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /couple command."""
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text(config.ERR_PRIVATE_CHAT)
        return

    if database.get_member_count(chat.id) < 3:
        await update.message.reply_text(config.ERR_NOT_ENOUGH_MEMBERS)
        return

    user = update.effective_user
    couple = database.get_random_couple(chat.id, exclude_user_id=user.id)
    
    if not couple:
        await update.message.reply_text(config.ERR_NOT_ENOUGH_MEMBERS)
        return

    caption = (
        f"💖 <b>Today's Couple</b> 💖\n"
        f"❤️ {format_mention(couple[0])}\n"
        f"❤️ {format_mention(couple[1])}\n"
        f"Match made by:\n{format_mention({'user_id': user.id, 'username': user.username, 'first_name': user.first_name})}\n"
        f"{random.choice(config.FUNNY_LINES)}"
    )

    await context.bot.send_photo(
        chat_id=chat.id,
        photo=config.COUPLE_IMAGE,
        caption=caption,
        parse_mode=ParseMode.HTML
    )


async def post_init(application) -> None:
    """Set bot commands on startup so they appear in the Telegram UI."""
    commands = [
        BotCommand("husband", "Pick today's husband"),
        BotCommand("wife", "Pick today's wife"),
        BotCommand("son", "Pick today's son"),
        BotCommand("daughter", "Pick today's daughter"),
        BotCommand("couple", "Pick today's perfect couple"),
        BotCommand("help", "Show help message"),
        BotCommand("start", "Start the bot")
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands set successfully.")
