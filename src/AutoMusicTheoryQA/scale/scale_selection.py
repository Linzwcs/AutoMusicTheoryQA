import random
import music21
import re
from ..prototype import BasePrototype, MusicTheorySingleChoiceQuestion, MusicSheet


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


class ScaleSelectionQuestion(BasePrototype):
    """
    生成一个乐理问题，要求用户根据ABC乐谱来识别音阶的名称。
    """
    difficulty = "easy"
    category = "Scale"
    # 问题文本现在是一个模板
    question_template = "Select the correctly written {key} key with {direction} direction."

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
    def produce(music_sheet: None):
        """生成一个完整的音阶识别问题。"""
        # 1. 随机选择一个音阶作为正确答案的基础
        key = random.choice(ScaleSelectionQuestion.key)
        scale = ScaleSelectionQuestion.key_to_scale[key]
        scale = convert_scale_to_abc(scale)
        direction = random.choice(['ascending', 'descending'])

        if direction == "ascending":
            scale = scale
        elif direction == "descending":
            scale = list(reversed(scale))

        header = f"L:1/4\nK:C\n"
        correct_answer = header + " ".join(scale)
        incorrect_answers = []
        distractors = set()
        while len(distractors) < 3:
            notes_with_error = scale.copy()
            # 随机选择一个非根音的位置进行修改
            idx_to_change = random.randint(1, len(notes_with_error) - 1)
            original_note = notes_with_error[idx_to_change]
            try:
                if len(original_note) == 1:
                    original_note = random.choice(["^", "_"]) + original_note
                elif len(original_note) == 2:
                    original_note = original_note[1]

                notes_with_error[idx_to_change] = original_note
                incorrect_answer = header + " ".join(notes_with_error)
                if incorrect_answer != correct_answer:
                    distractors.add(incorrect_answer)
            except (ValueError, IndexError):
                continue  # 如果出现意外错误则重试

        incorrect_answers = list(distractors)
        incorrect_answers = [header + " ".join(list(reversed(scale)))
                             ] + incorrect_answers
        question_text = ScaleSelectionQuestion.question_template.format(
            direction=direction, key=key)

        return MusicTheorySingleChoiceQuestion(
            question=question_text,
            abc_context="",
            difficulty=ScaleSelectionQuestion.difficulty,
            category=ScaleSelectionQuestion.category,
            correct_answer=correct_answer,
            incorrect_answer1=incorrect_answers[0],
            incorrect_answer2=incorrect_answers[1],
            incorrect_answer3=incorrect_answers[2],
            class_name=ScaleSelectionQuestion.__name__,
        )
