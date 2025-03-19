Sure! Here's the `README.md` formatted in a GitHub style for better readability:

```markdown
# Telegram Chat Participant Parser

A Python script that allows you to extract and manage participant data from Telegram chat groups using the **Telethon** library. This script supports retrieving participant information, exporting data to CSV format, and handling multiple Telegram chat groups.

---

## Features

- Extracts **detailed participant data** from Telegram chat groups.
- **Exports data to CSV format** with participant details.
- **Supports large groups** by paginating through participants.
- **Handles multiple Telegram accounts** using API credentials.
- **Easy setup** via a `.env` file for API keys.

---

## Requirements

- Python 3.7+ (recommended)
- [`telethon`](https://github.com/LonamiWebs/Telethon) library
- `.env` file for API credentials

---

## Installation

1. **Clone this repository:**

    ```bash
    git clone https://github.com/YuryyBright/ParserChat.git
    cd ParserChat
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your Telegram API credentials:**
   - Sign up for a Telegram developer account at [https://my.telegram.org](https://my.telegram.org).
   - Create a new application to get your **API ID** and **API Hash**.
   - Create a `.env` file in the root of the project with the following variables:

    ```.env
    TELEGRAM_API_ID=your_api_id
    TELEGRAM_API_HASH=your_api_hash
    ```

---

## How It Works

1. **Authenticate with Telegram** using the `API_ID` and `API_HASH` provided in the `.env` file.
2. **Fetch the list of chats** the authenticated user is part of.
3. **Parse participants** of a selected chat, extracting details such as:
   - ID
   - Username
   - First name
   - Last name
   - Phone number (if available)
   - Bot status
   - Premium status
4. **Export the data to a CSV** file for easy analysis and reporting.

---

## Usage

1. **Run the script:**

   ```bash
   python parser.py
   ```

2. **Follow the on-screen instructions** to:
   - Select a Telegram chat from your available chats.
   - Parse participants and export data to a CSV file.

    Example output:

    ```
    Доступні чати:
    1. Chat Group 1 (ID: 123456789)
    2. Chat Group 2 (ID: 987654321)
    Введіть номер чату:
    Всього учасників: 100
    ID: 12345, Username: @user1
    ID: 67890, Username: @user2
    ...
    ```

3. The **exported CSV file** will be saved in the current directory with a timestamped filename, e.g., `chat_participants_20250319_153045.csv`.

---

## Code Structure

- **`parser.py`**: Main entry point for running the script.
- **`requirements.txt`**: Lists all required dependencies.
- **`.env`**: Stores your Telegram API credentials.

---

## Contributing

Feel free to fork and contribute to this project! If you find bugs or want to add features, create a pull request with your changes.

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

```

---

### Highlights of the GitHub Markdown:

- **Headers** for easy navigation.
- **Code blocks** for commands and file content.
- Clear distinction between sections.
- **Links** for external resources like the Telethon library and contact email.
- **Lists** for quick reference (features, steps).

This format should make it visually appealing and easy to follow on GitHub! Let me know if you need further adjustments.
