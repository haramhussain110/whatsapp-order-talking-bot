# WhatsApp Order-Taking Bot

A WhatsApp-based automated ordering system built with Python, Flask, and Meta's WhatsApp Business Cloud API. Customers can browse a menu, build a cart, and place an order — all within a WhatsApp chat.

## What it does

- Sends an interactive menu when a customer messages the bot
- Lets customers add multiple items to their cart by typing item numbers
- Calculates the total automatically when the customer types "done"
- Sends an order confirmation back to the customer
- Logs every completed order (timestamp, customer number, items, total) to a CSV file for the business owner to review

## How it works

The bot uses a Flask server to receive incoming messages through a webhook connected to Meta's WhatsApp Business Cloud API. Each customer's cart is tracked in memory while they're ordering, and cleared once their order is confirmed.

For local development, the webhook is exposed to the internet using ngrok, which forwards requests from Meta's servers to the local Flask server.

## Tech stack

- Python
- Flask
- WhatsApp Business Cloud API (Meta)
- ngrok (for local webhook tunneling)
- python-dotenv (for environment variable management)

## Example flow

1. Customer sends "Hi" → bot replies with the menu
2. Customer sends "1" → Burger is added to their cart
3. Customer sends "3" → Fries is added to their cart
4. Customer sends "done" → bot replies with the order summary and total, and the order is saved

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install flask requests python-dotenv
   ```
3. Create a `.env` file in the project root with:
   ```
   ACCESS_TOKEN=your_whatsapp_access_token
   PHONE_NUMBER_ID=your_phone_number_id
   ```
4. Run the Flask server:
   ```
   python app.py
   ```
5. Use ngrok (or a similar tool) to expose port 5000 and configure the public URL as your webhook in Meta's developer dashboard

## Notes

This project currently runs on Meta's test WhatsApp number, meaning only pre-verified numbers can interact with it. To use it in production with real customers, the WhatsApp Business app would need to go through Meta's business verification process.

## Author

Built by Haram Hussain as part of a growing portfolio of automation and API-integration projects.
