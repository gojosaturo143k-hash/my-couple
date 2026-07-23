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


# ==========================================
# 🌟 VIP / FIXED USERS SYSTEM 🌟
# Yahan apne bhaiyon, mumma aur doston ki Telegram User IDs dalen.
# (Right click karein profile pe -> Copy User ID)
# ==========================================

# Jab ye 2 BHAI /wife use karenge, to unki WIFE YAHIN se fix aayegi
FIXED_WIFE_USERS = {
    8561695845: 5978049970,  # Bhai 1 ka ID: Uski fixed Wife ka ID
    7448958077: 8507634727,  # Bhai 2 ka ID: Uski fixed Wife ka ID
}

# Mummy ji ka special rule: Jab mummy /husband use karenge, to unka HUSBAND fix aayega
MUMMY_ID = 8507634727  # <- Yahan apni mumma ki Telegram ID dalo
FIXED_PAPA_ID = 7448958077  # <- Yahan apne papa (ya jisko unka husband banana hai) ki ID dalo

# Jab ye 3 DOST /son use karenge, to unke SON YAHIN se fix aayenge
FIXED_SON_USERS = {
    8561695845: 7085981434,  # Dost 1 ka ID: Uska fixed Son ka ID
    7448958077: 723206473,  # Dost 2 ka ID: Uska fixed Son ka ID
    8507634727: 8900080804,  # Dost 3 ka ID: Uska fixed Son ka ID
}
