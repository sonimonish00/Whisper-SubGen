# Subtitle Translator: Tamil ↔ English (Whisper-SubGen)

This Python script leverages the [faster-whisper](https://github.com/guillaumekln/faster-whisper) implementation of OpenAI’s Whisper small model to **transcribe** and **translate** Tamil audio/video into English subtitles (SRT). It’s wired for local paths—just clone, open in VSCode, and run.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [How to Change Source Language](#how-to-change-source-language)
- [Execution Time Estimates](#execution-time-estimates)
- [Alternative Approaches](#alternative-approaches)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License & Credits](#license--credits)

---

## Features

- **Automatic transcription** of Tamil dialogue from video/audio.
- **On-the-fly translation** into English (`task="translate"`).
- Outputs a **.srt** file with accurate timestamps via the [srt](https://pypi.org/project/srt/) library.
- Supports **CPU** (`int8` quantization) and **GPU** (`float16`) inference.

---

## Prerequisites

- **Python 3.8+**
- **FFmpeg** (audio/video demuxing)
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`
  - Windows: download from [ffmpeg.org](https://ffmpeg.org/)

---

## Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/sonimonish00/Whisper-SubGen.git
   cd Whisper-SubGen
   ```

2. **Open in VSCode**

   Use VSCode’s **File → Open Folder** on the cloned directory. Run commands in the **integrated terminal**.

3. **Install dependencies**

   ```bash
   pip install faster-whisper srt torch
   ```

   > **GPU users**: install a CUDA build of PyTorch before the above, e.g.:
   >
   > ```bash
   > pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   > ```

---

## Usage

1. The script (`translate_subtitles.py`) is pre–wired with absolute paths:

   ```python
   segments, info = model.transcribe(
       r"C:\Trauma-2025.mkv",   # input video
       task="translate",
       language="ta"           # source = Tamil
   )
   # ... generates C:\Trauma-2025_EN.srt
   ```

2. **Edit those paths** directly in `translate_subtitles.py` to point at your media file and desired output name.

3. **Run** in the VSCode terminal:
   ```bash
   python translate_subtitles.py
   ```

---

## How to Change Source Language

To translate from another language (e.g. Malayalam → English), change the `language` parameter:

```diff
- segments, info = model.transcribe(
-     ".../Trauma-2025.mkv",
-     task="translate",
-     language="ta"
- )
+ segments, info = model.transcribe(
+     ".../YourVideo.mkv",
+     task="translate",
+     language="ml"   # ISO 639-1 code for Malayalam
+ )
```

Just substitute `language="XX"` where `XX` is the [ISO 639-1 code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).

---

## Execution Time Estimates (Rough)

| Environment                     | 1 hr Video   | Notes                                  |
| ------------------------------- | ------------ | -------------------------------------- |
| CPU (Intel i5‑series) + int8    | ~1.5–2.5 hrs | slower single‐thread decode            |
| CPU (Intel i5‑series) + float16 | ~1–1.5 hrs   | less quantized precision               |
| GPU (NVIDIA RTX 3060) + fp16    | ~25–45 mins  | depends on VRAM & driver versions      |
| GPU (NVIDIA RTX 3060) + int8    | ~30–50 mins  | quantized speedup, slight quality loss |

> **Tip**: shorter clips scale roughly linearly (e.g. 30 min ≈ half time).

---

## Alternative Approaches

- **DeepL API**: separate translation service, higher translation quality but extra cost and latency.
- **WhisperX**: adds word‑level timestamps and alignment; slower and more complex setup.
- **Parallel execution**: split video into chunks and process in parallel (e.g., GNU `split` + `&`). Often I found overhead outweighed gain on small files.

### Audio‐first Workflow

If you prefer extracting audio, then translating:

```python
import subprocess
from faster_whisper import WhisperModel
import srt
from datetime import timedelta

# 1. Extract WAV (16 kHz, mono)
subprocess.run([
    "ffmpeg", "-i", "input_video.mp4",
    "-vn", "-acodec", "pcm_s16le",
    "-ar", "16000", "-ac", "1",
    "output.wav"
])

# 2. Translate audio → subtitles
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe("output.wav", task="translate", language="ta")

# 3. Compose & save SRT as before
# ... (same generate_srt & file write)
```

---

## Troubleshooting

- **Missing modules**: confirm `pip install` completed in the same Python interpreter VSCode is using.
- **FFmpeg errors**: ensure `ffmpeg` is on your `PATH` or provide full executable path.
- **Out‑of‑memory (GPU)**: switch to `device="cpu"` + `compute_type="int8"` or reduce `model_size_or_path` to `"base"`.

---

## Contributing

Open issues or PRs for bug fixes, feature requests, or performance tweaks. Please follow existing style and include clear commit messages.

---

## License & Credits

- **License**: MIT. See [LICENSE](LICENSE).
- **Credits**:
  - faster‑whisper by Ronnie Mess
  - srt by Jonas Winkler
  - FFmpeg for decoding
  - **Everything generated from ChatGPT** 🎉
