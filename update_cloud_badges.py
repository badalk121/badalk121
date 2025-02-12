import requests
from bs4 import BeautifulSoup

PROFILE_URL = "https://www.cloudskillsboost.google/public_profiles/6ec7a0ac-ef9f-4bfc-98ed-639f3b0878b6"

def fetch_badges():
    response = requests.get(PROFILE_URL)
    if response.status_code != 200:
        print("Failed to fetch profile")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    badges = soup.find_all("img", class_="some-badge-class")  # Update this selector based on CloudSkillBoost's HTML structure

    badge_data = []
    for badge in badges:
        badge_url = badge["src"]
        badge_name = badge["alt"]
        badge_data.append((badge_name, badge_url))

    return badge_data

def update_readme():
    badges = fetch_badges()
    if not badges:
        return

    content = "## 🚀 Cloud Skill Boost Badges\n"
    for name, url in badges:
        content += f"[![{name}]({url})]({PROFILE_URL})\n"

    with open("README.md", "r+") as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        for line in lines:
            if "## 🚀 Cloud Skill Boost Badges" in line:
                break
            file.write(line)
        file.write(content)

update_readme()
