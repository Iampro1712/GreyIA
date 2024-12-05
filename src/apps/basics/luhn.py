from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from moduls.utils.utils import loading_message

@Client.on_message(filters.command("luhn", prefixes=["/", "."]))
async def luhn(client, message):

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Creador", url="https://t.me/MasterBinn3r")],
        ]
    )

    TEXT = message.text.split()
    cc = " ".join(TEXT[1:]) if len(TEXT) > 1 else None

    card_number = cc
    stk = await loading_message(message, sticker_id=4)
    if await validate_card_number(card_number):
        await stk.delete()
        await message.reply("Valid card number 👍", reply_markup=keyboard)
    else:
        await stk.delete()
        await message.reply("Invalid card number 👎", reply_markup=keyboard)

    id = 6364510923
    user = message.from_user.first_name
    await client.send_message(id, f"Usuario {user} utilizo el comando")

async def validate_card_number(card_number: str) -> bool:
    # Remove any spaces or dashes from the card number
    card_number = card_number.replace(' ', '').replace('-', '')

    # Check if the card number is a valid length
    if len(card_number) < 13 or len(card_number) > 19:
        print("Invalid card number length")
        return False

    # Reverse the card number
    card_number = card_number[::-1]

    # Initialize the sum and the flag
    total = 0
    double = False

    # Iterate over each digit in the reversed card number
    for digit in card_number:
        # Check if the current digit is a valid digit
        if not digit.isdigit():
            print("Invalid card number")
            return False

        # Convert the digit to an integer
        digit = int(digit)

        # Double every second digit
        if double:
            digit *= 2

            # If the doubled digit is greater than 9, subtract 9
            if digit > 9:
                digit -= 9

        # Add the digit to the total
        total += digit

        # Toggle the flag for the next iteration
        double = not double

    # Check if the total is divisible by 10
    if total % 10 == 0:
        print("Valid card number")
        return True
    else:
        print("Invalid card number")
        return False