from helpers.file_helper import get_base_path


def construct_txt_path(filename) -> str:
    return get_base_path() + "reviewed_transcripts/" + filename + '.txt"'


def read_in_txt(filename):
    file = open(construct_txt_path(filename), 'r')
    content = file.read()
    file.close()
    return content


def write_to_text_file(filename, text):
    with open(construct_txt_path(filename), 'w') as file:
        file.write(text)
