import streamlit as st
from configuration import add_bg_from_local, configure_authors, configure_page


def main():
    configure_page()
    configure_authors()
    add_bg_from_local("data/background.png", "data/bot.png")

    st.markdown(  # Combined text and styling into one line for readability
        "<h1 style='text-align: center; color: black; font-size: 75px;'> 🤖 Fully-Fledged Trading Bot </h1> \
        <br> <br>",
        unsafe_allow_html=True,
    )

    welcome_message = '<p style="font-family:Arial Black; font-size: 20px;" align="center"> \
    This is a web app that allows you to <br> <br> \
        • Gather financial information from any financial market.  <br> \
        • Create trading strategies with various methods <br> \
        • Thoroughly backtest these strategies. <br> \
        • Compare and optimize strategy parameters <br> \
                                               <br> <br> \
        You can use the modules on the sidebar to navigate in the web app. \
    </p>'
    st.markdown(welcome_message, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
