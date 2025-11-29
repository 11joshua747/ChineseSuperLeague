import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 1. 加载模型和scaler（用绝对路径）
model_path = r'E:\miniconda\ChineseSuperLeague\logistic_regression_model.pkl'
scaler_path = r'E:\miniconda\ChineseSuperLeague\scaler.pkl'

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    st.success("✅ 模型和scaler加载成功！")
except FileNotFoundError as e:
    st.error(f"❌ 文件未找到：{e}")
    st.warning("请先运行07_logistic_regression.ipynb保存模型和scaler")
except Exception as e:
    st.error(f"❌ 加载失败：{e}")

# 2. 网页标题和说明
st.title("中超比赛主胜预测")
st.markdown("### 输入球队近期数据，预测是否主胜")

# 3. 用户输入界面（匹配你的特征名：home_last3_goals/away_last3_concede/home_last2_loss）
st.sidebar.header("输入特征")
home_last3_goals = st.sidebar.slider("主队近3场进球数", 0, 10, 3)
away_last3_concede = st.sidebar.slider("客队近3场失球数", 0, 10, 2)
home_last2_loss = st.sidebar.slider("主队近2场连败数", 0, 2, 0)

# 4. 整理输入数据（特征名必须和训练时一致！）
input_data = pd.DataFrame({
    'home_last3_goals': [home_last3_goals],
    'away_last3_concede': [away_last3_concede],
    'home_last2_loss': [home_last2_loss]
})

# 5. 标准化+预测
if st.button("开始预测"):
    try:
        # 标准化
        input_scaled = scaler.transform(input_data)
        # 预测
        prediction = model.predict(input_scaled)[0]
        prediction_proba = model.predict_proba(input_scaled)[0]
        
        # 结果展示
        st.subheader("预测结果：")
        if prediction == 1:
            st.success(f"主胜！概率：{prediction_proba[1]:.2%}")
        else:
            st.error(f"非主胜（平局/客胜）！主胜概率：{prediction_proba[1]:.2%}")
        
        # 概率分布
        st.subheader("概率分布")
        prob_df = pd.DataFrame({
            '结果': ['非主胜', '主胜'],
            '概率': prediction_proba
        })
        st.bar_chart(prob_df.set_index('结果'))
        
        # 输入数据展示
        st.subheader("输入数据")
        st.dataframe(input_data)
    except Exception as e:
        st.error(f"预测失败：{e}")