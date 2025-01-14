import sys, requests, json
from bs4 import BeautifulSoup
from datetime import datetime

def get_count_from_package_manager(package_name: str) -> int:

    endpoint = "https://rhinopackages.blob.core.windows.net/packages/data.json"
    response = requests.get(endpoint)
    response.raise_for_status()

    raw_data = response.text
    packages = json.loads(raw_data)

    download_count = 0
    for package in packages:
        if package["id"].lower() == package_name:
            download_count = package["downloads"]
            break;

    return download_count

def get_count_from_food4rhino(package_name: str) -> int:

    endpoint = f"https://www.food4rhino.com/en/app/{package_name}"
    response = requests.get(endpoint)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    element_type = "div"
    element_class = "downloads-count"
    element = soup.find(element_type, class_=element_class)

    download_count = 0
    if element:
        download_count = int(element.text.strip())

    return download_count

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\n\nError! Package name missing.\n")
        sys.exit(1)
    
    else:
        package_name = sys.argv[1]
        print(f"\n\nSearching for {package_name}...")

        pm_count = get_count_from_package_manager(package_name)
        f4r_count = get_count_from_food4rhino(package_name)

        now = datetime.now()
        print(now.strftime("\n\n%d %b, %Y \t\t\t %H:%M"))
        print("- - - - - - - - - - - - - - - - - - - -")
        
        print(f"Package Manager Downloads:  {pm_count}")
        print(f"Food4Rhino.com Downloads :  {f4r_count}")
        print(f"Total Downloads          :  {pm_count + f4r_count}")

        print("\n")
