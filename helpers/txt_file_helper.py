def read_in_txt(filename):
    file = open(filename, 'r')
    content = file.read()
    file.close()
    return content


def write_to_text_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)
