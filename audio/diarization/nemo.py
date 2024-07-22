'''
File for implementing nVidia NeMo

Embedding Extraction detailed [here](https://github.com/NVIDIA/NeMo/blob/8035dd0bf558d745471fd253c2882bc0d600db2f/docs/source/asr/speaker_recognition/results.rst#speaker-embedding-extraction)
Can see pure embedding helper file [here](https://github.com/NVIDIA/NeMo/blob/8035dd0bf558d745471fd253c2882bc0d600db2f/examples/speaker_tasks/recognition/extract_speaker_embeddings.py#L18)

NeMo definitely has its own embedding models but question is if I can run it in parallel with diarization
[This](https://github.com/NVIDIA/NeMo/tree/main/examples/speaker_tasks/diarization#run-speaker-diarization-on-your-audio-files) makes it look like I can
'''