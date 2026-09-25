# Retrieval Evaluation Report

## 1. Experimental setup

We evaluated Google, Bing, DuckDuckGo, and Yahoo for two queries:

- Query 1: `Modern Information Retrieval`
- Query 2: `information retrieval evaluation`

Google's first seven results are used as the relevance baseline. Bing and DuckDuckGo each have twenty retrieved results, while Yahoo has five. A document counts as relevant only when its URL exactly matches a URL in the Google baseline.

## 2. Evaluation metrics

### Precision and recall

For a retrieved set $A$ and relevance set $R$:

$$
P = \frac{|A \cap R|}{|A|}, \qquad
R = \frac{|A \cap R|}{|R|}.
$$

Precision is the fraction of retrieved documents that are relevant. Recall is the fraction of relevant documents that were retrieved.

### Single-valued summaries

The F-measure is the harmonic mean of precision and recall:

$$
F = \frac{2PR}{P + R}.
$$

Precision at rank $k$ is:

$$
P@k = \frac{|A_k \cap R|}{k},
$$

where $A_k$ contains the first $k$ ranks. Missing ranks are considered non-relevant when an engine returns fewer than $k$ results. P@5 and P@10 are required by the assignment. P@7 is also reported because it is included in the starter code.

### 11-point interpolated precision–recall

The standard recall levels are $0.0, 0.1, \ldots, 1.0$. At each standard recall level $r_j$, interpolated precision is the highest precision observed at any recall value greater than or equal to $r_j$:

$$
P_{interp}(r_j) = \max_{r \ge r_j} P(r).
$$

If an engine does not reach a recall level, its interpolated precision at that level is zero.

## 3. Scalar results

### Query 1: Modern Information Retrieval

| Engine | Precision | Recall | F | P@5 | P@7 | P@10 |
|---|---:|---:|---:|---:|---:|---:|
| Google (baseline) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.70 |
| Bing | 0.15 | 0.43 | 0.22 | 0.20 | 0.29 | 0.30 |
| DuckDuckGo | 0.10 | 0.29 | 0.15 | 0.40 | 0.29 | 0.20 |
| Yahoo | 0.20 | 0.14 | 0.17 | 0.20 | 0.14 | 0.10 |

Bing has the highest recall and F-measure among the three engines being compared. It finds three of the seven Google documents. DuckDuckGo has the strongest P@5 because both of its matches occur within its first five results. Yahoo has the highest overall precision, but this is based on a short list of five results containing only one Google document, so its recall is low.

### Query 2: information retrieval evaluation

| Engine | Precision | Recall | F | P@5 | P@7 | P@10 |
|---|---:|---:|---:|---:|---:|---:|
| Google (baseline) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.70 |
| Bing | 0.20 | 0.57 | 0.30 | 0.20 | 0.29 | 0.20 |
| DuckDuckGo | 0.20 | 0.57 | 0.30 | 0.20 | 0.14 | 0.20 |
| Yahoo | 0.20 | 0.14 | 0.17 | 0.20 | 0.14 | 0.10 |

Bing and DuckDuckGo have the same overall precision, recall, F-measure, P@5, and P@10. Each finds four of the seven Google documents. Bing has the better P@7 because two matching documents occur within its first seven positions, while DuckDuckGo has one. Yahoo again finds only one Google document and therefore has much lower recall and F-measure.

Google's precision, recall, and F-measure are 1.00 because Google defines the relevance baseline. Its P@10 is 0.70 because only seven Google results are loaded and the three missing ranks count as non-relevant.

## 4. Precision–recall results

### Query 1

| Engine | 0.0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Google | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Bing | 1.00 | 1.00 | 0.33 | 0.33 | 0.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| DuckDuckGo | 1.00 | 1.00 | 0.40 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Yahoo | 0.33 | 0.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Bing reaches the highest recall of the three compared engines: $3/7 \approx 0.43$. Its curve therefore becomes zero at recall level 0.5. DuckDuckGo reaches $2/7 \approx 0.29$, and Yahoo reaches only $1/7 \approx 0.14$. DuckDuckGo retrieves both matching documents early, which explains its strong precision at the first recall levels despite its lower total recall.

### Query 2

| Engine | 0.0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Google | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Bing | 0.29 | 0.29 | 0.29 | 0.29 | 0.29 | 0.29 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| DuckDuckGo | 0.33 | 0.33 | 0.27 | 0.27 | 0.27 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Yahoo | 0.20 | 0.20 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Bing and DuckDuckGo both reach $4/7 \approx 0.57$ recall, so their curves become zero at recall level 0.6. DuckDuckGo starts with higher interpolated precision, while Bing maintains approximately 0.29 through recall level 0.5. Yahoo again reaches only about 0.14 recall.

The interpolated curves are non-increasing because each point uses the maximum precision available at that recall level or any higher recall level. The generated figures are stored in the `plots` directory.
