import sys
import os
import time
import re
import folium
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QMenu, QMenuBar,
                             QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton,
                             QProgressBar, QLineEdit, QFileDialog, QLabel, QComboBox, 
                             QListWidget, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

KAKAO_API_KEY = ""

#Korean & English Translations

translations = {

	# General UI (en)

    'en': {
        'Address': 'Address:',
        'Category': 'Category:',
        'START': 'START',
        'STOP': 'STOP',
        'SHOW MAP': 'SHOW MAP',
        'Change Save Location': 'Change Save Location',
        'Exit': 'Exit',
        'Show/Hide Logs': 'Show/Hide Logs',
        'About': 'About',
        'File': 'File',
        'Settings': 'Settings',
        'Help': 'Help',
        'Language': 'Language',
        'Enter address': 'Enter address',
        
        # Logging (en)
        
        'Please enter an address.': 'Please enter an address.',
        'Scraping stopped by user.': 'Scraping stopped by user.',
        'Scraping completed.': 'Scraping completed.',
        'No data to plot. Please scrape data first.': 'No data to plot. Please scrape data first.',
        'Plotting map...': 'Plotting map...',
        'Map plotted successfully.': 'Map plotted successfully.',
        'Hours': 'Hours',
        'Phone': 'Phone',
        'Save location changed to:': 'Save location changed to:',
        'About Yogiyo Info Mapper': 'About Yogiyo Info Mapper',
        'Starting...': 'Starting...',
        'Address entered:': 'Address entered:',
        'Multiple address suggestions found. Selected:': 'Multiple address suggestions found. Selected:',
        'No additional address suggestions found.': 'No additional address suggestions found.',
        'No address suggestions found. Proceeding with entered address.': 'No address suggestions found. Proceeding with entered address.',
        'An error occurred while entering address:': 'An error occurred while entering address:',
        'Selected category:': 'Selected category:',
        'An error occurred while selecting category:': 'An error occurred while selecting category:',
        'Found {} restaurants': 'Found {} restaurants',
        'Scraping {}/{}:': 'Scraping {}/{}:',
        'Scraping complete. Data saved to': 'Scraping complete. Data saved to',
        'An error occurred while scraping restaurants:': 'An error occurred while scraping restaurants:',
        'Error in safe_click:': 'Error in safe_click:',
        'Error scraping': 'Error scraping',
        'An error occurred:': 'An error occurred:',
        'Could not geocode the address:': 'Could not geocode the address:',
        'Using default center.': 'Using default center.',
        'Using coordinates for address:': 'Using coordinates for address:',
        'Could not geocode address for': 'Could not geocode address for',
        'Map plotted successfully. Plotted {} out of {} restaurants.': 'Map plotted successfully. Plotted {} out of {} restaurants.',
        'Map saved to': 'Map saved to',
        'No coordinates found for address:': 'No coordinates found for address:',
        'Error fetching coordinates for': 'Error fetching coordinates for',
        'Error parsing coordinates for': 'Error parsing coordinates for',
        
	# Help (en)
	
        'Yogiyo Info Mapper': 'Yogiyo Info Mapper',
        'about_text': """
Yogiyo Info Mapper

This program scrapes restaurant information from Yogiyo and plots the locations on a map.

1. Enter an address.
2. Select a category.
3. Click 'Start' to begin the scraping process.
4. Data is saved as an Excel file.
5. Click 'Show Map' to view the scraped locations on a map.
    
Jonathan Booker Nelson
https://github.com/booknite
Version: 1.3
        """
    },
    
    	# General UI (kr)
    	
    'ko': {
        'Address': '주소',
        'Category': '카테고리',
        'START': '시작',
        'STOP': '정지',
        'SHOW MAP': '지도 표시',
        'Change Save Location': '저장 위치 변경',
        'Exit': '종료',
        'Show/Hide Logs': '로그 표시/숨기기',
        'About': '정보',
        'File': '파일',
        'Settings': '설정',
        'Help': '도움말',
        'Language': '언어',
        'Enter address': '주소를 입력하세요',
        
        # Logging (kr)
        
        'Please enter an address.': '주소를 입력해주세요.',
        'Scraping stopped by user.': '사용자에 의해 스크래핑이 중지되었습니다.',
        'Scraping completed.': '스크래핑이 완료되었습니다.',
        'No data to plot. Please scrape data first.': '표시할 데이터가 없습니다. 먼저 스크래핑을 실행해주세요.',
        'Plotting map...': '지도를 표시하는 중...',
        'Map plotted successfully.': '지도가 성공적으로 표시되었습니다.',
        'Hours': '영업시간',
        'Phone': '전화번호',
        'Save location changed to:': '저장 위치가 다음으로 변경되었습니다:',
        'About Yogiyo Info Mapper': 'Yogiyo Info Mapper 정보',
        'Starting...': '시작 중...',
        'Address entered:': '입력된 주소:',
        'Multiple address suggestions found. Selected:': '여러 주소 제안을 찾았습니다. 선택됨:',
        'No additional address suggestions found.': '추가 주소 제안을 찾지 못했습니다.',
        'No address suggestions found. Proceeding with entered address.': '주소 제안을 찾지 못했습니다. 입력한 주소로 진행합니다.',
        'An error occurred while entering address:': '주소 입력 중 오류가 발생했습니다:',
        'Selected category:': '선택된 카테고리:',
        'An error occurred while selecting category:': '카테고리 선택 중 오류가 발생했습니다:',
        'Found {} restaurants': '{}개의 음식점을 찾았습니다',
        'Scraping {}/{}:': '스크래핑 중 {}/{}:',
        'Scraping complete. Data saved to': '스크래핑 완료. 데이터 저장 위치:',
        'An error occurred while scraping restaurants:': '음식점 스크래핑 중 오류가 발생했습니다:',
        'Error in safe_click:': 'safe_click 중 오류:',
        'Error scraping': '스크래핑 오류',
        'An error occurred:': '오류가 발생했습니다:',
        'Could not geocode the address:': '주소를 지오코딩할 수 없습니다:',
        'Using default center.': '기본 중심점을 사용합니다.',
        'Using coordinates for address:': '주소에 대한 좌표 사용 중:',
        'Could not geocode address for': '다음 주소를 지오코딩할 수 없습니다:',
        'Map plotted successfully. Plotted {} out of {} restaurants.': '지도 표시 성공. {}개 중 {}개의 음식점을 표시했습니다.',
        'Map saved to': '지도 저장 위치:',
        'No coordinates found for address:': '주소에 대한 좌표를 찾을 수 없습니다:',
        'Error fetching coordinates for': '다음 주소의 좌표를 가져오는 중 오류 발생:',
        'Error parsing coordinates for': '다음 주소의 좌표를 파싱하는 중 오류 발생:',
        
        #Help (kr)
        
        'About Yogiyo Info Mapper': 'Yogiyo Info Mapper 정보',
        'about_text': """
Yogiyo Info Mapper

이 프로그램은 요기요에서 음식점 정보를 스크래핑하고 지도에 위치를 표시합니다.

1. 주소를 입력하세요.
2. 카테고리를 선택하세요.
3. '시작' 버튼을 클릭하여 스크래핑을 시작하세요.
4. 데이터는 Excel 파일로 저장됩니다.
5. '지도 표시' 버튼을 클릭하여 스크래핑된 위치를 지도에서 확인하세요.

Jonathan Booker Nelson
https://github.com/booknite
버전: 1.3
        """
    }
}
categories = {
    "음식점 전체보기": "All Restaurants",
    "1인분 주문": "Single Serving",
    "프랜차이즈": "Franchise",
    "치킨": "Chicken",
    "피자/양식": "Pizza/Western",
    "중국집": "Chinese",
    "한식": "Korean",
    "일식/돈까스": "Japanese/Pork Cutlet",
    "족발/보쌈": "Pigs' Feet/Bossam",
    "야식": "Late Night Snacks",
    "분식": "Korean Snacks",
    "카페/디저트": "Cafe/Dessert",
    "편의점/마트": "Convenience Store/Mart"
}
	
class ScrapingThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)
    log = pyqtSignal(str)
    partial_data = pyqtSignal(list) 

    def __init__(self, address, category, save_location, tr):
        super().__init__()
        self.address = address
        self.category = category
        self.save_location = save_location
        self.is_running = True
        self.scraped_data = []
        self.selected_address = None
        self.tr = tr
        self.output_file = None

	# Chrome WebDriver

    def run(self):
        driver = self.setup_driver()
        self.log.emit(self.tr("Starting..."))
        try:
            driver.get("https://www.yogiyo.co.kr/mobile/#/")
            time.sleep(5)
            if not self.is_running:
                return
            self.enter_address(driver)
            if not self.is_running:
                return
            self.select_category(driver)
            if not self.is_running:
                return
            self.scrape_restaurants(driver)
        except Exception as e:
            self.log.emit(f"{self.tr('An error occurred:')} {e}")
        finally:
            driver.quit()
            self.finished.emit(self.scraped_data)

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def enter_address(self, driver):
        try:
            address_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "address_input"))
            )
            address_input.clear()
            address_input.send_keys(self.address)
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="button_search_address"]/button[2]'))
            )
            search_button.click()
            self.log.emit(f"{self.tr('Address entered:')} {self.address}")
            time.sleep(5)

            try:
                address_suggestions = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="dropdown-menu ng-scope am-flip-x bottom-left"]//a'))
                )
                if len(address_suggestions) > 1:
                    self.selected_address = address_suggestions[1].text
                    self.log.emit(f"{self.tr('Multiple address suggestions found. Selected:')} {self.selected_address}")
                    address_suggestions[1].click()
                else:
                    self.log.emit(self.tr("No additional address suggestions found."))
                    self.selected_address = self.address
            except:
                self.log.emit(self.tr("No address suggestions found. Proceeding with entered address."))
                self.selected_address = self.address

            time.sleep(5)
        except Exception as e:
            self.log.emit(f"{self.tr('An error occurred while entering address:')} {e}")

    def select_category(self, driver):
        try:
            category_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[@class='category-name ng-binding' and text()='{self.category}']"))
            )
            category_element.click()
            self.log.emit(f"{self.tr('Selected category:')} {self.category}")
            time.sleep(5)
        except Exception as e:
            self.log.emit(f"{self.tr('An error occurred while selecting category:')} {e}")

    def sanitize_filename(self, filename):
        unsafe_chars = r'[<>:"/\\|?*\s]'
        return re.sub(unsafe_chars, '_', filename)

    def scrape_restaurants(self, driver):
        try:
            self.scroll_to_bottom(driver)
            restaurant_elements = driver.find_elements(By.CLASS_NAME, "restaurant-name")
            restaurants = [elem.text for elem in restaurant_elements]
            total_restaurants = len(restaurants)
            self.log.emit(self.tr("Found {} restaurants").format(total_restaurants))

            safe_address = self.sanitize_filename(self.selected_address or self.address)
            safe_category = self.sanitize_filename(self.category)
            filename = f"{safe_address} ({safe_category})"
            safe_filename = self.sanitize_filename(filename)
            self.output_file = os.path.join(self.save_location, f"{safe_filename}.xlsx")
            
            for i, restaurant in enumerate(restaurants, 1):
                if not self.is_running:
                    #self.save_data()  
                    return
                self.log.emit(self.tr("Scraping {}/{}:").format(i, total_restaurants) + f" {restaurant}")
                info = self.scrape_restaurant_info(driver, restaurant)
                self.scraped_data.append(info)
                self.progress.emit(int((i / total_restaurants) * 100))
                self.partial_data.emit(self.scraped_data)  

            #self.save_data()
            #self.log.emit(f"{self.tr('Scraping complete. Data saved to')} {self.output_file}")
        except Exception as e:
            self.log.emit(f"{self.tr('An error occurred while scraping restaurants:')} {e}")
        finally:
            self.save_data()
            
    def save_data(self):
        if self.scraped_data:
            df = pd.DataFrame(self.scraped_data, columns=["NAME", "HOURS", "PHONE", "ADDRESS"])
            df['PHONE'] = df['PHONE'].str.replace(r'\s*\(요기요 제공 번호\)', '', regex=True)
            df.to_excel(self.output_file, index=False)
            self.log.emit(f"{self.tr('Scraping complete. Data saved to')} {self.output_file}")
        else:
            self.log.emit(self.tr("No data to save."))

    def scroll_to_bottom(self, driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def safe_click(self, driver, element):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self.log.emit(f"{self.tr('Error in safe_click:')} {e}")
            raise

    def scrape_restaurant_info(self, driver, restaurant_name):
        try:
            restaurant_link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'restaurant-name') and normalize-space(text())='{restaurant_name}']"))
            )
            self.safe_click(driver, restaurant_link)
            time.sleep(5)

            info_tab = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '정보')]"))
            )
            self.safe_click(driver, info_tab)
            time.sleep(3)

            hours = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='info-item']//span[contains(@class, 'tc') and preceding-sibling::i[contains(text(), '영업시간')]]"))
            ).text
            phone = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='info-item']//span[contains(@class, 'tc') and preceding-sibling::i[contains(text(), '전화번호')]]"))
            ).text
            address = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='info-item']//span[contains(@class, 'tc') and preceding-sibling::i[contains(text(), '주소')]]"))
            ).text

            driver.back()
            time.sleep(3)
            return [restaurant_name, hours, phone, address]
        except Exception as e:
            self.log.emit(f"{self.tr('Error scraping')} {restaurant_name}: {e}")
            return [restaurant_name, "N/A", "N/A", "N/A"]

    def stop(self):
        self.is_running = False
        #self.save_data() 
        
	# Main application class for the scraper UI

class ScraperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yogiyo Info Mapper")
        self.setMinimumSize(450, 600)
        self.resize(450, 600)
        self.save_location = os.getcwd() # Default save location
        self.scraping_thread = None
        self.scraped_data = []
        self.selected_address = None
        self.current_language = 'en'  # Default language
        self.init_ui()
        self.set_style()
	
	# General UI
	
    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # Input
        
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
	    
        # Address
        
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText(self.tr("Enter address"))
        input_layout.addWidget(self.address_input)
	    
        # Category
        
        self.category_combo = QComboBox()
        for korean, english in categories.items():
            self.category_combo.addItem(f"{korean} - {english}", korean)
        input_layout.addWidget(self.category_combo)
	    
        main_layout.addWidget(input_widget)

        # Buttons
        
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        self.start_button = QPushButton(self.tr("START"))
        self.start_button.clicked.connect(self.start_scraping)
        self.stop_button = QPushButton(self.tr("STOP"))
        self.stop_button.clicked.connect(self.stop_scraping)
        self.stop_button.setEnabled(False)
        self.plot_map_button = QPushButton(self.tr("SHOW MAP"))
        self.plot_map_button.clicked.connect(self.plot_map)
        self.plot_map_button.setEnabled(False)
	    
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.plot_map_button)
	    
        main_layout.addWidget(button_widget)
    
        # Progress Bar
        
        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        # Log Area
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(100)
        main_layout.addWidget(self.log_area)

        # Main Content Area
        
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
		
        self.data_list = QListWidget()
        self.map_view = QWebEngineView()
		
        content_layout.addWidget(self.data_list, 1)
        content_layout.addWidget(self.map_view, 2)
		
        main_layout.addWidget(content_widget)

        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        self.file_menu = menu_bar.addMenu(self.tr("File"))
        self.settings_menu = menu_bar.addMenu(self.tr("Settings"))
        self.help_menu = menu_bar.addMenu(self.tr("Help"))

        self.select_location_action = QAction(self.tr("Change Save Location"), self)
        self.select_location_action.triggered.connect(self.select_save_location)
        self.file_menu.addAction(self.select_location_action)

        self.exit_action = QAction(self.tr("Exit"), self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        self.show_logs_action = QAction(self.tr('Show/Hide Logs'), self)
        self.show_logs_action.triggered.connect(self.toggle_logs)
        self.settings_menu.addAction(self.show_logs_action)

        language_menu = self.settings_menu.addMenu(self.tr("Language"))
        english_action = QAction("English", self)
        english_action.triggered.connect(lambda: self.change_language('en'))
        language_menu.addAction(english_action)
        korean_action = QAction("한국어", self)
        korean_action.triggered.connect(lambda: self.change_language('ko'))
        language_menu.addAction(korean_action)

        self.about_action = QAction(self.tr("About"), self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)

	# Styles

    def set_style(self):
	    self.setStyleSheet("""
	    QMainWindow {
		background-color: #f0f0f0;
	    }
	    QLabel {
		font-size: 14px;
		color: #333333;
	    }
	    QLineEdit, QComboBox {
		padding: 8px;
		border: 1px solid #cccccc;
		border-radius: 4px;
		background-color: #ffffff;
		font-size: 14px;
		min-height: 20px;
	    }
	    QComboBox::drop-down {
		subcontrol-origin: padding;
		subcontrol-position: top right;
		width: 25px;
		border-left-width: 1px;
		border-left-color: #cccccc;
		border-left-style: solid;
		border-top-right-radius: 3px;
		border-bottom-right-radius: 3px;
	    }
	    QComboBox::down-arrow {
		image: none;
		text-align: center;
		color: #FF9999;
	    }
	    QComboBox::down-arrow:after {
		content: "⯆";
		font-size: 16px;
		position: relative;
		top: -2px;
		right: -5px;
	    }
	    QComboBox QAbstractItemView {
		border: 1px solid #cccccc;
		selection-background-color: #e6e6e6;
		selection-color: #333333;
	    }
	    QComboBox QAbstractItemView::item {
		padding: 4px;
	    }
	    QComboBox QAbstractItemView::item:hover {
		background-color: #e6e6e6;
		color: #333333;
	    }
	    QPushButton {
		background-color: #FF9999;  
		color: white;
		padding: 8px 16px;
		border: none;
		border-radius: 4px;
		font-size: 14px;
		min-width: 100px;
		min-height: 30px;
	    }
	    QPushButton:hover {
		background-color: #FF8080; 
	    }
	    QPushButton:disabled {
		background-color: #FFB3B3;  
	    }
	    QProgressBar {
		border: 1px solid #cccccc;
		border-radius: 4px;
		text-align: center;
		min-height: 20px;
	    }
	    QProgressBar::chunk {
		background-color: #FF9999;  
	    }
	    QTextEdit, QListWidget {
		border: 1px solid #cccccc;
		border-radius: 4px;
		font-size: 12px;
	    }
	    QWidget {
		margin-top: 5px;
		margin-bottom: 5px;
	    }
	    """)

    def select_save_location(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr("Change Save Location"))
        if folder:
            self.save_location = folder
            self.show_log(f"{self.tr('Save location changed to:')} {self.save_location}")

    def start_scraping(self):
        address = self.address_input.text().strip()
        category = self.category_combo.currentData()

        if not address:
            self.show_log(self.tr("Please enter an address."))
            return

        self.stop_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self.plot_map_button.setEnabled(False)

        self.scraping_thread = ScrapingThread(address, category, self.save_location, self.tr)
        self.scraping_thread.progress.connect(self.update_progress)
        self.scraping_thread.finished.connect(self.on_scraping_finished)
        self.scraping_thread.log.connect(self.show_log)
        self.scraping_thread.partial_data.connect(self.update_scraped_data)
        self.scraping_thread.start()

    def stop_scraping(self):
        if self.scraping_thread:
            self.scraping_thread.stop()
            self.scraping_thread.wait()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.show_log(self.tr("Scraping stopped by user."))
        self.plot_map_button.setEnabled(True) 
        
    def update_scraped_data(self, data):
        self.scraped_data = data
        self.update_data_list()
        
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_scraping_finished(self, scraped_data):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.plot_map_button.setEnabled(True)
        self.scraped_data = scraped_data
        self.selected_address = self.scraping_thread.selected_address
        self.show_log(self.tr("Scraping completed."))
        self.update_data_list()

    def show_log(self, message):
        self.log_area.append(message)

    def toggle_logs(self):
        self.log_area.setVisible(not self.log_area.isVisible())

    def show_about(self):
        about_text = self.tr('about_text')
        QMessageBox.about(self, self.tr("About Yogiyo Info Mapper"), about_text)

    def update_data_list(self):
        self.data_list.clear()
        for i, data in enumerate(self.scraped_data, 1):
            name, hours, phone, address = data
            phone = re.sub(r'\s*\(요기요 제공 번호\)', '', phone)
            item_text = f"{i}. {name}\n{self.tr('Hours')}: {hours}\n{self.tr('Phone')}: {phone}\n{self.tr('Address')}: {address}\n"
            self.data_list.addItem(item_text)

    def plot_map(self):
        if not self.scraped_data:
            self.show_log(self.tr("No data to plot. Please scrape data first."))
            return

        self.show_log(self.tr("Plotting map..."))       
        
        default_lat, default_lng = 37.5665, 126.9780 # Default center (Seoul City Hall)
        
        center_lat, center_lng = self.get_coordinates(self.selected_address or self.address_input.text())
        if center_lat is None or center_lng is None:
            self.show_log(f"{self.tr('Could not geocode the address:')} {self.selected_address or self.address_input.text()}. {self.tr('Using default center.')}")
            center_lat, center_lng = default_lat, default_lng
        else:
            self.show_log(f"{self.tr('Using coordinates for address:')} {self.selected_address or self.address_input.text()}")

        m = folium.Map(location=[center_lat, center_lng], zoom_start=13)

        plotted_count = 0
        for restaurant in self.scraped_data:
            name, hours, phone, address = restaurant
            phone = re.sub(r'\s*\(요기요 제공 번호\)', '', phone)
            lat, lng = self.get_coordinates(address)
            if lat is not None and lng is not None:
                folium.Marker(
                    [lat, lng],
                    popup=f"<b>{name}</b><br>{self.tr('Hours')}: {hours}<br>{self.tr('Phone')}: {phone}<br>{self.tr('Address')}: {address}"
                ).add_to(m)
                plotted_count += 1
            else:
                self.show_log(f"{self.tr('Could not geocode address for')} {name}: {address}")

        map_html = m._repr_html_()
        self.map_view.setHtml(map_html)
        self.show_log(self.tr("Map plotted successfully. Plotted {} out of {} restaurants.").format(plotted_count, len(self.scraped_data)))

        # Save the map as an HTML file
        
        safe_address = self.scraping_thread.sanitize_filename(self.selected_address or self.address_input.text())
        safe_category = self.scraping_thread.sanitize_filename(self.category_combo.currentText())
        map_filename = f"{safe_address} ({safe_category}) - Map.html"
        map_path = os.path.join(self.save_location, map_filename)
        m.save(map_path)
        self.show_log(f"{self.tr('Map saved to')} {map_path}")

    def get_coordinates(self, address):
        url = f"https://dapi.kakao.com/v2/local/search/address.json"
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
        params = {"query": address}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            result = response.json()
            if result["documents"]:
                x = float(result["documents"][0]["x"])
                y = float(result["documents"][0]["y"])
                return y, x
            else:
                self.show_log(f"{self.tr('No coordinates found for address:')} {address}")
        except requests.RequestException as e:
            self.show_log(f"{self.tr('Error fetching coordinates for')} {address}: {e}")
        except (KeyError, IndexError, ValueError) as e:
            self.show_log(f"{self.tr('Error parsing coordinates for')} {address}: {e}")
        
        return None, None

    def change_language(self, lang):
        self.current_language = lang
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle("Yogiyo Info Mapper")
        self.address_input.setPlaceholderText(self.tr("Enter address"))
        self.start_button.setText(self.tr("START"))
        self.stop_button.setText(self.tr("STOP"))
        self.plot_map_button.setText(self.tr("SHOW MAP"))
        self.file_menu.setTitle(self.tr("File"))
        self.settings_menu.setTitle(self.tr("Settings"))
        self.help_menu.setTitle(self.tr("Help"))
        self.select_location_action.setText(self.tr("Change Save Location"))
        self.exit_action.setText(self.tr("Exit"))
        self.show_logs_action.setText(self.tr("Show/Hide Logs"))
        self.about_action.setText(self.tr("About"))

        # Update the data list if it contains any items
        
        if self.data_list.count() > 0:
            self.update_data_list()

    def tr(self, text):
        return translations[self.current_language].get(text, text)

def main():
    app = QApplication(sys.argv)
    window = ScraperApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
