# main.py

import os
import json
import argparse
import random
import re
from dataclasses import asdict
from .rhythm import (
    TimeSignatureQuestion, 
    BarLinePlacementQuestion
)
from .prototype import MusicSheet,MusicTheorySingleChoiceQuestion

# 注册所有可用的题目生成器
# 如果你未来创建了新的生成器，只需在这里添加即可
QUESTION_PROTOTYPES = [
    TimeSignatureQuestion,
    BarLinePlacementQuestion,
]


def split_abc_tunes(abc_content: str) -> list[str]:
    """将包含多首乐曲的ABC文件内容分割成独立的乐曲字符串列表。"""
    # 乐曲以 X: 编号开头
    tunes = re.split(r'\n(?=X:)', abc_content.strip())
    return [tune.strip() for tune in tunes if tune.strip()]

def generate_questions_from_file(file_path: str) -> list[dict]:
    """
    从单个ABC文件中读取所有乐曲，并为每首乐曲尝试生成所有类型的题目。
    """
    print(f"--- Processing file: {os.path.basename(file_path)} ---")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

    tunes = split_abc_tunes(content)
    generated_questions = []

    for i, tune_abc in enumerate(tunes):
        print(f"  -> Analyzing tune #{i+1}/{len(tunes)}...")
        try:
            music_sheet = MusicSheet(tune_abc)
            if not music_sheet.score:
                print(f"     [Warning] Skipping tune #{i+1} due to parsing failure.")
                continue

            # 为当前乐曲尝试所有已注册的生成器
            for generator_class in QUESTION_PROTOTYPES:
                question = generator_class.produce(music_sheet)
                if question:
                    generated_questions.append(asdict(question))
                    print(f"     [Success] Generated '{generator_class.__name__}'.")
                else:
                    print(f"     [Info] Could not generate '{generator_class.__name__}' for this tune (e.g., too short, unsupported feature).")
        
        except Exception as e:
            print(f"     [Error] An unexpected error occurred while processing tune #{i+1}: {e}")
            continue
            
    return generated_questions

def read_jsonl(input_file):
    with open(input_file, "r") as f:
        return [json.loads(line) for line in f]


def write_jsonl(output_file, data, mode="a"):
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode) as f:
        for d in data:
            f.write(json.dumps(d) + "\n")


def main():
    """主函数，负责解析命令行参数并启动批量生成过程。"""
    parser = argparse.ArgumentParser(
        description="Batch generate music theory questions from a directory of ABC files."
    )
    parser.add_argument(
        "input_file", 
        type=str,
    )
    parser.add_argument(
        "output_file", 
        type=str, 
    )
    args = parser.parse_args()


    all_questions = []
    
    data=read_jsonl(args.input_file)
    random.shuffle(data)
    
    for item in data[:50]:
        abc_music=item['abc_music']
        for Q in QUESTION_PROTOTYPES:
            music_sheet=MusicSheet(abc_music)
            question=Q.produce(music_sheet)
            if question is None:
                continue
            all_questions.append(asdict(Q.produce(music_sheet)))
    
    write_jsonl(args.output_file,all_questions,'w')        
    
        


if __name__ == "__main__":
    main()