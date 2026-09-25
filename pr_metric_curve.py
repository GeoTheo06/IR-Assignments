import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt


class PRCurveEvaluator:
    @staticmethod
    def calculate_11_point_precision(retrieved_docs, relevant_docs, precision_recall_func):
        """Computes 11-point interpolated precision using Person 1's PR function."""
        pr_values = []
        for idx, doc in enumerate(retrieved_docs):
            if doc in relevant_docs:
                p, r = precision_recall_func(retrieved_docs[:idx + 1], relevant_docs)
                pr_values.append((p, r))

        r_levels = [round(x, 1) for x in np.linspace(0.0, 1.0, 11).tolist()]
        p_values = []

        for r_level in r_levels:
            precisions = [p for p, r in pr_values if r >= r_level]
            p_interp = max(precisions) if precisions else 0.0
            p_values.append(p_interp)

        return r_levels, p_values

    @staticmethod
    def plot_curve(p_values, r_values, plt_title=None):
        """Generates and saves the precision vs recall plot."""
        plt.figure(figsize=(7, 5))
        plt.plot(r_values, p_values, marker='o', linestyle='-', color='b', label='11-pt Interpolated Precision')
        if plt_title:
            plt.title(plt_title)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        
        plots_dir = Path('plots')
        plots_dir.mkdir(parents=True, exist_ok=True)

        if plt_title:
            filename = plt_title.replace('\n', ' ').replace(':', ' -').replace('/', '-').replace('?', '').replace(' ', '_')
            plt.savefig(plots_dir / f'{filename}.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()