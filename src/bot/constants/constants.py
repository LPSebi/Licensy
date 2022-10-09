import discord
# Color
EMBED_ERROR_COLOR = 0xff0000
EMBED_WARNING_COLOR = 0xeed202
EMBED_SUCCESS_COLOR = 0x00ff00

# Embed
EMBED_ERROR_TITLE = "Error"
EMBED_ERROR_DESCRIPTION = "An error has occurred. Please try again later."
EMBED_ERROR_INVALID_PRICE = "Please enter a valid price."

EMBED_WARNING_TITLE = "Warning"
EMBED_WARNING_DESCRIPTION = "An error has occurred. This is a demo message, report this to the developers."


EMBED_SUCCESS_TITLE = "Success"
EMBED_SUCCESS_DESCRIPTION = "Success! This is a demo message, report this to the developers."

# Limits
PRODUCT_LIMIT = 10


# Full
EMBED_ERROR_FULL = discord.Embed(
    title=EMBED_ERROR_TITLE, description=EMBED_ERROR_DESCRIPTION, color=EMBED_ERROR_COLOR)
