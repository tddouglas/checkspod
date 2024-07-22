Can use [Observable 2.0](https://observablehq.com/blog/observable-2-0) for each data visualization of scraped data.

torchaudio._backend.set_audio_backend warning will be fixed soon. Fix
is [pushed to dev branch](https://github.com/pyannote/pyannote-audio/issues/1576).

## Next Diarization Steps

1. Add `reviewed` column to database (done)
2. Implement finetuning following [this guide](https://huggingface.co/blog/fine-tune-whisper).
   FYI, [this comment](https://github.com/m-bain/whisperX/issues/530#issuecomment-1773342094) explains how to use
   finetuned model with whisperX.
3. Create evaluation framework for analyzing performance
4. Create 10 transcription .txt files (done) and review them manually to make sure they are accurate
5. Create huggingface database using transcription file and use for finetuning. See if they help scores based on evaluation framework. 

## Next Speaker Verification Steps
1. Best guess for speaker verification (or speaker identification) is to try to extract speaker embeddings from a diarization run and check if that embedding matches another run
   - Looks like this approach has already been implemented [here](https://github.com/pyannote/pyannote-audio/issues/1383) but was never merged to main. 
2. Example of how to extract embedding and compare speaker [here](https://github.com/pyannote/pyannote-audio/blob/develop/tutorials/speaker_verification.ipynb). This is not combined with diarization though.

## Other Next Steps
- Explore NVidia [Nemo Diarization](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/speaker_diarization/resources.html)
  - Seems promising. Can use `get_cluster_avg_embs()` function gor embedding extraction. Question is just can I run that with diarization or does it need to be done separately. Some guidance on that [here](https://github.com/NVIDIA/NeMo/issues/8171). 
- Move pipeline into it's own class? Make it easier to initialize/update

## Reading
1. https://docs.voice-ping.com/voiceping-corporation-company-profile/apr-2024-speaker-diarization-performance-evaluation-pyannoteaudio-vs-nvidia-nemo-and-post-processing-approach-using-openais-gpt-4-turbo
2. https://www.gladia.io/blog/build-a-speaker-identification-system-for-online-meetings
3. https://medium.com/@gil.shomron/whos-talking-speaker-diarization-and-emotion-recognition-in-radio-3e9623baeb2c

## Thoughts
1. Speaker diarization is good but not great. There are some incorrectly attributed parts of speach which I suspect
   could be quite detrimental to the output of the quiz run.
2. Translation is pretty good. Almost 100% accuracy from initial glance.
3. What local LLM can I run to test quiz answer inference. Can do GPT-4 via API. But what can I do via HuggingFace?
4. Speaker labeling could be problematic. I should be able to get host and additional speakers from episode summary.
   However, matching diarization output (SPEAKER_OO) to the host name will be challenging. Can likely easily infer host
   by signoff. Matching remaining 2 will be tough.
    - Not supported in pyannote yet. Can think about adding it myself
    - Potential implementation option is laid out [here](https://github.com/pyannote/pyannote-audio/discussions/1667).
      Similar discussions
      found [here](https://github.com/pyannote/pyannote-audio/discussions/1226#discussioncomment-4686072).
5. Could I use the embeddings from previous diarization runs and compare to determine speaker similarity

## Notes
Definitions taken from [here](https://github.com/NVIDIA/NeMo/issues/1710#issuecomment-776261922)
- **Speaker Recognition** = Using labeled data to train a model from scratch or finetune an exisiting one to recognize speakers from given labels
- **Speaker Verification** = Verifying if to speakers are the same without the need for labels. Aka, you don't care who the speakers are, just if they are the same
- **Speaker Diarization** = Segmenting audio by speaker label
- 