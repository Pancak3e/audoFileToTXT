import whisper
import argparse
from pathlib import Path
from datetime import datetime
import time

def format_time(seconds):
    """Convert seconds to HH:MM:SS format"""
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def detect_sections(text, timestamps, words_per_section=150):
    """
    Detect logical sections in the transcript based on word count and punctuation
    """
    words = text.split()
    sections = []
    current_section = {
        'title': 'Section 1',
        'start_time': format_time(timestamps[0]),
        'content': []
    }
    
    word_count = 0
    current_words = []
    timestamp_idx = 0
    
    for word in words:
        current_words.append(word)
        word_count += 1
        
        # Create new section every ~150 words or at sentence endings
        if word_count >= words_per_section or word.endswith(('.', '!', '?')):
            current_text = ' '.join(current_words)
            current_section['content'] = current_text
            
            # Generate title from first few words
            title_words = current_words[:5]
            current_section['title'] = ' '.join(title_words) + '...'
            
            sections.append(current_section)
            
            # Update timestamp index
            timestamp_idx = min(timestamp_idx + 1, len(timestamps) - 1)
            
            # Start new section
            current_section = {
                'title': f'Section {len(sections) + 1}',
                'start_time': format_time(timestamps[timestamp_idx]),
                'content': []
            }
            current_words = []
            word_count = 0
    
    # Add remaining content as last section
    if current_words:
        current_section['content'] = ' '.join(current_words)
        sections.append(current_section)
    
    return sections

def transcribe_audio(audio_path):
    """
    Transcribe audio file using Whisper and create formatted output
    """
    print("Loading Whisper model (this might take a moment)...")
    model = whisper.load_model("base")
    
    print(f"\nTranscribing {audio_path}...")
    result = model.transcribe(str(audio_path), verbose=False)
    
    # Create output directory
    output_dir = Path("transcripts")
    output_dir.mkdir(exist_ok=True)
    
    # Generate filename based on input
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = Path(audio_path).stem
    
    # Save raw transcript
    raw_output = output_dir / f"{base_name}_raw_{timestamp}.txt"
    with open(raw_output, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    # Process and save formatted transcript
    sections = detect_sections(result["text"], [seg["start"] for seg in result["segments"]])
    
    formatted_output = output_dir / f"{base_name}_formatted_{timestamp}.txt"
    with open(formatted_output, "w", encoding="utf-8") as f:
        f.write(f"Transcript of: {audio_path}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Table of Contents
        f.write("TABLE OF CONTENTS\n")
        f.write("=" * 16 + "\n\n")
        for i, section in enumerate(sections, 1):
            f.write(f"{i}. [{section['start_time']}] {section['title']}\n")
        f.write("\n" + "=" * 80 + "\n\n")
        
        # Sections
        for i, section in enumerate(sections, 1):
            f.write(f"\nSection {i}: {section['title']}\n")
            f.write(f"Time: {section['start_time']}\n")
            f.write("-" * 40 + "\n")
            f.write(section['content'])
            f.write("\n\n" + "-" * 80 + "\n")
    
    print(f"\nTranscription complete!")
    print(f"Raw transcript saved to: {raw_output}")
    print(f"Formatted transcript saved to: {formatted_output}")

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files with sections and formatting")
    parser.add_argument("audio_path", help="Path to the audio file to transcribe")
    args = parser.parse_args()
    
    transcribe_audio(args.audio_path)

if __name__ == "__main__":
    main() 
