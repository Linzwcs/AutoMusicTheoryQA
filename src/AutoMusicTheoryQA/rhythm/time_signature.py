from ..prototype import BasePrototype,MusicSheet,MusicTheorySingleChoiceQuestion
import random
import re

class TimeSignatureQuestion(BasePrototype):
    difficult = 3
    catagory = "Rhythm&Beat"
    question="Select the correct time signature for the music score."
    choices=["2/4","2/2","3/4", "3/2", "4/4", "4/2","6/8","9/8"]
    @staticmethod
    def produce(music_sheet:MusicSheet,n_measure=4):
        header=music_sheet.header
        measure=music_sheet.get_first_n_measure(n_measure)
        time_signature=music_sheet.time_signature.ratioString
        header=re.sub(r"M:\s*(\d+/\d+)\n","",header)
        choices = TimeSignatureQuestion.choices.copy()
        try:
            choices.remove(time_signature)
        except ValueError:
            pass
        random.shuffle(choices)
        return MusicTheorySingleChoiceQuestion(
            question=TimeSignatureQuestion.question,
            abc_context=header+"\n"+measure,
            difficulty=TimeSignatureQuestion.difficult,
            catagory=TimeSignatureQuestion.catagory,
            correct_answer=time_signature,
            incorrect_answer1=choices[0],
            incorrect_answer2=choices[1],
            incorrect_answer3=choices[2]
        )
        