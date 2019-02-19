import pytest

from parser.common import count_lines_in_simple_question


@pytest.mark.parametrize(
    "input_string, expected",
    [
        (['Question ', ' ', ' manager wa ', 'utilize to accomplish this', 'to', ' ', 'hide', ' ', 'Question', ' ', 'Edit', ' ', 'Question', ' ', 'button.', ' ', 'B.', ' ', 'Create', ' '],2),
         (['multi', 'Question 54', ' ', 'field', ' ', 'called', ' ', 'Missing', ' ', 'Part/s', ' ', 'with', ' ', 'options', ' ',
        'Gadget,', ' ', 'Gizmo,', ' ', 'Question 21 ', 'Widget.'],1),
    ]
)
def test_count_lines_in_simple_question(input_string, expected):
    result = count_lines_in_simple_question(input_string)
    assert result == expected


