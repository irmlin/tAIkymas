import os
from dotenv import load_dotenv

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class ConversationNotInitializedError(BaseException):
    pass


class GPT:
    def __init__(self):
        self.__language_model = ChatOpenAI(temperature=0,
                                           openai_api_key=OPENAI_API_KEY,
                                           model_name='gpt-3.5-turbo',
                                           verbose=False)

        self.__entity_memory = None
        self.__conversation = None

    def new_chat(self):
        """
        Clear the memory of previous chat and initialize new memory/context.
        NOTE: after initializing new chat, the model will generate similar/identical outputs to previous inputs.
        """
        self.__entity_memory = ConversationEntityMemory(llm=self.__language_model, k=10)
        self.__conversation = ConversationChain(
            llm=self.__language_model,
            prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
            memory=self.__entity_memory
        )

    def ask(self, question: str) -> str:
        """
        Ask language model a question and return its output
        :param question: Input to the language model
        :return: Language model output
        """
        if self.__conversation is None:
            raise ConversationNotInitializedError('Please run new_chat() method to start a conversation!')
        return self.__conversation.run(input=question)
