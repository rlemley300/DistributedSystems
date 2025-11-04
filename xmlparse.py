import xml.etree.ElementTree as ET
import sys
import os
if len(sys.argv) != 4:
    print("Error: Invalid number of arguments.")
    print("Usage: python xmlparse.py plant_catalog.xml plantName percentChange")
    sys.exit(1)
xml_file = sys.argv[1]
searchName = sys.argv[2]
try:
    percent = float(sys.argv[3]) 
    if not (-90 < percent < 100):
        print(f"Error: Percent change ({percent}%) is outside the valid range of -90 to 100.")
        sys.exit(1)
except ValueError:
    print(f"Error: Invalid percentChange '{sys.argv[3]}'. Must be a number.")
    sys.exit(1)
if not os.path.exists(xml_file):
    print(f"Error: The file '{xml_file}' was not found.")
    sys.exit(1)
try:
    tree = ET.parse(xml_file)
except ET.ParseError as e:
    print(f"Error parsing XML file '{xml_file}': {e}")
    sys.exit(1)
root = tree.getroot()
plant_found = False
output_file = "plant_catalog_updated.xml"
for plant in root.findall('PLANT'):
    common_name_element = plant.find('COMMON')
    if common_name_element is not None and common_name_element.text == searchName:
        plant_found = True
        price_element = plant.find('PRICE')     
        if price_element is not None:
            try:
                current_price = float(price_element.text)
                current_price_cents = current_price * 100
                percent_multiplier = 1 + (percent / 100)
                new_price_cents = int(current_price_cents * percent_multiplier)
                new_price = new_price_cents / 100.0
                new_price_string = f"{new_price:.2f}"
                price_element.text = new_price_string
                print(f"Successfully found '{searchName}'.")
                print(f"Original price: ${current_price:.2f}")
                print(f"Applying {percent}% change. New price: ${new_price_string}")
            except ValueError:
                print(f"Error: Found '{searchName}' but its price '{price_element.text}' is not a valid number.")
            except Exception as e:
                print(f"An error occurred during price calculation: {e}")
        else:
            print(f"Error: Found '{searchName}' but it has no <PRICE> tag.")
        break
if not plant_found:
    print(f"Plant with common name '{searchName}' not found in '{xml_file}'.")
else:
    try:
        tree.write(output_file)
        print(f"Successfully updated XML and saved to '{output_file}'.")
    except IOError as e:
        print(f"Error: Could not write updated XML to '{output_file}': {e}")
