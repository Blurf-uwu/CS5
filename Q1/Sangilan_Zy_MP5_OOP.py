"""
GROCERY CART & INVENTORY SYSTEM (OOP VERSION)
"""


class GroceryItem:
    """
    Represents an individual grocery item with a name and price.
    Encapsulates item attributes for cart management.
    """

    def __init__(self, name: str, price: float):
        self.name: str = name
        self.price: float = price

    def __repr__(self) -> str:
        return f"GroceryItem('{self.name}', {self.price:.2f})"


class GroceryCart:
    """
    A class used to collect, manage, search, and analyze grocery cart items.
    Encapsulates cart operations including additions, searches, removals,
    and financial/statistical reporting.
    """

    def __init__(self):
        """Initializes an empty list of grocery items."""
        self.items: list[GroceryItem] = list()

    def add_item(self, name: str, price: float):
        """Adds a grocery item with its corresponding price to the cart."""
        self.items.append(GroceryItem(name, price))

    def is_empty(self) -> bool:
        """Checks if the cart contains no items."""
        return len(self.items) == 0

    def get_total_count(self) -> int:
        """Returns the total number of items in the cart."""
        return len(self.items)

    def get_item_names(self) -> list[str]:
        """Returns a list of all item names currently in the cart."""
        return [item.name for item in self.items]

    def get_prices(self) -> list[float]:
        """Returns a list of all item prices currently in the cart."""
        return [item.price for item in self.items]

    def get_total_bill(self) -> float:
        """Calculates and returns the sum of all item prices."""
        return sum(self.get_prices())

    def get_average_price(self) -> float:
        """Calculates and returns the average price per item."""
        if self.is_empty():
            return 0.0
        return self.get_total_bill() / self.get_total_count()

    def get_most_expensive(self) -> GroceryItem | None:
        """Returns the most expensive GroceryItem, or None if the cart is empty."""
        if self.is_empty():
            return None
        return max(self.items, key=lambda item: item.price)

    def get_cheapest(self) -> GroceryItem | None:
        """Returns the cheapest GroceryItem, or None if the cart is empty."""
        if self.is_empty():
            return None
        return min(self.items, key=lambda item: item.price)

    def get_sorted_prices(self) -> list[float]:
        """Returns all prices sorted in ascending order."""
        prices = self.get_prices()
        prices.sort()
        return prices

    def get_top_lowest_prices(self, n: int = 3) -> list[float]:
        """Returns up to the top n lowest prices in ascending order."""
        return self.get_sorted_prices()[:n]

    def search_item(self, search_name: str) -> bool:
        """
        Searches for an item by name in the cart (case-insensitive).
        Returns True if found, False otherwise.
        """
        target = search_name.strip().lower()
        return any(item.name.lower() == target for item in self.items)

    def remove_item(self, remove_name: str) -> GroceryItem | None:
        """
        Removes the first occurrence of an item by name (case-insensitive).
        Returns the removed GroceryItem, or None if not found.
        """
        target = remove_name.strip().lower()
        for idx, item in enumerate(self.items):
            if item.name.lower() == target:
                return self.items.pop(idx)
        return None

    def collect_items(self):
        """
        Prompts the user to enter grocery items and prices until 'done' is entered.
        Performs input validation for non-empty names and valid, non-negative prices.
        """
        print("=" * 70)
        print("GROCERY CART & INVENTORY SYSTEM")
        print("=" * 70)
        print("Enter grocery items and prices. Type 'done' as the item name to finish.")

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
                    self.add_item(item_name, price)
                    break
                except ValueError:
                    print("    [!] Invalid input! Please enter a numeric price.")

    def search_cart(self):
        """Prompts the user to search for an item in the cart and displays the result."""
        search_query = input("Search item in cart: ").strip()
        if self.search_item(search_query):
            print(f"--> Result: '{search_query.lower()}' IS in your cart!")
        else:
            print(f"--> Result: '{search_query.lower()}' is NOT in your cart!")

    def remove_cart_item(self):
        """Prompts the user to remove an item from the cart and displays the outcome."""
        remove_query = input("Enter item to remove: ").strip()
        removed = self.remove_item(remove_query)
        if removed:
            print(f"--> Success: Removed '{removed.name}' ({removed.price:.2f}) from cart.")
        else:
            print(f"--> Result: '{remove_query.lower()}' not found in cart.")

    def search_and_remove(self):
        """Runs the interactive search and removal routines."""
        print("-" * 70)
        print("SEARCH CART")
        print("-" * 70)
        self.search_cart()
        self.remove_cart_item()

    def display_summary(self):
        """Displays comprehensive cart analysis and price statistics."""
        print("-" * 70)
        print("CART SUMMARY & ANALYSIS")
        print("-" * 70)

        if self.is_empty():
            print("Your cart is empty.")
        else:
            items = self.get_item_names()
            prices = self.get_prices()
            total_count = self.get_total_count()
            total_bill = self.get_total_bill()
            avg_price = self.get_average_price()
            most_expensive = self.get_most_expensive()
            cheapest = self.get_cheapest()
            sorted_prices = self.get_sorted_prices()
            top_3_lowest = self.get_top_lowest_prices(3)

            print(f"Updated Cart Items : {items}")
            print(f"Total Items Count : {total_count}")
            print(f"Total Cart Bill : {total_bill:.2f}")
            print(f"Average Item Price : {avg_price:.2f}")
            print(f"Most Expensive Item : {most_expensive.name} ({most_expensive.price:.2f})")
            print(f"Cheapest Item Price : {cheapest.name} ({cheapest.price:.2f})")
            print(f"Sorted Prices : {sorted_prices}")
            print(f"Top 3 Lowest Prices : {top_3_lowest}")

        print("=" * 70)


def Run():
    """Executes a single session of the Grocery Cart & Inventory System."""
    cart = GroceryCart()
    cart.collect_items()
    cart.search_and_remove()
    cart.display_summary()


def main():
    """Main program driver with session restart functionality."""
    while True:
        Run()

        # Prompt to end program
        while True:
            stop_question = input("would you like to end (y/n)?: ").strip().lower()
            if stop_question in ["y", "n"]:
                print("\n \n \n")
                break
            print("please input a valid answer (y/n): ")

        if stop_question == "y":
            break

    print("Thank you for shopping with us!")


if __name__ == "__main__":
    main()