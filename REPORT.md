## Experimental Setup & Precision-vs-Recall Evaluation

### 1. Experimental Setup

To evaluate the performance of different web search engines, we used Google's top search results as our pseudo-ground truth (baseline) relevance set $R$, containing $\vert{}R\vert{} = 7$ relevant documents for each query. We evaluated three target search algorithms—Bing, DuckDuckGo, and Yahoo—against this baseline across two distinct search query caches (`query1_cache` and `query2_cache`).

The evaluation pipeline performs the following steps:

1. **Result Extraction**: For a target search engine, the top $N$ retrieved URLs ($S$) are fetched from the respective JSON cache files ($N=20$ for Bing and DuckDuckGo; $N=5$ for Yahoo).
2. **Precision & Recall Calculation**: For any prefix cutoff $k$, Precision ($P_k$) and Recall ($R_k$) are computed as:

$$P_k = \frac{\vert{}S_k \cap R\vert{}}{\vert{}S_k\vert{}}, \quad R_k = \frac{\vert{}S_k \cap R\vert{}}{\vert{}R\vert{}}$$


3. **11-Point Interpolation**: Standard recall levels are evaluated at 11 fixed thresholds $r \in \{0.0, 0.1, 0.2, \dots, 1.0\}$. The interpolated precision $P_{\text{interp}}(r)$ at recall level $r$ is defined as the maximum precision achieved at any recall level $r' \ge r$:

$$P_{\text{interp}}(r) = \max_{r' \ge r} P(r')$$



---

### 2. Results & Plot Interpretation

#### Query 1 (`query1_cache`)

* **Google (Baseline)**: Acts as the ground truth reference ($P = 1.0, R = 1.0$). Its 11-point interpolated precision curve remains flat at $1.0$ across all recall levels $0.0 \le r \le 1.0$.
* **Bing**: Achieves a overall precision of $0.15$ and a maximum recall of $0.43$ (retrieving 3 out of 7 baseline documents).


* *Plot Behavior*: The first relevant document appears at rank 7 ($P \approx 0.143, R \approx 0.143$), and the highest precision achieved for recall $\ge 0.143$ is $0.286$ (at rank 7 with 2 matches). Consequently, $P_{\text{interp}}(r) = 0.286$ for $r \in [0.0, 0.4]$, dropping to $0.0$ for $r \ge 0.5$.


* **DuckDuckGo**: Reaches an overall precision of $0.10$ and maximum recall of $0.29$ (2 out of 7 baseline documents).


* *Plot Behavior*: Finds its first match earlier at rank 3 ($P \approx 0.333, R \approx 0.143$). Interpolated precision starts at $0.333$ for $r \in [0.0, 0.1]$, drops to $0.286$ for $r \in [0.2, 0.4]$, and falls to $0.0$ for $r \ge 0.5$.


* **Yahoo**: Retrieves 5 total results, returning 1 baseline match ($P = 0.20, R = 0.14$).


* *Plot Behavior*: $P_{\text{interp}}(r) = 0.20$ for $r \in [0.0, 0.1]$, dropping to $0.0$ for all $r \ge 0.2$.



#### Query 2 (`query2_cache`)

* **Bing & DuckDuckGo**: Both algorithms achieve higher overlap with Google's baseline on Query 2, reaching a maximum recall of $0.57$ (4 out of 7 baseline documents) and an overall precision of $0.20$.


* *Plot Behavior*: Both graphs stay above zero up to a recall of 0.5. After $r = 0.6$, the line drops straight to 0.0 because neither search engine found the last 3 Google baseline results.


* **Yahoo**: Produces 1 matching result out of 5 retrieved documents ($P = 0.20, R = 0.14$), starts with a flat line at $0.20$ for $r \in [0.0, 0.1]$ before dropping to $0.0$.



---

### 3. Boundary Cases & Special Considerations

1. **Interpolation at $r = 0.0$**:
* According to standard Information Retrieval evaluation conventions, $P_{\text{interp}}(0.0)$ represents the maximum precision observed across *all* recall levels $r' \ge 0.0$. This ensures that algorithms finding relevant documents early in the ranking are rewarded with higher starting precision values.


2. **Unreached Recall Levels ($r > R_{\text{max}}$)**:
* When a search engine fails to achieve high recall levels (e.g., $r \ge 0.6$ for Bing on Query 2), no retrieved points satisfy the condition $r' \ge r$. In our implementation, `precisions` evaluates to an empty list, which safely defaults to $P_{\text{interp}}(r) = 0.0$.


3. **Monotonic Non-Increasing Property**:
* The 11-point interpolated precision curve is guaranteed to be non-increasing ($P_{\text{interp}}(r_a) \ge P_{\text{interp}}(r_b)$ for $r_a < r_b$). The empirical plots confirm this behavior across all algorithms and queries.