import requests
from bs4 import BeautifulSoup


def main():
    # Hardcoded website URL
    url = "https://www.who.int/teams/surveillance-prevention-control-AMR/national-action-plan-monitoring-evaluation/library-of-national-action-plans"  # Adjust the URL as needed

    # Get user input for a comma-separated list of countries and prepare a list of lowercase country names
    countries_input = input("Enter countries (comma separated): ")
    countries = [country.strip().lower() for country in countries_input.split(",") if country.strip()]

    # Retrieve the page content
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page. Status code:", response.status_code)
        return

    # Parse the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all publication items; adjust the class if needed
    publication_items = soup.find_all("div", class_="sf-publications-item")

    found = False
    for item in publication_items:
        # Extract the title text from the h3 tag with the corresponding class
        title_tag = item.find("h3", class_="sf-publications-item__title")
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            # Check if any country from the list appears in the title
            for country in countries:
                if country in title_text.lower():
                    found = True

                    # Extract the publication date
                    date_div = item.find("div", class_="sf-publications-item__date")
                    date_text = date_div.find("span").get_text(strip=True) if date_div and date_div.find(
                        "span") else "N/A"

                    # Extract the detail page URL from the first <a> tag (wrapping the title)
                    detail_link = item.find("a", href=True)
                    detail_url = detail_link["href"] if detail_link else "N/A"

                    # Extract the download URL from the <a> tag with class "download-url"
                    download_link = item.find("a", class_="download-url")
                    download_url = download_link["href"] if download_link else "N/A"

                    # Print the extracted metadata
                    print("Country match:", country.capitalize())
                    print("Title:", title_text)
                    print("Date:", date_text)
                    print("Detail URL:", detail_url)
                    print("Download URL:", download_url)
                    print("-" * 50)

                    # Once a match is found for this item, no need to check further countries
                    break

    if not found:
        print("No publications found for the given countries.")


if __name__ == "__main__":
    main()
