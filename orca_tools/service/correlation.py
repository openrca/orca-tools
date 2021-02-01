import pandas as pd


class CorrelationMatrix:

    def __init__(self, results):
        self._results = results

    def compute(self):
        data = {result[0]: result[2] for result in self._results}
        cols = [result[0] for result in self._results]

        df = pd.DataFrame(data, columns=cols)

        corr_matrix = df.corr(method='pearson')

        indexes = list(corr_matrix.index)
        for ix in indexes:
            for iy in indexes:
                corr_val = corr_matrix.at[ix, iy]
                if corr_val > 0.90 or corr_val < -0.90:
                    continue
                corr_matrix.at[ix, iy] = 0

        return corr_matrix
