import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# Bot Token
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Image URLs
HUSBAND_IMAGE = os.environ.get("HUSBAND_IMAGE", "https://placehold.co/600x400/1a1a2e/e94560?text=Today's+Husband")
WIFE_IMAGE = os.environ.get("WIFE_IMAGE", "https://placehold.co/600x400/1a1a2e/e94560?text=Today's+Wife")
SON_IMAGE = os.environ.get("SON_IMAGE", "https://placehold.co/600x400/1a1a2e/0f3460?text=Today's+Son")
DAUGHTER_IMAGE = os.environ.get("DAUGHTER_IMAGE", "https://placehold.co/600x400/1a1a2e/0f3460?text=Today's+Daughter")
COUPLE_IMAGE = os.environ.get("COUPLE_IMAGE", "https://placehold.co/600x400/1a1a2e/533483?text=Today's+Couple")

# Random funny ending lines
FUNNY_LINES = [
    "😂 Perfect Match!",
    "❤️ Destiny Chose You!",
    "💞 Couple of the Day!",
    "🤣 Family Complete!",
    "💍 Happily Ever After!",
    "🔥 Match Made in Heaven!",
    "😂 Sent by the Algorithm Gods!",
    "✨ Soulmates Found!"
]

# Error Messages
ERR_PRIVATE_CHAT = "⚠️ This command only works in groups."
ERR_NOT_ENOUGH_MEMBERS = "⚠️ Not enough members found in my database. Send more messages in the group so I can remember everyone!"

# Help Text
HELP_TEXT = """👋 <b>Welcome to Random Relationship Bot!</b>

I randomly pick members from this group and assign them fun relationships!

<b>📖 Commands:</b>
/husband - Pick today's husband
/wife - Pick today's wife
/son - Pick today's son
/daughter - Pick today's daughter
/couple - Pick today's perfect couple
/help - Show this message

<i>💡 Tip: I learn who is in the group as people send messages. If I say "Not enough members", just chat a bit more!</i>"""
