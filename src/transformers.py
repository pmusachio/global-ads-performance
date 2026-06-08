"""Custom scikit-learn components shared by training, the API and the dashboard.

These classes must live in a single importable module so that `joblib` can
locate them when unpickling the saved pipelines (training, serving and the
notebook all import from here).
"""
import numpy as np
from scipy.optimize import curve_fit
from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin


class AdstockTransformer(BaseEstimator, TransformerMixin):
    """Applies a geometric adstock (carryover) decay to a spend series.

    Each day's effective spend is its raw spend plus a decayed share of the
    previous day's effective spend: `effective[t] = spend[t] + decay_rate * effective[t-1]`.
    """

    def __init__(self, decay_rate: float = 0.3):
        self.decay_rate = decay_rate

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        out = np.zeros_like(X)
        out[0] = X[0]
        for i in range(1, X.shape[0]):
            out[i] = X[i] + self.decay_rate * out[i - 1]
        return out


class SaturationRegressor(BaseEstimator, RegressorMixin):
    """Fits a diminishing-returns curve `revenue = L * (1 - exp(-k * spend))`.

    `L` is the asymptotic revenue ceiling and `k` controls how quickly the
    channel saturates. Parameters are estimated with `scipy.optimize.curve_fit`.
    """

    def __init__(self, L_init: float = 1.0, k_init: float = 0.001):
        self.L_init = L_init
        self.k_init = k_init

    @staticmethod
    def _saturation_curve(spend, L, k):
        return L * (1 - np.exp(-k * spend))

    def fit(self, X, y):
        x = np.asarray(X).ravel()
        y = np.asarray(y).ravel()
        try:
            (L, k), _ = curve_fit(
                self._saturation_curve, x, y,
                p0=[self.L_init, self.k_init],
                bounds=([0, 0], [np.inf, np.inf]),
                maxfev=10000,
            )
            self.L_, self.k_ = L, k
        except RuntimeError:
            self.L_ = float(np.max(y) * 1.2)
            self.k_ = 1e-4
        return self

    def predict(self, X):
        x = np.asarray(X).ravel()
        return self._saturation_curve(x, self.L_, self.k_)


def saturation_curve(spend, L, k):
    """Standalone version of the saturation curve, used outside of pipelines
    (e.g. by the budget optimizer and the dashboard plots)."""
    return L * (1 - np.exp(-k * spend))
