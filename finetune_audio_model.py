from huggingface_hub import notebook_login
from datasets import load_dataset, DatasetDict


# TODO: In progress
def finetune():
    # Not sure how this works??
    notebook_login()  # Used to link notebook to hugging face hub which can be used as version control

    common_voice = DatasetDict()

    common_voice["train"] = load_dataset("mozilla-foundation/common_voice_11_0", "hi", split="train+validation",
                                         use_auth_token=True)
    common_voice["test"] = load_dataset("mozilla-foundation/common_voice_11_0", "hi", split="test", use_auth_token=True)

    print(common_voice)
