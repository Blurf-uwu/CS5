class Vehicle:
    """Blueprint for vehicle objects"""

    def __init__(self, brand, model, color):
        # attributes
        self.brand = brand
        self.model = model
        self.color = color

    def display_info(self):
        # print vehicle details
        print(f"This is a {self.color} {self.brand} (Model: {self.model}).")

    def start_engine(self):
        # print engine start message
        print(f"Engine started for {self.brand}!")


class ElectricVehicle:
    # placeholder class for EVs
    pass

def main():
    # get number of vehicles
    num_vehicles = int(input("Enter number of vehicles: "))

    # list to store vehicles
    vehicles = []

    # get details for each vehicle
    for i in range(num_vehicles):
        print(f"\n=== Enter Details for Vehicle {i + 1} ===")
        brand = input("Enter Brand: ")
        model = input("Enter Model: ")
        color = input("Enter Color: ")

        # add vehicle to list
        vehicles.append(Vehicle(brand, model, color))

    # display info and start engine for each vehicle
    for vehicle in vehicles:
        print(f"\n=== Vehicle {vehicles.index(vehicle) + 1} Details ===")
        vehicle.display_info()
        vehicle.start_engine()


# run program
main()
