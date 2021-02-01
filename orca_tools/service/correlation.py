import pandas as pd


class CorrelationMatrix:

    def __init__(self, results, corr_threshold=0.9):
        self._results = results
        self._corr_threshold = corr_threshold

    def compute(self):
        data = {result[0]: result[2] for result in self._results}
        cols = [result[0] for result in self._results]

        df = pd.DataFrame(data, columns=cols)

        corr_matrix = df.corr(method='pearson')

        indexes = list(corr_matrix.index)
        for ix in indexes:
            for iy in indexes:
                corr_val = corr_matrix.at[ix, iy]
                if abs(corr_val) < self._corr_threshold:
                    corr_matrix.at[ix, iy] = 0
        return corr_matrix
