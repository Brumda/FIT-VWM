import math
import os

import experiments
from helper_fuctions import read_file, get_tokens


class TextProcessor:
    def __init__(self, directory="./cleaned/"):
        self.directory = directory
        self.index_document = self.index_documents()
        self.term_dict, self.doc_dict = self.get_uniq_terms()
        self.all_dict = self.tfidf_term()
        # self.freqency_matrix = self.tfidf_term_seq()

    # nltk.download('punkt')
    # nltk.download('stopwords')
    # nltk.download('wordnet')

    def get_uniq_terms_experiment(self, size):
        term_maximum_frequency = {}
        term_file_frequency = {}

        for filename in os.listdir(self.directory):
            if size == 0:
                break
            if filename.endswith(".txt"):
                text_file = os.path.join(self.directory, filename)
                text = read_file(text_file)
                tokens = get_tokens(text)
                current_term_frequency = {}

                for token in tokens:
                    if token in current_term_frequency:
                        current_term_frequency[token] += 1
                    else:
                        current_term_frequency[token] = 1

                term_file_frequency[self.index_document[filename]] = current_term_frequency.copy()

                for term, freq in current_term_frequency.items():
                    if term in term_maximum_frequency:
                        term_maximum_frequency[term][0] = max(term_maximum_frequency[term][0], freq)
                        term_maximum_frequency[term][1] += 1
                    else:
                        term_maximum_frequency[term] = [freq, 1]
                size -= 1

        return term_maximum_frequency, term_file_frequency

    def get_uniq_terms(self):
        term_maximum_frequency = {}
        term_file_frequency = {}

        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):
                text_file = os.path.join(self.directory, filename)
                text = read_file(text_file)
                tokens = get_tokens(text)
                current_term_frequency = {}

                for token in tokens:
                    if token in current_term_frequency:
                        current_term_frequency[token] += 1
                    else:
                        current_term_frequency[token] = 1

                term_file_frequency[self.index_document[filename]] = current_term_frequency.copy()

                for term, freq in current_term_frequency.items():
                    if term in term_maximum_frequency:
                        term_maximum_frequency[term][0] = max(term_maximum_frequency[term][0], freq)
                        term_maximum_frequency[term][1] += 1
                    else:
                        term_maximum_frequency[term] = [freq, 1]

        return term_maximum_frequency, term_file_frequency

    def index_documents_experiment(self, size):
        index_document = {}
        index = 0
        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):
                index_document[filename] = index
                index += 1
                size -= 1
        return index_document

    def index_documents(self):
        index_document = {}
        index = 0
        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):
                index_document[filename] = index
                index += 1
        return index_document

    def tfidf_term_experiment(self, index_document, term_dict, doc_dict):
        doc_cnt = len(index_document)
        max_tfidf = 0
        all_dict = {}
        for term, value_term in term_dict.items():
            inner_dict = {}
            for index, value_doc in doc_dict.items():
                if term in value_doc:
                    tfidf = (value_doc[term] / value_term[0]) * math.log(doc_cnt / value_term[1])
                    if tfidf > max_tfidf:
                        max_tfidf = tfidf
                    inner_dict[index] = tfidf
            all_dict[term] = inner_dict.copy()
        for key1, value1 in all_dict.items():
            for key2, value2 in value1.items():
                all_dict[key1][key2] = (value2 - 0) / (max_tfidf - 0)
        return all_dict

    def tfidf_term(self):
        doc_cnt = len(self.index_document)
        max_tfidf = 0
        all_dict = {}
        for term, value_term in self.term_dict.items():
            inner_dict = {}
            for index, value_doc in self.doc_dict.items():
                if term in value_doc:
                    tfidf = (value_doc[term] / value_term[0]) * math.log(doc_cnt / value_term[1])
                    if tfidf > max_tfidf:
                        max_tfidf = tfidf
                    inner_dict[index] = tfidf
            all_dict[term] = inner_dict.copy()
        for key1, value1 in all_dict.items():
            for key2, value2 in value1.items():
                all_dict[key1][key2] = (value2 - 0) / (max_tfidf - 0)
        return all_dict

    def tfidf_term_seq_experiment(self, index_document, doc_dict, term_dict):
        doc_cnt = len(index_document)
        max_tfidf = 0
        matrix = []
        for id, value_doc in doc_dict.items():
            inner_list = []
            y = 0
            for term, value_term in term_dict.items():
                if term in value_doc:
                    tfidf = (value_doc[term] / value_term[0]) * math.log(doc_cnt / value_term[1])
                    if tfidf > max_tfidf:
                        max_tfidf = tfidf
                else:
                    tfidf = 0
                inner_list.append([term, tfidf])
                y += 1
            matrix.append([id, inner_list.copy()])
        for x, _ in enumerate(matrix):
            for y, _ in enumerate(matrix[x][1]):
                matrix[x][1][y][1] = (matrix[x][1][y][1] - 0) / (max_tfidf - 0)
        return matrix

    def tfidf_term_seq(self):
        doc_cnt = len(self.index_document)
        max_tfidf = 0
        matrix = []
        for id, value_doc in self.doc_dict.items():
            inner_list = []
            y = 0
            for term, value_term in self.term_dict.items():
                if term in value_doc:
                    tfidf = (value_doc[term] / value_term[0]) * math.log(doc_cnt / value_term[1])
                    if tfidf > max_tfidf:
                        max_tfidf = tfidf
                else:
                    tfidf = 0
                inner_list.append([term, tfidf])
                y += 1
            matrix.append([id, inner_list.copy()])
        for x, _ in enumerate(matrix):
            for y, _ in enumerate(matrix[x][1]):
                matrix[x][1][y][1] = (matrix[x][1][y][1] - 0) / (max_tfidf - 0)
        return matrix

    def get_tfidf(self, term):
        results = []
        if term in self.all_dict:
            for _, id in self.index_document.items():
                if id in self.all_dict[term]:
                    results.append(self.all_dict[term][id])
                else:
                    results.append(0)
            return results
        return [0] * len(self.index_document)

    def get_tfidf_seq(self, term):
        results = []
        for _, id in self.index_document.items():
            appended = False
            for inner_list in self.freqency_matrix:
                if not appended:
                    if inner_list[0] == id:
                        for curr in inner_list[1]:
                            if not appended:
                                if curr[0] == term:
                                    results.append(curr[1])
                                    appended = True
                                    break
                        if not appended:
                            results.append(0)
                        break
        return results

    def calculate_relevance(self, query, get_tfidf_curr):
        if ' ' not in query:
            return get_tfidf_curr(query)
        tokens = []
        current_token = ''
        parentheses_cnt = 0
        in_parentheses = False
        for char in query:
            if (char == ' ') and not in_parentheses:
                tokens.append(current_token.lower())
                current_token = ''
            elif char == '(':
                parentheses_cnt += 1
                if parentheses_cnt == 1:
                    in_parentheses = True
                else:
                    current_token += char
            elif char == ')':
                parentheses_cnt -= 1
                if parentheses_cnt == 0:
                    in_parentheses = False
                else:
                    current_token += char
            else:
                current_token += char
        if parentheses_cnt != 0:
            raise Exception("Invalid syntax: wrong parentheses")
        if current_token:
            tokens.append(current_token)
        if 'and' in tokens and 'or' in tokens:
            raise Exception("Invalid syntax: different operators in subquery")
        if 'and' in tokens:
            lower = 0
            upper = [0] * len(self.index_document)
            negated = False
            cleaned_tokens = [x for x in tokens if x != 'and']
            results = []
            for token in cleaned_tokens:
                if token == 'not':
                    negated = True
                else:
                    lower += 1
                    relevances = self.calculate_relevance(token, get_tfidf_curr)
                    if negated:
                        negated = False
                        for id, relevance in enumerate(relevances):
                            upper[id] += pow(1 - (1 - relevance), 2)
                    else:
                        for id, relevance in enumerate(relevances):
                            upper[id] += pow(1 - relevance, 2)
            for up in upper:
                results.append(1 - math.sqrt(up / lower))
            return results
        if 'or' in tokens:
            lower = 0
            upper = [0] * len(self.index_document)
            negated = False
            cleaned_tokens = [x for x in tokens if x != 'or']
            results = []
            for token in cleaned_tokens:
                if token == 'not':
                    negated = True
                else:
                    lower += 1
                    relevances = self.calculate_relevance(token, get_tfidf_curr)
                    if negated:
                        negated = False
                        for id, relevance in enumerate(relevances):
                            upper[id] += pow(1 - relevance, 2)
                    else:
                        for id, relevance in enumerate(relevances):
                            upper[id] += pow(relevance, 2)
            for up in upper:
                results.append(math.sqrt(up / lower))
            return results
        else:
            raise Exception("Invalid syntax: boolean operator missing")

    def get_sorted(self, query, num_doc=50, lookup_func='inv'):
        id_relevancy = {}
        message = ""
        try:
            if lookup_func == 'seq':
                relevancy = self.calculate_relevance(query, self.get_tfidf_seq)
            else:
                relevancy = self.calculate_relevance(query, self.get_tfidf)
            for cnt, file_name in enumerate(self.index_document.items()):
                if relevancy[cnt] > 0:
                    id_relevancy[file_name[0]] = relevancy[cnt]
        except Exception as e:
            print(e)
            message = e

        sorted_files = sorted(id_relevancy.items(), key=lambda x: x[1], reverse=True)
        if not message and len(sorted_files) == 0:
            message = "Nothing found, unlucky"
        return sorted_files[:num_doc], message


if __name__ == '__main__':
    vec = TextProcessor()
    experiments.time_query(vec)
