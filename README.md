Can use [Observable 2.0](https://observablehq.com/blog/observable-2-0) for each data visulazation of scraped data.

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