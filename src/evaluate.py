import openai
import concurrent.futures
from tqdm import tqdm
import json
from simple_parsing import ArgumentParser
from functools import partial
from dataclasses import dataclass
import os
import pandas as pd
from abc import abstractclassmethod
import re
import pandas as pd
from pprint import pprint
import random
from google import genai

with open("/Users/zhilin/Documents/Coding/ai4music/music-bench/keys.txt",
          'r') as f:
    api_keys = f.readlines()
    api_keys = [x.strip() for x in api_keys if x.strip() != ""]
    clients_pool = [genai.Client(api_key=key) for key in api_keys]
print(api_keys)
GLOBAL_IDX = 0
GLOBAL_POOL_SIZE = len(clients_pool)


def request_api(
    prompt: str,
    client: genai.Client,
):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(e)
        return None


def read_jsonl(input_file):
    with open(input_file, "r") as f:
        return [json.loads(line) for line in f]


def write_jsonl(output_file, data, mode="a"):

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode) as f:
        for d in data:
            f.write(json.dumps(d) + "\n")


def build_item(item):
    ins = 'Please read the following questions and select the best option from the four choices (A, B, C, and D) provided for each question.\n' + "Please mark your answer inside the \\boxed{} (e.g., \\boxed{A})."

    question = item['question'] + "\n"
    abc_context = item['abc_context']
    correct_answer = item['correct_answer']
    incorrect_answer1 = item['incorrect_answer1']
    incorrect_answer2 = item['incorrect_answer2']
    incorrect_answer3 = item['incorrect_answer3']

    options = [
        correct_answer, incorrect_answer1, incorrect_answer2, incorrect_answer3
    ]
    random.shuffle(options)

    option2answer = {k: v for k, v in zip("ABCD", options)}

    answer2options = {v: k for k, v in zip("ABCD", options)}

    correct_option = answer2options[correct_answer]
    item['prompt'] = ins + question + abc_context + "\n" + "\n".join(
        [f"{k}. {v}" for k, v in option2answer.items()])
    item['correct_option'] = correct_option
    return item


def main(
    input_file: str,
    output_file: str,
):
    data = read_jsonl(input_file)
    if os.path.exists(output_file):
        out = read_jsonl(output_file)
        data = data[len(out):]
    else:
        out = []

    global GLOBAL_IDX, GLOBAL_IDX, clients_pool
    for item in tqdm(data):
        item = build_item(item)
        response = None
        while response is None:
            client = clients_pool[GLOBAL_IDX]
            GLOBAL_IDX = (GLOBAL_IDX + 1) % GLOBAL_POOL_SIZE
            response = request_api(item['prompt'], client=client)
            if response is None:
                continue
            item['response'] = response
            print(response)
            write_jsonl(output_file, [item], "a")


@dataclass
class Config:
    input_file: str
    output_file: str


if __name__ == "__main__":

    parser = ArgumentParser(description="Process OpenAI prompts in parallel.")
    parser.add_arguments(Config, dest="config")
    args = parser.parse_args()

    main(
        input_file=args.config.input_file,
        output_file=args.config.output_file,
    )
