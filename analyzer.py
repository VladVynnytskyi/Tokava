import pandas as pd


def analyze_csv(file_path_or_buffer) -> dict:
    df = pd.read_csv(file_path_or_buffer)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")

    # Normalize column names so OpenAI and Anthropic CSVs both work
    if "project_id" not in df.columns and "workspace_id" in df.columns:
        df["project_id"] = df["workspace_id"]
    if "project_id" not in df.columns:
        df["project_id"] = "unknown"
    if "user_id" not in df.columns:
        df["user_id"] = "unknown"

    total_cost = round(df["cost_usd"].sum(), 4)
    total_requests = len(df)
    total_tokens = int(df["total_tokens"].sum())

    # Cost by model
    by_model = (
        df.groupby("model")["cost_usd"]
        .sum()
        .round(4)
        .sort_values(ascending=False)
        .to_dict()
    )

    # Cost by day
    df["date"] = df["timestamp"].dt.date
    by_day = (
        df.groupby("date")["cost_usd"]
        .sum()
        .round(4)
        .reset_index()
        .assign(date=lambda x: x["date"].astype(str))
        .rename(columns={"cost_usd": "cost"})
        .to_dict(orient="records")
    )

    # Top users by cost
    top_users = (
        df.groupby("user_id")["cost_usd"]
        .sum()
        .round(4)
        .sort_values(ascending=False)
        .head(10)
        .to_dict()
    )

    # Cost by project
    by_project = (
        df.groupby("project_id")["cost_usd"]
        .sum()
        .round(4)
        .sort_values(ascending=False)
        .to_dict()
    )

    # Anomalies: requests with cost > mean + 2*std
    mean_cost = df["cost_usd"].mean()
    std_cost = df["cost_usd"].std()
    threshold = mean_cost + 2 * std_cost
    anomalies = (
        df[df["cost_usd"] > threshold]
        .assign(timestamp=lambda x: x["timestamp"].astype(str))
        .sort_values("cost_usd", ascending=False)
        [["timestamp", "model", "user_id", "project_id", "cost_usd", "total_tokens"]]
        .head(20)
        .to_dict(orient="records")
    )

    # Tokens breakdown (input vs output)
    tokens_by_model = (
        df.groupby("model")[["input_tokens", "output_tokens"]]
        .sum()
        .astype(int)
        .reset_index()
        .to_dict(orient="records")
    )

    return {
        "summary": {
            "total_cost_usd": total_cost,
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "avg_cost_per_request": round(total_cost / total_requests, 6) if total_requests else 0,
            "date_range": {
                "from": str(df["timestamp"].min().date()),
                "to": str(df["timestamp"].max().date()),
            },
        },
        "by_model": by_model,
        "by_day": by_day,
        "by_project": by_project,
        "top_users": top_users,
        "tokens_by_model": tokens_by_model,
        "anomalies": anomalies,
    }
