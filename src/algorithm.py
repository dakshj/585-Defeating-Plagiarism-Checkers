from detect_plagiarism import detect_plagiarism
from language_model_replacements import LanguageModelReplacement
from logistic_regression import LogReg
from output import generate_output_text_from_tokens
from set_best_replacement_word import set_best_replacement_word
from tokenize_input_text import tokenize

PLAGIARISM_THRESHOLD = 60  # 60%
REPLACEMENTS_BEFORE_EACH_PLAGIARISM_CHECK = 2
MAX_PLAGIARISM_REDUCTION_REPLACEMENT_ITERATIONS = 5


def get_plagiarism_free_text(input_text):
    all_tokens_of_all_sentences = tokenize(input_text)

    print('Tokens after being read:')
    print(all_tokens_of_all_sentences + '\n\n\n\n')

    LogReg().set_replacements_in_tokens(all_tokens_of_all_sentences)

    print('Tokens after LogReg:')
    print(all_tokens_of_all_sentences + '\n\n\n\n')

    LanguageModelReplacement().set_language_model_replacements(all_tokens_of_all_sentences)
    print('Tokens after LangMod:')
    print(all_tokens_of_all_sentences + '\n\n\n\n')

    # TODO Add synonym API as well?

    current_plagiarism = 100.

    iterations = 0

    while iterations < MAX_PLAGIARISM_REDUCTION_REPLACEMENT_ITERATIONS and \
                    current_plagiarism > PLAGIARISM_THRESHOLD:
        set_best_replacement_word(all_tokens_of_all_sentences,
                                  REPLACEMENTS_BEFORE_EACH_PLAGIARISM_CHECK)
        current_plagiarism = \
            detect_plagiarism(generate_output_text_from_tokens(all_tokens_of_all_sentences))
        iterations += 1

    return generate_output_text_from_tokens(all_tokens_of_all_sentences)


if __name__ == '__main__':
    input_text = open('./../datasets/input_text.txt', encoding='utf8').read()
    print(get_plagiarism_free_text(input_text))
