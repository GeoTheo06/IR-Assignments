# Retrieval Evaluation

## 1. Experimental setup

To evaluate the performance of different web search engines, we used Google's top search results as our pseudo-ground truth (baseline) relevance set $R$, containing $\vert{}R\vert{} = 7$ relevant documents for each query. We evaluated three target search algorithms—Bing, DuckDuckGo, and Yahoo—against this baseline across two distinct search query caches (`query1_cache` and `query2_cache`).

**Result Extraction**: For a target search engine, the top $N$ retrieved URLs ($S$) are fetched from the respective JSON cache files ($N=20$ for Bing and DuckDuckGo; $N=5$ for Yahoo).

## 2. Precision and recall

For a retrieved result set $A$ and relevance set $R$, precision and recall are

$$
P = \frac{|A \cap R|}{|A|}, \qquad
R = \frac{|A \cap R|}{|R|}.
$$

Precision measures the fraction of retrieved documents that occur in the Google baseline. Recall measures the fraction of the seven Google baseline documents retrieved by an engine. Alternative URLs for the same underlying page are treated as different documents.

## 3. Single-valued summaries

The F-measure is the harmonic mean of precision and recall:

$$
F = \frac{2PR}{P + R}.
$$

It is zero when both precision and recall are zero and it is high only if both are high. Precision at rank $k$ is

$$
P@k = \frac{|A_k \cap R|}{|A_k|},
$$

where $A_k$ contains the available results within the first $k$ ranks. If an engine returns fewer than $k$ results, the denominator is the number of available results. This ensures that precision is calculated using only the results actually returned by the search engine. We did not use $k$ as the denominator for a shorter list because that would treat ranking positions that were not returned as non-relevant documents.

## 4. Scalar results

### Query 1: Modern Information Retrieval

| Engine | Precision | Recall | F | P@5 | P@7 | P@10 |
|---|---:|---:|---:|---:|---:|---:|
| Google (baseline) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Bing | 0.15 | 0.43 | 0.22 | 0.20 | 0.29 | 0.30 |
| DuckDuckGo | 0.10 | 0.29 | 0.15 | 0.40 | 0.29 | 0.20 |
| Yahoo | 0.20 | 0.14 | 0.17 | 0.20 | 0.20 | 0.20 |

Bing obtains the highest recall and F-measure among the three evaluated engines. It finds three of the seven Google documents, although those matches form only 15% of its twenty returned results. DuckDuckGo has the strongest P@5, showing that its matching results occur particularly early, but it finds only two Google documents overall. Yahoo has the highest overall precision, but this is based on a short list of five results containing only one Google document. Its low recall makes it weaker when coverage is important.

### Query 2: information retrieval evaluation

| Engine | Precision | Recall | F | P@5 | P@7 | P@10 |
|---|---:|---:|---:|---:|---:|---:|
| Google (baseline) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Bing | 0.20 | 0.57 | 0.30 | 0.20 | 0.29 | 0.20 |
| DuckDuckGo | 0.20 | 0.57 | 0.30 | 0.20 | 0.14 | 0.20 |
| Yahoo | 0.20 | 0.14 | 0.17 | 0.20 | 0.20 | 0.20 |

Bing and DuckDuckGo have identical overall precision, recall, F-measure, P@5, and P@10. Each retrieves four of the seven baseline documents within its twenty-result list. Bing has the better P@7, however, because two matching documents occur within its first seven positions while DuckDuckGo has only one. Yahoo again returns five results and only one Google document, so it has the same precision as the other engines but much lower recall and F-measure.

Google's precision, recall, F-measure, P@5, P@7, and P@10 are 1.00 because it is the benchmark.

## 5. 11-point interpolation

Standard recall levels are evaluated at 11 fixed thresholds $r \in \{0.0, 0.1, 0.2, \dots, 1.0\}$. The interpolated precision $P_{\text{interp}}(r)$ at recall level $r$ is defined as the maximum precision achieved at any recall level $r' \ge r$:

$$P_{\text{interp}}(r) = \max_{r' \ge r} P(r')$$

## 6. Results and plot interpretation

### Query 1 (`query1_cache`)

* **Google (Baseline)**: Acts as the ground truth reference ($P = 1.0, R = 1.0$). Its 11-point interpolated precision curve remains flat at $1.0$ across all recall levels $0.0 \le r \le 1.0$.
* **Bing**: Achieves an overall precision of $0.15$ and a maximum recall of $0.43$ (retrieving 3 out of 7 baseline documents).

