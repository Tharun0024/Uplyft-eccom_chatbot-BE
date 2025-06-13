import sqlite3
import re

DB_PATH = "database/products.db"

def get_gpt_response(user_message):
    user_message = user_message.lower()

    # Extract price limit (e.g., "under 300", "below 500")
    price_limit = None
    price_match = re.search(r"(under|below|less than)\s*(\d+)", user_message)
    if price_match:
        price_limit = float(price_match.group(2))

    # Try to extract keyword (e.g., "candles", "books")
    keywords = re.findall(r"\b[a-z]+\b", user_message)
    ignore = {"under", "below", "than", "show", "me", "buy", "get", "items", "products", "price", "cheap", "cost", "the", "a", "i", "want", "for", "to"}
    filtered_keywords = [word for word in keywords if word not in ignore]

    if not filtered_keywords and price_limit is None:
        return "❌ I couldn't understand your request. Try something like 'candles under 100'."

    # Build SQL query
    query = "SELECT name, price FROM products WHERE 1=1"
    params = []

    if filtered_keywords:
        keyword_clauses = []
        for word in filtered_keywords:
            keyword_clauses.append("LOWER(name) LIKE ?")
            params.append(f"%{word}%")
        query += " AND (" + " OR ".join(keyword_clauses) + ")"

    if price_limit:
        query += " AND price <= ?"
        params.append(price_limit)

    return run_sql_query(query, params)

def run_sql_query(query, params):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        if not results:
            return "❌ No matching products found."

        # Show top 5 products
        message = "🛍️ Here are some products I found:\n"
        for name, price in results[:5]:
            message += f"- {name} – ₹{price:.2f}\n"

        return message.strip()

    except Exception as e:
        return f"⚠️ Failed to run query: {str(e)}"
