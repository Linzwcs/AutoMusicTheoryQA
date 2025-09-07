# Synthesizing Sheet Music Problems for Evaluation and Reinforcement Learning


[![arXiv](https://img.shields.io/badge/arXiv-2509.04059-b31b1b.svg)](https://arxiv.org/abs/2509.04059)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue.svg)](https://github.com/Linzwcs/AutoMusicTheoryQA) <!--- Placeholder link -->
[![Hugging Face Datasets](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Datasets-yellow)](https://huggingface.co/datasets/Sylence/SSMR-Bench) <!--- Placeholder link -->

This repository contains the official code and resources for the paper **"Synthesizing Sheet Music Problems for Evaluation and Reinforcement Learning"**.


## Abstract

Enhancing the ability of Large Language Models (LLMs) and Multimodal Large Language Models (MLLMs) to interpret sheet music is a crucial step toward building AI musicians. However, current research lacks both evaluation benchmarks and training data for sheet music reasoning. To address this, we propose the idea of synthesizing sheet music problems grounded in music theory, which can serve both as evaluation benchmarks and as training data for reinforcement learning with verifiable rewards (RLVR). We introduce a data synthesis framework that generates verifiable sheet music questions in both textual and visual modalities, leading to the **Synthetic Sheet Music Reasoning Benchmark (SSMR-Bench)** and a complementary training set. Our results demonstrate that this approach not only advances model reasoning for sheet music but also unlocks new possibilities for AI-assisted music creation.

## Key Contributions

*   **Novel Synthesis Idea**: We are the first to propose leveraging music theory rules to programmatically synthesize verifiable sheet music problems, suitable for both evaluation and Reinforcement Learning with Verifiable Rewards (RLVR).
*   **Data Synthesis Framework**: We developed a fully programmatic framework to generate sheet music questions in both textual (ABC notation) and visual (staff notation) formats.
*   **SSMR-Bench & Training Data**: We release the **SSMR-Bench** benchmark and a corresponding training dataset to facilitate research in sheet music understanding.
*   **Proven Effectiveness**: We show that training on our synthetic data significantly enhances model reasoning abilities in sheet music, with trained models surpassing GPT-4 on `MusicTheoryBench` and showing improved capabilities in music composition.

## Getting Started

### Prerequisites

#### Python Libraries
You will need Python 3.8+ and the following libraries. You can install them via pip:
```bash
pip install music21 tqdm
```

#### System Dependencies
This framework requires two external command-line tools for converting ABC notation to images. They must be installed and accessible in your system's PATH.

*   **`abcm2ps`**: A tool to convert ABC files to PostScript.
*   **ImageMagick**: A suite of tools for image manipulation, specifically the `convert` command.

**On Debian/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install abcm2ps imagemagick
```

### Installation

Clone the repository to your local machine:
```bash
git clone https://github.com/Linzwcs/AutoMusicTheoryQA.git
cd AutoMusicTheoryQA
pip install -e .
```

### Data Generation Pipeline

Follow these steps to generate your own datasets.

#### Step 1: Generate Textual Questions

Use the `data_gen.py` script to generate questions from a source file containing ABC music. The input should be a JSONL file where each line is a JSON object with an `"abc_music"` key.

```bash
python -m AutoMusicTheoryQA.data_gen path/to/your/input_abc.jsonl path/to/text_output_dir
```
*   `AutoMusicTheoryQA` is the name of the main package directory.
*   This will create several JSONL files in `path/to/text_output_dir`, such as `Rhythm.jsonl`, `Chord.jsonl`, etc.

#### Step 2: Generate Visual (VQA) Questions

Use the `vqa_gen.py` script to convert the textual datasets generated in Step 1 into visual datasets. This script will create an `images` subdirectory in your output directory.

```bash

python -m AutoMusicTheoryQA.vqa_gen path/to/text_output_dir/Rhythm.jsonl path/to/vqa_output_dir

```
*   The script will read `Rhythm.jsonl`, generate images for each question, and save a new `vqa_Rhythm.jsonl` in `path/to/vqa_output_dir`.
*   The image files will be stored in `path/to/vqa_output_dir/images/`.
*   **Note:** This process can be time-consuming as it involves generating an image for each data entry.

## Citation

If you find our work useful, please cite our paper:

```bibtex
@article{wang2025synthesizing,
  title={Synthesizing Sheet Music Problems for Evaluation and Reinforcement Learning},
  author={Wang, Zhilin and Yang, Zhe and Luo, Yun and Li, Yafu and Zhang, Haoran and Zhang, Runzhe and Wong, Derek F. and Zhou, Jizhe and Cheng, Yu},
  journal={arXiv preprint arXiv:2509.04059},
  year={2025}
}
```

## Contact

For any questions, please contact:
*   `zhilin.nlp@gmail.com`
*   `yangzhe@stu.scu.edu.cn`
*   `yafuly@gmail.com`
*   `chengyu@cse.cuhk.edu.hk`


