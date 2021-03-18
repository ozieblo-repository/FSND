from suggest_gaps import suggest_gaps
from parse_sentence import parse_sentence
import pandas as pd

SOURCE_TEXT_PATH = "../tests/note.md" # connect to note form box
OUTPUT_FILE_NAME = "results.csv" # connect to the database

def md_handler() -> list:

    """
    Read source .md file and prepare it for the future wrangling.
    It gives a list of single sentences.
    """

    file = SOURCE_TEXT_PATH

    try:
        with open(file,'r') as input_file:
            input_text_list = []
            for textline in input_file:
                input_text_list.append(textline.strip())
            formatted_text = list((i for i in input_text_list if ("#" not in i) and i))
            print("Markdown file has been formatted.")
    except EnvironmentError:
        print('Error in md_handler. Please check the console.')

    return formatted_text

def main() -> pd.DataFrame:

    """
    Create .csv file with gap questions related to source text in .md format.
    """

    text = md_handler()

    output = pd.DataFrame(data = None,
                          columns=("Sentence","Question"))

    n_sentences = len(text)

    try:
        for n, sentence in enumerate(text):
            parsed_text = parse_sentence(sentence)
            new_record = suggest_gaps(parsed_text,
                                      sentence)
            print(f"Processed sentence {n+1} of {n_sentences}: ",
                  sentence)
            output = pd.concat([output, new_record])
    except EnvironmentError:
        print("Error in main file. Please check the console output.")

    n_questions = len(output)

    print("-" * 80)
    print(f"{n_questions} gap questions have been created based on {n_sentences} sentences.")

    try:
        output.to_csv(OUTPUT_FILE_NAME)
        print("Please review the output csv file.")
    except:
        "Error: Cannot create output file. Please check the console."

if __name__ == "__main__":
    main()