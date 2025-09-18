

# AI Test Case Generator (Beginner QA Guide)

This project helps you (even if you’re new to QA or Python) automatically generate professional test cases from plain English requirements using AI.

---

## What does it do?

- Reads your requirement (user story) from a text file
- Uses AI to create a full set of QA test cases (Sanity, Functional, Boundary, Negative)
- Lets you review and export the test plan as a spreadsheet (CSV)

---

## Quick Start (Step-by-Step)

### 1. Install Python and dependencies

- Make sure you have Python 3.10+ installed (https://www.python.org/downloads/)
- Open a terminal in the project folder and run:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Get a Groq API key (for AI)

- Sign up at https://console.groq.com/ and get your API key
- Create a file named `.env` in the project folder with this line:
  ```
  GROQ_API_KEY=your_groq_api_key_here
  ```

### 3. Add your requirement

- Open `data/requirements.txt` in a text editor
- Write your user story or requirement (for example: “The system should allow login with username/password and enforce password complexity.”)

### 4. Run the workflow in Jupyter (recommended for QA)

- Open the project in VS Code or Jupyter Lab
- Open `notebooks/demo.ipynb`
- Run all cells (top to bottom)
- You’ll see a table of generated test cases and a CSV file you can use in Excel or your test management tool

---

## Project Structure (What’s in each folder?)

- `src/` – Python code for the workflow and exporting test cases
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

| test_case_id | test_title | description | ... |
|--------------|------------|-------------|-----|
| 1            | Login with valid credentials | ... |
| 2            | Login with invalid password  | ... |

---

## License

MIT License
