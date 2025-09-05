# Synthesizing Sheet Music Problems for Evaluation and Reinforcement Learning


[![arXiv](https://img.shields.io/badge/arXiv-2509.04059-b31b1b.svg)](https://arxiv.org/abs/2509.04059)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue.svg)](https://github.com/Linzwcs/AutoMusicTheoryQA) <!--- Placeholder link -->
[![Hugging Face Datasets](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Datasets-yellow)](https://huggingface.co/datasets/YOUR_USERNAME/SSMR-Bench) <!--- Placeholder link -->

This repository contains the official code and resources for the paper **"Synthesizing Sheet Music Problems for Evaluation and Reinforcement Learning"**.


## Abstract

Enhancing the ability of Large Language Models (LLMs) and Multimodal Large Language Models (MLLMs) to interpret sheet music is a crucial step toward building AI musicians. However, current research lacks both evaluation benchmarks and training data for sheet music reasoning. To address this, we propose the idea of synthesizing sheet music problems grounded in music theory, which can serve both as evaluation benchmarks and as training data for reinforcement learning with verifiable rewards (RLVR). We introduce a data synthesis framework that generates verifiable sheet music questions in both textual and visual modalities, leading to the **Synthetic Sheet Music Reasoning Benchmark (SSMR-Bench)** and a complementary training set. Our results demonstrate that this approach not only advances model reasoning for sheet music but also unlocks new possibilities for AI-assisted music creation.

## Key Contributions

*   **Novel Synthesis Idea**: We are the first to propose leveraging music theory rules to programmatically synthesize verifiable sheet music problems, suitable for both evaluation and Reinforcement Learning with Verifiable Rewards (RLVR).
*   **Data Synthesis Framework**: We developed a fully programmatic framework to generate sheet music questions in both textual (ABC notation) and visual (staff notation) formats.
*   **SSMR-Bench & Training Data**: We release the **SSMR-Bench** benchmark and a corresponding training dataset to facilitate research in sheet music understanding.
*   **Proven Effectiveness**: We show that training on our synthetic data significantly enhances model reasoning abilities in sheet music, with trained models surpassing GPT-4 on `MusicTheoryBench` and showing improved capabilities in music composition.


## Updating...

## Getting Started

### Prerequisites

### Installation

### Data


### Evaluation


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


