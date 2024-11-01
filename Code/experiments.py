import random
import time

import matplotlib.pyplot as plt
import numpy as np

import lemmatization


def query_generator(term_num, all_dict, was_sub):
    query = random.choice(list(all_dict.keys()))

    or_and = 0
    operator = ''
    if or_and:
        operator = ' and'
    else:
        operator = ' or'
    query += operator
    term_num -= 1
    while term_num > 0:
        is_sub = random.randint(0, 1)
        is_negated = random.randint(0, 1)
        if is_sub:
            term_num, whatever = query_generator(term_num, all_dict, True)
            if is_negated:
                curr_addition = ' not (' + whatever + ')'
            else:
                curr_addition = ' (' + whatever + ')'
        else:
            term_num -= 1
            if is_negated:
                curr_addition = ' not ' + random.choice(list(all_dict.keys()))
            else:
                curr_addition = ' ' + random.choice(list(all_dict.keys()))
        query += curr_addition
        query += operator
        if was_sub:
            if random.randint(0, 1):
                break
    query = query.rsplit(' ', 1)[0]
    return term_num, query


def time_preprocess(processor):
    execution_times_seq = []
    execution_times_inv = []
    doc_number = []
    min_length = 10
    max_length = 303
    step = 25
    for length in range(min_length, max_length + 1, step):
        print('Doing', length, 'documents')
        term_dict, doc_dict = processor.get_uniq_terms_experiment(length)
        index_document = processor.index_documents_experiment(length)

        start_time_inv = time.time()
        processor.tfidf_term_experiment(index_document, term_dict, doc_dict)
        end_time_inv = time.time()
        execution_time_ms_inv = (end_time_inv - start_time_inv) * 1000
        execution_times_inv.append(execution_time_ms_inv)

        start_time_seq = time.time()
        processor.tfidf_term_seq_experiment(index_document, doc_dict, term_dict)
        end_time_seq = time.time()
        execution_time_ms_seq = (end_time_seq - start_time_seq) * 1000
        doc_number.append(length)
        execution_times_seq.append(execution_time_ms_seq)
        print('Documents', length, 'done')
    plt.plot(doc_number, execution_times_seq, label='seq')
    plt.plot(doc_number, execution_times_inv, label='inv')
    plt.xlabel('Number of document')
    plt.ylabel('Time (ms)')
    plt.title('Execution Time vs Number of documents')
    plt.grid(True)
    plt.legend()
    plt.savefig('execution_time_vs_documents_number2.png')
    plt.show()


def time_query_documents():
    document_lengths = []
    execution_times_seq_fin = []
    execution_times_inv_fin = []

    min_length1 = 50
    max_length1 = 450
    step1 = 50

    for length1 in range(min_length1, max_length1 + 1, step1):
        processor = lemmatization.TextProcessor(size=length1)

        query_lengths = []
        execution_times_seq = []
        execution_times_inv = []
        min_length2 = 2
        max_length2 = 100
        step2 = 25
        print('Doing', length1, 'documents')
        for length2 in range(min_length2, max_length2 + 1, step2):
            query = query_generator(length2, processor.all_dict, False)[1]
            print('Doing:', length2, 'queries')
            start_time_seq = time.time()
            sorted_query_seq = processor.get_sorted(query, 'seq')
            end_time_seq = time.time()
            execution_time_ms_seq = (end_time_seq - start_time_seq) * 1000
            query_lengths.append(length2)
            execution_times_seq.append(execution_time_ms_seq)

            start_time_inv = time.time()
            sorted_query_inv = processor.get_sorted(query, 'inv')
            end_time_inv = time.time()
            execution_time_ms_inv = (end_time_inv - start_time_inv) * 1000
            execution_times_inv.append(execution_time_ms_inv)
            print('Queries', length2, 'done')

        execution_times_inv_fin.append(execution_times_inv)
        execution_times_seq_fin.append(execution_times_seq)
        document_lengths.append(length1)
        print('Documents', length1, 'done')
    execution_times_seq_arr = np.array(execution_times_seq_fin)
    execution_times_inv_arr = np.array(execution_times_inv_fin)

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.imshow(execution_times_seq_arr, cmap='viridis', origin='lower', aspect='auto')
    plt.colorbar(label='Execution Time (ms)')
    plt.xlabel('Query Length')
    plt.ylabel('Document Length')
    plt.title('Sequential Processing')
    plt.xticks(range(len(query_lengths)), query_lengths)
    plt.yticks(range(len(document_lengths)), document_lengths)

    plt.subplot(2, 1, 2)
    plt.imshow(execution_times_inv_arr, cmap='viridis', origin='lower', aspect='auto')
    plt.colorbar(label='Execution Time (ms)')
    plt.xlabel('Query Length')
    plt.ylabel('Document Length')
    plt.title('Inverted Processing')
    plt.xticks(range(len(query_lengths)), query_lengths)
    plt.yticks(range(len(document_lengths)), document_lengths)

    plt.tight_layout()
    plt.savefig('execution_times_plot4.png')
    plt.show()


def time_query(processor):
    query_lengths = []
    execution_times_seq = []
    execution_times_inv = []

    min_length = 2
    max_length = 500
    step = 10

    for length in range(min_length, max_length + 1, step):
        query = query_generator(length, processor.all_dict, False)[1]
        print('Doing:', length, 'queries')
        start_time_seq = time.time()
        sorted_query_seq = processor.get_sorted(query, lookup_func='seq')
        end_time_seq = time.time()
        execution_time_ms_seq = (end_time_seq - start_time_seq) * 1000
        query_lengths.append(length)
        execution_times_seq.append(execution_time_ms_seq)

        start_time_inv = time.time()
        sorted_query_inv = processor.get_sorted(query, lookup_func='inv')
        end_time_inv = time.time()
        execution_time_ms_inv = (end_time_inv - start_time_inv) * 1000
        execution_times_inv.append(execution_time_ms_inv)
        print('Queries', length, 'done')

    plt.plot(query_lengths, execution_times_seq, label='seq')
    plt.plot(query_lengths, execution_times_inv, label='inv')
    plt.xlabel('Length of Query')
    plt.ylabel('Time (ms)')
    plt.title('Execution Time vs Query Length (random queries without sub-queries)')
    plt.grid(True)
    plt.legend()
    plt.savefig('execution_time_vs_query_length_both_random_query.png')
    plt.show()
