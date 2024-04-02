from peewee import *

# Define the database connection
db = SqliteDatabase('database/checkspod.db')

class BaseModel(Model):
    class Meta:
        database = db

class Episodes(BaseModel):
    title = CharField()
    publish_date = CharField()
    summary = TextField()
    filename = CharField()
    size = IntegerField()
    url = CharField()
    duration = FloatField()

class Questions(BaseModel):
    episode = ForeignKeyField(Episodes, backref='questions')
    question = TextField()
    answer = TextField()

class Participants(BaseModel):
    name = CharField()
    # Add other participant attributes as needed

class EpisodeQuestions(BaseModel):
    episode = ForeignKeyField(Episodes, backref='episode_questions')
    question = ForeignKeyField(Questions, backref='episode_questions')
    participant = ForeignKeyField(Participants, backref='episode_questions')
    participant_answer = CharField()
    award = IntegerField()

    class Meta:
        primary_key = CompositeKey('episode', 'question')
