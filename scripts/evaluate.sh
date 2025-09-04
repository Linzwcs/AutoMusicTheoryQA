python src/evaluate.py \
    --input_file ./data/music-bench/music-bench.jsonl \
    --output_file ./output/musicbench/llama3.1-8b-instruct.jsonl \
    --n_threads 128 \
    --prompt_key input \
    --response_key response \
    --answer_key output \
    --model_name qwen3  \
    --base_url http://127.0.0.1:9998/v1 \
    --max_tokens 8192 \
    --api_key "null"


python src/vqa_evaluate.py \
    --input_file ./data/music-bench/vqa-music-bench.jsonl \
    --image_dir ./music-bench/ \
    --output_file ./output/qwen2.5-vl-72b.jsonl \
    --n_threads 128 \
    --response_key response \
    --model_name qwen2.5-vl \
    --base_url http://127.0.0.1:9998/v1 \
    --max_tokens 8192 \
    --api_key "null"

