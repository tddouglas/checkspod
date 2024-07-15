from helpers.audio_file_helper import construct_rttm_path
from pyannote.core import Annotation, Segment


def read_rttm_file(filename):
    filepath = construct_rttm_path(filename)
    annotation = Annotation()
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 10:
                start_time = float(parts[3])
                duration = float(parts[4])
                end_time = start_time + duration
                speaker = parts[7]
                segment = Segment(start_time, end_time)
                annotation[segment, filename] = speaker
    return annotation