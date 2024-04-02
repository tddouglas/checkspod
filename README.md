Can use [Observable 2.0](https://observablehq.com/blog/observable-2-0) for each data visulazation of scraped data.

torchaudio._backend.set_audio_backend warning will be fixed soon. Fix
is [pushed to dev branch](https://github.com/pyannote/pyannote-audio/issues/1576).

## Thoughts

1. Speaker diarization is good but not great. There are some incorrectly attributed parts of speach which I suspect
   could be quite detrimental to the output of the quiz run. 
2. Translation is pretty good. Almost 100% accuracy from initial glance.
3. I should test how good LLM is at inferring results from speaker transcript. How does it work with output from code?
   How does it work with manual, perfect output fed in?
4. What local LLM can I run to test quiz answer inference. Can do GPT-4 via API. But what can I do via HuggingFace?