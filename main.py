"""
校园食堂美食测评系统
技术栈：Python + Streamlit + Pandas + Matplotlib
开发分工：A同学负责菜品录入&打分模块

注意：本文件仅包含公共基础代码和菜品录入打分模块，
其他功能（菜品检索、热度排行、数据可视化、智能推荐）由B同学开发。
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# ------------------------------
# Matplotlib 中文配置
# ------------------------------
def config_matplotlib():
    """配置Matplotlib，解决中文显示和负号乱码问题"""
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.family'] = 'sans-serif'

# 初始化Matplotlib配置
config_matplotlib()

# ------------------------------
# 数据文件操作函数
# ------------------------------
DATA_FILE = 'food_data.csv'
COLUMNS = ['食堂名称', '菜品名称', '口味分类', '价格', '评分', '评论', '录入时间']

def init_data_file():
    """初始化数据文件，若不存在则创建"""
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

def read_data():
    """读取CSV数据"""
    init_data_file()
    return pd.read_csv(DATA_FILE, encoding='utf-8-sig')

def save_data(df):
    """保存数据到CSV"""
    df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

def add_food_record(data):
    """追加一条菜品记录"""
    df = read_data()
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)

# ------------------------------
# 页面布局函数
# ------------------------------
def sidebar():
    """侧边栏导航"""
    st.sidebar.title("🍽️ 校园食堂美食测评")
    st.sidebar.markdown("---")
    
    # 所有菜单选项（保留完整菜单）
    menu = st.sidebar.radio(
        "功能菜单",
        [
            "菜品录入&打分",
            "菜品检索查询",
            "热度排行",
            "数据可视化",
            "智能饮食推荐"
        ]
    )
    
    return menu

# ------------------------------
# A同学负责模块：菜品录入&打分
# ------------------------------
def page_add_food():
    """菜品录入&打分页面"""
    st.title("📝 菜品录入&打分")
    st.markdown("---")
    
    # 表单输入
    with st.form(key='food_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            canteen_name = st.text_input("🏢 食堂名称", placeholder="请输入食堂名称")
            food_name = st.text_input("🍱 菜品名称", placeholder="请输入菜品名称")
        
        with col2:
            taste_category = st.selectbox(
                "👅 口味分类",
                ["减脂", "清淡", "重口", "香辣", "甜口"]
            )
            price = st.number_input("💰 价格（元）", min_value=0.0, step=0.5, format="%.2f")
        
        # 评分滑动条
        rating = st.slider("⭐ 综合评分", min_value=1, max_value=5, value=3, step=1)
        
        # 评论输入
        comment = st.text_area("💬 菜品评价", placeholder="请输入您对这道菜品的评价...", height=100)
        
        # 提交按钮
        submit_button = st.form_submit_button("✅ 提交评价")
    
    # 提交逻辑
    if submit_button:
        # 校验必填项
        if not canteen_name.strip():
            st.warning("⚠️ 请输入食堂名称！")
        elif not food_name.strip():
            st.warning("⚠️ 请输入菜品名称！")
        else:
            # 组装数据
            record = {
                '食堂名称': canteen_name.strip(),
                '菜品名称': food_name.strip(),
                '口味分类': taste_category,
                '价格': price,
                '评分': rating,
                '评论': comment.strip(),
                '录入时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 保存数据
            add_food_record(record)
            
            # 成功提示
            st.success("🎉 菜品评价提交成功！感谢您的测评~")
            
            # 显示提交的数据
            st.markdown("---")
            st.subheader("📋 您提交的评价")
            st.write(f"**食堂**: {record['食堂名称']}")
            st.write(f"**菜品**: {record['菜品名称']}")
            st.write(f"**口味**: {record['口味分类']}")
            st.write(f"**价格**: ¥{record['价格']:.2f}")
            st.write(f"**评分**: {'⭐' * record['评分']} ({record['评分']}分)")
            if record['评论']:
                st.write(f"**评价**: {record['评论']}")

# ------------------------------
# B同学负责模块（仅保留入口）
# ------------------------------
def page_search_food():
    """菜品检索查询（B同学开发）"""
    st.title("🔍 菜品检索查询")
    st.markdown("---")
    st.info("📌 此功能由B同学负责开发，敬请期待~")

def page_ranking():
    """热度排行（B同学开发）"""
    st.title("🏆 热度排行")
    st.markdown("---")
    st.info("📌 此功能由B同学负责开发，敬请期待~")

def page_visualization():
    """数据可视化（B同学开发）"""
    st.title("📊 数据可视化")
    st.markdown("---")
    st.info("📌 此功能由B同学负责开发，敬请期待~")

def page_recommendation():
    """智能饮食推荐（B同学开发）"""
    st.title("🤖 智能饮食推荐")
    st.markdown("---")
    st.info("📌 此功能由B同学负责开发，敬请期待~")

# ------------------------------
# 主函数
# ------------------------------
def main():
    """主程序入口"""
    # 页面配置
    st.set_page_config(
        page_title="校园食堂美食测评系统",
        page_icon="🍽️",
        layout="wide"
    )
    
    # 页面标题
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="font-size: 32px; color: #E74C3C;">🍽️ 校园食堂美食测评系统</h1>
        <p style="color: #7F8C8D;">发现校园里的美味，记录每一次味蕾的感动</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化数据文件
    init_data_file()
    
    # 侧边栏导航
    menu = sidebar()
    
    # 根据菜单选择显示对应页面
    if menu == "菜品录入&打分":
        page_add_food()
    elif menu == "菜品检索查询":
        page_search_food()
    elif menu == "热度排行":
        page_ranking()
    elif menu == "数据可视化":
        page_visualization()
    elif menu == "智能饮食推荐":
        page_recommendation()

if __name__ == "__main__":
    main()
