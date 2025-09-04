# main.py

import os
import json
import argparse
import random
import re
from dataclasses import asdict
from pathlib import Path
import uuid
import subprocess
from tqdm import tqdm
from copy import deepcopy

from .beats import (TimeSignatureQuestion, BarLinePlacementQuestion)
from collections import defaultdict
from .chords import ChordIdentificationQuestion, ChordsCompletionQuestion,ChordRootIdentificationQuestion,ChordKeyRootIdentificationQuestion
from .interval import IntervalNumberQuestion, NoteCompletionByInterval
from .scale import ScaleSelectionQuestion, ScaleIdentificationFromAbcQuestion
from .prototype import MusicSheet, MusicTheorySingleChoiceQuestion

QUESTION_PROTOTYPES = [
    TimeSignatureQuestion,
    BarLinePlacementQuestion,
    IntervalNumberQuestion,
    NoteCompletionByInterval,
    ChordIdentificationQuestion,
    ChordsCompletionQuestion,
    ScaleIdentificationFromAbcQuestion,
    ScaleSelectionQuestion
]


OPTION_TO_IMAGE = [
    BarLinePlacementQuestion.__name__,
    NoteCompletionByInterval.__name__,
    ChordsCompletionQuestion.__name__,
    ScaleSelectionQuestion.__name__,
]
ABC_CONTEXT_TO_IAMGE=[
    TimeSignatureQuestion.__name__,
    BarLinePlacementQuestion.__name__,
    IntervalNumberQuestion.__name__,
    NoteCompletionByInterval.__name__,
    ChordIdentificationQuestion.__name__,
    ChordsCompletionQuestion.__name__,
    ChordRootIdentificationQuestion.__name__,
    ChordKeyRootIdentificationQuestion.__name__,
    ScaleIdentificationFromAbcQuestion.__name__,
    
]
def convert_abc_to_image(abc, path: Path):
    tmp_abc = f"/tmp/{path.name}.abc"
    tmp_svg = f"/tmp/{path.name}.svg"
    with open(tmp_abc, "w") as f:
        f.write(f"X:1\n{abc}")
    res=subprocess.run(["abcm2ps", "-v", tmp_abc, "-O", tmp_svg],capture_output=True, text=True)
    
    if res.stderr!="":
        raise ValueError("error")
    tmp_svg = f"/tmp/{path.name}001.svg"
    res=subprocess.run(["magick", "convert", tmp_svg, "-trim", "-quality","2000", str(path)],capture_output=True, text=True)
   
    if res.stderr!="":
        raise ValueError("error")
    
    #cairosvg.svg2png(url=tmp_svg, write_to=str(path))
    return


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
    """主函数，负责解析命令行参数并启动批量生成过程。"""
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
    input_path=Path(args.input_file)
    data = read_jsonl(input_path)
    
    random.shuffle(data)
    
    original_questions=[]
    out_dir = Path(args.output_dir)
    for item in tqdm(data):
        item_clone=item.copy()
        try:
            if item['abc_context']:
                related_path = str(Path("images") / f"{str(uuid.uuid1())}.jpg")
                convert_abc_to_image(item['abc_context'], out_dir / related_path)
                item['abc_context'] = related_path

            if item['class_name'] in OPTION_TO_IMAGE:

                related_path =str(Path("images") / f"{str(uuid.uuid1())}.jpg")
                convert_abc_to_image(item['correct_answer'],
                                    out_dir / related_path)
                item['correct_answer'] = related_path

                related_path =str(Path("images") / f"{str(uuid.uuid1())}.jpg")
                convert_abc_to_image(item['incorrect_answer1'],
                                    out_dir / related_path)
                item['incorrect_answer1'] = related_path

                related_path = str(Path("images") / f"{str(uuid.uuid1())}.jpg")
                convert_abc_to_image(item['incorrect_answer2'],
                                    out_dir / related_path)
                item['incorrect_answer2'] = related_path

                related_path = str(Path("images") / f"{str(uuid.uuid1())}.jpg")
                convert_abc_to_image(item['incorrect_answer3'],
                                    out_dir / related_path)

                item['incorrect_answer3'] = related_path
            
            all_questions.append(item)
            
            original_questions.append(item_clone)
        except:
            print("ERRoR in parsing")
            
        
    write_jsonl(out_dir /("vqa_"+input_path.name), all_questions, 'w')

    write_jsonl(out_dir / (input_path.name), original_questions, 'w')


if __name__ == "__main__":
    main()
