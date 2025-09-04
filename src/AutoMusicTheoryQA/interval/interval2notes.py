import random
import music21
import re
from ..prototype import BasePrototype, MusicTheorySingleChoiceQuestion, MusicSheet


class NoteCompletionByInterval(BasePrototype):
    difficulty = "easy"  # 这是一个相对基础的乐理问题
    category = "Interval"
    question = "Select correct note to make the following note in music score form the {interval} interval"

    @staticmethod
    def produce(music_sheet: 'MusicSheet'):
        music_abc = music_sheet.get_first_n_measure(n=8)
        dechorded_measures_str = re.sub(
            r'\[([A-Ga-gz][,\']*\d*/?\d*) [^\]]*\]', r'\1', music_abc)
        unbarred_body = dechorded_measures_str.replace('|',
                                                       ' ').replace(':', '')
        unbarred_body = re.sub(r'\s+', ' ', unbarred_body).strip()
        all_tokens = re.findall(r'([_^=]?[A-Ga-gz][,\']*)', unbarred_body)
        # print(all_tokens)

        a = random.randint(0, len(all_tokens) - 1)
        b = random.randint(0, len(all_tokens) - 1)
        abc_note_1 = all_tokens[a]
        abc_note_2 = all_tokens[b]
        header = music_sheet.header

        try:
            temp_abc_for_analysis = f"{header}\n{" ".join([abc_note_1,abc_note_2])}"
            analysis_score = music21.converter.parse(temp_abc_for_analysis,
                                                     format='abc')
            notes_and_rests = list(analysis_score.flat.notesAndRests)
            ms_note_1, ms_note_2 = notes_and_rests
            interval = music21.interval.Interval(noteStart=ms_note_1,
                                                 noteEnd=ms_note_2)
            interval_number = interval.niceName.lower()
        except Exception as e:
            print(e)
            return None

        abc_header = header

        abc_context = f"{abc_header}\n{abc_note_1}"
        correct_answer = abc_note_2

        possible_choices = set(all_tokens)
        try:
            possible_choices.remove(abc_note_2)
        except:
            pass

        if len(possible_choices) < 3:
            return None

        incorrect_answers = random.sample(list(possible_choices), 3)
        incorrect_answers = [correct_answer.swapcase()] + incorrect_answers
        formatted_question = NoteCompletionByInterval.question.format(
            interval=interval_number)

        return MusicTheorySingleChoiceQuestion(
            question=formatted_question,
            abc_context=abc_context,
            difficulty=NoteCompletionByInterval.difficulty,
            category=NoteCompletionByInterval.category,
            correct_answer=abc_context + " " + correct_answer,
            incorrect_answer1=abc_context + " " + str(incorrect_answers[0]),
            incorrect_answer2=abc_context + " " + str(incorrect_answers[1]),
            incorrect_answer3=abc_context + " " + str(incorrect_answers[2]),
            class_name=NoteCompletionByInterval.__name__)
