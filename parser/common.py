
import os
import random

from parser.parser import answer_question


def fill_temp_with_everything_after_answer(temp, data_base, i, k):
    """Temporary data for checking answers"""
    for j in range(k, len(data_base[i])):
        temp.extend(data_base[i][j])
    for j in range(temp.count(" ")):
        temp.remove(" ")
    return temp


def fill_list_cell_with_only_correct_answer(temp):
    """Check number of correct answers"""
    last_cell = "".join(temp)
    last_cell = last_cell[last_cell.index(":") + 1 :]
    cell = [i for i, j in enumerate(last_cell) if j == "," and i < 12]
    if not cell:
        last_cell = last_cell[:1]
    if len(cell) == 1:
        last_cell = last_cell[:3:2]
    if len(cell) == 2:
        last_cell = last_cell[:5:2]
    if len(cell) == 3:
        last_cell = last_cell[:7:2]
    if len(cell) == 4:
        last_cell = last_cell[:9:2]
    if len(cell) == 5:
        last_cell = last_cell[:11:2]
    if "o" in last_cell or "r" in last_cell:
        last_cell = ""
    return last_cell


def fill_temp_data_after_answers(temp_max, i, temp_data, data_base, temp_data_base):
    """Write correct answers for tasks"""
    for j in range(temp_max):
        temp_data_base[i].append(data_base[i][j])
    temp_data_base[i].append(temp_data)
    return temp_data_base


def remove_empty_questions(temp_data_base):
    """Removes questions without content"""
    possible_chars_in_answers = ["A", "B", "C", "D", "E", "F"]
    for i in range(len(temp_data_base) - 1, 0, -1):
        if not temp_data_base[i][len(temp_data_base[i]) - 1]:
            del temp_data_base[i]
            continue
        if (
            temp_data_base[i][len(temp_data_base[i]) - 1][0]
            not in possible_chars_in_answers
        ):
            del temp_data_base[i]
            continue
    return temp_data_base


def delete_strings_after_correct_answers(data_base, lines):
    """Delete useless data between tasks"""
    max_range_for_base = count_lines_in_simple_question(lines)
    temp_data_base = [[] for _ in range(max_range_for_base)]
    for i, _ in enumerate(data_base):
        for j in range(len(data_base[i])):
            temp = []
            if "Answ" in data_base[i][j]:
                temp = fill_temp_with_everything_after_answer(temp, data_base, i, j)
                temp_data = fill_list_cell_with_only_correct_answer(temp)
                temp_max = j

        temp_data_base = fill_temp_data_after_answers(
            temp_max, i, temp_data, data_base, temp_data_base
        )
    return remove_empty_questions(temp_data_base)


def create_temporary_memory(data_base):
    """It creates a database for questions after filtering"""
    temporary_memory = [[[] for _ in range(8)] for _ in data_base]
    return temporary_memory


def split_data_to_simple_question(data_base):
    """Divide the questions into the question, answers and correct answers"""
    temporary_memory = create_temporary_memory(data_base)
    for i, _ in enumerate(data_base):
        flag = 0
        for j in range(len(data_base[i]) - 1):
            if data_base[i][j].startswith("A."):
                flag = 2
            if data_base[i][j].startswith("B."):
                flag = 3
            if data_base[i][j].startswith("C."):
                flag = 4
            if data_base[i][j].startswith("D."):
                flag = 5
            if data_base[i][j].startswith("E."):
                flag = 6
            if data_base[i][j].startswith("F."):
                flag = 7
            temporary_memory[i][flag].append(data_base[i][j])
        temporary_memory[i][1].append(data_base[i][len(data_base[i]) - 1])
    return temporary_memory


def shuffle_numbers(number_of_questions, temporary_memory):
    """Shuffle tasks who are going to use"""
    random_list = list(range(len(temporary_memory)))
    random.shuffle(random_list)
    questions_memory = [
        [[random_list[i]] for _ in range(9)] for i in range(number_of_questions)
    ]
    for i, _ in enumerate(questions_memory):
        questions_memory[i][8] = False
    return questions_memory


def shuflle_questions(number_of_questions, temporary_memory):
    """Shuffle questions"""
    questions_memory = shuffle_numbers(number_of_questions, temporary_memory)
    for i in range(number_of_questions):
        question_number = questions_memory[i][0][0]
        for j in range(len(temporary_memory[i])):
            questions_memory[i][j] = temporary_memory[question_number][j]
    return questions_memory


def check_maximum_number_of_question(temporary_memory, number_of_questions):
    """Check limit of questions"""
    if len(temporary_memory) < number_of_questions:
        return len(temporary_memory)
    return number_of_questions


def count_lines_in_simple_question(lines):
    """Function to counts questions"""
    count_question = -1
    for line in lines:
        if line.replace(" ", "").startswith("Question"):
            count_question += 1
    return count_question


