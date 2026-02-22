## Sports Analytics Dashboard — Men’s Singles Badminton

### Analytical Objective
This dashboard analyzes men's singles badminton match data to understand tournament activity over time, evaluate match competitiveness, and examine how badminton events are distributed across different countries. The goal is to identify performance trends and understand the global structure of elite badminton competitions.

### Data Source
The data used in this dashboard comes from publicly available Badminton World Federation (BWF) World Tour match records.
Dataset obtained from Kaggle: Badminton BWF World Tour Matches (2018-2021)
This dataset contains detailed match-level information, including tournament location, event type, match results, and scoring statistics.
Dataset link: https://www.kaggle.com/datasets/sanderp/badminton-bwf-world-tour

### Data Collection Method
The dataset was obtained through direct download from Kaggle as a CSV file.
No API access or web scraping was required.
The file was stored locally and uploaded to the GitHub Repository in the data folder for use in the Streamlit dashboard.

### Data Update Procedure (Future Seasons)
To keep the dashboard updated as new badminton tournaments occur:
 1. Visit the Kaggle dataset page or the official BWF tournament results website.
 2. Download the updated dataset, including new tournament matches.
 3. Replace the existing CSV file in the repository's data folder.
 4. Commit and push the updated file to GitHub.
 5. Restart or redeploy the Streamlit application to reflect the updated data.

### Sustainability of the Dashboard
Because the dataset can be easily replaced with new tournament data, this dashboard can be continuously updated to reflect current badminton competitions. This ensures the application functions as a living analytical tool rather than a one-time analysis.

### Technologies Used
Python, Pandas, Plotly, Streamlit, GitHub, and Streamlit Community Cloud.
