from fastapi import HTTPException
import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from helpers.ansi_helpers import pr_info, pr_error

BASE_URL = "https://www.edinburgh.gov.uk"
PARSER = "html.parser"
LIST_RECORD_CLASS = "list--record"


def get_possible_addresses_by_letter(letter, page_number):
    streets = []

    URL = f"{BASE_URL}/directory/10251/a-to-z/{letter}?page={page_number}"
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, PARSER)
        street_link_list = []
        street_links = []
        try:
            street_link_list = soup.find_all("ul", {"class": LIST_RECORD_CLASS})[0]
            street_links = street_link_list.find_all("a", {"class": "list__link"})
        except IndexError:
            street_link_list = []
            street_links = []
            pr_error(f"No streets found starting with {letter} on page {page_number}")
            return

        for street_link in street_links:
            if street_link:
                streets.append(street_link.contents[0])

    except requests.HTTPError as hp:
        pr_error(hp)
    else:
        pr_info(
            f"Fetched street names starting with {letter} successfully on page {page_number}"
        )

    return streets


def fetch_matching_street_names(street_name):
    query_url = f"{BASE_URL}/directory/search?directoryID=10251&showInMap=&keywords={street_name}&search=Search+directory"

    try:
        response = requests.get(query_url)
        response.raise_for_status()  # Raise an error for HTTP issues
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to fetch search results. Error: {str(e)}"
        )

    try:
        soup = BeautifulSoup(response.content, PARSER)
        search_results_list = soup.find_all("ul", {"class": LIST_RECORD_CLASS})
        search_results = search_results_list[0]
        children = search_results.findChildren("a", recursive=True)
        street_name_list = [
            [child.contents.pop(), BASE_URL + child["href"]] for child in children
        ]
    except IndexError:
        raise HTTPException(
            status_code=404, detail=f"No addresses found that match {street_name}"
        )

    return street_name_list


def get_pdf_link(street_name_list):
    if not street_name_list:
        raise HTTPException(status_code=404, detail="No addresses provided.")

    for address in street_name_list:
        url = address[1]  # Assume the URL is at index 1
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for HTTP issues
        except requests.RequestException as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to fetch URL: {url}. Error: {str(e)}"
            )

        try:
            soup = BeautifulSoup(response.content, "html.parser")
            editor_divs = soup.find_all("div", {"class": "definition__editor"})
            if not editor_divs:
                continue  # Skip if no matching divs are found

            links = editor_divs[0].findChildren("a", recursive=True)
            if links:
                return links[0]["href"]  # Return the first valid link
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error processing content from {url}: {str(e)}"
            )

    # If no valid link is found after processing all entries
    raise HTTPException(
        status_code=404, detail="No PDF link found for the provided addresses."
    )


def download_pdf_file(street_name):
    try:
        pr_info(f"Searching Edinburgh Council for '{street_name}'.")
        street_name_list = fetch_matching_street_names(street_name)
        pdf_link = get_pdf_link(street_name_list)
        response = requests.get(pdf_link)
        response.raise_for_status()  # Ensure the PDF link is valid

        pr_info("Downloading PDF file.")
        with open("temp/bin_calendar_temp.pdf", "wb") as pdf:
            pdf.write(response.content)
            pr_info("PDF file downloaded and saved successfully.")

    except HTTPException as e:
        # Log and re-raise the HTTPException as is
        pr_error(f"HTTPException: {e.detail} (status: {e.status_code})")
        raise e
    except requests.RequestException as e:
        # Handle any issues with the PDF download
        pr_error(f"Failed to download the PDF: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to download the PDF file.")
    except Exception as e:
        # Handle unexpected errors and log them
        pr_error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while downloading the PDF.",
        )
