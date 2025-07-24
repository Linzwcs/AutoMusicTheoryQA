import random
import music21
import re
from ..prototype import BasePrototype,MusicTheorySingleChoiceQuestion,MusicSheet

class IntervalNumberQuestion(BasePrototype):
    difficulty = "2"  # 这是一个相对基础的乐理问题
    catagory = "Intervals"
    question = "Given two notes with their ABC scores, select the correct name of the interval between them."

    @staticmethod
    def produce(music_sheet: 'MusicSheet'):
        
        music_abc=music_sheet.get_first_n_measure(n=8)
        dechorded_measures_str = re.sub(r'\[([A-Ga-gz][,\']*\d*/?\d*) [^\]]*\]', r'\1', music_abc)
        unbarred_body = dechorded_measures_str.replace('|', ' ').replace(':', '')
        unbarred_body = re.sub(r'\s+', ' ', unbarred_body).strip()
        all_tokens = re.findall(r'([_^\.=]?[A-Ga-gz][,\']*\d*/?\d*)', unbarred_body)
        a = random.randint(0, len(all_tokens)-1)
        b = random.randint(0, len(all_tokens)-1)
        abc_note_1 = all_tokens[a]
        abc_note_2 = all_tokens[b]
        header=music_sheet.header
        
        try:
            temp_abc_for_analysis = f"{header}\n{" ".join([abc_note_1,abc_note_2])}"            
            analysis_score = music21.converter.parse(temp_abc_for_analysis, format='abc')
            notes_and_rests = list(analysis_score.flat.notesAndRests)  
            ms_note_1,ms_note_2=notes_and_rests  
            interval = music21.interval.Interval(noteStart=ms_note_1, noteEnd=ms_note_2)
            interval_number=interval.niceName.lower()    
        except Exception as e:
            print(e)
        
    
        abc_header = header
        abc_context = f"{abc_header}\n{' '.join([abc_note_1,abc_note_2])}"
        
        correct_answer = str(interval_number)
        
        possible_choices =  ["perfect unison",
                    "minor second",
                    "major second",
                    "minor third",
                    "major third",
                    "perfect fourth",
                    "augmented fourth",  # or "tritone"
                    "diminished fifth",  # also "tritone"
                    "perfect fifth",
                    "minor sixth",
                    "major sixth",
                    "minor seventh",
                    "major seventh",
        ]
        
        try:
            possible_choices.remove(interval_number)
        except:
            pass
        
        if len(possible_choices) < 3:
            return None

        incorrect_answers = random.sample(possible_choices, 3)

        formatted_question = IntervalNumberQuestion.question
        
        return MusicTheorySingleChoiceQuestion(
            question=formatted_question,
            abc_context=abc_context,
            difficulty=IntervalNumberQuestion.difficulty,
            catagory=IntervalNumberQuestion.catagory,
            correct_answer=correct_answer,
            incorrect_answer1=str(incorrect_answers[0]),
            incorrect_answer2=str(incorrect_answers[1]),
            incorrect_answer3=str(incorrect_answers[2]),
        )