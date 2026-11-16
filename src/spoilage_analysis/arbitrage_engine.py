"""
AtmoSync - Spoilage Arbitrage Engine

Uses:
1. Avocado degradation report
2. Simulated commodity market data

All market prices, distances and transport costs
are illustrative prototype inputs, not real quotations.
"""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]

DEGRADATION_FILE = (
    ROOT_DIR / "data/processed/avocado_degradation_report.csv"
)

MARKET_FILE = (
    ROOT_DIR / "data/processed/mock_market_data.csv"
)

OUTPUT_FILE = (
    ROOT_DIR / "data/processed/avocado_arbitrage_report.csv"
)


def load_data():
    degradation = pd.read_csv(DEGRADATION_FILE)
    markets = pd.read_csv(MARKET_FILE)

    required_degradation = {
        "container_id",
        "remaining_hours_estimate",
    }

    required_market = {
        "container_id",
        "market_name",
        "market_price_per_kg",
        "distance_km",
        "transit_time_hours",
        "transport_cost_per_kg",
    }

    if not required_degradation.issubset(degradation.columns):
        raise ValueError("Invalid degradation report columns")

    if not required_market.issubset(markets.columns):
        raise ValueError("Invalid market data columns")

    return degradation, markets


def calculate_arbitrage(degradation, markets):

    df = markets.merge(
        degradation[
            ["container_id", "remaining_hours_estimate"]
        ],
        on="container_id",
        how="left",
        validate="many_to_one",
    )

    # Net realization per kg after illustrative transport cost.
    df["net_market_value_per_kg"] = (
        df["market_price_per_kg"]
        - df["transport_cost_per_kg"]
    )

    # Shipment must arrive before estimated remaining time.
    df["time_feasible"] = (
        df["remaining_hours_estimate"].notna()
        & (
            df["transit_time_hours"]
            < df["remaining_hours_estimate"]
        )
    )

    df["eligible_net_value_per_kg"] = np.where(
        df["time_feasible"],
        df["net_market_value_per_kg"],
        np.nan,
    )

    df["recommendation"] = "NOT_FEASIBLE"

    for container_id, indices in df.groupby(
        "container_id"
    ).groups.items():

        eligible = df.loc[indices][
            "eligible_net_value_per_kg"
        ]

        if eligible.notna().any():
            best_index = eligible.idxmax()
            df.loc[best_index, "recommendation"] = (
                "RECOMMENDED"
            )

    return df


def main():

    degradation, markets = load_data()

    report = calculate_arbitrage(
        degradation,
        markets,
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\nATMOSYNC SPOILAGE ARBITRAGE REPORT")
    print("=" * 85)

    print(
        report[
            [
                "container_id",
                "market_name",
                "market_price_per_kg",
                "distance_km",
                "transit_time_hours",
                "remaining_hours_estimate",
                "net_market_value_per_kg",
                "time_feasible",
                "recommendation",
            ]
        ].to_string(index=False)
    )

    print("\nOutput saved:", OUTPUT_FILE)
    print("\nArbitrage analysis completed.")


if __name__ == "__main__":
    main()