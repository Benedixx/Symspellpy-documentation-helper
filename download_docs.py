import requests
from bs4 import BeautifulSoup
import os
import urllib

# The URL to scrape
url = "https://symspellpy.readthedocs.io/en/latest/examples/index.html"

# The directory to store files in
output_dir = "./symspellpy-docs/"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Fetch the page
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
print(soup)

# Find all links to .html files
links = soup.find_all("a", href=True)

for link in links:
    href = link["href"]
    if href.endswith("/"):
        href = href[:-1]
        href = href + ".html"

    # If it's a .html file
    if href.endswith(".html"):
        # Make a full URL if necessary
        if not href.startswith("http"):
            href = urllib.parse.urljoin(url, href)

        # Fetch the .html file
        print(f"downloading {href}")

        # Check if the page has a <section> tag
        page_response = requests.get(href)
        page_soup = BeautifulSoup(page_response.text, "html.parser")
        section_tag = page_soup.find("section")

        if section_tag is None:
            print("Skipping download: No <section> tag found.")
            continue

        # Write it to a file
        file_name = os.path.join(output_dir, os.path.basename(href))
        with open(file_name, "wb") as file:  # Use binary mode instead of text mode
            file.write(page_response.content)
