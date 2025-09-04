import random
from ..prototype import MusicSheet, BasePrototype, MusicTheorySingleChoiceQuestion


def convert_scale_to_abc(scale):
    abc_scale = []

    flag = True
    for note in reversed(scale):
        if "B" in note and flag:
            flag = False
        if flag == True:
            note = note.lower()
        if len(note) == 2:
            if note[1] == "#":
                note = "^" + note[0]
            elif note[1] == "b":
                note = "_" + note[0]
        abc_scale = [note] + abc_scale
    abc_scale = abc_scale + [abc_scale[0].lower()]
    return abc_scale


class ScaleIdentificationFromAbcQuestion(BasePrototype):
    """
    生成一个乐理问题，要求用户根据ABC乐谱来识别音阶的名称。
    """
    difficulty = "easy"
    category = "Scale"
    question_template = "Select the most suitable key for the following musical score."

    key = [
        "C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B", "Am",
        "Bbm", "Bm", "Cm", "C#m", "Dm", "Ebm", "Em", "Fm", "F#m", "Gm", "G#m"
    ]
    key_to_scale = {
        "C": ["C", "D", "E", "F", "G", "A", "B"],
        "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
        "D": ["D", "E", "F#", "G", "A", "B", "C#"],
        "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
        "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
        "F": ["F", "G", "A", "Bb", "C", "D", "E"],
        "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
        "G": ["G", "A", "B", "C", "D", "E", "F#"],
        "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
        "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
        "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
        "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
        "Am": ["A", "B", "C", "D", "E", "F", "G"],
        "Bbm": ["Bb", "C", "Db", "Eb", "F", "Gb", "Ab"],
        "Bm": ["B", "C#", "D", "E", "F#", "G", "A"],
        "Cm": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
        "C#m": ["C#", "D#", "E", "F#", "G#", "A", "B"],
        "Dm": ["D", "E", "F", "G", "A", "Bb", "C"],
        "Ebm": ["Eb", "F", "Gb", "Ab", "Bb", "Cb", "Db"],
        "Em": ["E", "F#", "G", "A", "B", "C", "D"],
        "Fm": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
        "F#m": ["F#", "G#", "A", "B", "C#", "D", "E"],
        "Gm": ["G", "A", "Bb", "C", "D", "Eb", "F"],
        "G#m": ["G#", "A#", "B", "C#", "D#", "E", "F#"]
    }

    @staticmethod
    def produce(music_sheet=None):
        """生成一个完整的音阶识别问题。"""
        # 1. 随机选择一个音阶作为正确答案的基础
        key = random.choice(ScaleIdentificationFromAbcQuestion.key)
        scale = ScaleIdentificationFromAbcQuestion.key_to_scale[key]
        scale = convert_scale_to_abc(scale)
        scale *= 2
        random.shuffle(scale)
        header = f"L:1/4\nK:C\n"
        abc_context = header + " ".join(scale)
        correct_answer = key
        incorrect_answers = set()
        if "m" in correct_answer:
            incorrect_answers.add(correct_answer.replace("m", ''))
        else:
            incorrect_answers.add(correct_answer + "m")
        if "b" in correct_answer:
            incorrect_answers.add(correct_answer.replace("b", '#'))
            incorrect_answers.add(correct_answer.replace("b", ''))
        elif "#" in correct_answer:
            incorrect_answers.add(correct_answer.replace("#", 'b'))
            incorrect_answers.add(correct_answer.replace("#", ''))
        else:
            incorrect_answers.add(correct_answer[:1] + "b" +
                                  correct_answer[1:])
            incorrect_answers.add(correct_answer[:1] + "#" +
                                  correct_answer[1:])
        incorrect_answers = list(incorrect_answers)

        return MusicTheorySingleChoiceQuestion(
            question=ScaleIdentificationFromAbcQuestion.question_template,
            abc_context=abc_context,
            correct_answer=correct_answer,
            incorrect_answer1=incorrect_answers[0],
            incorrect_answer2=incorrect_answers[1],
            incorrect_answer3=incorrect_answers[2],
            difficulty=ScaleIdentificationFromAbcQuestion.difficulty,
            category=ScaleIdentificationFromAbcQuestion.category,
            class_name=ScaleIdentificationFromAbcQuestion.__name__)
