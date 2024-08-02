import requests
from bs4 import BeautifulSoup
import time

login_url = "http://bitway.asia/login/"
redirect_url = "http://bitway.asia/app/"
collect_url = "http://bitway.asia/free/?g=freebnb"

def get_user_credentials():
    user = "re9da"
    password = "@RedRaa23204004"
    return user, password

def login(session, user, password):
    payload = {
        'user': user,
        'pass': password
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36 EdgA/126.0.0.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Encoding': "gzip, deflate",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'Origin': "http://bitway.asia",
        'Referer': "http://bitway.asia/login/",
        'Accept-Language': "en-US,en;q=0.9"
    }

    response = session.post(login_url, data=payload, headers=headers)
    if response.status_code == 200 and "Logged" in response.text:
        print("Logged in successfully.")
    else:
        print("Login failed or unexpected response.")
        response.raise_for_status()

    # Update headers and cookies for further requests
    session.headers.update(headers)
    return session

def fetch_balance(session):
    response = session.get(redirect_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        balance_div = soup.find('div', class_='user-count')
        if balance_div:
            balance = balance_div.find('span').text
            print(f"Current Balance: {balance}")
        else:
            print("Balance element not found.")
    else:
        print(f"Failed to fetch balance. Status Code: {response.status_code}")

def collect_free_balance(session):
    cookies = {
        '_ga': 'GA1.1.217765984.1722487497',
        '_ga_DNV9MDR60Z': 'GS1.1.1722509076.3.0.1722509076.0.0.0',
        'PHPSESSID': '154917781aaaf573f6d53b1aa1f41327'
    }

    response = session.get(collect_url, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        balance_div = soup.find('div', class_='user-count')
        if balance_div:
            balance = balance_div.find('span').text
            print(f"Collected Balance: {balance}")
        else:
            print("Balance element not found in collected page.")
    else:
        print(f"Failed to collect balance. Status Code: {response.status_code}")

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"Countdown: {timer}", end='\r')
        time.sleep(1)
        seconds -= 1

def main():
    session = requests.Session()

    # Get user credentials
    user, password = get_user_credentials()

    while True:
        try:
            session = login(session, user, password)
            fetch_balance(session)
            collect_free_balance(session)
            # Fetch balance again after collection to see the updated amount
            fetch_balance(session)
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
        
        # Start countdown
        countdown_timer(600)  # 10 minutes in seconds

if __name__ == "__main__":
    main()