# Voter List OCR Automation

This project automates the process of downloading voter list PDFs from the Election Commission of India's website. It uses Selenium for web automation and Tesseract OCR for CAPTCHA solving.

## Prerequisites

Before setting up the project, ensure you have the following installed:
- Python (>=3.8)
- Google Chrome (latest version)
- ChromeDriver (automatically managed by `webdriver_manager`)
- Tesseract OCR

### Installing Tesseract OCR
- **Windows:** Download and install Tesseract from [here](https://github.com/UB-Mannheim/tesseract/wiki). Add its installation path to the system environment variables.
- **Linux (Ubuntu/Debian):**
  ```sh
  sudo apt install tesseract-ocr
  ```
- **Mac (Homebrew):**
  ```sh
  brew install tesseract
  ```

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/your-username/voter-list-ocr.git
cd voter-list-ocr
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
```

### 3. Activate the Virtual Environment
- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```sh
  source venv/bin/activate
  ```

### 4. Install Dependencies
```sh
pip install -r requirements.txt
```

### 5. Run the Script
```sh
python main.py
```

## Notes
- The script will prompt you to manually select the Assembly Constituency before proceeding.
- If the CAPTCHA solving fails, it will retry up to 5 times before exiting.

## Troubleshooting
- **Chrome version mismatch:** If Selenium fails to start Chrome, update ChromeDriver:
  ```sh
  pip install --upgrade webdriver-manager
  ```
- **Tesseract not found:** Ensure it's installed and accessible via the system path.
- **ModuleNotFoundError:** If any module is missing, run `pip install -r requirements.txt` again.
