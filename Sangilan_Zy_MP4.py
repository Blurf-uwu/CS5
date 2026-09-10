# === GRADE ANALYZER & HONOR ROLL TRACKER ===

# Dynamic Data Collection: Initialize an empty list called scores using list()
scores = list()

print("=== GRADE ANALYZER & HONOR ROLL TRACKER ===")
print("Enter student scores one by one. Type 'done' when finished.")

# Continuous prompt for student scores until 'done' is entered
while True:
    user_input = input("Enter grade: ")

    if user_input.strip().lower() == "done":
        break

    # Input validation
    try:
        grade = float(user_input)
        scores.append(grade)
    except ValueError:
        print("[!] Invalid input! Please enter a numeric grade or 'done'.")

# Empty List Safeguard: verify if any scores were entered using len(scores)
if len(scores) == 0:
    print("No scores entered.")
else:
    total_students = len(scores)
    highest_grade = max(scores)
    lowest_grade = min(scores)
    sum_grades = sum(scores)
    class_average = sum_grades / total_students

    # Honor Roll Extraction: scores strictly greater than or equal to Class Average
    honor_roll = list()
    for score in scores:
        if score >= class_average:
            honor_roll.append(score)

    # List Sorting: sort both lists in ascending order using .sort()
    scores.sort()
    honor_roll.sort()

    # Output Display
    print("--- CLASS PERFORMANCE SUMMARY ---")
    print(f"Total Students Processed : {total_students}")
    print(f"Sum of All Grades : {sum_grades}")
    print(f"Class Average : {class_average}")
    print(f"Highest Grade : {highest_grade}")
    print(f"Lowest Grade : {lowest_grade}")
    print("--- SORTED LISTS ---")
    print(f"All Scores (Ascending) : {scores}")
    print(f"Honor Roll (>= {class_average}) : {honor_roll}")
    print("================================================")