* *Plot Behavior*: The first relevant document appears at rank 1 ($P = 1.0, R \approx 0.143$). Consequently, $P_{\text{interp}}(r) = 1.0$ for $r \in [0.0, 0.1]$, $0.333$ for $r \in [0.2, 0.4]$, and $0.0$ for $r \ge 0.5$.

* **DuckDuckGo**: Reaches an overall precision of $0.10$ and maximum recall of $0.29$ (2 out of 7 baseline documents).

* *Plot Behavior*: Finds its first match at rank 1 ($P = 1.0, R \approx 0.143$). Interpolated precision is $1.0$ for $r \in [0.0, 0.1]$, drops to $0.4$ at $r = 0.2$, and falls to $0.0$ for $r \ge 0.3$.

* **Yahoo**: Retrieves 5 total results, returning 1 baseline match ($P = 0.20, R = 0.14$).

* *Plot Behavior*: The relevant document appears at rank 3, so $P_{\text{interp}}(r) = 0.333$ for $r \in [0.0, 0.1]$, dropping to $0.0$ for all $r \ge 0.2$.

![Query 1 - Google](<plots/Precision_vs_Recall_plot_for_google_ranking_(query1_cache)_considering_Google_search_as_the_baseline.png>)

![Query 1 - Bing](<plots/Precision_vs_Recall_plot_for_bing_ranking_(query1_cache)_considering_Google_search_as_the_baseline.png>)

![Query 1 - DuckDuckGo](<plots/Precision_vs_Recall_plot_for_duckduckgo_ranking_(query1_cache)_considering_Google_search_as_the_baseline.png>)

![Query 1 - Yahoo](<plots/Precision_vs_Recall_plot_for_yahoo_ranking_(query1_cache)_considering_Google_search_as_the_baseline.png>)

### Query 2 (`query2_cache`)

* **Bing & DuckDuckGo**: Both algorithms achieve higher overlap with Google's baseline on Query 2, reaching a maximum recall of $0.57$ (4 out of 7 baseline documents) and an overall precision of $0.20$.

* *Plot Behavior*: Both graphs stay above zero up to a recall of 0.5. After $r = 0.6$, the line drops straight to 0.0 because neither search engine found the last 3 Google baseline results.

* **Yahoo**: Produces 1 matching result out of 5 retrieved documents ($P = 0.20, R = 0.14$), starts with a flat line at $0.20$ for $r \in [0.0, 0.1]$ before dropping to $0.0$.

![Query 2 - Google](<plots/Precision_vs_Recall_plot_for_google_ranking_(query2_cache)_considering_Google_search_as_the_baseline.png>)

![Query 2 - Bing](<plots/Precision_vs_Recall_plot_for_bing_ranking_(query2_cache)_considering_Google_search_as_the_baseline.png>)

![Query 2 - DuckDuckGo](<plots/Precision_vs_Recall_plot_for_duckduckgo_ranking_(query2_cache)_considering_Google_search_as_the_baseline.png>)

![Query 2 - Yahoo](<plots/Precision_vs_Recall_plot_for_yahoo_ranking_(query2_cache)_considering_Google_search_as_the_baseline.png>)

## 7. Boundary cases and special considerations

1. **Interpolation at $r = 0.0$**:
* According to standard Information Retrieval evaluation conventions, $P_{\text{interp}}(0.0)$ represents the maximum precision observed across *all* recall levels $r' \ge 0.0$. This ensures that algorithms finding relevant documents early in the ranking are rewarded with higher starting precision values.

2. **Unreached Recall Levels ($r > R_{\text{max}}$)**:
* When a search engine fails to achieve high recall levels (e.g., $r \ge 0.6$ for Bing on Query 2), no retrieved points satisfy the condition $r' \ge r$. In our implementation, `precisions` evaluates to an empty list, which safely defaults to $P_{\text{interp}}(r) = 0.0$.

3. **Monotonic Non-Increasing Property**:
* The 11-point interpolated precision curve is guaranteed to be non-increasing ($P_{\text{interp}}(r_a) \ge P_{\text{interp}}(r_b)$ for $r_a < r_b$). The empirical plots confirm this behavior across all algorithms and queries.
