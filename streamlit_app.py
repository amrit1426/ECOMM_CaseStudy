import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="E-Commerce Sale Analysis",
    page_icon="🛒",
    layout="wide",
)

# Header
st.title("🛒 E-Commerce Sale Analysis Dashboard")
st.markdown("Customer purchase behavior and sale insights.")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("20251121_ECOMM_Dataset.csv")
    
    # Remove duplicates as per notebook
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Impute missing values
    df['Gender'].fillna(df['Gender'].mode()[0], inplace=True)
    df['City_Category'].fillna(df['City_Category'].mode()[0], inplace=True)
    
    # Fill Product_Category using ProductID mapping
    mapper = {}
    for row in range(df.shape[0]):
        ID = df.loc[row, 'ProductID']
        Category = df.loc[row, 'Product_Category']
        mapper[ID] = mapper.get(ID, Category)
    
    indexes = df[df['Product_Category'].isnull()].index
    for index in indexes:
        Category = mapper[df.loc[index, 'ProductID']]
        df.loc[index, 'Product_Category'] = Category
    
    df.dropna(subset=['Product_Category'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df

df = load_data()

# Chart styling helper
def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc",
        xaxis_gridcolor="#1e293b",
        yaxis_gridcolor="#1e293b",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    cities = st.multiselect(
        "City Category",
        options=df["City_Category"].dropna().unique(),
        default=df["City_Category"].dropna().unique(),
    )
    genders = st.multiselect(
        "Gender",
        options=df["Gender"].dropna().unique(),
        default=df["Gender"].dropna().unique(),
    )
    ages = st.multiselect(
        "Age Group",
        options=df["Age"].dropna().unique(),
        default=df["Age"].dropna().unique(),
    )
    marital_status = st.multiselect(
        "Marital Status",
        options=df["Marital_Status"].dropna().unique(),
        default=df["Marital_Status"].dropna().unique(),
    )

# Apply filters
filtered = df[
    df["City_Category"].isin(cities)
    & df["Gender"].isin(genders)
    & df["Age"].isin(ages)
    & df["Marital_Status"].isin(marital_status)
]

# Tabs
tab_overview, tab_analysis, tab_details = st.tabs(["Overview", "Analysis", "Details"])

with tab_overview:
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transactions", len(filtered))
    col2.metric(
        "Total Revenue (₹)",
        f"{filtered['Purchase'].sum():,.0f}" if len(filtered) else "N/A",
    )
    col3.metric(
        "Avg Purchase (₹)",
        f"{filtered['Purchase'].mean():,.0f}" if len(filtered) else "N/A",
    )
    col4.metric(
        "Unique Customers",
        filtered['UserID'].nunique() if len(filtered) else "N/A",
    )

    st.subheader("Gender Distribution")
    if len(filtered):
        gender_counts = filtered['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        fig = px.pie(
            gender_counts,
            values='Count',
            names='Gender',
            title='Gender Distribution',
            color_discrete_sequence=['#a855f7', '#ec4899'],
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#f8fafc")
        st.plotly_chart(fig, width="stretch")

    st.subheader("City Category Distribution")
    if len(filtered):
        city_counts = filtered['City_Category'].value_counts().reset_index()
        city_counts.columns = ['City_Category', 'Count']
        fig = px.pie(
            city_counts,
            values='Count',
            names='City_Category',
            title='City Category Distribution',
            color_discrete_sequence=px.colors.sequential.Viridis,
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#f8fafc")
        st.plotly_chart(fig, width="stretch")

with tab_analysis:
    st.subheader("Average Purchase by Age Group")
    if len(filtered):
        age_purchase = filtered.groupby('Age')['Purchase'].mean().reset_index()
        age_order = ['0-17', '18-25', '26-35', '36-45', '46-50', '51-55', '55+']
        age_purchase['Age'] = pd.Categorical(age_purchase['Age'], categories=age_order, ordered=True)
        age_purchase = age_purchase.sort_values('Age')
        fig = px.bar(
            age_purchase,
            x='Age',
            y='Purchase',
            title='Average Purchase by Age Group',
            color='Purchase',
            color_continuous_scale=px.colors.sequential.Purples,
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Age Group Distribution")
    if len(filtered):
        age_counts = filtered['Age'].value_counts().reset_index()
        age_counts.columns = ['Age', 'Count']
        age_order = ['0-17', '18-25', '26-35', '36-45', '46-50', '51-55', '55+']
        age_counts['Age'] = pd.Categorical(age_counts['Age'], categories=age_order, ordered=True)
        age_counts = age_counts.sort_values('Age')
        fig = px.pie(
            age_counts,
            values='Count',
            names='Age',
            title='Age Group Distribution',
            color_discrete_sequence=px.colors.sequential.Plasma,
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#f8fafc")
        st.plotly_chart(fig, width="stretch")

    st.subheader("Visitors by Occupation")
    if len(filtered):
        occ_counts = filtered['Occupation'].value_counts().reset_index()
        occ_counts.columns = ['Occupation', 'Count']
        fig = px.bar(
            occ_counts,
            x='Occupation',
            y='Count',
            title='Visitors by Occupation',
            color='Count',
            color_continuous_scale=px.colors.sequential.Purples,
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Average Purchase by Occupation")
    if len(filtered):
        occ_purchase = filtered.groupby('Occupation')['Purchase'].mean().reset_index()
        fig = px.line(
            occ_purchase,
            x='Occupation',
            y='Purchase',
            title='Average Purchase by Occupation',
            markers=True,
        )
        fig.update_traces(line_color='#a855f7')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Top 10 Products by Total Sales")
    if len(filtered):
        top_products = filtered.groupby('ProductID')['Purchase'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(
            top_products,
            x='ProductID',
            y='Purchase',
            title='Top 10 Products by Total Sales',
            color='Purchase',
            color_continuous_scale=px.colors.sequential.Purples,
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Purchase Price Distribution")
    if len(filtered):
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=filtered['Purchase'],
            nbinsx=50,
            name='Purchase Distribution',
            marker_color='#a855f7',
        ))
        fig.update_layout(
            title='Purchase Price Distribution',
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f8fafc",
            xaxis_gridcolor="#1e293b",
            yaxis_gridcolor="#1e293b",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig, width="stretch")

    st.subheader("Average Purchase by Marital Status & Gender")
    if len(filtered):
        marital_gender = filtered.groupby(['Marital_Status', 'Gender'])['Purchase'].mean().reset_index()
        fig = px.bar(
            marital_gender,
            x='Marital_Status',
            y='Purchase',
            color='Gender',
            barmode='group',
            title='Average Purchase by Marital Status & Gender',
            color_discrete_sequence=['#a855f7', '#ec4899'],
        )
        fig.update_layout(
            xaxis_ticktext=['Married', 'Unmarried'],
            xaxis_tickvals=[0, 1],
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Average Purchase by Product Category")
    if len(filtered):
        cat_purchase = filtered.groupby('Product_Category')['Purchase'].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(
            cat_purchase,
            x='Product_Category',
            y='Purchase',
            title='Average Purchase by Product Category',
            color='Purchase',
            color_continuous_scale=px.colors.sequential.Purples,
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Top 6 Product Categories by Gender")
    if len(filtered):
        male_top = filtered[filtered['Gender'] == 'M'].groupby('Product_Category')['Purchase'].mean().sort_values(ascending=False).head(6).reset_index()
        female_top = filtered[filtered['Gender'] == 'F'].groupby('Product_Category')['Purchase'].mean().sort_values(ascending=False).head(6).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=male_top['Product_Category'], y=male_top['Purchase'], name='Male', marker_color='#a855f7'))
        fig.add_trace(go.Bar(x=female_top['Product_Category'], y=female_top['Purchase'], name='Female', marker_color='#ec4899'))
        fig.update_layout(
            barmode='group',
            title='Top 6 Product Categories by Gender',
            xaxis_tickangle=-45,
        )
        st.plotly_chart(style_chart(fig), width="stretch")

with tab_details:
    st.subheader("Data Preview")
    st.dataframe(filtered.head(100), width="stretch")

# Footer
st.divider()
st.caption("Built with Streamlit | Data source: 20251121_ECOMM_Dataset.csv")
