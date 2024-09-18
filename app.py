import streamlit as st
from crawl4ai import WebCrawler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class HeadlessWebCrawler(WebCrawler):
    def __init__(self, verbose=False):
        # Set up Chrome options for headless operation
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        super().__init__(verbose=verbose)

    def close(self):
        self.driver.quit()  # Close the driver when done

def app():
    st.title("Web Scraping App with Crawl4AI")
    url = st.text_input("Enter URL", "https://www.eu-startups.com/directory/")
    
    if st.button("Scrape"):
        if url:
            st.write("Scraping URL:", url)
            try:
                # Create an instance of HeadlessWebCrawler
                crawler = HeadlessWebCrawler()
                # Warm up the crawler (load necessary models)
                crawler.warmup()
                # Run the crawler on the URL
                result = crawler.run(url=url)
                
                # Print the extracted content
                st.markdown(result.markdown)
            except Exception as e:
                st.error(f"Error occurred while scraping: {str(e)}")
            finally:
                crawler.close()  # Ensure the driver is closed
        else:
            st.warning("Please enter a URL")

if __name__ == "__main__":
    app()
