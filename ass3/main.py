import json

from pprint import pprint
from pathlib import Path

from pr_metric_curve import PRCurveEvaluator


def get_search_results(algo, dir="query1_cache", top_n=20):
    def get_ranking(cache_file):
        if cache_file.exists():
            with open(cache_file) as f:
                result = json.load(f)
        else:
            raise FileNotFoundError(f'Cache file {cache_file} not found')

        # Considering only the top_n rankings of the results
        _ranking = [x['link'] for x in result['organic_results']]
        return _ranking

    cache_dir = Path(f'{dir}')
    cache_dir.mkdir(parents=True, exist_ok=True)

    cache_file_path = cache_dir.joinpath(f'{algo}.json')
    ranking = get_ranking(cache_file_path)[:top_n]
    print(f'Number of search results: {len(ranking)}')
    pprint(ranking)

    return ranking


def precision_recall(retrieved_docs, relevant_docs):
    relevant_retrieved = 0

    for doc in retrieved_docs:
        if doc in relevant_docs:
            relevant_retrieved += 1

    if len(retrieved_docs) == 0:
        precision = 0
    else:
        precision = relevant_retrieved / len(retrieved_docs)

    if len(relevant_docs) == 0:
        recall = 0
    else:
        recall = relevant_retrieved / len(relevant_docs)

    return precision, recall


def precision_at_11_standard_recall_levels(retrieved_docs, relevant_docs):
    return PRCurveEvaluator.calculate_11_point_precision(
        retrieved_docs,
        relevant_docs,
        precision_recall
    )


def plot_precision_vs_recall_curve(p_values, r_values, plt_title=None):
    PRCurveEvaluator.plot_curve(p_values, r_values, plt_title)


def f_metric(retrieved_docs, relevant_docs):
    precision, recall = precision_recall(retrieved_docs, relevant_docs)

    if precision + recall == 0:
        return 0

    return 2 * precision * recall / (precision + recall)


def precision_at_k(retrieved_docs, relevant_docs, k):
    if k <= 0:
        return 0

    top_k_docs = retrieved_docs[:k]

    if len(top_k_docs) == 0:
        return 0

    relevant_in_top_k = 0

    for doc in top_k_docs:
        if doc in relevant_docs:
            relevant_in_top_k += 1

    return relevant_in_top_k / len(top_k_docs)


def p_at_5(retrieved_docs, relevant_docs):
    return precision_at_k(retrieved_docs, relevant_docs, 5)


def p_at_7(retrieved_docs, relevant_docs):
    return precision_at_k(retrieved_docs, relevant_docs, 7)


def p_at_10(retrieved_docs, relevant_docs):
    return precision_at_k(retrieved_docs, relevant_docs, 10)


def run_all_parts(dir):
    search_results = {
        'google': get_search_results('google', dir, top_n=7),
        'bing': get_search_results('bing', dir, top_n=20),
        'duckduckgo': get_search_results('duckduckgo', dir, top_n=20),
        'yahoo': get_search_results('yahoo', dir, top_n=20)
    }

    # Use Google's results as the relevance baseline.
    relevant_docs = set(search_results['google'])

    print('\nThe precision and recall scores for the various search algorithms with Google search as the baseline:')
    for ranking_name, retrieved_docs in search_results.items():
        precision, recall = precision_recall(retrieved_docs, relevant_docs)
        print(f'{ranking_name.ljust(11)} ranking  ==>  precision: {round(precision, 2)} '
              f'\t recall: {round(recall, 2)}')

    print('\nPlotting precision vs recall plots')
    for ranking_name, retrieved_docs in search_results.items():
        r_values, p_values = precision_at_11_standard_recall_levels(
            retrieved_docs,
            relevant_docs
        )
        plot_title = (f'Precision vs Recall plot for {ranking_name} ranking ({dir})\n'
                      f'considering Google search as the baseline')
        plot_precision_vs_recall_curve(p_values, r_values, plot_title)

    print('\nComputing the single valued summaries')
    for ranking_name, retrieved_docs in search_results.items():
        f_score = f_metric(retrieved_docs, relevant_docs)
        p_at_5_score = p_at_5(retrieved_docs, relevant_docs)
        p_at_7_score = p_at_7(retrieved_docs, relevant_docs)
        p_at_10_score = p_at_10(retrieved_docs, relevant_docs)

        print(f'{ranking_name.ljust(11)}   ==>  f: {round(f_score, 2)} '
              f'\t p@5: {round(p_at_5_score, 2)} '
              f'\t p@7: {round(p_at_7_score, 2)} '
              f'\t p@10: {round(p_at_10_score, 2)}')


if __name__ == '__main__':
    print('Running for query1_cache')
    run_all_parts(dir='query1_cache')
    print('\nRunning for query2_cache')
    run_all_parts(dir='query2_cache')
