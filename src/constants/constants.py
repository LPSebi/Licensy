import discord
# Color
embedSuccessColor = 0x00ff00
embedErrorColor = 0xff0000

# Embed
embedErrorTitle = "Error"
embedSuccessTitle = "Success"
embedErrorDescription = "An error has occurred. Please try again later."

embedErrorFull = discord.Embed(
    title=embedErrorTitle, description=embedErrorDescription, color=embedErrorColor)
