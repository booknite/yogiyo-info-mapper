# Yogiyo Info Mapper

This application scrapes restaurant information from the Yogiyo website, saves the data in Excel format, and displays the restaurant locations on an interactive map using Folium and the Kakao Map API.

## Features

* User-friendly GUI for inputting addresses and selecting categories
* Bilingual support (English and Korean)
* Web scraping of restaurant data (name, hours, phone, address) from Yogiyo
* Data export to Excel files
* Interactive map plotting using Kakao Map API
* Capable of scraping and mapping over 100 restaurants without interruption
* Graceful stop functionality, saving partial data if interrupted

## Setup

### Prerequisites

1. Python 3.7+
2. Required packages (install via `pip install -r requirements.txt`):
   - PyQt5
   - selenium
   - beautifulsoup4
   - folium
   - pandas
   - webdriver_manager

### Kakao API Key

Replace API key in the code with your Kakao REST API key:

```python
KAKAO_API_KEY = "your_kakao_api_key_here"
```

## Usage

1. Run the application:
   ```
   python yogiyo-info-mapper.py
   ```

2. Enter an address (in Korean) in the input field.
3. Select a restaurant category from the dropdown menu.
4. Click "START" to begin scraping. Data will be saved in an Excel file upon completion.
5. Click "SHOW MAP" to plot restaurant locations on a map (saves as an HTML file).
6. Use "STOP" to halt the process at any time (partial data will still be saved).

### File Naming

Excel and map files are named after the entered address and category:
- `평택시_안정로_7_(족발_보쌈).xlsx`
- `평택시_안정로_7_(족발_보쌈) - Map.html`

## Author

[booknite]

## License

This project is licensed under the MIT License.
