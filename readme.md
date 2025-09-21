



# AI Test Case Generator (Step-by-Step Beginner QA Guide)

This project helps you (even if you’re new to QA or Python) automatically generate professional test cases and Playwright E2E scripts from plain English requirements using AI.

---

## What is this?

This tool can:
- Read your requirement (user story) from a text file and use AI to create a full set of QA test cases (Sanity, Functional, Boundary, Negative), and lets you review and export the test plan as a spreadsheet (CSV).
- Generate Playwright end-to-end (E2E) test scripts from a plain English test scenario and a target website URL.

---

## Step 1: Install Python

If you don’t have Python yet:
- Go to https://www.python.org/downloads/
- Download and install Python 3.10 or newer (make sure to check "Add Python to PATH" during install)

---

## Step 2: Set up your project folder

Open a terminal (Command Prompt or PowerShell on Windows, Terminal on Mac/Linux) and navigate to your project folder. Example:

```
cd path/to/ai-test-generator
```

---

## Step 3: (Recommended) Create a virtual environment

This keeps your dependencies isolated.

On Windows:
```
python -m venv venv
venv\Scripts\activate
```
On Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

---

## Step 4: Install dependencies

With your virtual environment activated, run:
```
pip install -r requirements.txt
```

---

## Step 5: Get a Groq API key (for AI)

1. Sign up at https://console.groq.com/ and get your API key
2. In your project folder, create a file named `.env` (no filename, just ".env")
3. Add this line to `.env` (replace with your real key):
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

---

## Step 6: Add your requirement

1. Open `data/requirements.txt` in a text editor
2. Write your user story or requirement (for example: “The system should allow login with username/password and enforce password complexity.”)

---


## Step 7A: Generate a QA Test Plan (CSV) using the notebook

1. Open the project in VS Code or Jupyter Lab (install Jupyter if you don’t have it: `pip install jupyter`)
2. Open `notebooks/demo.ipynb`
3. Run all cells (top to bottom)
4. You’ll see a table of generated test cases and a CSV file you can use in Excel or your test management tool

---

## Step 7B: Generate a QA Test Plan (CSV) from the command line

You can also run the workflow as a script (no notebook needed):

```
cd src
python generate_test_plan.py
```
This will read your requirement from `data/requirements.txt` and output a CSV file with the generated test cases.

---

## Step 7C: Generate Playwright E2E Test Scripts from English

You can use the Playwright script generator to turn a plain English scenario and a website URL into Playwright code:

```
cd src
python generate_playwright_tests.py
```
You can edit the script to change the `query` (what you want to test) and `target_url` (the website to test) at the bottom of `generate_playwright_tests.py`.

The script will:
- Break down your scenario into atomic actions
- Generate Playwright code for each action
- Print the generated code and final state to the terminal

---


## Project Structure (What’s in each folder?)

- `src/` – Python code for the workflow and exporting test cases
  - `generate_test_plan.py` – Script to generate a QA test plan (CSV) from requirements
  - `generate_playwright_tests.py` – Script to generate Playwright E2E code from English and a website URL
- `notebooks/` – The main demo notebook for QA (run this!)
- `data/` – Where you put your requirements
- `outputs/` – Where your generated test cases will be saved

---

## QA Best Practices & Tips

- **Review the generated test cases:**
  - Make sure all requirement details are covered
  - Check for missing edge cases or negative scenarios
- **Customize the prompt:**
  - You can edit the prompt in the notebook to match your company’s QA style
- **Export and share:**
  - Use the CSV output to import into Jira, TestRail, or share with your team
- **Iterate:**
  - If the test plan isn’t perfect, tweak your requirement or the prompt and re-run

---

## Troubleshooting (Common QA Issues)

- **No test cases generated?**
  - Check your API key and requirement file
- **Error about prompt/model fields?**
  - Make sure the fields in the prompt and the code match (e.g., test_case_id, test_title, etc.)
- **Can’t export or open CSV?**
  - Make sure you have write permissions to the `outputs/` folder

---


## Example Output

### Test Plan CSV

| test_case_id | test_title | description | ... |
|--------------|------------|-------------|-----|
| 1            | Login with valid credentials | ... |
| 2            | Login with invalid password  | ... |

### Playwright Script Output

The Playwright script generator will print Python code for each action, for example:

```
from playwright.async_api import async_playwright
import asyncio
async def generated_script_run():
  async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page()
    await page.goto("https://example.com/")
    # ... more actions ...
    await browser.close()
```

---

## License

MIT License
