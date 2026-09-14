def Run_Cart ():
    """GROCERY CART & INVENTORY SYSTEM PROGRAM"""
    # Intro
    print("=" * 70)
    print("GROCERY CART & INVENTORY SYSTEM")
    print("=" * 70)
    print("Enter grocery items and prices. Type 'done' as the item name to finish.")

    # initalization of lists
    items = list()
    prices = list()

    # Prompt for items and prices until 'done'
    while True:
        item_name = input("Item name (or 'done'): ").strip()
        if item_name.lower() == "done":
            break
        if not item_name:
            continue

        # Price input validation
        while True:
            price_input = input(f"Price for {item_name}: ").strip()
            try:
                price = float(price_input)
                if price < 0:
                    print("    [!] Price cannot be negative. Please enter a valid price.")
                    continue
                items.append(item_name)
                prices.append(price)
                break
            except ValueError:
                print("    [!] Invalid input! Please enter a numeric price.")
    
    # Search & Removal
    print("-" * 70)
    print("SEARCH CART")
    print("-" * 70)

    # Cart Search
    search_item = input("Search item in cart: ").strip().lower()
    if search_item in items:
        print(f"--> Result: '{search_item}' IS in your cart!")
    else:
        print(f"--> Result: '{search_item}' is NOT in your cart!")

    # Cart Removal
    remove_item = input("Enter item to remove: ").strip().lower()
    if remove_item in items:
        idx = items.index(remove_item)
        removed_name = items.pop(idx)
        removed_price = prices.pop(idx)
        print(f"--> Success: Removed '{removed_name}' ({removed_price:.2f}) from cart.")
    else:
        print(f"--> Result: '{remove_item}' not found in cart.")

    # Cart Summary & Analysis
    print("-" * 70)
    print("CART SUMMARY & ANALYSIS")
    print("-" * 70)

    if len(items) == 0:
        print("Your cart is empty.")
    else:
        # Summary
        total_count = len(items)
        total_bill = sum(prices)
        avg_price = total_bill / total_count
        most_expensive_idx = prices.index(max(prices))
        most_expensive_item = items[most_expensive_idx]
        cheapest_idx = prices.index(min(prices))
        cheapest_item = items[cheapest_idx]

        print(f"Updated Cart Items : {items}")
        print(f"Total Items Count : {total_count}")
        print(f"Total Cart Bill : {total_bill:.2f}")
        print(f"Average Item Price : {avg_price:.2f}")
        print(f"Most Expensive Item : {most_expensive_item} ({max(prices):.2f})")
        print(f"Cheapest Item Price : {cheapest_item} ({min(prices):.2f})")

        # Sorting & Slicing 
        prices.sort()
        top_3_lowest = prices[:3]

        print(f"Sorted Prices : {prices}")
        print(f"Top 3 Lowest Prices : {top_3_lowest}")

    print("=" * 70)

stop = False
while True:
    if stop: break

    Run_Cart()
    # Prompt to end program
    stop_question = input("would you like to end (y/n)?: ").lower()
    while True:
        if stop_question in ["y","n"]:
            if stop_question == "y": 
                stop = True
                print("\n \n \n") 
                break
            else:
                print("\n \n \n") 
                break
        else:
            print("please input a valid answer (y/n): ")
            continue

print("Thank you for shopping with us!")