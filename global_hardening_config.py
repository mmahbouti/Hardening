
def convert_text_to_list(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
        #print(content)
    output_config = [line.strip() for line in content.splitlines() if line.strip()]
    return output_config

