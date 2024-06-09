import requests
import json
from dotenv import load_dotenv
import os
import random


def get_access_token():
    load_dotenv()
    username = os.getenv('API_USERNAME')
    password = os.getenv('PASSWORD')

    url = "https://api.check-promotions.kz/api/auth/sign-in/"

    payload = json.dumps({
        "username": username,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.text
    response_dict = json.loads(data)

    access_token = response_dict['accessToken']
    refresh_token = response_dict['refreshToken']

    print(f"Access Token: {access_token}\n")
    return access_token, refresh_token


def upload_img(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    script_dir = os.path.dirname(os.path.abspath(__file__))

    directory_path = os.path.join(script_dir, "bilings")

    url = "https://api.check-promotions.kz/api/tickets/upload-receipt/"

    files_list = os.listdir(directory_path)

    image_links = []
    uploaded_images = []

    for file_name in files_list:
        file_path = os.path.join(directory_path, file_name)

        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, headers=headers, files=files)
                response_text = response.text.strip('"')
                image_link = response_text if response_text.startswith(
                    "http") else None
                if image_link:
                    image_links.append(image_link)
                    uploaded_images.append(
                        {"file_name": file_name, "image_link": image_link})
                print(f"Uploaded {file_name}: {response.text}\n")
        else:
            print(f"Skipped {file_name}: Not an image file")

    print(f"[INFO] Images were uploaded successfully.\n")

    # Save the uploaded images info to a JSON file
    uploaded_images_dir = os.path.join(script_dir, "uploaded_images")
    os.makedirs(uploaded_images_dir, exist_ok=True)
    uploaded_images_path = os.path.join(
        uploaded_images_dir, "uploaded_images.json")
    with open(uploaded_images_path, 'w', encoding='utf-8') as f:
        json.dump(uploaded_images, f, ensure_ascii=False, indent=4)

    return image_links


def get_random_id(access_token):
    url = "https://api.check-promotions.kz/api/promotions/?skip=0&limit=10"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.text

    response_dict = json.loads(data)

    items = response_dict.get('items', [])

    if items:
        random_item = random.choice(items)

        random_id = random_item.get('id')

        print(f"Randomly selected ID: {random_id}\n")
        return random_id
    else:
        print("No items found in the response.")
        return None


def post_promotion(access_token, image_link):
    promotion_id = get_random_id(access_token)
    if not promotion_id:
        print("No promotion ID available.")
        return None

    url = "https://api.check-promotions.kz/api/tickets/"
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    payload = json.dumps({
        "imageLink": image_link,
        "promotionId": promotion_id
    })
    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        response_body = response.json()
    except json.JSONDecodeError:
        response_body = response.text

    report = {
        "Request Type": "POST",
        "Request Body": payload,
        "Response Code": response.status_code,
        "Response Body": response_body
    }

    if response.status_code == 500:
        error_logs_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "error_logs")
        os.makedirs(error_logs_dir, exist_ok=True)

        log_path = os.path.join(
            error_logs_dir, f"{image_link.split('/')[-1]}.json")
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=4)

    return report


def main():
    access_token, _ = get_access_token()
    image_links = upload_img(access_token)

    if image_links:
        for image_link in image_links:
            report = post_promotion(access_token, image_link)
            print(report)


if __name__ == "__main__":
    main()
