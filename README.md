<div align="center">

<img src="assets/AISecurity.png" alt="AI Security" width="600"/>

# AI Security

### An Educational Series by [Camilo Pestana, PhD](https://github.com/elcronos)

*Understanding how AI systems can be attacked — and how to defend them.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)](https://pytorch.org/)
[![Educational](https://img.shields.io/badge/Purpose-Educational-green.svg)]()

</div>

---

## About This Series

This repository contains the materials for a series of talks and hands-on notebooks on **AI Security** — a rapidly growing field at the intersection of machine learning and cybersecurity.

The series is divided into three parts:

- **Part 1 — Adversarial Attacks on Computer Vision Models**: How image classifiers can be systematically fooled, and how to build defenses against these attacks.
- **Part 2 — Adversarial Attacks on Audio Models**: How speech-to-text and audio classification models can be attacked in the spectrogram domain using the same gradient-based techniques as image attacks.
- **Part 3 — AI Security in Large Language Models (LLMs)**: How modern LLMs are vulnerable to prompt injection, jailbreaks, and other adversarial inputs — with interactive Docker environments running local LLMs where you can practice real attacks safely.

> **Purpose**: All content in this repository is strictly for **educational purposes**. The goal is to build intuition about AI vulnerabilities so that researchers, engineers, and developers can build more robust and trustworthy AI systems. No content here should be used for malicious purposes.

---

## Table of Contents

### Part 1 — Adversarial Attacks on Computer Vision

| # | Topic | Notebook | Status |
|---|-------|----------|--------|
| 01 | [Adversarial Attacks on CNNs](#01-adversarial-attacks-on-cnns) | `01_adversarial_attacks_cnns/` | ✅ Available |
| 02 | [Second-Order Attacks](#02-second-order-attacks) | `02_second_order_attacks/` | ✅ Available |
| 03 | [Adversarial Attacks on Object Detection](#03-adversarial-attacks-on-object-detection) | `03_adversarial_object_detection/` | ✅ Available |
| 04 | [Adversarial Reprogramming](#04-adversarial-reprogramming) | `04_adversarial_reprogramming/` | ✅ Available |
| 05 | [Defenses for CNNs](#05-defenses-for-cnns) | `05_defenses_cnns/` | ✅ Available |

### Part 2 — Adversarial Attacks on Audio

| # | Topic | Notebook | Status |
|---|-------|----------|--------|
| 06 | [Adversarial Audio Attacks](#06-adversarial-audio-attacks) | `06_adversarial_audio/` | ✅ Available |

### Part 3 — AI Security in Large Language Models

| # | Topic | Environment | Status |
|---|-------|-------------|--------|
| 07 | [Attacks on LLMs (Text-only)](#07-attacks-on-llms-text-only) | Docker + Local LLM | ✅ Available |
| 08 | [Attacks on Multimodal LLMs](#08-attacks-on-multimodal-llms) | Docker + Local LLM | ✅ Available |

---

## Part 1 — Adversarial Attacks on Computer Vision

### 01. Adversarial Attacks on CNNs

> **Notebook**: [`01_adversarial_attacks_cnns/adversarial_attacks_cnn.ipynb`](https://github.com/elcronos/AISecurity/blob/main/01_adversarial_attacks_cnns/adversarial_attacks_cnn.ipynb)

An introduction to adversarial attacks on image classifiers using ResNet50 and ImageNet. Covers the two most important white-box attacks:

- **FGSM** (Fast Gradient Sign Method) — Goodfellow et al., 2014
- **PGD** (Projected Gradient Descent) — Madry et al., 2017

**What you will learn:**
- How to craft adversarial examples that are imperceptible to humans but reliably fool deep neural networks
- A graphical breakdown of every component in the FGSM equation: the gradient, the sign operation, the perturbation budget ε
- Why FGSM can *recover* confidence at large ε (overshooting) and why PGD-20 solves this with iterative projection
- Quantitative evaluation: accuracy and confidence erosion across ε ∈ {0.005, 0.01, 0.1, 0.3} on a 20-class ImageNet subset (ε = 0.5 appears in single-image demos only)

**Requirements**: PyTorch, torchvision, matplotlib — see `01_adversarial_attacks_cnns/requirements.txt`

---

### 02. Second-Order Attacks

> **Notebook**: [`02_second_order_attacks/second_order_attacks.ipynb`](https://github.com/elcronos/AISecurity/blob/main/02_second_order_attacks/second_order_attacks.ipynb)

First-order attacks like FGSM and PGD follow the gradient sign. Second-order attacks use **curvature information** (the Hessian) to find more precise adversarial examples with smaller, less perceptible perturbations.

- **L-BFGS** (Szegedy et al., 2013) — the original adversarial attack; quasi-Newton optimization with logit-margin loss
- **C&W L2** (Carlini & Wagner, 2017) — minimises L2 distortion directly; Adam optimizer with adaptive loss; gold standard for robustness evaluation

**What you will learn:**
- Why gradient steps are suboptimal and how curvature-aware updates (Newton's method, L-BFGS) find smaller perturbations
- The logit-margin objective and why it avoids the gradient saturation that breaks cross-entropy at high-confidence predictions
- Why C&W was specifically designed to defeat gradient-masking defenses
- Quantitative comparison — accuracy, L2 distortion, computation time — across FGSM, PGD-40, L-BFGS, and C&W on a 5-class ImageNet subset (50 images, 10 per class)
- Per-class accuracy breakdown: grouped bar charts, line trends, and a full attacks × classes heatmap

**Key insight**: Second-order attacks achieve **lower L2 distortion** by concentrating perturbations on the most sensitive pixels. But because they are unconstrained in L∞, individual pixels can change by more than ε — a fundamentally different threat model from FGSM/PGD.

**Requirements**: PyTorch, torchvision, scipy, matplotlib — see `02_second_order_attacks/requirements.txt`

---

### 03. Adversarial Attacks on Object Detection

> **Notebook**: [`03_adversarial_object_detection/adversarial_object_detection.ipynb`](https://github.com/elcronos/AISecurity/blob/main/03_adversarial_object_detection/adversarial_object_detection.ipynb)

Classification is just the start. Real-world AI systems rely on **object detectors** — deployed in surveillance cameras, autonomous vehicles, and drone systems. This module shows how white-box adversarial attacks can make *persons completely invisible* to YOLOv5.

The attack implemented is **Adversarial Clothing** — an optimised patch texture applied to the torso region of a detected person, simulating a printed t-shirt that renders the wearer invisible to surveillance cameras.

**What you will learn:**
- How object detectors (YOLOv5su with anchor-free head) produce detection logits that can be directly attacked via backpropagation
- The white-box patch optimisation loop: gradient descent on the pixel values of the patch, minimising the objectness score of person detections
- Why the attack is physically deployable: the patch texture is composited onto the torso bounding box, mimicking a real garment print
- The effect of training iterations on suppression confidence: how loss curves reveal when the patch has converged

**Key papers:**
- Thys et al. (2019). *Fooling automated surveillance cameras* — [arXiv:1904.08653](https://arxiv.org/abs/1904.08653)
- Xu et al. (2020). *Adversarial T-shirt Had Salient Texture* — [arXiv:1910.11099](https://arxiv.org/abs/1910.11099)
- Brown et al. (2017). *Adversarial Patch* — [arXiv:1712.09665](https://arxiv.org/abs/1712.09665)

**Requirements**: PyTorch, ultralytics, matplotlib — see `03_adversarial_object_detection/requirements.txt`

---

### 04. Adversarial Reprogramming

> **Notebook**: [`04_adversarial_reprogramming/adversarial_reprogramming.ipynb`](https://github.com/elcronos/AISecurity/blob/main/04_adversarial_reprogramming/adversarial_reprogramming.ipynb)

A new class of adversarial attack that goes beyond misclassification — it **hijacks** a pre-trained neural network to perform a completely different task, without modifying any weights. Based on the paper by Elsayed, Goodfellow & Sohl-Dickstein (ICLR 2019).

- **Adversarial Reprogramming** (Elsayed et al., 2019) — [arXiv:1806.11146](https://arxiv.org/abs/1806.11146)

**What you will learn:**
- The core concept: how a frozen model can be repurposed to solve a different task via a learnable input transformation — without changing any weights
- The mathematical formulation: the adversarial program P, the input mapping h_f (embedding + masking), and the output mapping h_g (label remapping)
- How to implement and train an adversarial program from scratch using gradient-based optimisation
- Why this attack works: models encode surprisingly general-purpose representations that transfer across tasks
- Security implications: compute theft via API hijacking, covert channels, and safety-critical model compromise
- How adversarial reprogramming differs from classic evasion attacks and universal perturbations

**Implementation note**: The notebook demonstrates the concept using a lightweight sklearn MLP classifier on digit subsets (8×8 images from scikit-learn's `load_digits`), making it runnable without a GPU. Paper results (e.g. Inception V3 reprogrammed to classify MNIST at 97.3%) are reproduced as reference charts from the original publication.

**Requirements**: numpy, matplotlib, scikit-learn — lightweight, no GPU needed.

---

### 05. Defenses for CNNs

> **Notebook**: [`05_defenses_cnns/defenses_cnns.ipynb`](https://github.com/elcronos/AISecurity/blob/main/05_defenses_cnns/defenses_cnns.ipynb)

Attacks are only half the story. This module covers four families of defenses — from quick preprocessing heuristics to mathematically certified guarantees — and explains precisely *why* certifying robustness is fundamentally hard.

- **Input preprocessing** (JPEG compression, Gaussian smoothing, bit-depth reduction) — zero-retraining defenses that destroy high-frequency adversarial noise; evaluated against adaptive attackers to show their limitations
- **Adversarial Training** (FGSM-AT) — the minimax training objective; demonstrated by fine-tuning a frozen ResNet50 head on a 2-class subset (tench vs parachute) using a 50/50 clean+adversarial mix for 10 epochs, with side-by-side standard vs adversarial training comparison
- **Randomized Smoothing** (Cohen et al., 2019) — Monte Carlo smoothed classifier with probabilistic L₂ certified radius $r = \sigma \cdot \Phi^{-1}(p_A)$; accuracy vs radius tradeoff sweep across σ ∈ {0.12, 0.25, 0.50}
- **IBP Certified Training** (Interval Bound Propagation) — deterministic L∞ certification via linear relaxation; shows how IBP provides tight bounds for L∞ balls through linear layers
- **Why L₂ is harder to certify than L∞** — geometric intuition: L∞ balls stay axis-aligned through linear layers (IBP is tight), while L₂ balls become ellipsoids (IBP is a loose over-approximation); illustrated with a 3-panel figure

**What you will learn:**
- Why heuristic preprocessing defenses fail against *adaptive* attackers who craft examples through the defense
- How the adversarial training minimax objective formally trades clean accuracy for empirical robustness
- How randomized smoothing converts any classifier into one with a provable L₂ robustness certificate
- How IBP provides deterministic L∞ certified bounds and why it complements randomized smoothing
- Why the L∞ threat model (FGSM/PGD) is easier to certify deterministically than the L₂ threat model (C&W)
- How to read and interpret robustness benchmarks (RobustBench)

**Requirements**: PyTorch, torchvision, scipy, matplotlib — see `05_defenses_cnns/requirements.txt`

---

## Part 2 — Adversarial Attacks on Audio

### 06. Adversarial Audio Attacks

> **Notebook**: [`06_adversarial_audio/adversarial_audio.ipynb`](https://github.com/elcronos/AISecurity/blob/main/06_adversarial_audio/adversarial_audio.ipynb)

The same gradient-based attack math that fools image classifiers can be applied to audio models — by treating the **mel spectrogram as a 2D image**. This module demonstrates white-box attacks on a speech-to-text model (OpenAI Whisper) and an audio event classifier (Audio Spectrogram Transformer).

Three attack scenarios are covered:

- **Targeted adversarial STT** — perturb audio in the waveform domain with PGD so that Whisper outputs a specific target phrase (e.g. "open the door"), while the audio sounds unchanged to a human listener
- **Adversarial audio event classification** — fool MIT's AST classifier (527-class AudioSet) into misclassifying a sound clip using an Adam-based waveform-domain optimisation; shows why naive spectrogram-domain attacks break on round-trip and how waveform-domain perturbations fix it
- **FGSM vs multi-step comparison** — side-by-side evaluation of single-step (FGSM) vs Adam-based multi-step attacks on the AST evasion task, with spectrogram visualisations

**What you will learn:**
- How the mel spectrogram pipeline (waveform → STFT → mel filterbank → log compression) creates a differentiable image-like representation
- The round-trip problem: why perturbations applied in the spectrogram domain don't survive waveform reconstruction, and why both attacks operate in the raw waveform domain instead
- How to measure imperceptibility in audio: L∞ norm on the waveform as the acoustic analogue of pixel-space perturbation budgets
- Why AST (Audio Spectrogram Transformer) uses the same ViT patch-attention architecture as image transformers — making it vulnerable to gradient-based attacks
- The difference between targeted attacks (force a specific output) and untargeted evasion (any wrong label)

**Key models:**
- OpenAI Whisper (`whisper-base`) — targeted STT attack in the waveform domain
- `MIT/ast-finetuned-audioset-10-10-0.4593` — 527-class AudioSet event classifier, attacked via Adam-based waveform optimisation

**Requirements**: `openai-whisper`, `torchaudio`, `librosa`, `transformers`, `soundfile` — see install cell in notebook.

---

## Part 3 — AI Security in Large Language Models

Modern LLMs introduce a completely new attack surface. Unlike image classifiers, LLMs are prompted with natural language — and that same flexibility that makes them powerful also makes them exploitable.

### 07. Attacks on LLMs (Text-only)

> **Notebook**: `07_llm_attacks_text/` — Docker + local LLM (llama3.2:3b via Ollama)

Six interactive challenges, each simulating a real company chatbot with a different vulnerability. Everything runs locally — no API keys, no cloud costs.

| # | Challenge | Technique | Difficulty |
|---|-----------|-----------|------------|
| 1 | Prompt Injection | Override system instructions to leak a hidden promo code | Easy |
| 2 | Jailbreaking | Break a hard-scoped chatbot out of its persona using creative framing | Medium |
| 3 | Indirect Prompt Injection | Poison a RAG knowledge base via the admin panel; trigger retrieval to execute your payload | Hard |
| 4 | Data Exfiltration | Extract confidential credentials using encoding tricks and character-by-character extraction | Hard |
| 5 | Markdown Exfiltration | Leak secrets silently via a rendered markdown image URL | Hard |
| 6 | Guardrails Bypass | Evade a keyword-based content filter using synonyms, foreign languages, and indirect framing | Medium |

**What you will learn:**
- How prompt injection hijacks LLM behaviour when user input overrides system instructions
- Why instruction-based guardrails alone are insufficient — and how creative framing defeats them
- How RAG pipelines create an indirect injection surface through retrieved documents
- Why keyword-based content filters are fundamentally bypassable
- How markdown rendering in a browser can silently exfiltrate secrets to attacker-controlled servers

**Environment:**
- **LLM**: `llama3.2:3b` (≈2 GB download, runs on CPU)
- **Stack**: FastAPI app + Ollama inference server, orchestrated with Docker Compose
- **Interface**: Browser-based chat UI with per-challenge hints and solution walkthroughs

```bash
cd 07_llm_attacks_text
docker compose up --build
# First run pulls llama3.2:3b (~2 GB) — takes a few minutes
# Open http://localhost:8080 — try to break the chatbot!
```

---

### 08. Attacks on Multimodal LLMs

> **Notebook**: `08_llm_attacks_multimodal/` — Docker + local multimodal LLM (LLaVA via Ollama)

Five interactive challenges, each simulating a company chatbot that accepts both text and images. Everything runs locally — no API keys, no cloud costs.

| # | Challenge | Attack Type | Difficulty |
|---|-----------|-------------|------------|
| 1 | Document Scan | OCR-based visual prompt injection — embed instructions in an image | Easy |
| 2 | FigStep | Typographic jailbreak — render the prohibited request as image typography | Medium |
| 3 | Authority Override | Cross-modal authority injection — forge an official directive image | Medium |
| 4 | Phantom Patch | Adversarial patch bypass — use a pre-computed CLIP patch to confuse content moderation | Hard |
| 5 | Slow Burn | Multi-turn visual manipulation — combine image framing with progressive context shift | Hard |

**What you will learn:**
- Why visual inputs bypass text-based safety filters (OCR-based prompt injection)
- How the FigStep attack renders harmful text as image typography to evade input classifiers
- Why authority markers in images are trivially spoofable (cross-modal authority injection)
- How adversarial patches exploit non-robust neural network vision features (CLIP gradient ascent)
- How multi-turn conversations accumulate context that progressively erodes model restrictions

**Companion Jupyter notebook** (`adversarial_patch_generator.ipynb`):
Generates a real CLIP gradient-based adversarial patch — the mathematical foundation of Challenge 4.
Covers CLIP embedding space, gradient ascent optimisation, and defences (feature squeezing, adversarial training, randomised smoothing).

**Key papers:**
- Qi et al. (2024). *Visual Adversarial Examples Jailbreak Aligned Large Language Models* — [arXiv:2306.13213](https://arxiv.org/abs/2306.13213)
- Gong et al. (2025). *FigStep: Jailbreaking Large Vision-Language Models via Scalable Typography-based Visual Prompts* — [arXiv:2311.05608](https://arxiv.org/abs/2311.05608)
- Rahmatullaev et al. (2025). *Universal Adversarial Attack on Aligned Multimodal LLMs* — [arXiv:2502.07987](https://arxiv.org/abs/2502.07987)

**Environment:**
- **LLM**: `llava:7b` (~4.7 GB download, runs on CPU; GPU strongly recommended)
- **Stack**: FastAPI app + Ollama inference server, orchestrated with Docker Compose
- **Interface**: Browser-based chat UI with image upload (drag-and-drop) per-challenge hints and solution walkthroughs
- **Port**: `http://localhost:8081` (offset from Module 07 so both can run simultaneously)

```bash
cd 08_llm_attacks_multimodal
docker compose up --build
# First run pulls llava:7b (~4.7 GB) — takes several minutes
# Open http://localhost:8081 — upload images to attack the bot!

# Optional: use a higher-quality model
MODEL_NAME=llava-llama3:8b docker compose up
```

---

## Getting Started

### Part 1 — Computer Vision Notebooks

```bash
git clone https://github.com/elcronos/AISecurity.git

# Create a virtual environment (do this once)
python -m venv venv && source venv/bin/activate   # macOS/Linux
# python -m venv venv && venv\Scripts\activate     # Windows
```

**Module 01 — Adversarial Attacks on CNNs**
```bash
cd AISecurity/01_adversarial_attacks_cnns
pip install -r requirements.txt
jupyter notebook adversarial_attacks_cnn.ipynb
```

**Module 02 — Second-Order Attacks**
```bash
cd AISecurity/02_second_order_attacks
pip install -r requirements.txt
jupyter notebook second_order_attacks.ipynb
```

**Module 03 — Adversarial Attacks on Object Detection**
```bash
cd AISecurity/03_adversarial_object_detection
pip install -r requirements.txt
jupyter notebook adversarial_object_detection.ipynb
```

**Module 04 — Adversarial Reprogramming**
```bash
cd AISecurity/04_adversarial_reprogramming
pip install numpy matplotlib scikit-learn jupyter
jupyter notebook adversarial_reprogramming.ipynb
```

**Module 05 — Defenses for CNNs**
```bash
cd AISecurity/05_defenses_cnns
pip install -r requirements.txt
jupyter notebook defenses_cnns.ipynb
```

**Module 06 — Adversarial Audio Attacks**
```bash
cd AISecurity/06_adversarial_audio
pip install openai-whisper torchaudio librosa soundfile transformers accelerate matplotlib numpy torch
jupyter notebook adversarial_audio.ipynb
```

> **Apple Silicon (M1/M2/M3/M4)**: PyTorch will automatically use the MPS GPU backend for a 5–15× speedup over CPU. Requires PyTorch ≥ 1.12 and macOS ≥ 12.3.
> C&W and L-BFGS are optimization-based attacks — running on MPS is strongly recommended over CPU.

### Part 3 — LLM Docker Environments

**Requirements**: [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Compose plugin)

**Module 07 — Attacks on LLMs (Text-only)**
```bash
cd AISecurity/07_llm_attacks_text
docker compose up --build
```
- First run downloads `llama3.2:3b` (~2 GB) — subsequent starts are instant
- Open **http://localhost:8080** in your browser
- To use a different model: `MODEL_NAME=qwen2.5:7b docker compose up`
- To stop: `docker compose down`

> Docker environments run entirely **locally** — no API keys, no cloud costs, no data sent externally.

---

## Series Structure

```
AISecurity/
├── 01_adversarial_attacks_cnns/
│   ├── adversarial_attacks_cnn.ipynb
│   └── requirements.txt
├── 02_second_order_attacks/
│   ├── second_order_attacks.ipynb
│   └── requirements.txt
├── 03_adversarial_object_detection/
│   ├── adversarial_object_detection.ipynb
│   └── requirements.txt
├── 04_adversarial_reprogramming/
│   └── adversarial_reprogramming.ipynb
├── 05_defenses_cnns/
│   ├── defenses_cnns.ipynb
│   └── requirements.txt
├── 06_adversarial_audio/
│   └── adversarial_audio.ipynb
├── 07_llm_attacks_text/
│   ├── docker-compose.yml
│   └── app/
│       ├── main.py                   # FastAPI app + 6 challenge configs
│       ├── rag_engine.py             # BM25 document store (Challenge 3)
│       ├── rag_graph.py              # LangGraph RAG pipeline (Challenge 3)
│       ├── auth.py                   # JWT auth for admin panel (Challenge 3)
│       ├── Dockerfile
│       ├── entrypoint.sh             # Pulls LLM model on first start
│       ├── requirements.txt
│       └── static/
│           ├── index.html            # Challenge selection page
│           ├── chat.html             # Challenge chat interface
│           └── admin.html            # Knowledge base admin panel (Challenge 3)
└── 08_llm_attacks_multimodal/
    ├── docker-compose.yml
    ├── adversarial_patch_generator.ipynb  # Companion: CLIP gradient-based patch generation
    └── app/
        ├── main.py                   # FastAPI app + 5 multimodal challenge configs
        ├── image_utils.py            # Image validation, resize, base64 encoding
        ├── Dockerfile
        ├── entrypoint.sh             # Pulls LLaVA model on first start
        ├── requirements.txt
        └── static/
            ├── index.html            # Challenge selection page
            ├── chat.html             # Multimodal chat UI (image upload + text)
            └── adversarial_patch.png # Pre-generated patch for Challenge 4
```

---

## About the Author

**Camilo Pestana, PhD** is an AI researcher and engineer specialising in computer vision, multimodal learning, and AI safety. This series draws from both academic research and practical red-teaming experience to make AI security accessible to a broad technical audience.

- GitHub: [@elcronos](https://github.com/elcronos)

---

## References

1. Szegedy et al. (2013). *Intriguing Properties of Neural Networks*. [arXiv:1312.6199](https://arxiv.org/abs/1312.6199)
2. Goodfellow et al. (2014). *Explaining and Harnessing Adversarial Examples*. [arXiv:1412.6572](https://arxiv.org/abs/1412.6572)
3. Madry et al. (2017). *Towards Deep Learning Models Resistant to Adversarial Attacks*. [arXiv:1706.06083](https://arxiv.org/abs/1706.06083)
4. Carlini & Wagner (2017). *Evaluating the Robustness of Neural Networks*. [arXiv:1608.04644](https://arxiv.org/abs/1608.04644)
5. Cohen et al. (2019). *Certified Adversarial Robustness via Randomized Smoothing*. [arXiv:1902.02918](https://arxiv.org/abs/1902.02918)
6. Brown et al. (2017). *Adversarial Patch*. [arXiv:1712.09665](https://arxiv.org/abs/1712.09665)
7. Thys et al. (2019). *Fooling automated surveillance cameras: adversarial patches to attack person detection*. [arXiv:1904.08653](https://arxiv.org/abs/1904.08653)
8. Xu et al. (2020). *Adversarial T-shirt Had Salient Texture and Adaptive Patterns for Clothes*. [arXiv:1910.11099](https://arxiv.org/abs/1910.11099)
9. Elsayed, Goodfellow & Sohl-Dickstein (2019). *Adversarial Reprogramming of Neural Networks*. [arXiv:1806.11146](https://arxiv.org/abs/1806.11146)
10. Perez & Ribeiro (2022). *Ignore Previous Prompt: Attack Techniques For Language Models*. [arXiv:2211.09527](https://arxiv.org/abs/2211.09527)
11. Greshake et al. (2023). *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
12. Radford et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision* (CLIP). [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)
13. Qi et al. (2024). *Visual Adversarial Examples Jailbreak Aligned Large Language Models*. [arXiv:2306.13213](https://arxiv.org/abs/2306.13213)
14. Gong et al. (2025). *FigStep: Jailbreaking Large Vision-Language Models via Scalable Typography-based Visual Prompts*. [arXiv:2311.05608](https://arxiv.org/abs/2311.05608)
15. Rahmatullaev et al. (2025). *Universal Adversarial Attack on Aligned Multimodal LLMs*. [arXiv:2502.07987](https://arxiv.org/abs/2502.07987)

---

## License

This repository is licensed under the [MIT License](LICENSE). All content is provided for educational purposes only.

> **Disclaimer**: The techniques demonstrated in this series are for learning and research. Always obtain explicit permission before testing adversarial techniques on systems you do not own.
