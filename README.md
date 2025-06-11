# Bank Review Analysis

## Overview

This project aims to scrape, store, analyze, and visualize customer reviews for various banking applications from the Google Play Store. The goal is to derive actionable insights into customer satisfaction, identify key pain points and feature requests, and compare the performance of different banks.

## Project Structure

The repository is organized as follows:

```
.github/workflows/   # CI/CD pipeline configurations
data/                # Raw and processed data files
notebooks/           # Jupyter notebooks for analysis and visualization
scripts/             # Automation scripts (e.g., data scraping, DB loading)
src/                 # Reusable source code and utility functions
tests/               # Unit tests for the source code
.env                 # Environment variables (ignored by Git)
.gitignore           # Files and directories to be ignored by Git
plan.md              # Detailed project plan
requirements.txt     # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.10
- Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd week3-insurance-assessemnt
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add the necessary credentials (e.g., for your Oracle Database).
    ```
    DB_USER=your_username
    DB_PASSWORD=your_password
    DB_DSN=your_dsn
    ```

## Usage

-   **Data Scraping and Processing:** Run the scripts in the `/scripts` directory to collect and process the data.
-   **Exploratory Data Analysis:** Use the Jupyter notebooks in the `/notebooks` directory to explore the dataset and visualize the findings.

