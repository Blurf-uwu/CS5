def get_letter_grade(score) -> str:
    """
    converts numerical score to letter grade. returns str.
    """

    if score<60.00: 
        return "F"
    elif score < 63.00:
        return "D-"
    elif score < 67.00:
        return "D"
    elif score < 70.00:
        return "D+"
    elif score < 73.00:
        return "C-"
    elif score < 77.00:
        return "C"
    elif score < 80.00:
        return "C+"
    elif score < 83.00:
        return "B-"
    elif score < 87.00:
        return "B"
    elif score < 90.00:
        return "B+"
    elif score < 93.00:
        return "A-"
    elif score < 97.00:
        return "A"
    else:
        return "A+"

def display_class_statistics(scores):
    """
    computes and displays (prints) class statistics: 
    total no. of students, class average score, highest score, lowest score, passing students, and overall pass rate.
    returns None
    """
    #Header
    print("="*50)
    print(f"{"CLASS SUMMARY STATISTICS":^50}")
    print("="*50)

    #Display of Statistics
    print(f"Total Student Evaluated: {len(scores)}")

    average_score = sum(scores)/len(scores)
    print(f"Class Average Score: {average_score:.2f}%")
    print(f"Highest Score: {max(scores):.2f}% ({get_letter_grade(max(scores))})")
    print(f"Lowest Score: {min(scores):.2f}% ({get_letter_grade(min(scores))})")

    #Counting the number of passers and determining pass rate
    passers = 0
    for score in scores:
        if score >= 60:
            passers+=1
    print(f"Passing Students (>= 60): {passers}/{len(scores)}")
    print(f"Overall Pass Rate: {(passers/len(scores)*100):.2f} %")
    
    print("="*50)


def main():
    """
    manages interactive score entry loop using a while loop. 
    utilizes other functions(display_class_statistics and get_letter_grade)
    to accomplish the main function of this program (get scores, analyze, and return statistics)
    """

    print("=== CS 5 Student Performance & Grade Tracker ===")
    print("Enter student percentage scores (0 to 100). Type 'done' when finished.")

    #Initialize list of student scores
    scores_list = list()
    while True:
        #Input validation and loop for input of student scores
        try:
            indiv_score = (input("Key in score (or 'done): "))
            if indiv_score.strip().lower() == 'done': break
            indiv_score = float(indiv_score)

            if (not 0 <= indiv_score <=100):
                print(f"{indiv_score} is invalid. Score must be between 0 and 100")
            else:
                scores_list.append(indiv_score)
        except ValueError:
            print("Invalid input. Please enter a numerical score or 'done'.")

    #Header for Individual Grade Report
    print("="*50)
    print(f"{"INDIVIDUAL GRADE REPORT":^50}")
    print("="*50)

    #iterate through the list of show each individual grade report
    for i in range(len(scores_list)):
        print(f"Student {i+1}: {scores_list[i]:.2f}% --> Grade: {get_letter_grade(scores_list[i])}")

    #analyzes and displays class statistics
    display_class_statistics(scores_list)
    

#run program    
main()