import re
import random
from fractions import Fraction
import music21
from ..prototype import BasePrototype, MusicTheorySingleChoiceQuestion, MusicSheet


class BarLinePlacementQuestion(BasePrototype):
    difficult = "easy"
    category = "Beat"
    question = "Based on the time signature, which option correctly places the bar lines for the given sequence of notes?"
    beats = ["2/4", "2/2", "3/4", "3/2", "4/4", "4/2", "9/8", "12/8"]

    @staticmethod
    def _insert_barlines(beats: list, notes_with_duration: list,
                         measure_duration: Fraction) -> str:
        """
        根据精确的时值信息，为ABC标记列表插入小节线。
        """
        barred_tokens = []
        current_measure_val = Fraction(0)
        base_frac = Fraction("1/4")
        idx = 0

        for beat in beats:
            tokens = re.findall(r'([_^\.=]?[A-Ga-gz][,\']*\d*/?\d*)', beat)
            token_nums = len(tokens)
            cumulative = Fraction(0)
            for i in range(token_nums):
                note_obj = notes_with_duration[idx + i]
                note_val = Fraction(base_frac *
                                    note_obj.duration.quarterLength)
                cumulative += note_val

            if current_measure_val + cumulative > measure_duration + Fraction(
                    1, 64):  # 使用容差
                if barred_tokens and barred_tokens[-1] != '|':
                    barred_tokens.append('|')
                current_measure_val = Fraction(0)

            barred_tokens.append(beat)
            current_measure_val += cumulative

            if abs(current_measure_val - measure_duration) < Fraction(
                    1, 64):  # 使用容差
                barred_tokens.append('|')
                current_measure_val = Fraction(0)
            idx += token_nums

        result = " ".join(barred_tokens)
        result = re.sub(r'\s\s+', ' ', result).strip()
        if not result.startswith('|'): result = '| ' + result
        if not result.endswith('|'): result += ' |'

        result = re.sub(r'(\| \s*)+', '| ', result)
        return result

    @staticmethod
    def produce(music_sheet: MusicSheet, n_measure=4):
        if not music_sheet.score or not music_sheet.time_signature: return None
        ts = music_sheet.time_signature
        header = music_sheet.header
        original_measures_str = music_sheet.get_first_n_measure(
            n_measure, drop_chord=True)
        if not original_measures_str: return None

        dechorded_measures_str = re.sub(
            r'\[([A-Ga-gz][,\']*\d*/?\d*) [^\]]*\]', r'\1',
            original_measures_str)

        unbarred_body = dechorded_measures_str.replace('|',
                                                       ' ').replace(':', '')
        unbarred_body = re.sub(r'\s+', ' ', unbarred_body).strip()
        all_tokens = re.findall(r'([_^\.=]?[A-Ga-gz][,\']*\d*/?\d*)',
                                unbarred_body)
        beats = unbarred_body.split(" ")

        try:
            temp_abc_for_analysis = f"{header}\n{dechorded_measures_str}"
            analysis_score = music21.converter.parse(temp_abc_for_analysis,
                                                     format='abc')
            notes_and_rests = list(analysis_score.flat.notesAndRests)
        except Exception:
            return None

        if len(all_tokens) != len(notes_and_rests) or len(all_tokens) < 3:
            return None

        correct_barred_body = BarLinePlacementQuestion._insert_barlines(
            beats, notes_and_rests, Fraction(ts.ratioString))
        question_context = f"{header}\n{unbarred_body}"

        distractors = set()
        possible_wrong_ts_durations = BarLinePlacementQuestion.beats.copy()

        try:
            possible_wrong_ts_durations = [
                t for t in possible_wrong_ts_durations
                if Fraction(t) != Fraction(ts.ratioString)
            ]

        except ValueError:
            pass
        #print(ts.ratioString)
        #print(possible_wrong_ts_durations)
        for wrong_duration in possible_wrong_ts_durations:
            wrong_duration = Fraction(wrong_duration)
            distractor_body = BarLinePlacementQuestion._insert_barlines(
                beats, notes_and_rests, wrong_duration)

            if distractor_body != correct_barred_body:
                distractors.add(distractor_body)

        distractor_list = list(distractors)
        if len(distractor_list) < 3:
            return None
        random.shuffle(distractor_list)

        return MusicTheorySingleChoiceQuestion(
            question=BarLinePlacementQuestion.question,
            abc_context=question_context,  # 无小节线的版本
            difficulty=str(BarLinePlacementQuestion.difficult),
            category=BarLinePlacementQuestion.category,
            correct_answer=f"{header}\n{correct_barred_body}",  # 带有谱头和正确小节线的版本
            incorrect_answer1=f"{header}\n{distractor_list[0]}",
            incorrect_answer2=f"{header}\n{distractor_list[1]}",
            incorrect_answer3=f"{header}\n{distractor_list[2]}",
            class_name=BarLinePlacementQuestion.__name__)
