import csv
import os
from datetime import datetime

# --- Hardcoded stock prices (start set, but you can add more while running) ---
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "MSFT": 310,
    "GOOGL": 140,
    "AMZN": 135
}

# Portfolio holds quantities for all known symbols
PORTFOLIO = {symbol: 0 for symbol in STOCK_PRICES}

# Folder where results will be saved
RESULTS_DIR = "Portfolio_Results"
os.makedirs(RESULTS_DIR, exist_ok=True)  # ✅ Create folder if not exists


def show_available_stocks():
    print("\n=== Available Stocks ===")
    for symbol, price in STOCK_PRICES.items():
        qty = PORTFOLIO.get(symbol, 0)
        print(f"{symbol:<6} → Price: ${price:<8} | Quantity: {qty}")
    print("===============================")


def get_nonneg_int(prompt):
    while True:
        try:
            val = int(input(prompt).strip())
            if val < 0:
                print("❌ Please enter a non-negative number.")
                continue
            return val
        except ValueError:
            print("❌ Invalid quantity. Please enter a number.")


def calculate_breakdown():
    total = 0
    details = []
    for sym, qty in PORTFOLIO.items():
        if qty > 0:
            price = STOCK_PRICES[sym]
            value = qty * price
            total += value
            details.append((sym, qty, price, value))
    return total, details


def display_summary(total, details):
    print("\n📊 Investment Summary:")
    print("=" * 50)
    if not details:
        print("No purchased stocks.")
    else:
        for stock, qty, price, value in details:
            print(f"{stock:<6} → Price: ${price:<6} | Quantity: {qty:<6} | Total: ${value:,.2f}")
    print("=" * 50)
    print(f"💰 Total Investment : ${total:,.2f}")


def generate_timestamped_filename(default_name, ext):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base, _ = os.path.splitext(default_name)
    return os.path.join(RESULTS_DIR, f"{base}_{timestamp}{ext}")


def save_results(total, details):
    choice = input("\nDo you want to save results (txt/csv/none)? ").strip().lower()
    
    if choice == "txt":
        filename = input("Enter filename (leave blank for auto): ").strip()
        if not filename:
            filename = generate_timestamped_filename("portfolio", ".txt")
        elif not filename.endswith(".txt"):
            filename = os.path.join(RESULTS_DIR, filename + ".txt")
        else:
            filename = os.path.join(RESULTS_DIR, filename)

        with open(filename, "w") as f:
            f.write("Investment Summary\n")
            f.write("=" * 50 + "\n")
            for stock, qty, price, value in details:
                f.write(f"{stock:<6} → Price: ${price:<6} | Quantity: {qty:<6} | Total: ${value:,.2f}\n")
            f.write("=" * 50 + "\n")
            f.write(f"Total Investment: ${total:,.2f}\n")
        print("✅ Results saved to", os.path.abspath(filename))

    elif choice == "csv":
        filename = input("Enter filename (leave blank for auto): ").strip()
        if not filename:
            filename = generate_timestamped_filename("portfolio", ".csv")
        elif not filename.endswith(".csv"):
            filename = os.path.join(RESULTS_DIR, filename + ".csv")
        else:
            filename = os.path.join(RESULTS_DIR, filename)

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Stock", "Quantity", "Price", "Total"])
            for stock, qty, price, value in details:
                writer.writerow([stock, qty, price, value])
            writer.writerow([])
            writer.writerow(["Final Total", "", "", total])
        print("✅ Results saved to", os.path.abspath(filename))

    else:
        print("ℹ️ Results not saved.")


def main():
    print("📊 Welcome to Stock Portfolio Tracker!\n")

    while True:
        show_available_stocks()
        raw = input("Enter stock symbol (or 'done'): ").strip()
        stock = raw.strip("'\"").upper()  # handle 'done' / "done" as well

        if stock == "DONE":
            break

        # Unknown symbol → offer to add with price, then ask quantity immediately
        if stock not in STOCK_PRICES:
            print(f"❌ {stock} not available.")
            choice = input(f"Do you want to add {stock}? (y/n): ").strip().lower()
            if choice != "y":
                continue
            try:
                price = float(input(f"Enter price per share for {stock}: ").strip())
                STOCK_PRICES[stock] = price
                if stock not in PORTFOLIO:
                    PORTFOLIO[stock] = 0
                qty = get_nonneg_int(f"Quantity of {stock}: ")
                PORTFOLIO[stock] += qty
                print(f"✅ {stock} added with price ${price} and quantity {qty}.")
            except ValueError:
                print("❌ Invalid price. Skipping this stock.")
            continue  # go to next loop iteration

        # Known symbol → just ask quantity
        qty = get_nonneg_int(f"Quantity of {stock}: ")
        PORTFOLIO[stock] += qty

    # After user types done
    total, details = calculate_breakdown()
    display_summary(total, details)
    save_results(total, details)
    print("👋 Thank you for using Stock Portfolio Tracker!")


if __name__ == "__main__":
    main()
