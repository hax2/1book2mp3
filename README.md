# PDF to MP3 Converter Guide

This script converts a PDF document into MP3 audio files using Edge TTS and merges them into a smaller number of final audio files. Below is a step-by-step guide to use the script.

---

## Requirements

1. **Python 3.6+**
2. Install required Python packages:
   ```bash
   pip install edge-tts pydub PyPDF2
   ```

3. Install **ffmpeg** for audio processing:
   - On macOS (using Homebrew):
     ```bash
     brew install ffmpeg
     ```
   - On Ubuntu/Debian:
     ```bash
     sudo apt install ffmpeg
     ```
   - On Windows: Download from [FFmpeg official website](https://ffmpeg.org/download.html) and add it to your PATH.

---

## Usage

### Command Format
Run the script from the terminal using:
```bash
python3 book2mp3.py <path_to_pdf> [options]
```

### Required Argument
- `<path_to_pdf>`: Path to the PDF file you want to convert.

### Optional Arguments
- `-o`, `--output`: Specify the output folder for MP3 files (default: `output_mp3s`).
- `-c`, `--chunk-size`: Set the approximate number of characters per text chunk (default: `6000`).
- `-v`, `--voice`: Choose the Edge TTS voice (default: `en-US-JennyNeural`).

---

## Example

### Basic Usage
```bash
python3 book2mp3.py example.pdf
```

### Custom Output Folder and Voice
```bash
python3 book2mp3.py example.pdf -o custom_output -v en-GB-RyanNeural
```

---

## Output

1. **Intermediate MP3 Files**: Saved as `part_001.mp3`, `part_002.mp3`, etc., in the output folder.
2. **Merged MP3 Files**: Final merged files are saved as `final_part_001.mp3`, `final_part_002.mp3`, etc.

---

## Notes
- Ensure your PDF contains selectable text; scanned PDFs without OCR won't work.
- Adjust `CHUNK_SIZE` and `PAUSE_DURATION` in the script if experiencing issues with large files or throttling.
- Check [Edge TTS voices](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech) for additional voice options.
