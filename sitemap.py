import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
import time

def crawl_website(start_url, base_url):
    visited = set()
    to_visit = [start_url]
    
    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue
        
        visited.add(current_url)
        print(f"Crawling: {current_url}")
        
        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                
                for link in links:
                    href = link['href']
                    full_url = urljoin(base_url, href)
                    
                    if full_url.startswith(base_url) and full_url not in visited:
                        to_visit.append(full_url)
            
            time.sleep(1)  # Be polite to the server
        except Exception as e:
            print(f"Error crawling {current_url}: {e}")
    
    return visited

def generate_sitemap(urls, output_file):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for url in urls:
        url_element = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_element, "loc")
        loc.text = url
    
    tree = ET.ElementTree(urlset)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    base_url = "https://www.scales-technology.co.ke/"  # Replace with your website's base URL
    start_url = base_url
    
    crawled_urls = crawl_website(start_url, base_url)
    generate_sitemap(crawled_urls, "sitemap.xml")
    print(f"Sitemap generated with {len(crawled_urls)} URLs.")