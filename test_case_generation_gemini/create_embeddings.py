import google.generativeai as genai
import os

import textwrap
import numpy as np
import pandas as pd

def embed_fn(_model, title, text):
    return genai.embed_content(model=_model,
                             content=text,
                             task_type="retrieval_document",
                             title=title)["embedding"]

def find_best_passage(_model, query, dataframe):
    query_embedding = genai.embed_content(model=_model,
                                        content=query,
                                        task_type="retrieval_query")
    dot_products = np.dot(np.stack(dataframe['Embeddings']), query_embedding["embedding"])
    idx = np.argmax(dot_products)
    return dataframe.iloc[idx]['Text'] # Return text from index with max value

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

DOCUMENT1 = {
    "title": "Operating the Climate Control System",
    "content": "Your Googlecar has a climate control system that allows you to adjust the temperature and airflow in the car. To operate the climate control system, use the buttons and knobs located on the center console.  Temperature: The temperature knob controls the temperature inside the car. Turn the knob clockwise to increase the temperature or counterclockwise to decrease the temperature. Airflow: The airflow knob controls the amount of airflow inside the car. Turn the knob clockwise to increase the airflow or counterclockwise to decrease the airflow. Fan speed: The fan speed knob controls the speed of the fan. Turn the knob clockwise to increase the fan speed or counterclockwise to decrease the fan speed. Mode: The mode button allows you to select the desired mode. The available modes are: Auto: The car will automatically adjust the temperature and airflow to maintain a comfortable level. Cool: The car will blow cool air into the car. Heat: The car will blow warm air into the car. Defrost: The car will blow warm air onto the windshield to defrost it."}
DOCUMENT2 = {
    "title": "Touchscreen",
    "content": "Your Googlecar has a large touchscreen display that provides access to a variety of features, including navigation, entertainment, and climate control. To use the touchscreen display, simply touch the desired icon.  For example, you can touch the \"Navigation\" icon to get directions to your destination or touch the \"Music\" icon to play your favorite songs."}
DOCUMENT3 = {
    "title": "Shifting Gears",
    "content": "Your Googlecar has an automatic transmission. To shift gears, simply move the shift lever to the desired position.  Park: This position is used when you are parked. The wheels are locked and the car cannot move. Reverse: This position is used to back up. Neutral: This position is used when you are stopped at a light or in traffic. The car is not in gear and will not move unless you press the gas pedal. Drive: This position is used to drive forward. Low: This position is used for driving in snow or other slippery conditions."}

documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]
df = pd.DataFrame(documents)
df.columns = ['Title', 'Text']
df['Embeddings'] = df.apply(lambda row: embed_fn("models/embedding-001", row['Title'], row['Text']), axis=1)

query = "How do you shift gears in the Google car?"
response = find_best_passage("models/embedding-001", query, df)
print(response)

