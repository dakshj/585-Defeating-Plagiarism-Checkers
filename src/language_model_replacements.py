import gensim

import remove_punctuations
import tokenize_input_text
from check_candidate_type import is_candidate_pos_type

FILE_FACEBOOK_WORD_VECTORS = './../datasets/wiki.en.vec'


class LanguageModelReplacement:
    model = None

    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format(FILE_FACEBOOK_WORD_VECTORS)

    def set_language_model_replacements(self, all_tokens_of_all_sentences):
        for sentence in all_tokens_of_all_sentences:
            for token in sentence:
                if not is_candidate_pos_type(token.pos) or token.is_stopword:
                    continue

                try:
                    replacement_words = []
                    for word, prob in self.model.similar_by_word(
                            token.word_without_punctuations):
                        word = remove_punctuations.remove_surrounding_punctuations(word)

                        if word != token.word_without_punctuations:
                            replacement_words.append(word)

                    if replacement_words:
                        token.replacements_langmod = replacement_words
                except KeyError:
                    pass


if __name__ == '__main__':
    input_text = open('./../datasets/input_text.txt', encoding='utf8').read()

    all_tokens_of_all_sentences = tokenize_input_text.tokenize(input_text)

    lmr = LanguageModelReplacement()
    lmr.set_language_model_replacements(all_tokens_of_all_sentences)

    for sentence in all_tokens_of_all_sentences:
        for token in sentence:
            if is_candidate_pos_type(token.pos) and not token.is_stopword:
                print(token)
