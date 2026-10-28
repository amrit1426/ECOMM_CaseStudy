# E-Commerce Sale Analysis — Case Study

## Project Overview

This project analyzes customer purchase behavior for **ECOMM Private Limited**, an Indian e-commerce company headquartered in Delhi. The dataset captures purchases made by different customers for selected products with high sales in the last month, including customer demographics, product details, and total purchase amounts.

The analysis supports ECOMM's customer retention and profitability strategy by:
- Categorizing customers based on purchase behavior
- Optimizing delivery partner assignments by area
- Stocking best-selling products for major sale events
- Providing personalized offers

## Dataset

- **Records:** 240,882
- **Features:** 10
- **Size:** ~24 MB
- **Source:** ECOMM database (1 month before Big Billion Day sale)

### Features
| Feature | Description |
|---------|-------------|
| User_ID | Unique ID for each user |
| Product_ID | Unique ID for each product |
| Gender | Gender of the user (M/F) |
| Age | Age of the user |
| Occupation | Occupation of the user |
| City_Category | Category of the city (A/B/C) |
| Current_City_Years | Number of years stayed in the current city |
| Marital_Status | Marital status (0 = Married, 1 = Unmarried) |
| Product_Category | Category of the product purchased (1-18) |
| Purchase | Purchase amount in ₹ |

## Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- pandas-profiling / ydata-profiling

## Repository Structure

```
C:\Users\AB\hermes-work\data_projects\20251121_ECOMM_CaseStudy + GitHub
┣ 📓 ECommerceSaleAnalysis-230719-141622.ipynb   ← Main analysis notebook
┣ 📊 20251121_ECOMM_Dataset.csv                  ← Raw dataset
┣ 📂 0qY8FUtNQkmeeFiVgBRd_Documents_20240622_E-Commerce Sale Analysis\
┃ ┗ 📓 E-Commerce Sale Analysis.ipynb
┃ ┗ 📄 Pre Profiling Report.html
┣ 📂 qyYgzHJ1QemrlaUB8zNe_E-Commerce Sale Analysis_20240623_ECOMM_CaseStudy\
┃ ┗ 📓 E-Commerce Sale Analysis.ipynb
┣ 📦 *.zip archives
┗ 📄 README.md                                   ← Project documentation
```

## Key Business Insights

- **Product Category 10** has the highest average purchase price (~₹19,617)
- **Male customers** dominate overall purchase volume, but **female customers** show similar top-category preferences
- **~42%** of site visits come from **City B**
- **~68%** of site visitors are aged between **26-50**
- Average purchase price falls between **₹5,000 - ₹10,000**

## Actionable Recommendations

1. Target discounts to age groups below 26 and above 50 to balance revenue
2. Add more delivery partners in **City B** for the Big Billion Day sale
3. Stock up on **top 10 selling products** and items priced between ₹5,000-₹10,000
4. Offer personalized promotions based on gender and top category preferences
5. Provide special offers to underrepresented occupations to grow the customer base

## How to Run

1. Clone the repository
2. Install dependencies: `pip install pandas numpy matplotlib seaborn pandas-profiling`
3. Open `ECommerceSaleAnalysis-230719-141622.ipynb` in Jupyter

## About

This case study was completed as part of a data analytics certification program, focusing on customer analytics and business intelligence for an e-commerce context.
