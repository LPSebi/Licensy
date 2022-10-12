import discord
# Color
EMBED_ERROR_COLOR = 0xff0000
EMBED_WARNING_COLOR = 0xeed202
EMBED_SUCCESS_COLOR = 0x00ff00
EMBED_CONFIRMED_COLOR = 0x00ff00
EMBED_CANCELED_COLOR = 0xff0000

# Embed
EMBED_ERROR_TITLE = "Error"
EMBED_ERROR_DESCRIPTION = "An error has occurred. Please try again later."
EMBED_ERROR_INVALID_PRICE = "Please enter a valid price."

EMBED_ERROR_DESCRIPTION_MAX_PRODUCTS = "You have reached the maximum amount of products. Please delete one to create a new one."
EMBED_ERROR_DESCRIPTION_NOT_INITIALIZED = "This server is not initialized. Please run the command `/init` to initialize the server."


EMBED_WARNING_TITLE = "Warning"
EMBED_WARNING_DESCRIPTION = "An error has occurred. This is a demo message, report this to the developers."


EMBED_SUCCESS_TITLE = "Success"
EMBED_SUCCESS_DESCRIPTION = "Success! This is a demo message, report this to the developers."


EMBED_CONFIRMED_TITLE = "Confirmed"
EMBED_CONFIRMED_DESCRIPTION = "Confirmed! Thank you for confirming your choice."


EMBED_CANCELED_TITLE = "Canceled"
EMBED_CANCELED_DESCRIPTION = "Canceled! Thank you for canceling your choice."


# Limits
PRODUCT_LIMIT = 10


# Full
EMBED_ERROR_FULL = discord.Embed(
    title=EMBED_ERROR_TITLE, description=EMBED_ERROR_DESCRIPTION, color=EMBED_ERROR_COLOR)
