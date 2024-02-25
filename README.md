# Hidden-But-Not-For-You-


This Python script is a simple directory scanner designed to discover common directories on a target website. It utilizes a list of common directory paths and recursively searches through internal links to find additional directories.
Version 0.0.1 beta.
## How It Works

1. The script starts by defining a set of common directory paths (`COMMON_PATHS`) typically found on websites, such as admin panels, login pages, and resource directories.
2. It then defines functions to generate paths based on a target URL (`generate_paths`) and to extract internal links from HTML content (`get_internal_links`).
3. The `hidden.py` function is the core of the script. It iteratively checks each path for existence on the target website. If a directory is found, it prints a message. If recursive scanning is enabled, it also searches internal links for additional directories to explore.
4. The `main` function handles command-line arguments using `argparse`, including the target URL and an optional flag for recursive scanning.
5. Upon running the script, it prints a logo and author information, parses command-line arguments, and initiates the directory scanning process.

## Usage

1. Ensure you have Python installed on your system.
2. Install the required packages by running: `pip install requests beautifulsoup4`.
3. Save the provided Python script to a file (e.g., `hidden.py`).
4. Open a terminal or command prompt.
5. Navigate to the directory containing the script.
6. Run the script with the following command: Replace `<target_url>` with the URL of the website you want to scan. Add the `-r` flag if you want to enable recursive scanning.
7. The script will start scanning the target website for common directories and display any findings.

## Contact

For any bugs or problems, please feel free to contact the author at [Me](mailto:jjtech23@yahoo.com).