def remove_beginning_strings_in_question(temp_data_base):
    """Removing the content before the first task"""
    remove_number = 0
    for i, _ in enumerate(temp_data_base):
        number_question = 1 + i
        for j in range(4):
            if str(number_question) in temp_data_base[i][j]:
                del temp_data_base[i][j]
        for j in range(5):
            if temp_data_base[i][j] == "":
                remove_number += 1
        del temp_data_base[i][: 1 + remove_number]
        add = "Question: " + str(number_question)
        temp_data_base[i].insert(0, str(add))
    return temp_data_base


def split_the_base_into_list_of_questions(lines):
    """Divide the file into parts containing a single question"""
    max_range_for_base = count_lines_in_simple_question(lines)
    flag = -1
    temp_data_base = [[] for _ in range(max_range_for_base)]
    contents_in_cell = []
    for line in lines:
        if line.replace(" ", "").startswith("Question"):
            temp_data_base[flag].extend(contents_in_cell)
            flag += 1
            del contents_in_cell[:]
        contents_in_cell.append(line)
    temp_data_base = remove_beginning_strings_in_question(temp_data_base)
    return temp_data_base



def remove_page_number(lines):
    """Finds and deletes consecutive page numbers"""
    lines_now = []
    number_page_inside = 1

    for line in lines:
        temp_line = line.replace(" ", "")
        if temp_line == str(number_page_inside):
            number_page_inside += 1
            continue
        else:
            lines_now.append(line)
    return lines_now


def remove_section_page_footer(lines):
    """Find page footer at the beginning"""
    temp_lines = []
    for line in lines:
        temp_line = line.replace(" ", "")
        if temp_line.startswith("Question"):
            break
        else:
            if temp_line != "":
                temp_lines.append(line)
    return delete_page_footer(lines, temp_lines)


def delete_page_footer(lines, temp_lines):
    """Delete page footer in the file"""
    lines_now = []
    flag = True
    for line in lines:
        for wrong_lines in temp_lines:
            if line.replace(" ", "") == wrong_lines.replace(" ", ""):
                flag = False
        if flag:
            lines_now.append(line)
        else:
            flag = True
    return lines_now


def delete_empty_lines_at_beginning_of_the_document(lines):
    """Delete empty lines"""
    while not lines[0].replace(" ", "").startswith("Question"):
        del lines[0]
    return lines


def delete_empy_lines_in_document(lines):
    """Delete empty lines"""
    lines_now = []
    for line in lines:
        if line == "":
            continue
        else:
            lines_now.append(line)
    return lines_now



def cls():
    """Function console clearing"""
    os.system("cls" if os.name == "nt" else "clear")



def check_number_answers_in_question(questions_memory, i):
    """Count the number of possible answers possible"""
    numbers_question = 6
    if len(questions_memory[i][7]) < 4:
        numbers_question = 5
    if len(questions_memory[i][6]) < 4:
        numbers_question = 4
    return numbers_question


def convert_correct_answers(questions_memory, random_list, values, i):
    """Convert a letters to numbers in the previously determined order"""
    temp_data = []
    for j in range(len(questions_memory[i][1][0])):
        for key, value in random_list.items():
            if questions_memory[i][1][0][j] == key:
                temp_data.append(value)
                break
    for j, _ in enumerate(temp_data):
        for k, _ in enumerate(values):
            if temp_data[j] == values[k] + 1:
                temp_data[j] = k + 1
                break
    temp_data2 = "".join(sorted(map(str, temp_data)))
    return temp_data2


def print_possible_answers(questions_memory, values, i, numbers_question):
    """Print possible answers"""
    number_question = 1
    for j in range(numbers_question):
        print(number_question, ". ", "".join(questions_memory[i][values[j] + 2][1:]))
        number_question += 1


def create_random_list(numbers_question):
    """Create a random list of possible answers"""
    values = list(range(numbers_question))
    random.shuffle(values)
    return values


def ask_question(questions_memory, number_of_questions):
    """Function showing content"""

    random_list = dict(A=1, B=2, C=3, D=4, E=5, F=6)
    for i in range(number_of_questions):
        numbers_question = check_number_answers_in_question(questions_memory, i)
        values = list(range(numbers_question))
        random.shuffle(values)
        values = create_random_list(numbers_question)
        print(i + 1, ": ", "".join(questions_memory[i][0][1:]))
        print_possible_answers(questions_memory, values, i, numbers_question)
        temp_data2 = convert_correct_answers(questions_memory, random_list, values, i)
        # TODO correct answers:
        #print("Do not tell anyone the correct answers are ", temp_data2)
        questions_memory[i][8] = answer_question(temp_data2)
    return questions_memory




