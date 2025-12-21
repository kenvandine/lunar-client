import requests
from bs4 import BeautifulSoup
import re
import sys

def get_highest_lunar_client_version():
    url = 'https://www.lunarclient.com/changelog'
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve the changelog page.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all div elements that may contain version information
    version_sections = soup.find_all('div')

    all_versions = []
    for section in version_sections:
        text = section.get_text(strip=True)
        if "launcher -" in text:
            # Use regex to extract the version number
            version_match = re.search(r'v(\d+\.\d+\.\d+)', text)
            if version_match:
                all_versions.append(version_match.group(1))

    if all_versions:
        #print("Found Lunar Client versions:")
        #for version in all_versions:
        #    print(version)

        # Convert version strings to tuples for comparison
        version_tuples = [tuple(map(int, v.split('.'))) for v in all_versions]
        highest_version = max(version_tuples)

        # Convert back to string format
        highest_version_str = '.'.join(map(str, highest_version))
        #print(f"\nHighest Lunar Client version: {highest_version_str}")
        return f"{highest_version_str}"
    else:
        print("No launcher version updates found in the changelog.")
        return None

if __name__ == "__main__":
    latest_version = get_highest_lunar_client_version()
    if latest_version:
        print(latest_version)
    else:
        sys.exit(1)
