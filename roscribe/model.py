import os

from langchain.chat_models import ChatOpenAI


def llm_init(model_name="gpt-3.5-turbo-16k",
             temperature=0.2,
             max_tokens=10000,
             model_kwargs={'frequency_penalty':0.2, 'presence_penalty':0}):

    llm = ChatOpenAI(model_name=model_name,
                     temperature=temperature,
                     max_tokens=max_tokens,
                     model_kwargs=model_kwargs,
                     openai_api_key=os.getenv('OPENAI_API_KEY'))

    return llm
