"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import numpy as np
import pandas as pd
import time

_LOREM_IPSUM = """
The result of your code will appear here!!!
"""
def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.1)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.1)

def Text_Len(input):
    return len(input)

st.title("Executor")

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
text = ""
with left_column:
    st.write("")
    st.write("")
    st.write("")
    text = st.text_area("Write your **Python :snake: Program** here :sunglasses:", height=600)

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    btn_cols = st.columns(8)
    with btn_cols[0]:
        st.button(" :arrow_forward: ", on_click=Text_Len(), args=(input=text))
            #st.write_stream(stream_data)
            #st.write(f"You wrote {len(text)} characters.")
    with btn_cols[1]:
        st.button(" :repeat: ")
    text = st.text_area("", height=594)





# df = pd.DataFrame({
#   'first column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })


# st.write("Printing the table with 'magic'")
# df


# st.write("Printing the table with the 'table' widget")
# st.table(df)


# st.write("Plotting a line chart of random dataframe...")
# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])
# st.line_chart(chart_data)


# st.write("Now, displaying dots in a map")
# #map_data = pd.DataFrame(
# #    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
# #    columns=['lat', 'lon'])
# #st.map(map_data)
# d = {"lat": [20.688640], "lon":[-103.351017]}
# df = pd.DataFrame.from_dict(d)
# with st.expander("map"):
#     st.map(df, size=2, use_container_width=False, zoom=10)


# st.write("Using widgets")
# x = st.slider('x')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)

# st.text_input("Your name", key="name")
# # You can access the value at any point with:
# st.session_state.name


# st.write("Using Checkboxes")
# if st.checkbox('Show dataframe'):
#     chart_data = pd.DataFrame(
#        np.random.randn(20, 3),
#        columns=['a', 'b', 'c'])
#     chart_data


# st.write("Using slectbox for options")
# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
#     })
# option = st.selectbox(
#     'Which number do you like best?',
#      df['first column'])
# 'You selected: ', option


# st.write("Control the layout of your app")
# left_column2, right_column2 = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column2.button('Press me!')

# # Or even better, call Streamlit functions inside a "with" block:
# with right_column2:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")






# with st.sidebar:
#     st.write("This is my sidebar")

#     add_selectbox = st.selectbox(
#         'How would you like to be contacted?',
#         ('Email', 'Home phone', 'Mobile phone')
#     )


#     add_slider = st.slider(
#         'Select a range of values',
#         0.0, 100.0, (25.0, 75.0)
#     )


#     'Starting a long computation...'
#     # Add a placeholder
#     latest_iteration = st.empty()
#     bar = st.progress(0)

#     for i in range(100):
#       # Update the progress bar with each iteration.
#       latest_iteration.text(f'Iteration {i+1}')
#       bar.progress(i + 1)
#       time.sleep(0.1)
#     '...and now we\'re done!'
