import os
import whisperx

from audio_to_text.audio_to_text import get_torch_device
from helpers.audio_file_helper import construct_wav_path


# Utilizes Whipserx for diarlization and transcription instead of Custom Implementation above.
def whisperx_diarization_transcribe(filename) -> str:
    audio_file = construct_wav_path(filename)
    device = get_torch_device()
    batch_size = 16  # reduce if low on GPU mem
    compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)
    options = {
        "max_new_tokens": None,
        "clip_timestamps": None,
        "hallucination_silence_threshold": None,
    }

    model = whisperx.load_model("large-v2", device, compute_type=compute_type, asr_options=options)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    # print("Before Alignment\n", result["segments"])  # before alignment

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    # print("After Alignment\n", result["segments"])  # after alignment

    # 3. Assign speaker labels
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=os.getenv('HUGGING_FACE_AUTH_TOKEN'), device=device)

    # add min/max number of speakers if known
    diarize_segments = diarize_model(audio)
    # diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)

    result = whisperx.assign_word_speakers(diarize_segments, result)
    final_res = ""
    for segment in result["segments"]:
        if 'speaker' in segment:
            speaker = segment['speaker']
        else:
            speaker = 'UNKNOWN'

        formatted_text = f"{speaker} - {segment['text']}"
        final_res += formatted_text + '\n'

    # print(f"Final text is:\n{final_res}")
    return final_res
