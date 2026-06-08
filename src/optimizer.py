"""Budget allocation optimizer shared by the API and the dashboard.

Given the saturation parameters (L, k) learned for each channel, finds the
spend allocation that maximizes total predicted revenue subject to a total
budget cap, a minimum global ROAS, and per-channel share bounds.
"""
from typing import Dict, List

import numpy as np
from scipy.optimize import minimize

from src.transformers import saturation_curve


def optimize_allocation(
    channel_params: Dict[str, Dict[str, float]],
    total_budget: float,
    min_roas: float,
    min_share: float = 0.10,
    max_share: float = 0.60,
):
    """Solves the budget allocation problem with SLSQP.

    Args:
        channel_params: mapping of channel name -> {"L": ..., "k": ...}.
        total_budget: total daily budget available to allocate.
        min_roas: minimum acceptable global ROAS (revenue / spend).
        min_share / max_share: fraction of the total budget each channel must
            receive at minimum / maximum.

    Returns:
        A dict describing the optimization outcome (`success`, allocation,
        estimated revenue/spend/ROAS), regardless of whether SLSQP converged.
    """
    channels: List[str] = list(channel_params.keys())

    def objective(allocation):
        total_revenue = 0.0
        for i, channel in enumerate(channels):
            p = channel_params[channel]
            total_revenue += saturation_curve(allocation[i], p["L"], p["k"])
        return -total_revenue

    bounds = tuple((total_budget * min_share, total_budget * max_share) for _ in channels)
    constraints = [
        {"type": "ineq", "fun": lambda x: total_budget - np.sum(x)},
        {"type": "ineq", "fun": lambda x: -objective(x) - min_roas * np.sum(x)},
    ]
    initial_guess = [total_budget / len(channels)] * len(channels)

    result = minimize(
        objective, initial_guess, method="SLSQP", bounds=bounds, constraints=constraints
    )

    if not result.success:
        return {"success": False, "message": "Optimization failed to converge under the given constraints."}

    allocation = result.x
    spend = float(np.sum(allocation))
    revenue = float(-result.fun)
    return {
        "success": True,
        "allocation": dict(zip(channels, [round(float(a), 2) for a in allocation])),
        "estimated_revenue": round(revenue, 2),
        "estimated_spend": round(spend, 2),
        "estimated_roas": round(revenue / spend, 2) if spend > 0 else 0.0,
    }
