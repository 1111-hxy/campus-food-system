"""
校园食堂美食测评系统
技术栈：Python + Streamlit + Pandas + Matplotlib
开发分工：A同学负责菜品录入&打分、菜品检索查询模块

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
            canteen_name = st.selectbox("🏢 食堂名称", ["鲲园", "泽园"])
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
        if not food_name.strip():
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
# A同学负责模块：菜品检索查询
# ------------------------------
def page_search_food():
    """菜品检索查询页面"""
    st.title("🔍 菜品检索查询")
    st.markdown("---")
    
    # 获取数据
    df = read_data()
    
    # 搜索条件区域
    st.subheader("📋 搜索条件")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_canteen = st.selectbox("🏢 食堂名称", ["全部", "鲲园", "泽园"])
    with col2:
        search_food = st.text_input("🍱 菜品名称", placeholder="输入菜品名称关键词")
    with col3:
        taste_filter = st.selectbox(
            "👅 口味分类",
            ["全部", "减脂", "清淡", "重口", "香辣", "甜口"]
        )
    
    # 评分筛选
    rating_min, rating_max = st.slider(
        "⭐ 评分范围",
        min_value=1,
        max_value=5,
        value=(1, 5),
        step=1
    )
    
    # 价格筛选
    price_min, price_max = st.slider(
        "💰 价格范围（元）",
        min_value=0.0,
        max_value=50.0,
        value=(0.0, 50.0),
        step=0.5,
        format="%.2f"
    )
    
    # 搜索按钮
    search_button = st.button("🔍 开始搜索")
    
    # 执行搜索
    if search_button or search_canteen != "全部" or search_food or taste_filter != "全部":
        # 应用筛选条件
        filtered_df = df.copy()
        
        # 食堂名称筛选
        if search_canteen != "全部":
            filtered_df = filtered_df[filtered_df['食堂名称'] == search_canteen]
        
        # 菜品名称筛选
        if search_food.strip():
            filtered_df = filtered_df[filtered_df['菜品名称'].str.contains(search_food.strip(), case=False)]
        
        # 口味分类筛选
        if taste_filter != "全部":
            filtered_df = filtered_df[filtered_df['口味分类'] == taste_filter]
        
        # 评分范围筛选
        filtered_df = filtered_df[(filtered_df['评分'] >= rating_min) & (filtered_df['评分'] <= rating_max)]
        
        # 价格范围筛选
        filtered_df = filtered_df[(filtered_df['价格'] >= price_min) & (filtered_df['价格'] <= price_max)]
        
        # 显示结果
        st.markdown("---")
        st.subheader("📊 搜索结果")
        
        if filtered_df.empty:
            st.warning("😔 未找到符合条件的菜品")
        else:
            st.success(f"🎉 找到 {len(filtered_df)} 条记录")
            
            # 显示数据表格
            st.dataframe(
                filtered_df[['食堂名称', '菜品名称', '口味分类', '价格', '评分', '评论', '录入时间']],
                use_container_width=True,
                column_config={
                    '食堂名称': st.column_config.TextColumn('🏢 食堂名称'),
                    '菜品名称': st.column_config.TextColumn('🍱 菜品名称'),
                    '口味分类': st.column_config.TextColumn('👅 口味分类'),
                    '价格': st.column_config.NumberColumn('💰 价格（元）', format="%.2f"),
                    '评分': st.column_config.NumberColumn('⭐ 评分'),
                    '评论': st.column_config.TextColumn('💬 评论'),
                    '录入时间': st.column_config.TextColumn('📅 录入时间')
                }
            )
            
            # 显示详细信息卡片
            st.markdown("---")
            st.subheader("🗂️ 菜品详情")
            
            for _, row in filtered_df.iterrows():
                with st.expander(f"🍽️ {row['菜品名称']} - {row['食堂名称']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**食堂**: {row['食堂名称']}")
                        st.write(f"**口味**: {row['口味分类']}")
                        st.write(f"**价格**: ¥{row['价格']:.2f}")
                        st.write(f"**评分**: {'⭐' * int(row['评分'])} ({row['评分']}分)")
                    with col2:
                        st.write(f"**录入时间**: {row['录入时间']}")
                        if row['评论']:
                            st.write(f"**评论**: {row['评论']}")
                        else:
                            st.write(f"**评论**: 暂无")

def page_ranking():
    """热度排行页面"""
    st.title("🏆 热度排行")
    st.markdown("---")
    
    # 获取数据
    df = read_data()
    
    if df.empty:
        st.warning("😔 暂无数据，请先添加菜品评价！")
        return
    
    # 热度统计选项
    ranking_type = st.radio(
        "📊 选择排行类型",
        ["按食堂热度", "按菜品热度", "按口味热度", "按评分排行"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if ranking_type == "按食堂热度":
        # 统计各食堂的菜品数量和平均评分
        canteen_stats = df.groupby('食堂名称').agg({
            '菜品名称': 'count',
            '评分': 'mean',
            '价格': 'mean'
        }).round(2)
        canteen_stats.columns = ['菜品数量', '平均评分', '平均价格']
        canteen_stats = canteen_stats.sort_values('菜品数量', ascending=False)
        
        # 显示统计表格
        st.subheader("🏢 食堂热度排行榜")
        st.dataframe(
            canteen_stats,
            use_container_width=True
        )
        
        # 绘制柱状图
        fig, ax = plt.subplots(figsize=(10, 6))
        canteen_stats['菜品数量'].plot(kind='bar', ax=ax, color='#FF6B6B')
        ax.set_title('各食堂菜品数量统计', fontsize=16, fontweight='bold')
        ax.set_xlabel('食堂名称', fontsize=12)
        ax.set_ylabel('菜品数量', fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        
    elif ranking_type == "按菜品热度":
        # 显示所有菜品评分排行
        food_stats = df.groupby(['食堂名称', '菜品名称']).agg({
            '评分': ['mean', 'count'],
            '价格': 'first',
            '口味分类': 'first'
        }).round(2)
        food_stats.columns = ['平均评分', '评价次数', '价格', '口味']
        food_stats = food_stats.sort_values('平均评分', ascending=False)
        
        st.subheader("🍽️ 菜品评分排行榜")
        st.dataframe(
            food_stats,
            use_container_width=True
        )
        
        # 绘制评分排行图
        top_foods = food_stats.head(10)
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = plt.cm.RdYlGn([score/5 for score in top_foods['平均评分']])
        bars = ax.barh(range(len(top_foods)), top_foods['平均评分'], color=colors)
        ax.set_yticks(range(len(top_foods)))
        ax.set_yticklabels([f"{idx[0]}-{idx[1][:10]}" for idx in top_foods.index])
        ax.set_xlabel('评分', fontsize=12)
        ax.set_title('Top 10 菜品评分排行', fontsize=16, fontweight='bold')
        ax.invert_yaxis()
        for i, (bar, score) in enumerate(zip(bars, top_foods['平均评分'])):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'{score:.1f}', va='center', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)
        
    elif ranking_type == "按口味热度":
        # 统计各口味的菜品数量
        taste_stats = df.groupby('口味分类').agg({
            '菜品名称': 'count',
            '评分': 'mean',
            '价格': 'mean'
        }).round(2)
        taste_stats.columns = ['菜品数量', '平均评分', '平均价格']
        taste_stats = taste_stats.sort_values('菜品数量', ascending=False)
        
        st.subheader("👅 口味热度排行榜")
        st.dataframe(
            taste_stats,
            use_container_width=True
        )
        
        # 绘制饼图
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # 口味数量饼图
        colors = ['#FF9999', '#FFCC99', '#99FF99', '#9999FF', '#FF99FF']
        axes[0].pie(taste_stats['菜品数量'], labels=taste_stats.index, autopct='%1.1f%%', 
                    colors=colors[:len(taste_stats)], startangle=90)
        axes[0].set_title('口味分布占比', fontsize=14, fontweight='bold')
        
        # 口味平均评分柱状图
        taste_stats['平均评分'].plot(kind='bar', ax=axes[1], color='#4ECDC4')
        axes[1].set_title('各口味平均评分', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('口味', fontsize=12)
        axes[1].set_ylabel('平均评分', fontsize=12)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        st.pyplot(fig)
        
    else:  # 按评分排行
        # 最高评分菜品
        top_rated = df.nlargest(10, '评分')
        
        st.subheader("⭐ 高分菜品TOP10")
        
        # 显示详细卡片
        cols = st.columns(2)
        for idx, (_, row) in enumerate(top_rated.iterrows()):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FFF4E6, #FFE4E1); 
                            padding: 15px; border-radius: 10px; margin: 5px 0;">
                    <h4>🍽️ {row['菜品名称']}</h4>
                    <p><strong>🏢 食堂：</strong>{row['食堂名称']}</p>
                    <p><strong>⭐ 评分：</strong>{'⭐' * int(row['评分'])} ({row['评分']}分)</p>
                    <p><strong>👅 口味：</strong>{row['口味分类']}</p>
                    <p><strong>💰 价格：</strong>¥{row['价格']:.2f}</p>
                    <p><strong>📅 时间：</strong>{row['录入时间']}</p>
                </div>
                """, unsafe_allow_html=True)

