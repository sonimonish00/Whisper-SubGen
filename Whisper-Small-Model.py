from faster_whisper import WhisperModel
import srt
from datetime import timedelta

# 1. Initialize model correctly
model = WhisperModel(
    model_size_or_path="small",  # positional argument
    device="cpu",
    compute_type="int8"
)

print("Transcribing and translating...")
segments, info = model.transcribe(
    r"C:\Trauma-2025.mkv",
    task="translate",
    language="ta"
)

# 2. Generate SRT using attribute access
def generate_srt(segments):
    subtitles = []
    for i, seg in enumerate(segments):
        subtitles.append(
            srt.Subtitle(
                index=i+1,
                start=timedelta(seconds=seg.start),
                end=timedelta(seconds=seg.end),
                content=seg.text.strip()
            )
        )
    return srt.compose(subtitles)

# 3. Write to file
srt_data = generate_srt(segments)
with open(r"C:\Trauma-2025_EN.srt", "w", encoding="utf-8") as f:
    f.write(srt_data)

print("✅ Subtitle file created: Trauma-2025_EN.srt")
