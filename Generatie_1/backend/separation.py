# backend/separation.py
from pathlib import Path
import subprocess
import shutil
from pydub import AudioSegment


def convert_to_wav(input_path: Path) -> Path:
    """Convert any audio file to WAV so Demucs can process it reliably."""
    wav_path = input_path.with_suffix(".wav")
    audio = AudioSegment.from_file(input_path)
    audio.export(wav_path, format="wav")
    return wav_path


def separate_stems(audio_path: str, output_dir: str) -> list[str]:
    """
    Run Demucs separation.
    Converts MP3 → WAV automatically to avoid torchaudio/torchcodec issues.
    """

    audio_path = Path(audio_path).resolve()

    # Convert MP3/FLAC/M4A/etc → WAV
    if audio_path.suffix.lower() != ".wav":
        audio_path = convert_to_wav(audio_path)

    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    demucs_output_root = Path("separated")

    # Run Demucs normally (no --dl flag)
    subprocess.run([
        "demucs",
        "-n", "htdemucs",
        str(audio_path)
    ], check=True)

    # Locate the output folder
    model_dir = demucs_output_root / "htdemucs"
    song_dirs = list(model_dir.iterdir())

    if not song_dirs:
        raise RuntimeError("Demucs did not produce any output folders.")

    song_dir = song_dirs[0]

    # Move stems into your project folder
    stems = []
    for stem_file in song_dir.iterdir():
        dest = output_dir / stem_file.name
        shutil.move(str(stem_file), str(dest))
        stems.append(str(dest.resolve()))

    # Clean up Demucs temporary output
    shutil.rmtree(demucs_output_root)

    return stems