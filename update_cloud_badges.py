import requests
from bs4 import BeautifulSoup

PROFILE_URL = "https://www.cloudskillsboost.google/public_profiles/6ec7a0ac-ef9f-4bfc-98ed-639f3b0878b6"

def fetch_badges():
    response = requests.get(PROFILE_URL)
    if response.status_code != 200:
        print("Failed to fetch profile")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    badges = soup.find_all("img")  # Modify selector if needed

    badge_data = []
    for badge in badges:
        badge_url = badge["src"]
        badge_name = badge.get("alt", "Cloud Badge")
        badge_data.append((badge_name, badge_url))

    return badge_data

def update_readme():
    badges = fetch_badges()
    if not badges:
        return

    new_badge_section = "<!-- START_CLOUD_BADGES -->\n"
    for name, url in badges:
        # new_badge_section += f"[![{name}]({url})]({PROFILE_URL})\n"
        new_badge_section += f'<a href="{PROFILE_URL}"><img src="{url}" alt="{name}" width="200"></a>\n'
    new_badge_section += "\n<!-- END_CLOUD_BADGES -->"

    with open("README.md", "r+") as file:
        content = file.read()
        start = content.find("<!-- START_CLOUD_BADGES -->")
        end = content.find("<!-- END_CLOUD_BADGES -->") + len("<!-- END_CLOUD_BADGES -->")

        if start != -1 and end != -1:
            content = content[:start] + new_badge_section + content[end:]
        else:
            content += "\n" + new_badge_section

        file.seek(0)
        file.truncate()
        file.write(content)

update_readme()
