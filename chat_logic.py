import sqlite3
import re

def get_local_response(user_message):
    conn = sqlite3.connect('database/products.db')
    cursor = conn.cursor()

    user_message = user_message.lower()
    response = "❌ Sorry, I couldn't find relevant products for that."

    # Detect price filter
    price_match = re.search(r'under\s*(\d+)', user_message)
    keyword_match = re.search(r'products|items|show|find|buy|search', user_message)

    if price_match:
        max_price = float(price_match.group(1))
        cursor.execute("SELECT name, price FROM products WHERE price <= ? ORDER BY price ASC LIMIT 5", (max_price,))
        results = cursor.fetchall()

        if results:
            response = "🛍️ Here are some products under ₹{}:\n".format(int(max_price))
            for name, price in results:
                response += f"- {name} – ₹{price:.2f}\n"
        else:
            response = f"❌ No products found under ₹{int(max_price)}."

    elif any(word in user_message for word in ['card', 'bag', 'mug', 'candle', 'hook', 'cup', 'gift']):
        keyword = next(word for word in user_message.split() if word in user_message)
        cursor.execute("SELECT name, price FROM products WHERE name LIKE ? LIMIT 5", ('%' + keyword + '%',))
        results = cursor.fetchall()

        if results:
            response = f"🛒 Products matching '{keyword}':\n"
            for name, price in results:
                response += f"- {name} – ₹{price:.2f}\n"
        else:
            response = f"❌ No matching products found for '{keyword}'."

    elif "hello" in user_message or "hi" in user_message:
        response = "👋 Hi there! I'm Uplyft AI. You can ask me to show products, like 'show me candles under 300' or 'find me a gift'."

    conn.close()
    return response
