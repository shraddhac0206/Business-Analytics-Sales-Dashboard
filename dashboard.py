"""
Business Analytics Dashboard
A comprehensive Streamlit dashboard for analyzing sales performance.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
    <style>
    /* Main styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* KPI Cards */
    .kpi-container {
        background: #ffffff;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    /* Insight boxes */
    .insight-box {
        background: linear-gradient(to right, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem 2rem;
        border-radius: 8px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        font-size: 0.95rem;
        line-height: 1.8;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .insight-box:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .insight-box strong {
        color: #667eea;
        font-weight: 700;
        font-size: 1.05rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    .insight-metric {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0 0.3rem;
    }
    .insight-positive {
        border-left-color: #48bb78;
    }
    .insight-positive strong {
        color: #48bb78;
    }
    .insight-warning {
        border-left-color: #ed8936;
    }
    .insight-warning strong {
        color: #ed8936;
    }
    .insight-critical {
        border-left-color: #f56565;
    }
    .insight-critical strong {
        color: #f56565;
    }
    .insight-recommendation {
        background: #e6fffa;
        border-left-color: #38b2ac;
        margin-top: 0.5rem;
        padding: 1rem 1.5rem;
    }
    .insight-recommendation strong {
        color: #38b2ac;
    }
    .insights-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    .insight-category {
        font-size: 0.85rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    
    /* Section headers */
    h2 {
        color: #2d3748;
        font-weight: 600;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #718096;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        font-weight: 500;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the sales data."""
    try:
        df = pd.read_csv('sales_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M').astype(str)
        df['year_month'] = pd.to_datetime(df['date']).dt.to_period('M')
        return df
    except FileNotFoundError:
        st.error("sales_data.csv not found. Please run generate_sample_data.py first.")
        st.stop()

def calculate_kpis(df):
    """Calculate key performance indicators."""
    total_revenue = df['sales_amount'].sum()
    total_cost = df['cost'].sum()
    total_profit = df['profit'].sum()
    overall_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    return {
        'revenue': total_revenue,
        'cost': total_cost,
        'profit': total_profit,
        'margin': overall_margin,
        'transactions': len(df)
    }

