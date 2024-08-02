from pyannote.core import Annotation, Segment

from helpers.file_helper import get_base_path


def construct_rttm_path(filename):
    return get_base_path() + 'rttm_audio/' + filename + '.rttm'


def read_rttm_file(filename: str) -> Annotation:
    """
    Reads in rttm file from checkspod_files/rttm_audio folder
    @param filename: Just filename. We are appending base path and file extension
    @return: Annotation representing the audio file
    """
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
