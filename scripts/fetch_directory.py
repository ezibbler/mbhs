import json
from bs4 import BeautifulSoup
import requests
from decouple import config

# Load environment variables
# dotenv.load_dotenv()

def get_current_staff():
    current_staff = requests.get('https://strapi.mbhs.edu/api/directory?pagination[limit]=1000').json().get('data')
    current_staff = [i['attributes']['name'] for i in current_staff]
    #print(current_staff)
    print(f'Found {len(current_staff)} current staff members')
    return current_staff

def parse_staff_directory_to_json(html_content, current_staff):

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a list to store the extracted staff information as dictionaries
    staff_info_json = []

    # Find all department headers and iterate through them
    for department_header in soup.find_all('h5', class_='bg-cyan dark-gray-text py-2 pl-2'):
        department_name = department_header.get_text(strip=True)

        # Find the sibling unordered lists for each department header
        for ul in department_header.find_next_siblings('ul', class_='box-one-light'):
            for li in ul.find_all('li'):
                # Extract staff name, title, and email
                name = li.find('span', class_='dark-gray-border').get_text(strip=True) if li.find('span', class_='dark-gray-border') else ''

                staffinfo_element = li.find('div', class_='staffinfo clearfix mtm')
                title = staffinfo_element.find('p').get_text(strip=True) if staffinfo_element else ''

                email_element = li.find('a', href=lambda x: x and x.startswith('mailto:'))
                email = email_element.get_text(strip=True) if email_element else ''

                # Append the information to the staff_info_json list as a dictionary
                staff_info_json.append({
                  #'Department': department_name,
                  'name': name,
                  'title': title,
                  'email': email,
                  "createdBy": "Python Web Scraping Script",
                  "updatedBy": "Python Web Scraping Script"
                })


    #print(staff_info_json)
    new_staff = []
    for i in staff_info_json:
      # find staff i in current staff and delete from current staff
      if i['name'] in current_staff:
        current_staff.remove(i['name'])
      else:
         new_staff.append(i['name'])
      
      # res = requests.post('https://strapi.mbhs.edu/api/directory', headers={
      #   'Authorization': f'Bearer {config("STRAPI_API_KEY")}',
      # }, json={'data': i})
      
    
    #res.raise_for_status()
    #print(res)

    # print the staff in current staff not found in mcps
    print("The following staff are no longer found in the MCPS Directory (please remove from the MBHS directory):")
    for i in range(len(current_staff)):
      print(f'{i+1}: {current_staff[i]}')

    # print the staff in mcps not found in current staff
    print("The following staff are new to the MCPS Directory and have been added to the MBHS directory:")
    for i in range(len(new_staff)):
      print(f'{i+1}: {new_staff[i]}')

    # Save the extracted data to a JSON file
    # with open(json_file_path, 'w') as jsonfile:
    #     json.dump(staff_info_json, jsonfile, indent=4)

# Specify the path to the input HTML file and the output JSON file
html = requests.get('https://ww2.montgomeryschoolsmd.org/directory/directory_Boxschool.aspx?processlevel=04757').text

# Execute the function to parse the HTML and save the data to JSON
current_staff = get_current_staff()
parse_staff_directory_to_json(html, current_staff)