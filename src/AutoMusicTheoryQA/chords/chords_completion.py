import random
import music21
from music21 import harmony, chord, note, stream, clef
import re
from ..prototype import BasePrototype, MusicTheorySingleChoiceQuestion, MusicSheet


class ChordsCompletionQuestion(BasePrototype):
    difficulty = "easy"  # 这是一个相对基础的乐理问题
    # 将类别改为更准确的 "Chords"
    category = "Chord"
    # 修改了问题模板中的拼写错误 (serval -> several)
    question = "Given several notes, select the correct Note to form a {} chord."

    @staticmethod
    def _convert_to_abc(abc_context: list, correct_answer, incorrect_answers):
        #print(abc_context+[correct_answer]+incorrect_answers)
        min_value = None
        for n in abc_context + [correct_answer]:
            #print(n)
            #print(type(n))
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
        correct_answer = map_fn(correct_answer)
        incorrect_answers = list(map(map_fn, incorrect_answers))

        return abc_context, correct_answer, incorrect_answers

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
            chord_obj = harmony.ChordSymbol(chord_symbol_str,
                                            root=chosen_root_name)
            triad_notes = chord_obj.notes[:3]
        except Exception as e:
            # 如果 music21 创建失败，可以简单地重新尝试或抛出错误
            print(f"Error creating chord {chord_symbol_str}: {e}")
            # In a real app, you might want to retry
            return ChordsCompletionQuestion.produce()

        correct_answer_note = random.choice(triad_notes)
        # 剩下的音符作为已知条件
        given_notes = [n for n in triad_notes if n != correct_answer_note]

        correct_answer = correct_answer_note.nameWithOctave
        correct_note_names = {n.name for n in triad_notes}  # 用于检查重复

        incorrect_answers = set()
        offsets = [-2, -1, 1, 2, 3, -3]
        random.shuffle(offsets)

        i = 0

        while len(incorrect_answers) < 3 and i < len(offsets):
            offset = offsets[i]
            # 对正确答案的音高进行移调
            potential_incorrect_pitch = correct_answer_note.pitch.transpose(
                offset)
            potential_incorrect_note_name = potential_incorrect_pitch.nameWithOctave

            # 确保生成的错误答案不是和弦内的任何一个音
            if potential_incorrect_note_name not in correct_note_names:
                incorrect_answers.add(potential_incorrect_note_name)
            i += 1

        incorrect_answers = list(incorrect_answers)

        score_stream = stream.Score()
        part = stream.Part()
        measure = stream.Measure()
        measure.append(clef.TrebleClef())
        # 将已知音符作为一个和弦显示，更紧凑
        display_chord = chord.Chord(given_notes)
        measure.append(display_chord)
        part.append(measure)
        score_stream.append(part)

        abc_context = list(score_stream.flat.notesAndRests)
        abc_context = [n.nameWithOctave for n in abc_context[0]]

        abc_context, correct_answer, incorrect_answers = ChordsCompletionQuestion._convert_to_abc(
            abc_context, correct_answer, incorrect_answers)
        #print(abc_context)
        formatted_question = ChordsCompletionQuestion.question.format(
            full_chord_name.replace("-", "b"))
        header = "K:C\nL:1/4\n"
        return MusicTheorySingleChoiceQuestion(
            question=formatted_question,
            abc_context=header + f"[{''.join(abc_context)}]",
            difficulty=ChordsCompletionQuestion.difficulty,
            category=ChordsCompletionQuestion.category,
            correct_answer=header +
            f"[{''.join(abc_context+[correct_answer])}]",
            incorrect_answer1=header +
            f"[{''.join(abc_context+[incorrect_answers[0]])}]",
            incorrect_answer2=header +
            f"[{''.join(abc_context+[incorrect_answers[1]])}]",
            incorrect_answer3=header +
            f"[{''.join(abc_context+[incorrect_answers[2]])}]",
            class_name=ChordsCompletionQuestion.__name__)
