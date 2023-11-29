# Whatsapp Chat Analyzer and Summarizer

This is a Streamlit-based application for analyzing WhatsApp group chat data. The application allows users to upload their WhatsApp chat data, preprocesses it, and provides various analyses and visualizations to gain insights into the communication patterns within the group.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Test](#test)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nimishmedatwal/whatsapp_chat_analysis
   cd whatsapp-chat-analyzer
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Upload WhatsApp chat data: Click on the "Choose a file" button in the sidebar to upload your WhatsApp chat data in text format.

2. Select user and analyze: Choose a user from the dropdown list to view statistics and visualizations specific to that user. Click the "Show Analysis" button to generate and display insights.

3. Date Range and Model Selection: Use the sidebar to select a date range and choose a summarization model from the available options. You can also opt to generate a newsletter intro.

4. Summarize: Click the "Summarize" button to generate a summary based on the selected date range and model. The summary will be displayed below the button.

## Features

- **Statistics Area:** Provides overall statistics such as total messages, total words, media shared, and links shared.

- **Timeline Visualizations:** Presents monthly and daily timelines of message activity within the group.

- **Activity Maps:** Displays the busiest day, busiest month, and a weekly activity heatmap.

- **Most Busy Users (Group Level):** Identifies and displays the most active users in the group.

- **WordCloud:** Generates a word cloud based on the selected user's messages.

- **Most Common Words:** Displays a bar chart of the most common words used by the selected user.

- **Emoji Analysis:** Provides a dataframe and a pie chart showing the distribution of emojis used by the selected user.

- **Summarization:** Allows users to summarize the chat data within a specified date range using different summarization models. The summary can be displayed and saved.

## Test
Demo Link: [Click here](https://whatsappsummary.streamlit.app/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
