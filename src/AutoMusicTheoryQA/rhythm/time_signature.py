from ..prototype import BasePrototype, MusicSheet, MusicTheorySingleChoiceQuestion
import random
import re
from fractions import Fraction


class TimeSignatureQuestion(BasePrototype):
    difficult = "easy"
    category = "Beat"
    question = "Select the correct time signature for the music score."
    choices = [
        '2/8', '6/8', '12/8', '9/8', '6/4', '15/16', '7/8', '2/1', '8/4',
        '3/2', '5/8', '4/2', '9/4', '2/4', '4/1', '3/4', '3/8', '4/4', '2/2',
        '3/1'
    ]

    @staticmethod
    def produce(music_sheet: MusicSheet, n_measure=4):
        header = music_sheet.header
        measure = music_sheet.get_first_n_measure(n_measure)
        time_signature = music_sheet.time_signature.ratioString
        header = re.sub(r"M:\s*(\d+/\d+)\n", "", header)
        choices = TimeSignatureQuestion.choices.copy()
        try:
            choices = [
                t for t in choices if Fraction(t) != Fraction(time_signature)
            ]
        except ValueError:
            pass
        random.shuffle(choices)
        return MusicTheorySingleChoiceQuestion(
            question=TimeSignatureQuestion.question,
            abc_context=header + "\n" + measure,
            difficulty=TimeSignatureQuestion.difficult,
            category=TimeSignatureQuestion.category,
            correct_answer=time_signature,
            incorrect_answer1=choices[0],
            incorrect_answer2=choices[1],
            incorrect_answer3=choices[2],
            class_name=TimeSignatureQuestion.__name__)
