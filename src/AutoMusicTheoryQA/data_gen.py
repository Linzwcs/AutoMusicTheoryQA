# main.py

import os
import json
import argparse
import random
import re
from dataclasses import asdict
from .rhythm import (TimeSignatureQuestion, BarLinePlacementQuestion)
from collections import defaultdict
from .chords import ChordIdentificationQuestion, ChordsCompletionQuestion, ChordKeyRootIdentificationQuestion, ChordRootIdentificationQuestion
from .interval import IntervalNumberQuestion, NoteCompletionByInterval
from .scale import ScaleSelectionQuestion, ScaleIdentificationFromAbcQuestion
from .prototype import MusicSheet, MusicTheorySingleChoiceQuestion

QUESTION_PROTOTYPES = [
    TimeSignatureQuestion, BarLinePlacementQuestion, IntervalNumberQuestion,
    NoteCompletionByInterval, ChordIdentificationQuestion,
    ChordsCompletionQuestion, ChordRootIdentificationQuestion,
    ChordKeyRootIdentificationQuestion, ScaleIdentificationFromAbcQuestion,
    ScaleSelectionQuestion
]


def read_jsonl(input_file):
    with open(input_file, "r") as f:
        return [json.loads(line) for line in f]


def write_jsonl(output_file, data, mode="a"):
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode) as f:
        for d in data:
            f.write(json.dumps(d) + "\n")


def deduplicate(questions: list):
    question_pool = set()
    deduplicated_questions = []
    for question in questions:
        q = question['question'] + "\n" + question['abc_context']
        if q not in question_pool:
            question_pool.add(q)
            deduplicated_questions.append(question)
    return deduplicated_questions


def main():
    parser = argparse.ArgumentParser(
        description=
        "Batch generate music theory questions from a directory of ABC files.")
    parser.add_argument(
        "input_file",
        type=str,
    )
    parser.add_argument(
        "output_dir",
        type=str,
    )
    args = parser.parse_args()

    all_questions = []

    data = read_jsonl(args.input_file)
    random.shuffle(data)
    all_questions = defaultdict(list)
    for Q in QUESTION_PROTOTYPES:
        for item in data:
            abc_music = item['abc_music']
            music_sheet = MusicSheet(abc_music)
            try:
                question = Q.produce(music_sheet)
            except:
                question = None
            if question is None:
                continue
            all_questions[question.category].append(asdict(question))

    for k in all_questions.keys():
        all_questions[k] = deduplicate(all_questions[k])
        write_jsonl(f"{args.output_dir}/{k}.jsonl", all_questions[k], 'w')


if __name__ == "__main__":
    main()
