"""
File for implementing nVidia NeMo

Embedding Extraction detailed [here](https://github.com/NVIDIA/NeMo/blob/8035dd0bf558d745471fd253c2882bc0d600db2f/docs/source/asr/speaker_recognition/results.rst#speaker-embedding-extraction)
Can see pure embedding helper file [here](https://github.com/NVIDIA/NeMo/blob/8035dd0bf558d745471fd253c2882bc0d600db2f/examples/speaker_tasks/recognition/extract_speaker_embeddings.py#L18)

NeMo definitely has its own embedding models but question is if I can run it in parallel with diarization
[This](https://github.com/NVIDIA/NeMo/tree/main/examples/speaker_tasks/diarization#run-speaker-diarization-on-your-audio-files) makes it look like I can

File base taken from [here](https://docs.voice-ping.com/voiceping-corporation-company-profile/apr-2024-speaker-diarization-performance-evaluation-pyannoteaudio-vs-nvidia-nemo-and-post-processing-approach-using-openais-gpt-4-turbo#block-19767a83bf1f43f583e9c370f57222ac)
"""

import json
import os
from nemo.collections.asr.models import NeuralDiarizer
from omegaconf import OmegaConf
import wget


def diarize_audio(input_file):
    # Diarization configuration
    meta = {
        'audio_filepath': input_file,
        'offset': 0,
        'duration': None,
        'label': 'infer',
        'text': '-',
        'num_speakers': None,  # Incase you want to pre-identify the number of people, add it here)
        'rttm_filepath': None,
        'uem_filepath': None
    }

    # Write manifest
    with open('input_manifest.json', 'w') as fp:
        json.dump(meta, fp)
        fp.write('\n')

    output_dir = os.path.join('output')
    os.makedirs(output_dir, exist_ok=True)

    # Load model config
    model_config = 'diar_infer_telephonic.yaml'
    if not (model_config):
        config_url = "https://raw.githubusercontent.com/NVIDIA/NeMo/main/examples/speaker_tasks/diarization/conf/inference/diar_infer_general.yaml"
        model_config = wget.download(config_url)  # Update the path to the MSDD model configuration
    config = OmegaConf.load(model_config)

    config.diarizer.msdd_model.model_path = 'diar_msdd_telephonic'  # telephonic speaker diarization model
    config.diarizer.msdd_model.parameters.sigmoid_threshold = [0.7, 1.0]  # Evaluate with T=0.7 and T=1.0

    # Initialize diarizer
    msdd_model = NeuralDiarizer(cfg=config)

    # Diarize audio
    diarization_result = msdd_model.diarize()

    return diarization_result