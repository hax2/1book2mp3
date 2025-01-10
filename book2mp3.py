#!/usr/bin/env python3

import os
import sys
import argparse
import asyncio
import time
from edge_tts import Communicate
from pydub import AudioSegment

CHUNK_SIZE = 6000  # Adjusted to handle more text per chunk
PAUSE_DURATION = 2  # Pause in seconds between requests
FINAL_MERGE_COUNT = 7  # Number of final merged MP3 files

async def text_to_mp3(text, index, output_folder, voice="en-US-JennyNeural"):
    """
    Convert text to an MP3 file using Edge TTS
    """
    mp3_filename = os.path.join(output_folder, f"part_{index:03d}.mp3")
    communicate = Communicate(text=text, voice=voice)
    await communicate.save(mp3_filename)
    print(f"[+] Saved: {mp3_filename}")
    return mp3_filename

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyPDF2
    """
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        sys.exit("PyPDF2 is not installed. Please install via: pip install PyPDF2")
    
    reader = PdfReader(pdf_path)
    text_list = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_list.append(page_text)
    return "\n".join(text_list)

def split_into_chunks(text, chunk_size=CHUNK_SIZE):
    """
    Split long text into smaller chunks
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(" ".join(current_chunk)) >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def merge_mp3s(mp3_files, output_folder, final_count=FINAL_MERGE_COUNT):
    """
    Merge MP3 files into a smaller number of final files
    """
    if not mp3_files:
        print("[!] No MP3 files to merge.")
        return
    
    print("[*] Merging MP3 files...")
    num_files_per_merge = max(1, len(mp3_files) // final_count)
    merged_files = []

    for i in range(0, len(mp3_files), num_files_per_merge):
        chunk_files = mp3_files[i:i + num_files_per_merge]
        combined = AudioSegment.empty()

        for file in chunk_files:
            combined += AudioSegment.from_file(file)

        merged_filename = os.path.join(output_folder, f"final_part_{len(merged_files) + 1:03d}.mp3")
        combined.export(merged_filename, format="mp3")
        print(f"[+] Merged file created: {merged_filename}")
        merged_files.append(merged_filename)

    print(f"[+] Total merged files: {len(merged_files)}")
    return merged_files

async def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF to multiple MP3s using Edge TTS and merge into final files."
    )
    parser.add_argument("file", help="Path to the PDF file.")
    parser.add_argument(
        "-o", "--output",
        default="output_mp3s",
        help="Folder where MP3 files will be saved (default: output_mp3s)."
    )
    parser.add_argument(
        "-c", "--chunk-size",
        type=int,
        default=CHUNK_SIZE,
        help="Approximate number of characters per text chunk (default: 6000)."
    )
    parser.add_argument(
        "-v", "--voice",
        default="en-US-JennyNeural",
        help="Edge TTS voice to use (default: en-US-JennyNeural)."
    )
    args = parser.parse_args()

    input_path = args.file
    output_folder = args.output
    chunk_size = args.chunk_size
    voice = args.voice

    if not os.path.isfile(input_path):
        sys.exit(f"[!] File not found: {input_path}")

    os.makedirs(output_folder, exist_ok=True)

    print("[*] Extracting text from PDF...")
    raw_text = extract_text_from_pdf(input_path)

    if not raw_text.strip():
        sys.exit("[!] No text could be extracted. Exiting.")

    print("[*] Splitting text into chunks...")
    chunks = split_into_chunks(raw_text, chunk_size=chunk_size)
    total_chunks = len(chunks)
    print(f"[*] Total chunks: {total_chunks}")

    print("[*] Converting chunks to MP3s...")
    mp3_files = []
    for i, chunk in enumerate(chunks, start=1):
        mp3_file = await text_to_mp3(chunk, i, output_folder, voice)
        mp3_files.append(mp3_file)
        time.sleep(PAUSE_DURATION)  # Add pause to avoid throttling

    print("[*] Merging MP3 files into final files...")
    merge_mp3s(mp3_files, output_folder)

    print("[+] All tasks completed!")

if __name__ == "__main__":
    asyncio.run(main())
