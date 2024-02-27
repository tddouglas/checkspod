from nltk.book import *
import whisper

# Take in text and process it

'''
Goal - Separate out last 5 minutes of audio into text and determine:
1. What are the names of the quiz participants. 
2. What questions are asked in the quiz.
3. What answer did each contestant provide to a quiz question.  
4. If a contestant got the question correct or partially correct, how many points were they awarded? Unless stated otherwise, a correct answer is worth 1 point.
5. Who was the overall winner of the quiz? 

Data Store:
Participants Table -
1. ParticipantId (id: number)
2. ParticipantName (string)

Questions Table -
1. QuestionId (id: number)
2. EpisodeNumber (number)
3. Question - What was the question (string)
4. Answer - What was the correct answer (string)

Quiz Table -
1. QuestionId (id: fk)
2. ParticpantId - Who answered the question (id: fk)
3. ParticpantAnswer - What was the particpant's answer (string)
4. Award - Number of points awarded (number)
'''

nltk.download("book")
text8.concordance("quiz")  # analyze quiz usage in corpus


def gpt_analyze_transcript():
    # use GPT assistant to copy custom GPT functionality. Described below:
    # https://www.agenthost.ai/blog/open-ai-host-gpt-website
    pass

