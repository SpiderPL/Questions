def read_info():
    """Reading the file name and how many questions should it ask"""
    # TODO use 123.pdf file name
    file_name = str(input('Write file name: ').strip())
    number_of_questions = int("".join(
        sorted(filter(lambda x: x.isdigit(), input("How many question you want?: ")))))
    return number_of_questions, file_name

def answer_question(correct_answer):
    """Check if this answer is correct"""
    if correct_answer == "".join(
        sorted(filter(lambda x: x.isdigit(), input("write an answer: ")))
    ):
        print("\nCorrect \n")
        return True
    print("\nTry Again \n")
    return False