def generate_insights(df, kpis):
    """Generate professional business insights with enhanced structure and recommendations."""
    insights = []
    
    # Overall performance insight
    avg_transaction = kpis['revenue'] / kpis['transactions'] if kpis['transactions'] > 0 else 0
    revenue_millions = kpis['revenue'] / 1000000
    revenue_billions = kpis['revenue'] / 1000000000 if revenue_millions >= 1000 else None
    
    revenue_display = f"${revenue_billions:.2f}B" if revenue_billions else f"${revenue_millions:.2f}M"
    
    insights.append({
        'category': 'EXECUTIVE SUMMARY',
        'title': 'Overall Performance Overview',
        'content': f"The organization generated <span class='insight-metric'>{revenue_display}</span> in total revenue across <span class='insight-metric'>{kpis['transactions']:,} transactions</span>, with an average transaction value of <span class='insight-metric'>${avg_transaction:,.2f}</span>. This represents a solid revenue foundation for the analyzed period.",
        'type': 'info',
        'recommendation': None
    })
    
    # Margin insight with recommendations
    if kpis['margin'] > 35:
        insights.append({
            'category': 'PROFITABILITY',
            'title': 'Strong Financial Performance',
            'content': f"The organization demonstrates exceptional financial health with an overall profit margin of <span class='insight-metric'>{kpis['margin']:.2f}%</span>, which significantly exceeds industry benchmarks. This indicates highly effective cost management and optimal pricing strategies.",
            'type': 'positive',
            'recommendation': 'Maintain current operational excellence. Consider reinvesting excess profits into growth initiatives or market expansion.'
        })
    elif kpis['margin'] > 25:
        insights.append({
            'category': 'PROFITABILITY',
            'title': 'Moderate Profitability Performance',
            'content': f"The current profit margin of <span class='insight-metric'>{kpis['margin']:.2f}%</span> falls within acceptable parameters. There is clear opportunity for improvement through targeted operational efficiency initiatives and strategic pricing adjustments.",
            'type': 'warning',
            'recommendation': 'Focus on cost reduction in high-volume categories, review supplier contracts, and implement dynamic pricing strategies to improve margins by 3-5 percentage points.'
        })
    else:
        insights.append({
            'category': 'PROFITABILITY',
            'title': 'Profitability Improvement Required',
            'content': f"The profit margin of <span class='insight-metric'>{kpis['margin']:.2f}%</span> is below optimal thresholds and requires immediate strategic attention.",
            'type': 'critical',
            'recommendation': 'Urgent action needed: Conduct comprehensive cost analysis, renegotiate supplier contracts, review pricing models, and implement lean operational processes. Target margin improvement of 5-8 percentage points within the next quarter.'
        })
    
    # Monthly trend analysis
    monthly_data = df.groupby('year_month').agg({
        'sales_amount': 'sum',
        'profit': 'sum'
    }).reset_index()
    monthly_data['margin'] = (monthly_data['profit'] / monthly_data['sales_amount'] * 100)
    
    if len(monthly_data) > 1:
        recent_avg = monthly_data['sales_amount'].iloc[-3:].mean()
        previous_avg = monthly_data['sales_amount'].iloc[:-3].mean() if len(monthly_data) > 3 else recent_avg
        recent_trend = recent_avg - previous_avg
        trend_pct = (recent_trend / previous_avg * 100) if previous_avg > 0 else 0
        
        if recent_trend > 0:
            insights.append({
                'category': 'TREND ANALYSIS',
                'title': 'Positive Revenue Growth Trend',
                'content': f"The trailing 3-month average revenue of <span class='insight-metric'>${recent_avg:,.2f}</span> represents a <span class='insight-metric'>{trend_pct:+.1f}%</span> increase (${recent_trend:,.2f}) compared to prior periods, indicating strong positive momentum and successful growth initiatives.",
                'type': 'positive',
                'recommendation': 'Capitalize on growth momentum by scaling successful strategies, increasing marketing investment in high-performing channels, and expanding capacity to meet growing demand.'
            })
        else:
            insights.append({
                'category': 'TREND ANALYSIS',
                'title': 'Revenue Decline Detected',
                'content': f"The trailing 3-month average revenue of <span class='insight-metric'>${recent_avg:,.2f}</span> shows a decline of <span class='insight-metric'>{abs(trend_pct):.1f}%</span> (${abs(recent_trend):,.2f}) compared to previous periods. This trend requires immediate strategic intervention.",
                'type': 'critical',
                'recommendation': 'Conduct comprehensive market analysis, review sales team performance, evaluate marketing ROI, assess competitive landscape, and implement corrective action plans. Consider promotional campaigns or product mix adjustments.'
            })
    
    # Category analysis
    category_performance = df.groupby('product_category').agg({
        'sales_amount': 'sum',
        'profit': 'sum',
        'margin': 'mean'
    }).reset_index()
    category_performance['margin_pct'] = (category_performance['profit'] / category_performance['sales_amount'] * 100)
    
    top_category = category_performance.loc[category_performance['sales_amount'].idxmax()]
    best_margin_category = category_performance.loc[category_performance['margin_pct'].idxmax()]
    worst_margin_category = category_performance.loc[category_performance['margin_pct'].idxmin()]
    category_revenue_pct = (top_category['sales_amount'] / kpis['revenue'] * 100) if kpis['revenue'] > 0 else 0
    
    insights.append({
        'category': 'PRODUCT PORTFOLIO',
        'title': 'Product Category Performance',
        'content': f"The <span class='insight-metric'>{top_category['product_category']}</span> category is the primary revenue driver, generating <span class='insight-metric'>${top_category['sales_amount']:,.2f}</span> ({category_revenue_pct:.1f}% of total revenue). The <span class='insight-metric'>{best_margin_category['product_category']}</span> category demonstrates superior margin performance at {best_margin_category['margin_pct']:.2f}%, while {worst_margin_category['product_category']} shows the lowest margin at {worst_margin_category['margin_pct']:.2f}%.",
        'type': 'info',
        'recommendation': f"Strategic focus: Expand marketing and inventory for {best_margin_category['product_category']} category. Review pricing and cost structure for {worst_margin_category['product_category']} to improve profitability. Diversify revenue sources to reduce dependency on {top_category['product_category']}."
    })
    
    # Regional analysis
    regional_performance = df.groupby('region').agg({
        'sales_amount': 'sum',
        'profit': 'sum'
    }).reset_index()
    regional_performance['margin_pct'] = (regional_performance['profit'] / regional_performance['sales_amount'] * 100)
    regional_performance = regional_performance.sort_values('sales_amount', ascending=False)
    
    top_region = regional_performance.iloc[0]
    bottom_region = regional_performance.iloc[-1]
    region_revenue_pct = (top_region['sales_amount'] / kpis['revenue'] * 100) if kpis['revenue'] > 0 else 0
    
    insights.append({
        'category': 'GEOGRAPHIC PERFORMANCE',
        'title': 'Regional Market Analysis',
        'content': f"The <span class='insight-metric'>{top_region['region']}</span> region is the highest-performing market, contributing <span class='insight-metric'>${top_region['sales_amount']:,.2f}</span> ({region_revenue_pct:.1f}% of total revenue) with a margin of {top_region['margin_pct']:.2f}%. The {bottom_region['region']} region shows the lowest performance at ${bottom_region['sales_amount']:,.2f}.",
        'type': 'info',
        'recommendation': f"Increase investment in {top_region['region']} region to maximize returns. Develop targeted growth strategies for {bottom_region['region']} region, including market research, sales team expansion, and localized marketing campaigns."
    })
    
    # Customer analysis
    customer_performance = df.groupby('customer').agg({
        'sales_amount': 'sum',
        'profit': 'sum'
    }).reset_index()
    customer_performance = customer_performance.sort_values('sales_amount', ascending=False)
    
    top_customer = customer_performance.iloc[0]
    top_10_revenue = customer_performance.head(10)['sales_amount'].sum()
    top_10_pct = (top_10_revenue / kpis['revenue'] * 100) if kpis['revenue'] > 0 else 0
    top_customer_pct = (top_customer['sales_amount'] / kpis['revenue'] * 100) if kpis['revenue'] > 0 else 0
    
    insights.append({
        'category': 'CUSTOMER BASE',
        'title': 'Customer Concentration Analysis',
        'content': f"Customer portfolio analysis reveals that the top customer <span class='insight-metric'>{top_customer['customer']}</span> represents {top_customer_pct:.1f}% of total revenue (<span class='insight-metric'>${top_customer['sales_amount']:,.2f}</span>). The top 10 customers collectively account for <span class='insight-metric'>{top_10_pct:.1f}%</span> of total revenue.",
        'type': 'info' if top_10_pct < 50 else 'warning',
        'recommendation': f"Implement customer retention programs for top accounts. Develop mid-market acquisition strategy to reduce concentration risk. Create customer success programs to increase lifetime value."
    })
    
    if top_10_pct > 50:
        insights.append({
            'category': 'RISK ASSESSMENT',
            'title': 'High Customer Concentration Risk',
            'content': f"Critical risk identified: The top 10 customers represent <span class='insight-metric'>{top_10_pct:.1f}%</span> of total revenue, creating significant vulnerability to customer churn.",
            'type': 'critical',
            'recommendation': 'Immediate action required: Develop comprehensive customer retention strategy, diversify customer base through aggressive mid-market acquisition, implement account management best practices, and create contingency plans for key account loss.'
        })
    
    # Seasonal/Time-based insights
    df_temp = df.copy()
    df_temp['month_name'] = pd.to_datetime(df_temp['date']).dt.month_name()
    monthly_sales = df_temp.groupby('month_name')['sales_amount'].sum().sort_values(ascending=False)
    best_month = monthly_sales.index[0]
    worst_month = monthly_sales.index[-1]
    best_month_revenue = monthly_sales.iloc[0]
    worst_month_revenue = monthly_sales.iloc[-1]
    best_month_pct = (best_month_revenue / kpis['revenue'] * 100) if kpis['revenue'] > 0 else 0
    
    insights.append({
        'category': 'SEASONAL PATTERNS',
        'title': 'Seasonal Performance Patterns',
        'content': f"Analysis reveals that <span class='insight-metric'>{best_month}</span> demonstrates peak sales performance, generating <span class='insight-metric'>${best_month_revenue:,.2f}</span> ({best_month_pct:.1f}% of revenue), while {worst_month} shows the lowest performance at ${worst_month_revenue:,.2f}.",
        'type': 'info',
        'recommendation': f"Optimize inventory and staffing for {best_month} peak period. Develop targeted marketing campaigns for {worst_month} to boost sales. Create seasonal promotions and adjust resource allocation based on these patterns."
    })
    
    return insights

