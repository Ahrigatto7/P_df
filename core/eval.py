import pandas as pd


def evaluate_search(model_search_fn, test_set):
    """Evaluate a search function with a test set."""
    records = []
    for item in test_set:
        pred = model_search_fn(item["question"])
        is_correct = item["gold_answer"] in pred["answer"]
        records.append(
            {
                "질문": item["question"],
                "정답": item["gold_answer"],
                "모델답": pred["answer"],
                "정답여부": int(is_correct),
            }
        )
    df = pd.DataFrame(records)
    acc = df["정답여부"].mean()
    return df, acc


# Streamlit 평가 UI 예시

def render_eval_ui():
    import streamlit as st

    test_set = [
        {"question": "OOO 규칙은?", "gold_answer": "정답1"},
        # ...
    ]

    from .vector_ops import hybrid_search

    def search_fn(q: str):
        return hybrid_search(q)

    df, acc = evaluate_search(search_fn, test_set)
    st.write(df)
    st.write(f"정확도: {acc:.2%}")
    st.bar_chart(df["정답여부"])

