# llist of employees
employee_roster = [
    "Zy SANGILAN",
    "Raffy Gerardo",
    "RAFFY gerardo",
    "Miggy Grande",
    "ZY SANGILAN",
    "Xander Ferrero",
    "zy sangilan",
    "MiGGy GRANDE",
    "BOB SMITH",
    "John CS",
    "xandy ferrs"
]


def find_employee(roster, name):
    """
    case-insensitive linear search in roster for name.
    """
    matching_indices = []
    # strip and lower for case-insensitive matching
    target = name.strip().lower()

    # linear search
    for index in range(len(roster)):
        if roster[index].strip().lower() == target:
            matching_indices.append(index)

    return matching_indices


def main():
    # header
    print("=" * 40)
    print(f"EMPLOYEE FINDER")
    print("=" * 40)

    #prompt
    to_find = input("Find: ")
    print(find_employee(employee_roster, to_find))


if __name__ == "__main__":
    main()
