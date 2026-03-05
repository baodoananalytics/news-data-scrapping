# news-data-scrapping
Automated news extraction by BeautifulSoup for web scraping and Power Automate for daily delivery to communication channels

# Overview
Developed an automated news aggregation workflow to provide daily updates on the Vietnamese Real Estate and Construction Materials sectors. The pipeline utilizes Requests and BeautifulSoup for web scraping (source, title, URL, summary), Pandas for structured data management in Excel, and Power Automate to trigger automated delivery to chatbox platforms.

# Technologies Used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4E9A06?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-005571?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Microsoft Excel](https://img.shields.io/badge/Microsoft_Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![Power Automate](https://img.shields.io/badge/Power_Automate-0066FF?style=for-the-badge&logo=power-automate&logoColor=white)

# Data Overview
The pipeline aggregates high-quality market intelligence from Vietnam’s most prestigious financial and real estate e-magazines, including CafeF.vn, Vietstock.vn, and Batdongsan.com.vn.

1. **Comprehensive Metadata Extraction:**
For every captured article, the workflow extracts a structured dataset to ensure full traceability:
  * Source Attribution: Originating publisher.
  * Metadata: Article Title and a concise Summary.
  * Direct Access: Original Source URL for deep-dive reading.
  * Temporal Tracking: Exact Published Time to maintain chronological relevance.

2. **Intelligent Keyword-based Filtering:**
To maintain the news content exactly, the script implements a strict Boolean filtering logic. An article is only processed if its title contains at least one industry-specific keyword:
  * Real Estate Sector: Targeted via terms such as "Nhà ở" (Housing), "Dự án" (Projects), and "Bất động sản".
  * Construction Materials: Filtered by strategic keywords like "Thép" (Steel) and "Vật liệu xây dựng" (Construction Materials).