def main():
    """Main dashboard function."""
    # Professional header
    st.markdown("""
        <div class="main-header">
            <h1>Business Analytics Dashboard</h1>
            <p>Comprehensive Sales Performance Analysis & Strategic Insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Data Filters")
    st.sidebar.markdown("---")
    
    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    else:
        df_filtered = df
    
    # Category filter
    categories = ['All'] + sorted(df['product_category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Product Category", categories)
    if selected_category != 'All':
        df_filtered = df_filtered[df_filtered['product_category'] == selected_category]
    
    # Region filter
    regions = ['All'] + sorted(df['region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Region", regions)
    if selected_region != 'All':
        df_filtered = df_filtered[df_filtered['region'] == selected_region]
    
    # Calculate KPIs
    kpis = calculate_kpis(df_filtered)
    
    # Display KPIs with professional styling
    st.header("Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Revenue", f"${kpis['revenue']:,.2f}", delta=None)
    with col2:
        st.metric("Total Profit", f"${kpis['profit']:,.2f}", delta=None)
    with col3:
        st.metric("Profit Margin", f"{kpis['margin']:.2f}%", delta=None)
    with col4:
        st.metric("Total Cost", f"${kpis['cost']:,.2f}", delta=None)
    with col5:
        st.metric("Transactions", f"{kpis['transactions']:,}", delta=None)
    
    st.markdown("---")
    
    # Generate and display insights
    st.header("Strategic Business Insights")
    st.markdown("*Comprehensive automated analysis with actionable recommendations based on current performance data*")
    
    insights = generate_insights(df_filtered, kpis)
    
    # Group insights by category
    categories = {}
    for insight in insights:
        cat = insight['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(insight)
    
    # Display insights with enhanced formatting
    for category, category_insights in categories.items():
        for insight in category_insights:
            insight_class = f"insight-{insight['type']}" if insight['type'] in ['positive', 'warning', 'critical'] else ""
            
            # Build insight HTML as a single clean string
            category_html = f'<div class="insight-category">{insight["category"]}</div>'
            title_html = f'<strong>{insight["title"]}</strong>'
            content_html = f'<div style="margin-top: 0.75rem;">{insight["content"]}</div>'
            insight_html = f'<div class="insight-box {insight_class}">{category_html}{title_html}{content_html}</div>'
            
            st.markdown(insight_html, unsafe_allow_html=True)
            
            if insight['recommendation']:
                rec_html = f'<div class="insight-box insight-recommendation"><strong>Recommended Action</strong><div style="margin-top: 0.5rem;">{insight["recommendation"]}</div></div>'
                st.markdown(rec_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Trend Analysis Section
    st.header("Performance Analysis & Trends")
    
    # Monthly trends
    tab1, tab2, tab3, tab4 = st.tabs(["Monthly Trends", "Product Category Analysis", "Regional Analysis", "Customer Analysis"])
    
    with tab1:
        st.subheader("Monthly Revenue & Profit Trends")
        monthly_data = df_filtered.groupby('year_month').agg({
            'sales_amount': 'sum',
            'profit': 'sum',
            'cost': 'sum'
        }).reset_index()
        monthly_data['margin'] = (monthly_data['profit'] / monthly_data['sales_amount'] * 100)
        monthly_data['year_month'] = monthly_data['year_month'].astype(str)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_data['year_month'],
            y=monthly_data['sales_amount'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#667eea')
        ))
        fig.add_trace(go.Scatter(
            x=monthly_data['year_month'],
            y=monthly_data['profit'],
            mode='lines+markers',
            name='Profit',
            line=dict(color='#48bb78', width=3),
            marker=dict(size=8, color='#48bb78')
        ))
        fig.update_layout(
            title=dict(text="Monthly Revenue and Profit Trends", font=dict(size=18, color='#2d3748')),
            xaxis_title="Period",
            yaxis_title="Amount (USD)",
            hovermode='x unified',
            height=450,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#4a5568'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_margin = px.bar(
                monthly_data,
                x='year_month',
                y='margin',
                title="Monthly Profit Margin",
                labels={'margin': 'Margin (%)', 'year_month': 'Period'},
                color='margin',
                color_continuous_scale='Viridis'
            )
            fig_margin.update_layout(
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif", size=12, color='#4a5568'),
                title_font=dict(size=16, color='#2d3748')
            )
            st.plotly_chart(fig_margin, use_container_width=True)
        
        with col2:
            st.subheader("Monthly Performance Summary")
            monthly_summary = monthly_data.copy()
            monthly_summary.columns = ['Period', 'Revenue ($)', 'Profit ($)', 'Cost ($)', 'Margin (%)']
            monthly_summary = monthly_summary.round(2)
            st.dataframe(
                monthly_summary,
                use_container_width=True,
                hide_index=True
            )
    
    with tab2:
        st.subheader("Product Category Performance Analysis")
        category_data = df_filtered.groupby('product_category').agg({
            'sales_amount': 'sum',
            'profit': 'sum',
            'cost': 'sum'
        }).reset_index()
        category_data['margin'] = (category_data['profit'] / category_data['sales_amount'] * 100)
        category_data = category_data.sort_values('sales_amount', ascending=False)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                category_data,
                x='product_category',
                y='sales_amount',
                title="Revenue by Product Category",
                labels={'sales_amount': 'Revenue (USD)', 'product_category': 'Product Category'},
                color='sales_amount',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                height=450,
                xaxis_tickangle=-45,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif", size=12, color='#4a5568'),
                title_font=dict(size=16, color='#2d3748')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                category_data,
                x='product_category',
                y='margin',
                title="Profit Margin by Product Category",
                labels={'margin': 'Margin (%)', 'product_category': 'Product Category'},
                color='margin',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                height=450,
                xaxis_tickangle=-45,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif", size=12, color='#4a5568'),
                title_font=dict(size=16, color='#2d3748')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Category Performance Summary")
        category_summary = category_data.copy()
        category_summary.columns = ['Product Category', 'Revenue ($)', 'Profit ($)', 'Cost ($)', 'Margin (%)']
        category_summary = category_summary.round(2)
        st.dataframe(
            category_summary,
            use_container_width=True,
            hide_index=True
        )
    
    with tab3:
        st.subheader("Regional Performance Analysis")
        regional_data = df_filtered.groupby('region').agg({
            'sales_amount': 'sum',
            'profit': 'sum',
            'cost': 'sum'
        }).reset_index()
        regional_data['margin'] = (regional_data['profit'] / regional_data['sales_amount'] * 100)
        regional_data = regional_data.sort_values('sales_amount', ascending=False)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(
                regional_data,
                values='sales_amount',
                names='region',
                title="Revenue Distribution by Region",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif", size=12, color='#4a5568'),
                title_font=dict(size=16, color='#2d3748')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                regional_data,
                x='region',
                y='margin',
                title="Profit Margin by Region",
                labels={'margin': 'Margin (%)', 'region': 'Region'},
                color='margin',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif", size=12, color='#4a5568'),
                title_font=dict(size=16, color='#2d3748')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Regional Performance Summary")
        regional_summary = regional_data.copy()
        regional_summary.columns = ['Region', 'Revenue ($)', 'Profit ($)', 'Cost ($)', 'Margin (%)']
        regional_summary = regional_summary.round(2)
        st.dataframe(
            regional_summary,
            use_container_width=True,
            hide_index=True
        )
    
    with tab4:
        st.subheader("Customer Performance Analysis")
        customer_data = df_filtered.groupby('customer').agg({
            'sales_amount': 'sum',
            'profit': 'sum',
            'margin': 'mean'
        }).reset_index()
        customer_data = customer_data.sort_values('sales_amount', ascending=False)
        top_customers = customer_data.head(20)
        
        fig = px.bar(
            top_customers,
            x='customer',
            y='sales_amount',
            title="Top 20 Customers by Revenue",
            labels={'sales_amount': 'Revenue (USD)', 'customer': 'Customer'},
            color='sales_amount',
            color_continuous_scale='Reds'
        )
        fig.update_layout(
            height=500,
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#4a5568'),
            title_font=dict(size=16, color='#2d3748')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Top 20 Customers Summary")
        customer_summary = top_customers.copy()
        customer_summary.columns = ['Customer', 'Revenue ($)', 'Profit ($)', 'Avg Margin (%)']
        customer_summary = customer_summary.round(2)
        st.dataframe(
            customer_summary,
            use_container_width=True,
            hide_index=True
        )
    
    # Data table
    st.markdown("---")
    st.header("Transaction Data")
    with st.expander("View Filtered Transaction Data"):
        display_df = df_filtered.copy()
        # Select and rename only the columns we want to display
        column_mapping = {
            'date': 'Date',
            'product_category': 'Product Category',
            'region': 'Region',
            'customer': 'Customer',
            'sales_amount': 'Sales Amount ($)',
            'cost': 'Cost ($)',
            'profit': 'Profit ($)',
            'margin': 'Margin (%)',
            'month': 'Month',
            'year_month': 'Year-Month'
        }
        # Only select columns that exist in the dataframe
        available_columns = {k: v for k, v in column_mapping.items() if k in display_df.columns}
        display_df = display_df[list(available_columns.keys())].rename(columns=available_columns)
        st.dataframe(display_df, use_container_width=True)

if __name__ == "__main__":
    main()
