import discord
# Color
embedErrorColor = 0xff0000
embedWarningColor = 0xeed202
embedSuccessColor = 0x00ff00

# Embed
embedErrorTitle = "Error"
embedErrorDescription = "An error has occurred. Please try again later."
embedErrorInvalidPrice = "Please enter a valid price."

embedWarningTitle = "Warning"
embedWarningDescription = "An error has occurred. This is a demo message, report this to the developers."


embedSuccessTitle = "Success"
embedSuccessDescription = "Success! This is a demo message, report this to the developers."


embedErrorFull = discord.Embed(
    title=embedErrorTitle, description=embedErrorDescription, color=embedErrorColor)
