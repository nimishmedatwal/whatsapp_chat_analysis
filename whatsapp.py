import streamlit as st
import group_chat_summarizer 

def main():
    st.title("WhatsApp Chat Summarizer")

    # File Upload
    st.sidebar.header("Upload Chat Export File")
    chat_file = st.sidebar.file_uploader("Choose a file", type=["txt", "json"])

    if chat_file:
        st.sidebar.success("File uploaded successfully!")

        # Chat Type
        chat_type = st.sidebar.selectbox("Select Chat Type", ["WhatsApp", "Signal", "Slack"])

        # Date Range
        st.sidebar.header("Select Date Range")
        start_date = st.sidebar.date_input("Start Date", format="MM/DD/YYYY")
        end_date = st.sidebar.date_input("End Date", format="MM/DD/YYYY")
        start_date = start_date.strftime("%m/%d/%Y")
        end_date = end_date.strftime("%m/%d/%Y")

        # Model Selection
        model = st.sidebar.selectbox("Select OpenAI Model", ["models/text-bison-001"])

        generate_newsletter = st.sidebar.checkbox("Generate Newsletter Intro")

        # Summarize Button
        if st.sidebar.button("Summarize"):
            summary_file = "summary_output.txt"  #
            is_newsletter = generate_newsletter

            # Call the summarization function
            group_chat_summarizer.main(chat_type, chat_file, summary_file, str(start_date), str(end_date), is_newsletter, model)

            # Display Summary
            with open(summary_file, "r", encoding="utf-8") as summary_file:
                summary = summary_file.read()
                st.subheader("Summary")
                st.markdown(summary, unsafe_allow_html=False, help=None)


if __name__ == "__main__":
    main()
