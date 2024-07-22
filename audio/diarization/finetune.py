import os

from datasets import load_dataset, DatasetDict


# TODO: Finetuning implementation in progress.
# Instructions here - https://huggingface.co/blog/fine-tune-whisper
# General instructions here - https://huggingface.co/docs/transformers/en/training
def finetune():
    common_voice = DatasetDict()

    # CommonVoice Dataset - https://huggingface.co/datasets/mozilla-foundation/common_voice_13_0/discussions
    common_voice["train"] = load_dataset("mozilla-foundation/common_voice_13_0", "hi", split="train+validation",
                                         token=os.getenv('HUGGING_FACE_AUTH_TOKEN'), trust_remote_code=True)
    common_voice["test"] = load_dataset("mozilla-foundation/common_voice_13_0", "hi", split="test")

    # Format of DataSetDict - https://huggingface.co/docs/datasets/en/package_reference/main_classes#datasets.DatasetDict
    common_voice = common_voice.remove_columns(
        ["age", "client_id", "gender", "locale", "path", "segment", "down_votes", "up_votes"])

    # Mozilla Common_voice doesn't have helpful accent labels. Only 'indian' and 'native'


def print_dataset(dataset: DatasetDict):
    for split, dataset in dataset.items():
        print(f"Split: {split}")
        for idx, entry in enumerate(dataset):
            accent = entry['accent']
            if accent != '':
                print(f"Entry {idx}: {entry}")
                print("\n")