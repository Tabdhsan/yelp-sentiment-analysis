import openai
from API_KEYS import OPEN_AI_KEY

CHEAP_MODEL = "text-curie-001"
EXP_MODEL = "text-davinci-003"
GPT_MODEL = "gpt-3.5-turbo"
openai.api_key = OPEN_AI_KEY

def get_info_about_graphs(graph1, graph2):

    graph1Text = ', '.join(f'({x}, {y})' for x, y in graph1)
    graph2Text = ', '.join(f'({x}, {y})' for x, y in graph2)

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""
                I have two graphs where the x axis is Year and the y axis is Rating. The first graph has the folowing values in (x,y) format: {graph1Text}. The second graph has the following values in (x,y) format: {graph2Text}. Return a one paragaph blurb about the general trends of the graphs and potential reasons why they are following these trends. For context, the ratings are yelp ratings out of 5 stars.
                """
            }
        ],
    )
    gpt_summary = res.choices[0].message.content

    return gpt_summary

