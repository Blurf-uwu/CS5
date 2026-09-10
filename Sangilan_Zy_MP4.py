"""
GRADE ANALYZER & HONOR ROLL TRACKER
"""
stop = False
while True:
    if stop: break
    
    scores = list()

    print("=== GRADE ANALYZER & HONOR ROLL TRACKER ===")
    print("Enter student scores one by one. Type 'done' when finished.")

    # Prompt for scores until 'done' is inputted
    while True:
        user_input = input("Enter grade: ")

        if user_input.lower() == "done":
            break

        # Input validation
        try:
            grade = float(user_input)
            scores.append(grade)
        except ValueError:
            print("    [!] Invalid input! Please enter a numeric grade or 'done'.")

    # Verify if any scores were inputted
    if len(scores) == 0:
        print("No scores entered.")
    else:
        total_students = len(scores)
        highest_grade = max(scores)
        lowest_grade = min(scores)
        sum_grades = sum(scores)
        class_average = sum_grades / total_students

        # Honor Roll
        honor_roll = list()
        for score in scores:
            if score >= class_average:
                honor_roll.append(score)

        # Sorting Lists
        scores.sort()
        honor_roll.sort()

        # Output
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
    
    stop_question = input("would you like to end (y/n)?: ").lower()
    while True:
        if stop_question in ["y","n"]:
            if stop_question == "y": 
                stop = True
                break
            else: break
        else:
            print("please input a valid answer (y/n): ")
            continue
        
print("[END OF HONOR ROLL IDENTIFICATION]")