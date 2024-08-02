import logging
import numpy as np
from pydub import AudioSegment
import ffmpeg

from helpers.file_helper import get_base_path

# Class for importing and manipulating audio files. Checkspod_downloader downloads .mp3 files from economist.com
# This will take in a .mp3 file, shorten it to 7 minutes and convert it to a .wav for pyannote

logger = logging.getLogger(__name__)


def construct_wav_path(filename):
    return get_base_path() + filename + '.wav'


def construct_mp3_path(filename):
    return get_base_path() + 'original_audio/' + filename + '.mp3'


# Open mp3 file, shorten it, then convert it to .wav
def mp3_to_wav_pipeline(mp3_audio_path, wav_audio_path):
    # TODO: Ensure this still works. Requires adopting new checkspod schema
    mp3_audio = load_mp3_audio(mp3_audio_path)
    shortened_audio = shorten_audio(mp3_audio)
    export_wav_audio(shortened_audio, wav_audio_path)


def load_mp3_audio(audio_path):
    return AudioSegment.from_mp3(audio_path)


def load_wav_audio(audio_path):
    return AudioSegment.from_file(construct_wav_path(audio_path))


def audio_to_nparray(trimmed_audio):
    samples = np.array(trimmed_audio.get_array_of_samples())
    return samples


def load_audio(file: (str, bytes), sr: int = 16000):
    """
    Open an audio file and read as mono waveform, resampling as necessary

    Parameters
    ----------
    file: (str, bytes)
        The audio file to open or bytes of audio file

    sr: int
        The sample rate to resample the audio if necessary

    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """

    if isinstance(file, bytes):
        inp = file
        file = 'pipe:'
    else:
        inp = None

    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(file, format="s16le", acodec="pcm_s16le", ac=2, ar=48000)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=inp)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio:\n {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


# Trim .mp3 audio file to specified time (s)
def shorten_audio(audio):
    # last_5_minutes = audio[-300000:]

    if len(audio) < 430000:  # Check if audio is less than 7 minutes. Is so, don't shorten
        return audio
    return audio[-430000:]  # Last 7 minutes


def export_wav_audio(audio, filename):
    audio.export(construct_wav_path(filename))
