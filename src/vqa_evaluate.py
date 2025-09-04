import openai
import concurrent.futures
from tqdm import tqdm
import json
from simple_parsing import ArgumentParser
from functools import partial
from dataclasses import dataclass
import os
import base64  # 新增: 用于图像编码
from typing import List, Dict, Union  # 新增: 用于类型提示
import random


# --- 新增：图像编码辅助函数 ---
def encode_image_to_base64(image_path: str) -> str:
    """将图像文件编码为Base64字符串"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"警告: 图像文件未找到 {image_path}")
        return None
    except Exception as e:
        print(f"警告: 编码图像时出错 {image_path}: {e}")
        return None


# --- 修改：API请求函数以适应多模态输入 ---
def request_api(
        messages: List[Dict],  # 修改: 参数从 prompt: str 变为 messages: List[Dict]
        temperature: float,
        top_p: float,
        max_tokens: int,
        client: openai.OpenAI,
        model_name: str,
        n_samples:
    int = 1,  # 注意：ChatCompletions API 的 n 参数通常用于生成多个独立的 completion，这里保持为1
):
    try:
        # ChatCompletions API现在直接使用messages
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,  # 修改: 直接传递 messages
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=n_samples,
        )
        return list(map(lambda x: x.message.content, response.choices))[0]
    except Exception as e:
        # 返回错误信息，便于调试
        return f"Error: {e}"


# --- 无需修改的辅助函数 ---
def read_jsonl(input_file):
    with open(input_file, "r", encoding='utf-8') as f:
        return [json.loads(line) for line in f]


def write_jsonl(output_file, data, mode="a"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode, encoding='utf-8') as f:
        for d in data:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")


# --- 重写：为VQA任务构建消息负载 ---
def build_vqa_prompt_payload(item: dict, image_dir: str) -> List[Dict]:
    """
    为VQA任务构建多模态消息负载。
    
    Args:
        item (dict): 输入数据，应包含 'question' 和 'image' 键。
        image_dir (str): 存放图像的根目录。

    Returns:
        List[Dict]: 用于API请求的messages列表，如果图像处理失败则返回None。
    """


def build_vqa_prompt_payload(item: dict,
                             image_dir: str) -> Union[List[Dict], None]:
    """
    为包含图像和文本选项的VQA任务构建多模态消息负载。

    Args:
        item (dict): 输入数据，包含 'question', 'abc_context', 'correct_answer', 'incorrect_answer1~3' 等字段。
        image_dir (str): 图像的根目录路径。

    Returns:
        List[Dict]: API所需的 messages 格式；图像处理失败返回 None。
    """
    ins = 'Please read the following questions and select the best option from the four choices (A, B, C, and D) provided for each question.\n' + "Please mark your answer inside the \\boxed{} (e.g., \\boxed{A})."
    class_name = item.get('class_name', None)
    question_text = item.get('question', None)
    image_file = item.get('abc_context', None)

    if question_text is None or image_file is None:
        print(f"警告: 跳过不完整的项目: {item}")
        return None

    # 构建题干图像路径并转为 base64

    if image_file == "":
        content = [
            {
                "type": "text",
                "text": ins + "\n" + question_text
            },
        ]
    else:
        full_image_path = os.path.join(image_dir, image_file)
        base64_image = encode_image_to_base64(full_image_path)
        content = [{
            "type": "text",
            "text": ins + "\n" + question_text
        }, {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpg;base64,{base64_image}"
            }
        }]

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

    # 构建消息内容

    for label in "ABCD":
        # 检查是否为图片路径
        answer = option2answer[label]
        if isinstance(answer, str) and (answer.endswith('.jpg')
                                        or answer.endswith('.png')):
            answer_path = os.path.join(image_dir, answer)
            base64_ans_image = encode_image_to_base64(answer_path)
            if base64_ans_image is None:
                return None
            content.append({"type": "text", "text": f"\n{label}. "})
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpg;base64,{base64_ans_image}"
                }
            })
        else:
            content.append({"type": "text", "text": f"\n{label}. {answer}"})

    # 构造最终消息
    messages = [{"role": "user", "content": content}]
    return (messages, correct_option)


# --- 修改：主函数以处理VQA流程 ---
def main(
    input_file: str,
    output_file: str,
    image_dir: str,  # 新增: 图像目录参数
    n_threads: int = 10,
    response_key: str = "response",
    model_name: str = "Qwen2-VL-2B-Instruct",  # 修改: 默认使用支持视觉的模型
    api_key: str = "your_openai_api_key",
    base_url: str = "https://api.openai.com/v1",
    temperature: float = 0.2,  # VQA通常需要更精确的答案，降低温度
    top_p: float = 1.0,
    max_tokens: int = 300,  # VQA答案可能稍长
    n_samples: int = 1,
):
    data = read_jsonl(input_file)

    # 支持断点续传
    if os.path.exists(output_file):
        out_data = read_jsonl(output_file)
        print(f"输出文件已存在，包含 {len(out_data)} 条记录。将从断点继续...")
        processed_ids = {
            item.get('id', item.get('question'))
            for item in out_data
        }  # 假设有唯一ID或用问题做标识
        data = [
            item for item in data
            if item.get('id', item.get('question')) not in processed_ids
        ]
        print(f"剩余 {len(data)} 条记录需要处理。")

    client = openai.OpenAI(base_url=base_url, api_key=api_key)

    partialed_request_api = partial(
        request_api,
        client=client,
        model_name=model_name,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n_samples=n_samples,
    )

    with concurrent.futures.ThreadPoolExecutor(
            max_workers=n_threads) as executor:
        futures = []
        for item in data:
            # 为每个项目构建VQA消息负载
            messages, correct_option = build_vqa_prompt_payload(
                item, image_dir)
            item['correct_option'] = correct_option
            if messages:
                # 为调试目的，可以将payload存入item
                item['prompt_payload'] = messages
                future = executor.submit(partialed_request_api,
                                         messages=messages)
                futures.append((future, item))

        with tqdm(total=len(futures), desc="Processing VQA requests") as pbar:
            for future, item in futures:
                response = future.result()
                item[response_key] = response

                pbar.update(1)
                # 每次完成后立即写入，防止中断时丢失数据
                write_jsonl(output_file, [item], "a")


# --- 修改：配置类以包含图像目录 ---
@dataclass
class Config:
    input_file: str  # .jsonl file with 'question' and 'image' keys
    output_file: str  # .jsonl file to store the responses
    image_dir: str  # Directory where image files are stored
    n_threads: int = 10  # Number of threads to use for parallel processing
    response_key: str = "response"
    model_name: str = "Qwen2-VL-2B-Instruct"  # Vision-capable model
    api_key: str = "yz_test"  # OpenAI API key
    base_url: str = "http://0.0.0.0:8000"  # OpenAI API base URL
    temperature: float = 0.2
    top_p: float = 1.0
    max_tokens: int = 300
    n_samples: int = 1


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Process VQA requests in parallel using OpenAI API.")
    parser.add_arguments(Config, dest="config")
    args = parser.parse_args()

    # 检查API密钥是否设置
    if args.config.api_key == "your_openai_api_key" or not args.config.api_key:
        api_key_from_env = os.environ.get("OPENAI_API_KEY")
        if api_key_from_env:
            args.config.api_key = api_key_from_env
            print("使用环境变量中的OPENAI_API_KEY。")
        else:
            raise ValueError(
                "错误: 请提供API密钥，通过 --api_key 参数或设置 OPENAI_API_KEY 环境变量。")

    main(
        input_file=args.config.input_file,
        output_file=args.config.output_file,
        image_dir=args.config.image_dir,  # 传递 image_dir
        n_threads=args.config.n_threads,
        response_key=args.config.response_key,
        model_name=args.config.model_name,
        api_key=args.config.api_key,
        base_url=args.config.base_url,
        temperature=args.config.temperature,
        top_p=args.config.top_p,
        max_tokens=args.config.max_tokens,
        n_samples=args.config.n_samples,
    )
