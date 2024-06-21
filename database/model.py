from peewee import *

# Define the database connection
db = SqliteDatabase('database/checkspod.db')

class BaseModel(Model):
    class Meta:
        database = db

class Episodes(BaseModel):
    title = CharField()  #title of episode
    publish_date = CharField()  #Date episode was published online
    summary = TextField()  #Summary of episode
    filename = CharField()  #Formatted as date episode aired without any file extension. E.g. 2024-03-22-2
    size = IntegerField()  #file size in MB
    url = CharField()  #url where episode was downloaded from
    duration = FloatField()  #duration of episode (s)

class Questions(BaseModel):
    episode = ForeignKeyField(Episodes, backref='questions')
    question = TextField()  #What was the question
    answer = TextField()  #What was the correct answer

class Participants(BaseModel):
    name = CharField()
    # Add other participant attributes as needed

class EpisodeQuestions(BaseModel):
    episode = ForeignKeyField(Episodes, backref='episode_questions')
    question = ForeignKeyField(Questions, backref='episode_questions')
    participant = ForeignKeyField(Participants, backref='episode_questions')
    participant_answer = CharField()  #What was the participant's answer
    award = IntegerField()  #Number of points awarded for each question

    class Meta:
        primary_key = CompositeKey('episode', 'question')