def page_visualization():
    """数据可视化页面"""
    st.title("📊 数据可视化")
    st.markdown("---")
    
    # 获取数据
    df = read_data()
    
    if df.empty:
        st.warning("😔 暂无数据，请先添加菜品评价！")
        return
    
    # 可视化类型选择
    viz_type = st.selectbox(
        "📈 选择可视化类型",
        ["口味分布", "价格分布", "评分分布", "食堂对比", "综合分析"]
    )
    
    st.markdown("---")
    
    if viz_type == "口味分布":
        st.subheader("👅 口味分类统计")
        
        # 计算各口味数量
        taste_counts = df['口味分类'].value_counts()
        
        # 绘制饼图
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        wedges, texts, autotexts = ax.pie(
            taste_counts.values, 
            labels=taste_counts.index,
            autopct='%1.1f%%',
            colors=colors[:len(taste_counts)],
            explode=[0.05] * len(taste_counts),
            shadow=True,
            startangle=90
        )
        ax.set_title('口味分类分布图', fontsize=16, fontweight='bold')
        
        # 美化标签
        for text in texts:
            text.set_fontsize(12)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # 显示统计表格
        st.markdown("### 📋 口味统计详情")
        taste_df = pd.DataFrame({
            '口味': taste_counts.index,
            '数量': taste_counts.values,
            '占比': (taste_counts.values / taste_counts.sum() * 100).round(2).astype(str) + '%'
        })
        st.dataframe(taste_df, use_container_width=True, hide_index=True)
        
    elif viz_type == "价格分布":
        st.subheader("💰 价格区间统计")
        
        # 创建价格区间
        price_bins = [0, 5, 10, 15, 20, 30, 50]
        price_labels = ['0-5元', '5-10元', '10-15元', '15-20元', '20-30元', '30-50元']
        df['价格区间'] = pd.cut(df['价格'], bins=price_bins, labels=price_labels, include_lowest=True)
        price_distribution = df['价格区间'].value_counts().sort_index()
        
        # 绘制柱状图
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(price_distribution.index, price_distribution.values, 
                     color='#3498DB', edgecolor='white', linewidth=2)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_xlabel('价格区间', fontsize=12)
        ax.set_ylabel('菜品数量', fontsize=12)
        ax.set_title('价格区间分布图', fontsize=16, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        # 价格统计信息
        st.markdown("### 📊 价格统计信息")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("平均价格", f"¥{df['价格'].mean():.2f}")
        with col2:
            st.metric("最低价格", f"¥{df['价格'].min():.2f}")
        with col3:
            st.metric("最高价格", f"¥{df['价格'].max():.2f}")
        with col4:
            st.metric("价格中位数", f"¥{df['价格'].median():.2f}")
        
    elif viz_type == "评分分布":
        st.subheader("⭐ 评分分布统计")
        
        # 评分统计
        rating_counts = df['评分'].value_counts().sort_index()
        
        # 绘制柱状图
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#E74C3C', '#E67E22', '#F39C12', '#2ECC71', '#27AE60']
        bars = ax.bar(rating_counts.index, rating_counts.values, color=colors, edgecolor='white', linewidth=2)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_xlabel('评分（分）', fontsize=12)
        ax.set_ylabel('菜品数量', fontsize=12)
        ax.set_title('评分分布图', fontsize=16, fontweight='bold')
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        # 评分统计信息
        st.markdown("### 📊 评分统计信息")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("平均评分", f"{df['评分'].mean():.2f} ⭐")
        with col2:
            st.metric("最高评分", f"{df['评分'].max()} ⭐")
        with col3:
            st.metric("最低评分", f"{df['评分'].min()} ⭐")
            
    elif viz_type == "食堂对比":
        st.subheader("🏢 食堂对比分析")
        
        # 各食堂统计
        canteen_stats = df.groupby('食堂名称').agg({
            '菜品名称': 'count',
            '评分': 'mean',
            '价格': 'mean'
        }).round(2)
        canteen_stats.columns = ['菜品数量', '平均评分', '平均价格']
        canteen_stats = canteen_stats.sort_values('菜品数量', ascending=False)
        
        # 绘制对比图
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # 菜品数量对比
        canteen_stats['菜品数量'].plot(kind='bar', ax=axes[0], color='#FF6B6B', edgecolor='white')
        axes[0].set_title('各食堂菜品数量', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('食堂名称', fontsize=11)
        axes[0].set_ylabel('数量', fontsize=11)
        axes[0].tick_params(axis='x', rotation=45)
        
        # 平均评分对比
        canteen_stats['平均评分'].plot(kind='bar', ax=axes[1], color='#4ECDC4', edgecolor='white')
        axes[1].set_title('各食堂平均评分', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('食堂名称', fontsize=11)
        axes[1].set_ylabel('评分', fontsize=11)
        axes[1].tick_params(axis='x', rotation=45)
        
        # 平均价格对比
        canteen_stats['平均价格'].plot(kind='bar', ax=axes[2], color='#45B7D1', edgecolor='white')
        axes[2].set_title('各食堂平均价格', fontsize=14, fontweight='bold')
        axes[2].set_xlabel('食堂名称', fontsize=11)
        axes[2].set_ylabel('价格（元）', fontsize=11)
        axes[2].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # 显示统计表格
        st.markdown("### 📋 食堂统计详情")
        st.dataframe(canteen_stats, use_container_width=True)
        
    else:  # 综合分析
        st.subheader("📊 综合数据分析")
        
        # 创建综合图表
        fig = plt.figure(figsize=(14, 10))
        
        # 口味与评分关系
        ax1 = fig.add_subplot(2, 2, 1)
        taste_rating = df.groupby('口味分类')['评分'].mean().sort_values(ascending=False)
        taste_rating.plot(kind='bar', ax=ax1, color='#9B59B6')
        ax1.set_title('各口味平均评分', fontsize=12, fontweight='bold')
        ax1.set_xlabel('口味', fontsize=10)
        ax1.set_ylabel('平均评分', fontsize=10)
        ax1.tick_params(axis='x', rotation=45)
        
        # 价格与评分关系散点图
        ax2 = fig.add_subplot(2, 2, 2)
        scatter = ax2.scatter(df['价格'], df['评分'], c=df['评分'], 
                            cmap='RdYlGn', s=100, alpha=0.7, edgecolors='white')
        ax2.set_title('价格与评分关系', fontsize=12, fontweight='bold')
        ax2.set_xlabel('价格（元）', fontsize=10)
        ax2.set_ylabel('评分', fontsize=10)
        plt.colorbar(scatter, ax=ax2, label='评分')
        
        # 每月评价趋势（如果有日期数据）
        ax3 = fig.add_subplot(2, 2, 3)
        df['月份'] = pd.to_datetime(df['录入时间']).dt.to_period('M')
        monthly_counts = df.groupby('月份').size()
        monthly_counts.plot(kind='line', ax=ax3, marker='o', color='#E74C3C', linewidth=2)
        ax3.set_title('月度评价趋势', fontsize=12, fontweight='bold')
        ax3.set_xlabel('月份', fontsize=10)
        ax3.set_ylabel('评价数量', fontsize=10)
        ax3.grid(alpha=0.3)
        
        # 综合评分雷达图（简化版）
        ax4 = fig.add_subplot(2, 2, 4)
        categories = ['口味多样性', '性价比', '平均评分', '评价数量']
        # 计算各项指标（归一化）
        taste_diversity = len(df['口味分类'].unique()) / 5
        cost_performance = 1 - (df['价格'].mean() - df['价格'].min()) / (df['价格'].max() - df['价格'].min() + 0.01)
        avg_rating = df['评分'].mean() / 5
        review_count = min(df.shape[0] / 20, 1)
        
        values = [taste_diversity, cost_performance, avg_rating, review_count]
        colors = plt.cm.Set3([0.2, 0.4, 0.6, 0.8])
        bars = ax4.bar(categories, values, color=colors, edgecolor='white', linewidth=2)
        ax4.set_title('综合指标分析', fontsize=12, fontweight='bold')
        ax4.set_ylabel('得分（0-1）', fontsize=10)
        ax4.set_ylim(0, 1.1)
        for bar, value in zip(bars, values):
            ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
                    f'{value:.2f}', ha='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # 显示总体统计
        st.markdown("### 📈 总体统计信息")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("总菜品数", len(df))
        with col2:
            st.metric("总食堂数", df['食堂名称'].nunique())
        with col3:
            st.metric("平均评分", f"{df['评分'].mean():.2f} ⭐")
        with col4:
            st.metric("平均价格", f"¥{df['价格'].mean():.2f}")
        with col5:
            st.metric("口味种类", df['口味分类'].nunique())

def page_recommendation():
    """智能饮食推荐页面"""
    st.title("🤖 智能饮食推荐")
    st.markdown("---")
    
    # 获取数据
    df = read_data()
    
    if df.empty:
        st.warning("😔 暂无数据，请先添加菜品评价！")
        return
    
    # 用户偏好设置
    st.subheader("🎯 设置您的偏好")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        preferred_canteen = st.selectbox("🏢 食堂偏好", ["全部", "鲲园", "泽园"])
    
    with col2:
        preferred_taste = st.selectbox("👅 口味偏好", ["全部", "减脂", "清淡", "重口", "香辣", "甜口"])
    
    with col3:
        price_range = st.selectbox("💰 价格偏好", ["全部", "0-10元", "10-20元", "20元以上"])
    
    # 推荐类型选择
    recommendation_type = st.radio(
        "📊 推荐类型",
        ["智能综合推荐", "高分菜品推荐", "口味匹配推荐", "营养均衡推荐"],
        horizontal=True
    )
    
    # 生成推荐按钮
    if st.button("✨ 生成推荐"):
        # 根据偏好筛选数据
        filtered_df = df.copy()
        
        # 食堂筛选
        if preferred_canteen != "全部":
            filtered_df = filtered_df[filtered_df['食堂名称'] == preferred_canteen]
        
        # 口味筛选
        if preferred_taste != "全部":
            filtered_df = filtered_df[filtered_df['口味分类'] == preferred_taste]
        
        # 价格筛选
        if price_range == "0-10元":
            filtered_df = filtered_df[(filtered_df['价格'] >= 0) & (filtered_df['价格'] <= 10)]
        elif price_range == "10-20元":
            filtered_df = filtered_df[(filtered_df['价格'] > 10) & (filtered_df['价格'] <= 20)]
        elif price_range == "20元以上":
            filtered_df = filtered_df[filtered_df['价格'] > 20]
        
        if filtered_df.empty:
            st.warning("� 未找到符合您偏好的菜品，请调整筛选条件！")
            return
        
        st.markdown("---")
        
        if recommendation_type == "智能综合推荐":
            # 综合评分 = 评分 * 0.6 + 价格优惠度 * 0.4
            # 价格优惠度：价格越低越好，归一化处理
            max_price = filtered_df['价格'].max()
            min_price = filtered_df['价格'].min()
            price_range_val = max_price - min_price if max_price != min_price else 1
            
            filtered_df['综合评分'] = (
                filtered_df['评分'] * 0.6 + 
                ((max_price - filtered_df['价格']) / price_range_val) * 0.4
            ).round(2)
            
            recommendations = filtered_df.sort_values('综合评分', ascending=False).head(5)
            
            st.subheader("🌟 智能综合推荐")
            st.markdown("**推荐算法**: 综合考虑评分（60%权重）和性价比（40%权重）")
            
            # 展示推荐卡片
            cols = st.columns(2)
            for idx, (_, row) in enumerate(recommendations.iterrows()):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #E8F5E9, #E3F2FD); 
                                padding: 15px; border-radius: 10px; margin: 10px 0;
                                border-left: 4px solid #4CAF50;">
                        <h4>🍽️ {row['菜品名称']}</h4>
                        <p><strong>🏢 食堂：</strong>{row['食堂名称']}</p>
                        <p><strong>👅 口味：</strong>{row['口味分类']}</p>
                        <p><strong>💰 价格：</strong>¥{row['价格']:.2f}</p>
                        <p><strong>⭐ 评分：</strong>{row['评分']}分</p>
                        <p><strong>📊 综合得分：</strong>{row['综合评分']:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        elif recommendation_type == "高分菜品推荐":
            # 按评分排序，推荐评分最高的菜品
            recommendations = filtered_df.sort_values('评分', ascending=False).head(5)
            
            st.subheader("⭐ 高分菜品推荐")
            st.markdown("**推荐算法**: 按用户评分从高到低排序")
            
            # 展示推荐卡片
            cols = st.columns(2)
            for idx, (_, row) in enumerate(recommendations.iterrows()):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FFF3E0, #FFECB3); 
                                padding: 15px; border-radius: 10px; margin: 10px 0;
                                border-left: 4px solid #FF9800;">
                        <h4>🍽️ {row['菜品名称']}</h4>
                        <p><strong>🏢 食堂：</strong>{row['食堂名称']}</p>
                        <p><strong>👅 口味：</strong>{row['口味分类']}</p>
                        <p><strong>💰 价格：</strong>¥{row['价格']:.2f}</p>
                        <p><strong>⭐ 评分：</strong>{'⭐' * int(row['评分'])} ({row['评分']}分)</p>
                        <p><strong>💬 评论：</strong>{row['评论'][:30]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        elif recommendation_type == "口味匹配推荐":
            # 根据口味偏好推荐
            if preferred_taste != "全部":
                taste_recommendations = filtered_df.sort_values('评分', ascending=False).head(5)
                st.subheader(f"👅 {preferred_taste}口味推荐")
            else:
                # 如果没有选择口味，展示各口味代表菜品
                taste_recommendations = []
                for taste in ["减脂", "清淡", "重口", "香辣", "甜口"]:
                    taste_df = filtered_df[filtered_df['口味分类'] == taste]
                    if not taste_df.empty:
                        taste_recommendations.append(taste_df.nlargest(1, '评分').iloc[0])
                
                st.subheader("👅 多样口味推荐")
            
            # 展示推荐卡片
            cols = st.columns(2)
            for idx, row in enumerate(taste_recommendations):
                if isinstance(row, pd.Series):
                    with cols[idx % 2]:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #F3E5F5, #E1BEE7); 
                                    padding: 15px; border-radius: 10px; margin: 10px 0;
                                    border-left: 4px solid #9C27B0;">
                            <h4>🍽️ {row['菜品名称']}</h4>
                            <p><strong>🏢 食堂：</strong>{row['食堂名称']}</p>
                            <p><strong>👅 口味：</strong>{row['口味分类']}</p>
                            <p><strong>💰 价格：</strong>¥{row['价格']:.2f}</p>
                            <p><strong>⭐ 评分：</strong>{row['评分']}分</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        elif recommendation_type == "营养均衡推荐":
            # 营养均衡推荐：推荐不同口味的搭配
            # 推荐策略：减脂+清淡（健康）、重口+香辣（过瘾）、甜口（甜点）
            
            st.subheader("🥗 营养均衡推荐")
            st.markdown("**推荐算法**: 根据营养搭配原则推荐组合菜品")
            
            # 组合推荐
            combinations = [
                {"name": "健康减脂套餐", "tastes": ["减脂", "清淡"]},
                {"name": "风味过瘾套餐", "tastes": ["重口", "香辣"]},
                {"name": "甜蜜下午茶", "tastes": ["甜口"]},
                {"name": "均衡营养套餐", "tastes": ["清淡", "减脂", "甜口"]}
            ]
            
            for combo in combinations:
                with st.expander(f"🍱 {combo['name']}"):
                    combo_items = []
                    for taste in combo['tastes']:
                        taste_df = filtered_df[filtered_df['口味分类'] == taste]
                        if not taste_df.empty:
                            combo_items.append(taste_df.nlargest(1, '评分').iloc[0])
                    
                    if combo_items:
                        total_price = sum(item['价格'] for item in combo_items)
                        avg_rating = sum(item['评分'] for item in combo_items) / len(combo_items)
                        
                        for item in combo_items:
                            st.markdown(f"""
                            <div style="display: flex; align-items: center; gap: 15px; padding: 10px; background: #F8FAFC; border-radius: 8px; margin: 5px 0;">
                                <span style="font-size: 24px;">🍽️</span>
                                <div>
                                    <strong>{item['菜品名称']}</strong> - {item['食堂名称']}
                                    <br>
                                    <span style="color: #666; font-size: 13px;">
                                        👅 {item['口味分类']} | 💰 ¥{item['价格']:.2f} | ⭐ {item['评分']}分
                                    </span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div style="text-align: right; padding: 10px; margin-top: 10px; background: #E8F5E9; border-radius: 8px;">
                            <strong>套餐总价：</strong>¥{total_price:.2f} | 
                            <strong>平均评分：</strong>{avg_rating:.1f}⭐
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("暂无符合条件的菜品")
        
        # 今日推荐小贴士
        st.markdown("---")
        st.subheader("💡 今日饮食小贴士")
        
        tips = [
            "🥛 早餐建议选择清淡或减脂类菜品，营养均衡更健康",
            "🍚 午餐可以适当选择重口味，补充能量迎接下午课程",
            "🍎 晚餐建议清淡为主，减轻肠胃负担",
            "💧 用餐前后记得多喝水，保持身体水分",
            "🥗 搭配不同口味的菜品，让营养更均衡",
            "⏰ 按时就餐，养成良好的饮食习惯"
        ]
        
        import random
        st.success(random.choice(tips))

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
