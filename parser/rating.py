def results(questions_memory, start, stop, number_of_questions):
    """Show statistic after cycle of learning"""
    correct_answers = 0
    for i, _ in enumerate(questions_memory):
        if questions_memory[i][8]:
            correct_answers += 1
    print(correct_answers, "questions right out of", number_of_questions)
    print("The test was solved in %.1f seconds" % (stop - start))
    effectiveness = "%.1f" % ((correct_answers / number_of_questions) * 100)
    speed_rate = "%.1f" % ((stop - start) / number_of_questions)
    print(
        "It gives {} % and average time for answer was {} seconds".format(
            effectiveness, speed_rate
        )
    )