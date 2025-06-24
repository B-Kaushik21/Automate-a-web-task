# Automate a web task

This script uses Selenium WebDriver to:
- Log in to Instagram (using dummy credentials)
- Navigate to a target profile (e.g., `cbitosc`)
- Auto-follow if not already following
- Extract details like full name, bio, posts, followers, and link
- Save the data to a text file

## How to Run
1. Clone this repo
2. Install dependencies:
```
pip install -r requirements.txt
```
4. Set your Instagram dummy username/password in `instagram.py`
5. Run the script:


## Dependencies
- Python 3.8+
- Selenium
- Chrome + matching [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)

