#!/usr/bin/env python3

"""A program for learning content from a script"""

import time
import cProfile
import pstats
import io


from parser.pdf_reader import import_data_from_file
from parser.parser import read_info
from parser.rating import results
from parser.common import (
    remove_page_number,
    remove_section_page_footer,
    delete_empty_lines_at_beginning_of_the_document,
    delete_empy_lines_in_document,
    split_the_base_into_list_of_questions,
    split_data_to_simple_question,
    check_maximum_number_of_question,
    shuflle_questions,
    ask_question,
    delete_strings_after_correct_answers,
)


def main():
    """A function that calls all intermediate functions"""
    pr = cProfile.Profile()
    pr.enable()
    start = time.time()
    number_of_questions, file_name = read_info()
    lines = import_data_from_file(file_name)
    lines = remove_page_number(lines)
    lines = remove_section_page_footer(lines)
    lines = delete_empty_lines_at_beginning_of_the_document(lines)
    lines = delete_empy_lines_in_document(lines)
    data_base = split_the_base_into_list_of_questions(lines)
    data_base = delete_strings_after_correct_answers(data_base, lines)
    temporary_memory = split_data_to_simple_question(data_base)
    number_of_questions = check_maximum_number_of_question(
        temporary_memory, number_of_questions
    )
    question_memory = shuflle_questions(number_of_questions, temporary_memory)
    stop = time.time()
    print("The program worked for %.2f seconds" % (stop - start))
    start = time.time()
    questions_memory = ask_question(question_memory, number_of_questions)
    stop = time.time()
    results(questions_memory, start, stop, number_of_questions)
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    #print(s.getvalue())

if __name__ == "__main__":
    main()
