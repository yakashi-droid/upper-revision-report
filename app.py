import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="上方修正予測レポート",
    layout="wide"
)

st.title("📈 上方修正予測レポート")

st.markdown(
    f"""
    **生成日時**：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}  
    **対象**：上方修正率60%以上 & 修正3回以上
    """
)

st.divider()

data = [
    ["2026-01-20", 6557, "ＡＩＡＩグループ", "2026-01-30", 10, "金曜", 1.00, 3, 0],
    ["2026-01-20", 8362, "福井銀行", "2026-02-03", 14, "月曜", 0.67, 2, 1],
    ["2026-01-21", 9267, "Genky Drugstores", "2026-01-27", 6, "木曜", 1.00, 2, 0],
    ["2026-01-22", 6023, "ダイハツインフィニアース", "2026-01-29", 7, "金曜", 1.00, 5, 0],
    ["2026-01-23", 4800, "オリコン", "2026-02-05", 13, "金曜", 0.67, 2, 1],
]

columns = [
    "date", "code", "name", "earnings_date",
    "days_before", "weekday", "up_rate",
    "up_count", "down_count"
]

df = pd.DataFrame(data, columns=columns)

df["total_revision"] = df["up_count"] + df["down_count"]

filtered = df[
    (df["up_rate"] >= 0.6) &
    (df["total_revision"] >= 3)
].copy()

filtered["上方率"] = (filtered["up_rate"] * 100).astype(int).astype(str) + "%"
filtered["修正履歴"] = filtered["up_count"].astype(str) + "↑ / " + filtered["down_count"].astype(str) + "↓"

display_df = filtered[
    [
        "date",
        "code",
        "name",
        "earnings_date",
        "days_before",
        "weekday",
        "上方率",
        "修正履歴"
    ]
].rename(columns={
    "date": "予測日",
    "code": "コード",
    "name": "銘柄名",
    "earnings_date": "決算発表日",
    "days_before": "何日前",
    "weekday": "出やすい曜日"
})

def highlight_up_rate(val):
    if val == "100%":
        return "background-color:#ffb3b3"
    elif int(val.replace("%", "")) >= 75:
        return "background-color:#ffd9b3"
    else:
        return ""

styled_df = display_df.style.applymap(
    highlight_up_rate,
    subset=["上方率"]
)

st.subheader("🔥 今後7日間に修正が出そうな銘柄")
st.dataframe(styled_df, use_container_width=True)
