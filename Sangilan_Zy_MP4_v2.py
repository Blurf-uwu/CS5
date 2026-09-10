"""
GRADE ANALYZER & HONOR ROLL TRACKER (OOP VERSION)
"""

class GradeAnalyzer:
    """
    A class used to collect, analyze, and report student grades.
    Encapsulates student score data and grade analysis operations.
    """

    def __init__(self):
        """Initializes an empty list of scores for the analyzer instance."""
        self.scores = list()

    def add_score(self, score: float):
        """Adds a single numeric score to the collection."""
        self.scores.append(score)

    def is_empty(self) -> bool:
        """Checks if no scores have been collected."""
        return len(self.scores) == 0

    def get_total_students(self) -> int:
        """Returns the total number of student scores entered."""
        return len(self.scores)

    def get_sum(self) -> float:
        """Calculates and returns the sum of all entered grades."""
        return sum(self.scores)

    def get_average(self) -> float:
        """Calculates and returns the class average."""
        if self.is_empty():
            return 0.0
        return self.get_sum() / self.get_total_students()

    def get_highest(self) -> float:
        """Returns the highest grade in the class."""
        if self.is_empty():
            return None
        return max(self.scores)

    def get_lowest(self) -> float:
        """Returns the lowest grade in the class."""
        if self.is_empty():
            return None
        return min(self.scores)

    def get_honor_roll(self) -> list:
        """
        Filters and returns scores that meet or exceed the class average,
        sorted in ascending order.
        """
        if self.is_empty():
            return list()

        class_avg = self.get_average()
        honor_roll = [score for score in self.scores if score >= class_avg]
        honor_roll.sort()
        return honor_roll

    def get_sorted_scores(self) -> list:
        """Returns all entered scores sorted in ascending order."""
        sorted_list = list(self.scores)
        sorted_list.sort()
        return sorted_list

    def collect_scores(self):
        """Prompts the user repeatedly to input student scores until 'done' is entered."""
        print("=== GRADE ANALYZER & HONOR ROLL TRACKER ===")
        print("Enter student scores one by one. Type 'done' when finished.")

        while True:
            user_input = input("Enter grade: ")

            if user_input.strip().lower() == "done":
                break

            # Input validation
            try:
                grade = float(user_input)
                self.add_score(grade)
            except ValueError:
                print("    [!] Invalid input! Please enter a numeric grade or 'done'.")

    def display_summary(self):
        """Displays the performance summary and sorted score lists."""
        if self.is_empty():
            print("No scores entered.")
            return

        total_students = self.get_total_students()
        sum_grades = self.get_sum()
        class_average = self.get_average()
        highest_grade = self.get_highest()
        lowest_grade = self.get_lowest()
        all_scores_sorted = self.get_sorted_scores()
        honor_roll = self.get_honor_roll()

        print("--- CLASS PERFORMANCE SUMMARY ---")
        print(f"Total Students Processed : {total_students}")
        print(f"Sum of All Grades : {sum_grades}")
        print(f"Class Average : {class_average}")
        print(f"Highest Grade : {highest_grade}")
        print(f"Lowest Grade : {lowest_grade}")
        print("--- SORTED LISTS ---")
        print(f"All Scores (Ascending) : {all_scores_sorted}")
        print(f"Honor Roll (>= {class_average}) : {honor_roll}")
        print("================================================")


def main():
    analyzer = GradeAnalyzer()
    analyzer.collect_scores()
    analyzer.display_summary()


if __name__ == "__main__":
    main()
