<div align="center">

# AI Security

### A Educational Series by [Camilo Pestana, PhD](https://github.com/elcronos)

*Understanding how AI systems can be attacked — and how to defend them.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)](https://pytorch.org/)
[![Educational](https://img.shields.io/badge/Purpose-Educational-green.svg)]()

</div>

---

## About This Series

This repository contains the materials for a series of talks and hands-on notebooks on **AI Security** — a rapidly growing field at the intersection of machine learning and cybersecurity.

The series is divided into two parts:

- **Part 1 — Adversarial Attacks on Computer Vision Models**: How image classifiers can be systematically fooled, and how to build defenses against these attacks.
- **Part 2 — AI Security in Large Language Models (LLMs)**: How modern LLMs are vulnerable to prompt injection, jailbreaks, and other adversarial inputs — with interactive Docker environments running local LLMs where you can practice real attacks safely.

> **Purpose**: All content in this repository is strictly for **educational purposes**. The goal is to build intuition about AI vulnerabilities so that researchers, engineers, and developers can build more robust and trustworthy AI systems. No content here should be used for malicious purposes.

---

## Table of Contents

### Part 1 — Adversarial Attacks on Computer Vision

| # | Topic | Notebook | Status |
|---|-------|----------|--------|
| 01 | [Adversarial Attacks on CNNs](#01-adversarial-attacks-on-cnns) | `01_adversarial_attacks_cnns/` | ✅ Available |
| 02 | [Second-Order Attacks](#02-second-order-attacks) | `02_second_order_attacks/` | 🔜 Coming Soon |
| 03 | [Defenses for CNNs](#03-defenses-for-cnns) | `03_defenses_cnns/` | 🔜 Coming Soon |

### Part 2 — AI Security in Large Language Models

| # | Topic | Environment | Status |
|---|-------|-------------|--------|
| 04 | [Attacks on LLMs (Text-only)](#04-attacks-on-llms-text-only) | Docker + Local LLM | 🔜 Coming Soon |
| 05 | [Attacks on Multimodal LLMs](#05-attacks-on-multimodal-llms) | Docker + Local LLM | 🔜 Coming Soon |

---

## Part 1 — Adversarial Attacks on Computer Vision

### 01. Adversarial Attacks on CNNs

> **Notebook**: `01_adversarial_attacks_cnns/adversarial_attacks_cnn.ipynb`

An introduction to adversarial attacks on image classifiers using ResNet50 and ImageNet. Covers the two most important white-box attacks:

- **FGSM** (Fast Gradient Sign Method) — Goodfellow et al., 2014
- **PGD** (Projected Gradient Descent) — Madry et al., 2017

**What you will learn:**
- How to craft adversarial examples that are imperceptible to humans but reliably fool deep neural networks
- A graphical breakdown of every component in the FGSM equation: the gradient, the sign operation, the perturbation budget ε
- Why FGSM can *recover* confidence at large ε (overshooting) and why PGD solves this with iterative projection
- Quantitative evaluation: accuracy and confidence erosion across ε ∈ {0.005, 0.01, 0.1, 0.3, 0.5} on a 20-class ImageNet subset

**Requirements**: PyTorch, torchvision, matplotlib — see `01_adversarial_attacks_cnns/requirements.txt`

---

### 02. Second-Order Attacks

> 🔜 *Coming Soon*

First-order attacks like FGSM and PGD follow the gradient sign. Second-order attacks use curvature information (the Hessian) to find more precise and transferable adversarial examples.

**Planned topics:**
- Newton's method applied to adversarial attacks
- The **C&W attack** (Carlini & Wagner, 2017) — optimization-based, L2-bounded
- **NewtonFool** and curvature-aware perturbations
- Comparison: FGSM vs PGD vs C&W — effectiveness, perceptibility, transferability

---

### 03. Defenses for CNNs

> 🔜 *Coming Soon*

Attacks are only half the story. This module covers the main families of certified and empirical defenses.

**Planned topics:**
- **Adversarial Training** (Madry et al.) — the strongest known empirical defense
- **Input preprocessing**: JPEG compression, spatial smoothing, feature squeezing
- **Certified defenses**: Randomized Smoothing (Cohen et al., 2019) — provable robustness guarantees
- **Detection methods**: identifying adversarial inputs before they reach the classifier
- Robustness benchmarks: RobustBench, AutoAttack

---

## Part 2 — AI Security in Large Language Models

Modern LLMs introduce a completely new attack surface. Unlike image classifiers, LLMs are prompted with natural language — and that same flexibility that makes them powerful also makes them exploitable.

### 04. Attacks on LLMs (Text-only)

> 🔜 *Coming Soon* — Docker environment included

This module introduces adversarial attacks against text-based LLMs, focusing on the techniques most relevant to real-world deployments.

**Planned topics:**
- **Prompt injection**: hijacking LLM behaviour by embedding instructions in user input
- **Jailbreaking**: bypassing safety alignment with adversarial prompts (role-play, prefix injection, suffix attacks)
- **Indirect prompt injection**: attacking LLMs through retrieved context (RAG poisoning, tool outputs)
- **Data extraction**: prompting the model to leak its system prompt or training data

**Interactive Docker environment:**
Each attack module ships with a **Docker container running a local LLM configured as a secure chatbot**. The environment includes:
- A pre-configured chatbot with security controls and a system prompt you must bypass
- A hint system that progressively reveals attack strategies if you get stuck
- A payload library with known jailbreak techniques to test and adapt
- Scoring: the challenge is solved when the LLM breaks its security constraints and reveals the protected information

```bash
# Launch the LLM attack environment (coming soon)
docker pull elcronos/aisecurity-llm-04
docker run -p 8080:8080 elcronos/aisecurity-llm-04
# Open http://localhost:8080 — try to break the chatbot!
```

---

### 05. Attacks on Multimodal LLMs

> 🔜 *Coming Soon* — Docker environment included

Multimodal LLMs (GPT-4V, LLaVA, Gemini) accept both images and text, opening an entirely new attack surface: adversarial images designed to hijack the model's text output.

**Planned topics:**
- **Visual prompt injection**: embedding hidden instructions inside images
- **Adversarial patches**: physical-world perturbations that fool vision-language models
- **Cross-modal attacks**: using an adversarial image to override the text system prompt
- **OCR-based injection**: hiding text instructions in image content (screenshots, documents)

**Interactive Docker environment:**
Similar to Module 04 but the chatbot also accepts images. Challenges include:
- Crafting images that contain hidden adversarial instructions
- Bypassing image-content moderation
- Multi-turn attack strategies combining text and image inputs

```bash
# Launch the multimodal attack environment (coming soon)
docker pull elcronos/aisecurity-llm-05
docker run -p 8080:8080 elcronos/aisecurity-llm-05
```

---

## Getting Started

### Part 1 — Computer Vision Notebooks

```bash
git clone https://github.com/elcronos/AISecurity.git
cd AISecurity/01_adversarial_attacks_cnns

# Create a virtual environment
python -m venv venv && source venv/bin/activate   # macOS/Linux
# python -m venv venv && venv\Scripts\activate     # Windows

pip install -r requirements.txt
jupyter notebook adversarial_attacks_cnn.ipynb
```

> **Apple Silicon (M1/M2/M3/M4)**: PyTorch will automatically use the MPS GPU backend for a 5–15× speedup over CPU. Requires PyTorch ≥ 1.12 and macOS ≥ 12.3.

### Part 2 — LLM Docker Environments

Each LLM module will include a `docker-compose.yml` for one-command startup. Docker environments will run entirely **locally** — no API keys, no cloud costs, no data sent externally.

---

## Series Structure

```
AISecurity/
├── 01_adversarial_attacks_cnns/
│   ├── adversarial_attacks_cnn.ipynb
│   └── requirements.txt
├── 02_second_order_attacks/          # coming soon
├── 03_defenses_cnns/                 # coming soon
├── 04_llm_attacks_text/              # coming soon
│   ├── docker-compose.yml
│   └── challenges/
└── 05_llm_attacks_multimodal/        # coming soon
    ├── docker-compose.yml
    └── challenges/
```

---

## About the Author

**Camilo Pestana, PhD** is an AI researcher and engineer specialising in computer vision, multimodal learning, and AI safety. This series draws from both academic research and practical red-teaming experience to make AI security accessible to a broad technical audience.

- GitHub: [@elcronos](https://github.com/elcronos)

---

## References

1. Goodfellow et al. (2014). *Explaining and Harnessing Adversarial Examples*. [arXiv:1412.6572](https://arxiv.org/abs/1412.6572)
2. Madry et al. (2017). *Towards Deep Learning Models Resistant to Adversarial Attacks*. [arXiv:1706.06083](https://arxiv.org/abs/1706.06083)
3. Carlini & Wagner (2017). *Evaluating the Robustness of Neural Networks*. [arXiv:1608.04644](https://arxiv.org/abs/1608.04644)
4. Cohen et al. (2019). *Certified Adversarial Robustness via Randomized Smoothing*. [arXiv:1902.02918](https://arxiv.org/abs/1902.02918)
5. Perez & Ribeiro (2022). *Ignore Previous Prompt: Attack Techniques For Language Models*. [arXiv:2211.09527](https://arxiv.org/abs/2211.09527)
6. Greshake et al. (2023). *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)

---

## License

This repository is licensed under the [MIT License](LICENSE). All content is provided for educational purposes only.

> **Disclaimer**: The techniques demonstrated in this series are for learning and research. Always obtain explicit permission before testing adversarial techniques on systems you do not own.
