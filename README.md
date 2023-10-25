# Shein Website Data Scraping

![shein](https://cloudfront-us-east-2.images.arcpublishing.com/reuters/RXLBDI72RJPVZE5OMX7JMA32BI.jpg)

This project focuses on scraping product information and customer reviews from the Shein website. The gathered data can be used for analysis, insights, and enhancing the overall shopping experience.

# Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Technologies Needed](#technologies-needed)
- [Benefits](#benefits)

  
# Project Overview

The goal of this project is to collect valuable information from the Shein website, including product details and customer reviews, for further analysis and understanding. The project comprises three Python scripts for collecting product links, scraping product features, and scraping product reviews:

1. **Get_Links.py**: This script gathers all available product URLs from the Shein website and stores them in a CSV file named "All_Links.csv." These URLs can later be used to fetch detailed product information.

2. **Scrap_All_Links.py**: This script scrapes product features, including images, from the collected product URLs. It organizes the extracted data and downloaded images, saving them in a CSV file named "Product_Features.csv" and in a structured folder hierarchy.
   
      - **sku_name**: The name of the product as listed on the website.
      - **sku_id**: The unique identifier assigned to the product by the website.
      - **price**: The current price of the product.
      - **club_price**: The price of the product for club members, if applicable.
      - **orig_price**: The original price of the product before any discounts.
      - **badge**: Any label or badge associated with the product (e.g., "New", "Sale").
      - **size**: Available sizes for the product.
      - **quick_ship**: Information about quick shipping options for the product.
      - **delivery_1**: Delivery details for a specific option.
      - **delivery_2**: Another delivery option for the product.
      - **return_policy**: The return policy for the product.
      - **description**: A detailed description of the product.
      - **model_size**: The model's size information for the product.
      - **model_height**: The height of the model wearing the product.
      - **model_Bust**: The bust size of the model wearing the product.
      - **model_waist**: The waist size of the model wearing the product.
      - **model_hips**: The hips size of the model wearing the product.
      - **brand**: The brand of the product.
      - **collection**: The collection or line the product belongs to.
      - **avg_rating**: The average rating of the product based on customer reviews.
      - **rating_num**: The number of customer reviews/ratings for the product.
      - **fit_small**: Information about how the product fits if it's smaller than expected.
      - **fit_true**: Information about how the product fits as expected.
      - **fit_large**: Information about how the product fits if it's larger than expected.
      - **img_url**: The URL of the main product image.
      - **time_stamp**: The timestamp indicating when the data was scraped.

      #### Organized Images:
      The script not only extracts product features but also downloads the associated product images. It then organizes these images into a structured folder hierarchy to maintain clarity and ease of access.

4. **Scrap_Reviews_By_Interaction.py**: This script scrapes customer reviews for each product URL in "All_Links.csv" and stores the extracted data as JSON objects in a CSV file named "Product_Reviews.csv." Each JSON object contains review details such as ratings, fit information, review text, and review dates.

    ### Review Information:
    The reviews are organized in a JSON format within the "Product_Reviews.csv" file:

      - **weight**: The weight of the reviewer providing feedback.
      - **bust_size**: The bust size of the reviewer providing feedback.
      - **star**: The rating given by the reviewer (in stars).
      - **review**: The text of the review provided by the customer.
      - **overall_fit**: How the product fits overall, as mentioned by the reviewer.
      - **color**: The color fit of the product, as mentioned by the reviewer.
      - **size**: The size fit of the product, as mentioned by the reviewer.
      - **review_date**: The date when the review was submitted.

# Prerequisites

Before diving into the scraping scripts, ensure you have the following prerequisites ready:

```bash
# Install Python 3.x
pip install python

# Install Selenium for web automation
pip install selenium

# Install BeautifulSoup for HTML parsing
pip install beautifulsoup4

# Install pandas for data manipulation
pip install pandas

# Install numpy for numerical operations
pip install numpy

# Download and set up Chrome WebDriver
# Make sure the WebDriver executable is in your system's PATH

# Ensure you have the necessary dependencies installed
```

# Technologies Needed

To successfully run the web scraping and data processing scripts, you'll require the following technologies:

- **Python**: The core programming language used for scripting and automation. It's versatile and well-suited for web scraping tasks.

- **Selenium**: A robust web testing framework that automates interactions with web elements, simulates user actions, and navigates web pages.

- **BeautifulSoup**: A Python library for parsing HTML and XML documents. It's essential for extracting structured data from web pages.

- **pandas**: A powerful data manipulation and analysis library. It's used to efficiently handle tabular data and organize scraped information.

- **numpy**: A fundamental library for numerical computations. It's useful for working with arrays, matrices, and mathematical operations.

- **Chrome WebDriver**: A tool for browser automation that allows programmatically controlling a Chrome browser instance. It's crucial for simulating user interactions and navigating web pages.

These technologies collectively empower you to automate data collection, extract insights from websites, and efficiently process and analyze the gathered data.

# Benefits

1. **Informed Product Development**: Gain valuable insights from customer reviews and preferences to enhance product design, resulting in offerings that better match customer needs and expectations.

2. **Enhanced Customer Experience**: Optimize product descriptions, sizing recommendations, and user experience based on analyzed feedback, leading to increased customer satisfaction and engagement.

3. **Competitor Analysis**: Analyze competitors' products, customer sentiments, and pricing strategies for informed decision-making, enabling you to stay competitive in the market.

4. **Trend Identification**: Detect emerging fashion trends and popular styles through sentiment analysis, allowing you to capitalize on timely opportunities and stay ahead of industry shifts.

5. **Targeted Marketing**: Craft tailored marketing campaigns based on product attributes, fit preferences, and customer segments, improving conversion rates and driving sales growth.








