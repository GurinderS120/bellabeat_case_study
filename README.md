# Bellabeat Case Study - Data Analysis & Marketing Recommendations

## **📌 Project Overview**

This project analyzes **Fitbit user data** to provide **marketing insights for Bellabeat** a company specializing in **women’s health-focused smart devices**. The goal is to understand how consumers use non-Bellabeat wearables and leverage these insights to improve Bellabeat’s engagement strategy, particularly for the **Bellabeat App & Membership**.

## **🔍 Business Task**

Bellabeat wants to understand **how consumers use non-Bellabeat smart devices** and apply these insights to **enhance its marketing strategy**. The goal is to identify engagement trends and recommend strategies to **increase user adoption of Bellabeat’s products and membership services**.

## **📊 Data Source**

The dataset used in this analysis comes from <a href="https://www.kaggle.com/datasets/arashnic/fitbit/data" target="_blank">Kaggle</a>, which aggregates Fitbit data. It includes user tracking for **activity, sleep, heart rate, and weight** across two separate time periods in 2016.

## **🛠️ Analysis Workflow**

This project follows the **six-phase data analysis process:**

1️⃣ **Ask** → Define the business task and goals.\
2️⃣ **Prepare** → Load and assess the data for relevance and completeness.\
3️⃣ **Process** → Clean, transform, and structure the data for analysis.\
4️⃣ **Analyze** → Identify user behavior patterns and tracking engagement.\
5️⃣ **Share** → Summarize findings with **visuals & key insights**.\
6️⃣ **Act** → Provide **marketing recommendations** based on the analysis.

🔗 **For a full breakdown of each phase, see** [`analysis_report.md`](./reports/analysis_report.md)

## **📈 Key Findings & Marketing Recommendations**

### **📌 Key Findings:**

✅ **55% of users don’t track sleep, and 57% don’t track heart rate**, revealing an opportunity to increase engagement.\
✅ Users who **track multiple metrics** are more engaged than those who track only one.\
✅ **Activity tracking is the most common**, but sleep & weight tracking are underutilized.\
✅ **Tracking consistency varies**, meaning some users need better engagement strategies.

### **🚀 Marketing Recommendations:**

1️⃣ **Encourage Comprehensive Tracking** → Use reminders & gamification to drive engagement.\
2️⃣ **Promote Sleep Tracking** → Educate users on how sleep impacts fitness & wellness.\
3️⃣ **Convert Engaged Users to Membership** → Offer free trials & in-app prompts.\
4️⃣ **Collect More Recent Data** → The dataset is from 2016; continuous tracking data would improve insights.

## **📦 Project Structure**

```bash
📂 bellabeat_case_study/
├── 📂 data/
│   ├── raw                 # Raw dataset (Fitbit data)
│   ├── processed           # Cleaned and processed datasets
│
├── 📂 notebooks/           # Jupyter Notebooks for analysis & visualization
│
├── 📂 reports/
│   ├── analysis_report.md  # Detailed breakdown of analysis & findings
│
├── 📂 scripts/
│   ├── main.py             # Main script for running analysis
│   ├── data_processing.py  # Data cleaning & processing logic
│   ├── analysis.py         # Data analysis & visualization scripts
│
├── .gitignore              # Ignored files/folders (e.g., venv, temp files)
├── README.md               # Overview & project documentation
├── requirements.txt        # Required Python libraries
```

## **🚀 How to Run the Project**

1️⃣ **Clone this repository:**

```bash
git clone https://github.com/GurinderS120/bellabeat_case_study.git
cd bellabeat_case_study
```

2️⃣ **Create a virtual environment & install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

3️⃣ **Run the analysis:**

```bash
python scripts/main.py
```

4️⃣ **View the report:** Check the [`analysis_report.md`](./reports/analysis_report.md) for a deep dive into findings and recommendations.

---

🚀 **For more details, see the full report in** [`analysis_report.md`](./reports/analysis_report.md)
