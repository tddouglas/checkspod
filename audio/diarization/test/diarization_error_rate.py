from pyannote.core import Segment, Annotation
from pyannote.metrics.diarization import DiarizationErrorRate

"""
Copied from https://docs.voice-ping.com/voiceping-corporation-company-profile/apr-2024-speaker-diarization-performance-evaluation-pyannoteaudio-vs-nvidia-nemo-and-post-processing-approach-using-openais-gpt-4-turbo#block-19767a83bf1f43f583e9c370f57222ac
"""


# Read reference and hypothesis files
def read_rttm(file_path):
    data = Annotation()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 7:
                start_time = float(parts[3])
                end_time = start_time + float(parts[4])
                speaker_id = parts[7]
                segment = Segment(start_time, end_time)
                data[segment] = speaker_id
    return data


ref_file_path = "ground-truth.rttm"
hyp_rttm_file_path1 = "pyannote.rttm"
hyp_rttm_file_path2 = "pyannote(pre-identified speaker no).rttm"
hyp_rttm_file_path3 = "Nemo.rttm"
hyp_rttm_file_path4 = "Nemo(pre-identified speaker no).rttm"

reference = read_rttm(ref_file_path)
hypothesis1 = read_rttm(hyp_rttm_file_path1)
hypothesis2 = read_rttm(hyp_rttm_file_path2)
hypothesis3 = read_rttm(hyp_rttm_file_path3)
hypothesis4 = read_rttm(hyp_rttm_file_path4)

# Initialize Diarization Error Rate
diarization_error_rate = DiarizationErrorRate()

# Evaluate DER
der1 = diarization_error_rate(reference, hypothesis1)
der2 = diarization_error_rate(reference, hypothesis2)
der3 = diarization_error_rate(reference, hypothesis3)
der4 = diarization_error_rate(reference, hypothesis4)

print(f'DER for pyannote: {der1:.3f}')
print(f'DER for pyannote with number of speakers pre-identified: {der2:.3f}')
print(f'DER for Nemo: {der3:.3f}')
print(f'DER for Nemo with number of speakers pre-identified: {der4:.3f}')
