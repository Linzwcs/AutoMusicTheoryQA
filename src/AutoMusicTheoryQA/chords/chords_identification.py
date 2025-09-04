import random
import music21
from music21 import harmony, chord, note, stream, clef
import re
from ..prototype import BasePrototype, MusicTheorySingleChoiceQuestion, MusicSheet

import random
import music21
from music21 import harmony, chord, note, stream, clef
import re


class ChordIdentificationQuestion(BasePrototype):
    difficulty = "easy"  # 这是一个相对基础的乐理问题
    # 将类别改为更准确的 "Chords"
    category = "Chord"
    # 修改了问题模板中的拼写错误 (serval -> several)
    question = "Select the correct chord name based on the following music sheet."

    @staticmethod
    def _convert_to_abc(abc_context: list):

        min_value = None
        for n in abc_context:

            if min_value is not None:
                min_value = min(int(re.findall(r"\d+", n)[0]), min_value)
            else:
                min_value = int(re.findall(r"\d+", n)[0])
        min_value = str(min_value)

        def map_fn(x):
            if min_value not in x:
                x = x.lower()
            x = re.sub("\d+", "", x)
            if "-" in x:
                x = "_" + x[0]
            if "#" in x:
                x = "^" + x[0]
            return x

        abc_context = list(map(map_fn, abc_context))

        return abc_context

    @staticmethod
    def produce(
            music_sheet: 'MusicSheet' = None):  # music_sheet is optional here
        """
        Generates a multiple-choice question asking to complete a triad.
        """

        root_notes = [
            'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'F', 'B-', 'E-', 'A-',
            'D-', 'G-'
        ]

        chord_types = {
            'Major': '',
            'minor': 'm',
            'diminished': 'dim',
            'augmented': 'aug'
        }
        type_names = list(chord_types.keys())
        chosen_root_name = random.choice(root_notes)
        chosen_type_name = random.choice(list(chord_types.keys()))
        chosen_type_symbol = chord_types[chosen_type_name]

        # 完整的和弦名称，用于问题描述 (e.g., "C Major")
        full_chord_name = f"{chosen_root_name} {chosen_type_name}"
        # 用于 music21 创建和弦的符号 (e.g., "Cm")
        chord_symbol_str = chosen_root_name + chosen_type_symbol

        # 2. 获取和弦的构成音
        # 使用 harmony.ChordSymbol 可以轻松获取三和弦的音符
        try:
            # 在根音后添加'4'来指定八度，确保和弦对象能被正确创建
            chord_obj = harmony.ChordSymbol(chord_symbol_str,
                                            root=chosen_root_name)
            triad_notes = chord_obj.notes[:3]
        except Exception as e:
            # 如果创建失败（不太可能发生，但作为保障），则重新生成一个问题
            print(f"Error creating chord {chord_symbol_str}: {e}")
            return ChordIdentificationQuestion.produce()

        incorrect_answers = set()
        while len(incorrect_answers) < 3:
            distractor = None
            # 随机决定是改变根音还是改变调性来制造干扰项
            chosen_root_name = chosen_root_name.replace("-", "b")
            if random.random() < 0.5:
                # 策略1: 根音相同，调性不同
                new_type_name = random.choice(type_names)
                if new_type_name != chosen_type_name:  # 确保调性已改变
                    distractor = chosen_root_name + chord_types[new_type_name]
            else:
                # 策略2: 调性相同，根音不同
                new_root_name = random.choice(root_notes)
                new_root_name = new_root_name.replace("-", "b")
                if new_root_name != chosen_root_name:  # 确保根音已改变
                    distractor = new_root_name + chosen_type_symbol

            # 确保生成的干扰项不为None，且不与正确答案重复
            if distractor and distractor != chord_symbol_str:
                incorrect_answers.add(distractor)

        incorrect_answers = list(incorrect_answers)
        abc_context = [n.nameWithOctave for n in triad_notes]

        abc_context = ChordIdentificationQuestion._convert_to_abc(abc_context)
        #print(abc_context)
        formatted_question = ChordIdentificationQuestion.question.format(
            full_chord_name.replace("-", "b"))
        header = "K:C\nL:1/4\n"

        return MusicTheorySingleChoiceQuestion(
            question=formatted_question,
            abc_context=header + f"[{''.join(abc_context)}]",
            difficulty=ChordIdentificationQuestion.difficulty,
            category=ChordIdentificationQuestion.category,
            correct_answer=chord_symbol_str.replace("-", "b"),
            incorrect_answer1=incorrect_answers[0],
            incorrect_answer2=incorrect_answers[1],
            incorrect_answer3=incorrect_answers[2],
            class_name=ChordIdentificationQuestion.__name__)
