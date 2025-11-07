import os
import time
import requests

def ping_url(url, delay, max_trials):
    """
    Attempts to ping a URL up to max_trials times with a delay between attempts.
    Args:
        url (str): The URL to ping
        delay (int/float): The delay in seconds between attempts
        max_trials (int): The maximum number of trials
    Returns:
        bool: True if a 200 response is received, False if max_trials exceeded
    """
    trials = 0
    while trials < max_trials:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(delay)
        trials += 1
    return False

def run():
    """
    Retrieves input values from environment variables and calls ping_url.
    Environment variables expected:
        INPUT_URL: The URL to ping
        INPUT_DELAY: The delay between attempts (in seconds)
        INPUT_MAX_TRIALS: The maximum number of trials
    Raises:
        Exception: If ping_url returns False
    """
    url = os.getenv("INPUT_URL")
    delay = float(os.getenv("INPUT_DELAY", 1))
    max_trials = int(os.getenv("INPUT_MAX_TRIALS", 5))
    result = ping_url(url, delay, max_trials)
    if not result:
        raise Exception(f"Failed to ping {url} after {max_trials} attempts")
    
    github_output_path = os.getenv("GITHUB_OUTPUT")
    if github_output_path:
        with open(github_output_path, 'a') as file:
            print(f'url-reachable={result}', file=file)

if __name__ == "__main__":
    print("Hello world")
    run()