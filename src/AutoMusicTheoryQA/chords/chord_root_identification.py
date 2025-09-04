import random
import music21
from music21 import harmony, chord, note, stream, clef
import re
from ..prototype import BasePrototype, MusicTheorySingleChoiceQuestion, MusicSheet

import random
import music21
from music21 import harmony, chord, note, stream, clef
import re


class ChordRootIdentificationQuestion(BasePrototype):
    difficulty = "easy"  # 这是一个相对基础的乐理问题
    # 将类别改为更准确的 "Chords"
    category = "Chord-e"
    # 修改了问题模板中的拼写错误 (serval -> several)
    question = "Select the correct root note of chord name based on the following music sheet."

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
            return ChordRootIdentificationQuestion.produce()

        abc_context = [n.nameWithOctave for n in triad_notes]

        abc_context = ChordRootIdentificationQuestion._convert_to_abc(
            abc_context)
        #print(abc_context)
        formatted_question = ChordRootIdentificationQuestion.question.format(
            full_chord_name.replace("-", "b"))
        header = "K:C\nL:1/4\n"

        assert chosen_root_name.replace("-", "b") in abc_context

        incorrect_answers = abc_context.copy()
        incorrect_answers.remove(chosen_root_name.replace("-", "b"))
        if len(chosen_root_name) == 1:
            incorrect_answers.append(chosen_root_name +
                                     random.choice(["#", "b"]))
        elif len(chosen_root_name) == 2:
            incorrect_answers.append(chosen_root_name[:1])
        else:
            assert ValueError(f"ERROR in chosen_root_name")
        random.shuffle(abc_context)
        return MusicTheorySingleChoiceQuestion(
            question=formatted_question,
            abc_context=header + f"[{''.join(abc_context)}]",
            difficulty=ChordRootIdentificationQuestion.difficulty,
            category=ChordRootIdentificationQuestion.category,
            correct_answer=chosen_root_name.replace("-", "b"),
            incorrect_answer1=incorrect_answers[0],
            incorrect_answer2=incorrect_answers[1],
            incorrect_answer3=incorrect_answers[2],
            class_name=ChordRootIdentificationQuestion.__name__)


class ChordKeyRootIdentificationQuestion(BasePrototype):
    difficulty = "easy"  # 这是一个相对基础的乐理问题
    # 将类别改为更准确的 "Chords"
    category = "Chord-c"
    # 修改了问题模板中的拼写错误 (serval -> several)
    question = "Identify the correct root note of the chord in the following sheet music."
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
    def convert_abc_2_standard(triad, key):
        scale = ChordKeyRootIdentificationQuestion.key_to_scale[key]
        note_mapping = {k[0]: k for k in scale}
        note_mapping.update({k.lower()[0]: k.lower() for k in scale})
        return [note_mapping[t] for t in triad]

    @staticmethod
    def produce(
            music_sheet: 'MusicSheet' = None):  # music_sheet is optional here
        """
        Generates a multiple-choice question asking to complete a triad.
        """
        triad_notes = [
            "CEG",
            "DFA",
            "EGB",
            "FAc",
            "GBd",
            "Ace",
            "Bdf",
        ]
        key = random.choice(ChordKeyRootIdentificationQuestion.key)
        triad = list(random.choice(triad_notes))

        mapped_traid = ChordKeyRootIdentificationQuestion.convert_abc_2_standard(
            triad, key)
        root_name = mapped_traid[0]

        random.shuffle(triad)

        abc_context = f"K:{key}\nL:1/4\n[{"""""".join(triad)}]"
        incorrect_answers = set(mapped_traid) | set(triad)
        incorrect_answers.add(root_name[0])
        incorrect_answers.add(root_name[0] + "b")
        incorrect_answers.add(root_name[0] + "#")
        incorrect_answers.remove(root_name)
        incorrect_answers = list(incorrect_answers)
        random.shuffle(incorrect_answers)

        return MusicTheorySingleChoiceQuestion(
            question=ChordKeyRootIdentificationQuestion.question,
            abc_context=abc_context,
            difficulty=ChordKeyRootIdentificationQuestion.difficulty,
            category=ChordKeyRootIdentificationQuestion.category,
            correct_answer=root_name,
            incorrect_answer1=incorrect_answers[0],
            incorrect_answer2=incorrect_answers[1],
            incorrect_answer3=incorrect_answers[2],
            class_name=ChordKeyRootIdentificationQuestion.__name__)
