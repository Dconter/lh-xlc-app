import streamlit as st
import pandas as pd
import os

# ---- 配置页面 ----
st.set_page_config(layout="wide", page_title="商品管理系统")

# ---- 数据文件路径 ----
CSV_FILE = "123.csv"

# ---- 加载数据函数 ----
def load_data(filepath):
    if not os.path.exists(filepath):
        return pd.DataFrame(columns=['类别', '物品', '单位', '价格（元）', '备注'])
    try:
        df = pd.read_csv(filepath)
        # 确保列名正确，如果CSV文件中的列名与代码中的不完全一致，需要调整
        # 例如，如果CSV 中的列名是 "Price (Yuan)"，你需要在这里映射
        # df = df.rename(columns={'Price (Yuan)': '价格（元）'})
        return df
    except Exception as e:
        st.error(f"读取CSV文件时出错: {e}")
        return pd.DataFrame(columns=['类别', '物品', '单位', '价格（元）', '备注'])

# ---- 保存数据函数 ----
def save_data(df, filepath):
    try:
        df.to_csv(filepath, index=False)
        st.success("数据已成功保存！")
    except Exception as e:
        st.error(f"保存CSV文件时出错: {e}")

# ---- 主应用逻辑 ----
def main():
    st.title("商品信息管理系统")
    st.write("这是一个简单的网页应用，用于查看和编辑 `123.csv` 中的商品信息。")

    # 重新加载数据
    df = load_data(CSV_FILE)

    # ---- 数据展示与编辑区 ----
    st.subheader("商品列表")

    # 使用 st.data_editor 进行交互式编辑
    # st.data_editor 提供了内置的编辑功能，包括添加、删除、修改行
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",  # 允许动态添加/删除行
        column_order=("类别", "物品", "单位", "价格（元）", "备注"), # 定义列的顺序
        height=400,
        use_container_width=True
    )

    # ---- 操作按钮 ----
    if st.button("保存更改"):
        # 检查是否有实际的更改
        if not edited_df.equals(df):
            save_data(edited_df, CSV_FILE)
        else:
            st.warning("没有检测到更改，无需保存。")

    # ---- 添加新商品 ----
    st.subheader("添加新商品")
    with st.form("add_item_form"):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            new_category = st.text_input("类别")
        with col2:
            new_item = st.text_input("物品")
        with col3:
            new_unit = st.text_input("单位")
        with col4:
            new_price = st.number_input("价格（元）", min_value=0.0, format="%.2f")
        with col5:
            new_notes = st.text_input("备注")

        submitted = st.form_submit_button("添加")
        if submitted:
            if new_item and new_category: # 至少物品和类别不能为空
                new_row = pd.DataFrame([{
                    '类别': new_category,
                    '物品': new_item,
                    '单位': new_unit,
                    '价格（元）': new_price,
                    '备注': new_notes
                }])
                # 重新加载数据，然后追加新行，再保存
                # 这样做是为了避免并发写入问题（虽然在这里不太可能）
                # 更直接的方式是: updated_df = pd.concat([df, new_row], ignore_index=True)
                # 但为了确保是从最新加载的数据基础上添加，我们重新加载
                current_df = load_data(CSV_FILE)
                updated_df = pd.concat([current_df, new_row], ignore_index=True)
                save_data(updated_df, CSV_FILE)
                st.success(f"商品 '{new_item}' 已添加！请刷新页面查看。") # Streamlit 需要手动刷新才能看到最新数据
            else:
                st.warning("物品和类别是必填项。")

    st.markdown("---")
    st.write("Built with [Streamlit](https://streamlit.io/) and [Pandas](https://pandas.pydata.org/)")

# ---- 运行应用 ----
if __name__ == "__main__":
    main()
