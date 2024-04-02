from transformers import pipeline, AutoTokenizer
import torch

# Take in text and process it

'''
Goal - Separate out last 5 minutes of audio into text and determine:
1. What are the names of the quiz participants. 
2. What questions are asked in the quiz.
3. What answer did each contestant provide to a quiz question.  
4. If a contestant got the question correct or partially correct, how many points were they awarded? Unless stated otherwise, a correct answer is worth 1 point.
5. Who was the overall winner of the quiz? 

Data Store:
Episodes Table -
1. Id - Epside Id
2. Title - title of episode
3. publish_date - Date episode was published online
4. summary - Summary of episode
5. filename - name of file without any extension
6. size - file size in MB (? I think)
7. url - url where episode was downloaded from
8. duration - duration of episode (s)  

Participants Table -
1. id (id: number)
2. participant_name (string)

Questions Table -
1. id (id: number)
2. episode_id (number) (id: fk)
3. question - What was the question (string)
4. answer - What was the correct answer (string)

episode_questions Table -
1. episode_id - (id: fk)
2. question_id - (id: fk)
2. participant_id - Who answered the question (id: fk)
3. participant_answer - What was the particpant's answer (string)
4. award - Number of points awarded (number)
'''


# Can you the nltk library and concordance() to analyze text
# nltk.download("book")
# text8.concordance("quiz")  # analyze quiz usage in corpus


def gpt_analyze_transcript():
    # use GPT assistant to copy custom GPT functionality. Described below:
    # https://www.agenthost.ai/blog/open-ai-host-gpt-website
    pass

# This function should take the full transcript and truncate it where the quiz starts
def quiz_determination():
    pass


# TODO: Find appropriate model to use. From huggingface chat (https://huggingface.co/chat/models) - MistralAi seems to give me best results with current prompt
# Attempt to fine-tune on a qa dataset - https://huggingface.co/datasets?task_ids=task_ids%3Aextractive-qa
# review transformer tutorials - https://huggingface.co/docs/transformers/tasks/question_answering
def local_analysis(prompt):
    model = "tiiuae/falcon-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    torch.manual_seed(0)

    sequences = pipe(
        prompt,
        max_new_tokens=10,
        do_sample=True,
        top_k=10,
        return_full_text=False,
    )
    for seq in sequences:
        print(f"Result: {seq['generated_text']}")
