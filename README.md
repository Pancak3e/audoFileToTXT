# Audio Transcription Tool

This Python application transcribes audio files using OpenAI's Whisper model locally. It provides a nicely formatted output with timestamps, sections, and a table of contents.

## Features

- Transcribes audio files using Whisper's base model
- Automatically detects and creates logical sections
- Generates both raw and formatted transcripts
- Includes timestamps and table of contents
- Works with various audio formats (mp3, wav, m4a, etc.)

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. The first run will automatically download:
   - The Whisper base model (about 1GB)
   - NLTK punkt tokenizer data

## Usage

Run the script with your audio file as an argument:

```bash
python transcribe.py path/to/your/audio/file.mp3
```

The script will create two files in a `transcripts` directory:
- `*_raw_[timestamp].txt`: The raw transcript
- `*_formatted_[timestamp].txt`: A formatted version with sections and timestamps

## Output Format

The formatted transcript includes:
- File information and generation timestamp
- Table of contents with timestamps
- Sections with titles and timestamps
- Clean formatting for easy reading

## Notes

- For large audio files, the transcription might take some time
- The base Whisper model is used by default for a good balance of accuracy and speed
- Sections are automatically detected based on natural breaks in speech and sentence structure.
