import requests
from bs4 import BeautifulSoup


def parse_time_to_minutes(time_str):
    time_str = time_str.strip()  # Remove any leading or trailing whitespace
    minutes = 0

    # Check if the time string is in the format "Xd. Yh."
    if "d." in time_str and "h." in time_str:
        days, hours_str = time_str.split("d.")
        hours = hours_str.split("h.")
        minutes = int(days.strip()) * 24 * 60 + int(hours[0].strip()) * 60

    elif "d" in time_str:
        days = int(time_str.replace("d.", "").strip())
        minutes = days * 24 * 60

    # Check if the time string is in the format "Xh. Ymin."
    elif "h." in time_str and "min." in time_str:
        hours, minutes_str = time_str.split("h.")
        minutes = int(hours.strip()) * 60 + int(minutes_str.replace("min.", "").strip())

    # Check if the time string is in the format "Xh."
    elif time_str.endswith("h."):
        hours = int(time_str.replace("h.", "").strip())
        minutes = hours * 60

    elif time_str.endswith("min."):
        minutes = int(time_str.replace("min.", "").strip())

    elif time_str == "REVIVED":
        return 0

    # Handle other cases
    else:
        print(f"Invalid time string: {time_str}")
    # Check if the time string is in the format "Xmin."

    return minutes




def extract_boss_records():
    # Make a GET request to the URL
    url = "https://shaiya-universe.com/DropList/Bosses"
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the div elements with class 'row item text-center d-flex justify-content-center'
    boss_divs = soup.find_all("div", class_="row item text-center d-flex justify-content-center")

    # Initialize an empty list to store the results
    results = []

    # Loop through each boss div and extract the required data
    for boss_div in boss_divs:
        # Extract the boss name
        boss_name = boss_div.find("b").get_text().strip()

        # Extract the location
        location = boss_div.find("span").get_text().strip()

        # Extract the respawn time and remaining time
        time_div = boss_div.find_all("div", class_="col-12 col-md-3")[-1]
        remaining_time = time_div.find("b").get_text().strip()
        respawn_time = time_div.find("span", class_="text-muted").get_text().strip()

        boss = {
            "name": boss_name,
            "location": location,
            "remaining_time": parse_time_to_minutes(remaining_time),
            "respawn_time": respawn_time
        }

        # Append the extracted data to the results list
        results.append(boss)

    # Print the results list
    return results

print(extract_boss_records())