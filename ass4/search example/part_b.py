"""Run the vector comparison experiments for Assignment 4."""

from pathlib import Path
from inverted_index import InvertedIndex
from utils import read_data


QUERY = "scotland kings and thanes"
WEIGHTINGS = ["TF", "TF-IDF", "Log-Entropy"]
OPERATORS = ["euclidean", "pearson", "spearman", "manhattan"]


def build_index():
    # Locate the Shakespeare collection relative to this module.
    folder = Path(__file__).parent / "shakespeare"
    documents = read_data(str(folder))
    documents.sort()  # Use a repeatable document order.

    index = InvertedIndex()
    for document in documents:
        index.add_document(document)

    print("Documents:", index.get_total_docs())
    print("Vocabulary terms:", index.get_total_terms())
    print("Processed query:", index.process_text(QUERY))
    return index


def run_experiment(index, weighting, comparison):
    use_tfidf = False
    use_log_entropy = False

    if weighting == "TF-IDF":
        use_tfidf = True
        index.calcTFIDF()
    elif weighting == "Log-Entropy":
        use_log_entropy = True
        index.calcLogEntropy()
    elif weighting != "TF":
        raise ValueError("Unknown weighting: " + weighting)

    # Use matching document and query weights.
    index.generate_term_by_doc_matrix(
        tfidf=use_tfidf, log_entropy=use_log_entropy
    )
    results = index.search(
        QUERY,
        tfidf=use_tfidf,
        log_entropy=use_log_entropy,
        comparison=comparison
    )

    print("\n" + weighting + " / " + comparison)
    if comparison == "euclidean" or comparison == "manhattan":
        print("Smaller distance is better.")
    else:
        print("Larger score is better.")

    print(f"{'Rank':<6} {'Document':<40} {'Score':>14}")
    for i in range(min(10, len(results))):
        document = results[i][0]
        score = results[i][1]
        print(f"{i + 1:<6} {document:<40} {score:>14.6f}")

    return results


def run_all_experiments(index):
    # Store full rankings by weighting scheme and operator.
    all_results = {}
    for weighting in WEIGHTINGS:
        for comparison in OPERATORS:
            results = run_experiment(index, weighting, comparison)
            all_results[(weighting, comparison)] = results
    return all_results


def find_rank(results, document_name):
    for i in range(len(results)):
        if results[i][0] == document_name:
            return i + 1
    return None


# Run all twelve comparison experiments.
if __name__ == "__main__":
    index = build_index()
    run_all_experiments(index)
