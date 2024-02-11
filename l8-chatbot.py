import os
from openai import OpenAI
import panel as pn  # GUI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,
                                              messages=messages,
                                              temperature=0)
    return response.choices[0].message.content

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(model=model,
                                              messages=messages,
                                              temperature=temperature)
    return response.choices[0].message.content

def collect_messages(event):
    prompt = inp.value
    inp.value = ''  # Clear the input after getting the value
    context.append({'role': 'user', 'content': f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
    chat_area.objects = panels  # Update the chat area with new panels

def end_chat(event):
    chat_area.objects.append(pn.pane.Markdown("### Chat Ended", width=600, style={'background-color': '#FFCCCC'}))
    inp.disabled = True  # Disable input
    button_conversation.disabled = True  # Disable conversation button
    button_end_chat.disabled = True  # Disable end chat button

pn.extension()

panels = []  # collect display

context = [{'role': 'system', 'content': """...""" }]  # Update with the health advice context

inp = pn.widgets.TextInput(placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Send", button_type="primary")
button_end_chat = pn.widgets.Button(name="End Chat", button_type="danger")

button_conversation.on_click(collect_messages)
button_end_chat.on_click(end_chat)

chat_area = pn.Column(*panels)  # Dynamic chat area to append messages

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation, button_end_chat),
    chat_area,
)

def show_dashboard():
    dashboard.show()

show_dashboard()
