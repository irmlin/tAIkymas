import threading
from concurrent.futures.thread import ThreadPoolExecutor

from gamecontroller.game_mode_handlers.base_handler import BaseHandler
from gamecontroller.game_state import GameState
from gamecontroller.utils import generate_animation
from gpt import GPT
from validator import InputValidator

fetching_done = False


class MultipleChoiceQuestion:
    def __init__(self, question, choices, correct_answer, explanations):
        self.question = question
        self.choices = choices
        self.correct_answer = correct_answer
        self.explanations = explanations
        self.points = 0

    def check_answer(self, selected_answer):
        selected_answer = selected_answer.upper()
        correct = selected_answer == self.correct_answer

        if correct:
            self.points += 1
            explanation = self.explanations[selected_answer]
        else:
            explanation = self.explanations[selected_answer]

        return explanation

def display_question(question):
    print(question.question)
    for key, value in question.choices.items():
        print(f"{key}. {value}")

    selected_answer = input("Enter the letter of your answer: ").upper()

    while selected_answer not in question.choices.keys():
        print("Invalid input. Please enter A, B, or C.")
        selected_answer = input("Enter the letter of your answer: ").upper()

    explanation = question.check_answer(selected_answer)
    print(explanation + '\n')

question_1 = MultipleChoiceQuestion(
    "How is Natural Language Processing (NLP) technology commonly used in recruitment?",
    {
        "A": "Analyzing candidates' CVs to help understand their skills and experience.",
        "B": "For automatic interviewing of candidates and submission of evaluations.",
        "C": "To determine the candidate's appearance and education."
    },
    "A",
    {
        "A": "Correct! Analyzing candidates' CVs using NLP technology assists in understanding their skills and experience.",
        "B": "Although NLP can help in the analysis of interview transcripts, direct automatic evaluation can be an overly complex process. This can lead to inaccuracies or incorrect conclusions, because NLP cannot fully understand contexts or emotional content. NLP technology can be useful as a support, but it is still important to keep people's judgment and decision-making.",
        "C": "NLP mostly analyzes text information, not visual content or education. NLP technology can be useful as an assistive tool, but it's still important to keep decision making and evaluation to people."
    },

)
question_2 = MultipleChoiceQuestion(
    "How can emotion recognition technology be useful in the process of evaluating employee engagement?",
    {
        "A": "To determine the leadership and communication skills of employees.",
        "B": "For identifying all employees' problems and providing them with a detailed psychological assessment.",
        "C": "For understanding the emotional state of employees at the workplace, determining their level of satisfaction."
    },
    "C",
    {
        "A": "While emotion recognition technology can help understand how employees react to certain situations, it cannot directly measure leadership ability or communication skills.",
        "B": "Although technology can help identify certain emotions and psychological states, it cannot fully and absolutely evaluate all employee problems or provide a complete psychological assessment. It can only be an initial tool, but not a complete assessment process.",
        "C": "Correct! Emotion recognition technology can be used to understand the emotional state of employees at the workplace and determine their level of satisfaction."
    },

)
question_3 = MultipleChoiceQuestion(
    "How can machine learning be useful for market segmentation?",
    {
        "A": "For the analysis of large data sets and the identification of specific user groups.",
        "B": "For accurate identification of all user behavior patterns and future market trends.",
        "C": "For accurate determination of all market segments without any inaccuracies."
    },
    "A",
    {
        "A": "Correct! Machine learning can be used to analyze large data sets and identify specific user groups for market segmentation.",
        "B": "Although machine learning can predict patterns of behavior, it cannot completely predict all future trends without any inaccuracies.",
        "C": "Machine learning can identify and determine market segments, but there may be some inaccuracies, so human interpretation is required to verify the results."
    },

)
question_4 = MultipleChoiceQuestion(
    "How can NLP (natural language processing) be useful in preparing a marketing strategy plan?",
    {
        "A": "For the development of a comprehensive marketing strategy plan, considering the language and behavior of consumers, emotions and attitudes.",
        "B": "For the automatic creation of a marketing strategy plan without human intervention.",
        "C": "To analyze large amounts of text data, helping to identify important topics and user opinions, which are useful for the formation of marketing strategy."
    },
    "C",
    {
        "A": "While NLP can help understand users' language and behavior, it may have limited ability to identify users' emotional states or accurately predict their attitudes.",
        "B": "NLP is only a tool that can help with text analysis and understanding, but not completely replace human creativity and strategic thinking.",
        "C": "Correct! NLP can be utilized to analyze large amounts of text data, identifying important topics and user opinions, which are useful for forming a marketing strategy."
    },

)
question_5 = MultipleChoiceQuestion(
    "How can machine learning be useful for calculating the need of raw materials for production?",
    {
        "A": "By analyzing historical consumption patterns and predicting future demand accurately.",
        "B": "By using machine learning algorithms to estimate raw material needs based solely on current inventory levels.",
        "C": "By randomly generating estimates for raw material needs using machine learning algorithms without data analysis."
    },
    "A",
    {
        "A": "Correct! Machine learning can analyze historical consumption patterns to predict future demand accurately, aiding in calculating raw material needs.",
        "B": "While using machine learning algorithms to estimate raw material needs based on current inventory levels might provide some insights, it's a limited approach. This method may not account for changing demand patterns, market trends, or other external factors that significantly impact raw material requirements.",
        "C": "Randomly generating estimates for raw material needs using machine learning algorithms without proper data analysis or consideration of historical patterns would result in unreliable predictions and inefficient resource planning."
    },

)
question_6 = MultipleChoiceQuestion(
    "How can AI-driven predictive maintenance enhance production planning processes in manufacturing industries?",
    {
        "A": "By employing AI models to monitor machinery but solely focusing on historical data without real-time monitoring for predictive maintenance.",
        "B": "By using AI to predict failures but implementing maintenance after breakdowns, leading to increased unplanned downtime.",
        "C": "By using AI algorithms to predict machinery failures and schedule maintenance before breakdowns occur, thus reducing unplanned downtime."
    },
    "C",
    {
        "A": "Employing AI models that only rely on historical data without real-time monitoring might miss identifying imminent failures, reducing its effectiveness in preventing unexpected breakdowns.",
        "B": "While AI can predict failures, implementing maintenance after breakdowns defeats the purpose of predictive maintenance, resulting in increased unplanned downtime rather than reducing it.",
        "C": "Correct! AI-driven predictive maintenance involves using AI algorithms to predict machinery failures and schedule proactive maintenance before breakdowns occur, thereby reducing unplanned downtime."
    },

)
question_7 = MultipleChoiceQuestion(
    "How does Machine Learning assist in optimizing inventory levels in a supply chain?",
    {
        "A": "By using Machine Learning algorithms that solely focus on predicting future inventory needs, neglecting current stock levels.",
        "B": "By analyzing historical data and demand patterns to predict future inventory needs accurately, optimizing stock levels and reducing excess inventory costs.",
        "C": "By employing machine learning to optimize inventory levels with a focus on current and historical data, enhancing stock management in typical scenarios."
    },
    "B",
    {
        "A": "Using Machine Learning algorithms that only focus on predicting future inventory needs without considering current stock levels might lead to overstocking or stockouts. Effective inventory management requires a balance between predicting future demands and considering present inventory levels for efficient stock management.",
        "B": "Correct! Machine Learning analyzes historical data and demand patterns to predict future inventory needs accurately, aiding in optimizing stock levels and reducing excess inventory costs.",
        "C": "Employing machine learning to optimize inventory levels focusing on current and historical data generally enhances stock management. However, it may not cover all variables impacting demand and inventory, potentially leading to less accurate predictions in certain situations."
    },

)
question_8 = MultipleChoiceQuestion(
    "In what ways does Natural Language Processing (NLP) contribute to inventory management systems?",
    {
        "A": "By using NLP for analyzing unstructured data like customer feedback, product descriptions, and supplier emails to gain insights, improve demand forecasting, and enhance decision-making in inventory management.",
        "B": "By employing NLP techniques to analyze customer sentiments and emotional tone in inventory-related documents, improving decision-making with nuanced insights.",
        "C": "By leveraging NLP for sentiment analysis in customer reviews, contributing to understanding demand trends and preferences to some extent."
    },
    "A",
    {
        "A": "Correct! NLP in inventory management involves analyzing unstructured data like customer feedback, product descriptions, and supplier emails to gain insights, improve demand forecasting, and enhance decision-making.",
        "B": "Analyzing customer sentiments and emotional tones within inventory-related documents using NLP might not directly impact or significantly enhance traditional inventory management decision-making. Emotional analysis in such documents may not offer actionable insights relevant to optimizing stock levels, supply chain efficiency, and warehouse operations, which are core aspects of inventory management.",
        "C": "Though NLP in customer reviews can offer insights into demand trends and preferences, it might not encompass all factors influencing demand trends, such as market dynamics, seasonality, or external economic factors, which are crucial in comprehensive demand trend analysis."
    },

)
question_9 = MultipleChoiceQuestion(
    "How does natural language processing (NLP) contribute to user development, specifically in improving the effectiveness of chatbot interactions?",
    {
        "A": "Natural language processing (NLP) enhances user development by enabling chatbots to understand and respond to user queries in a more contextually relevant and human-like manner.",
        "B": "Natural language processing (NLP) has no impact on user development, as chatbots operate solely based on pre-programmed responses and cannot adapt to user nuances.",
        "C": "Natural language processing (NLP) struggles to accurately interpret complex or ambiguous user inputs limiting its effectiveness in certain scenarios."
    },
    "A",
    {
        "A": "Correct! NLP significantly contributes to user development by enabling chatbots to understand and respond to user queries in a more contextually relevant and human-like manner.",
        "B": "Incorrect because the statement incorrectly suggests that NLP has no impact on user development and implies that chatbots operate solely based on pre-programmed responses. In reality, NLP plays a crucial role in chatbot development, allowing systems to understand and generate human-like responses by learning from data.",
        "C": "Partially correct because this answer acknowledges the contribution of NLP to user development but suggests limitations by mentioning struggles with complex or ambiguous user inputs. While NLP may face challenges in certain contexts, advancements in the field aim to address these limitations, and it is still a valuable tool for improving user interactions and understanding in various scenarios."
    },

)
question_10 = MultipleChoiceQuestion(
    "How can collaborative filtering, a recommendation system technique, contribute to enhancing user experiences in personalized content recommendations?",
    {
        "A": "Collaborative filtering facilitates user development by analyzing user behavior and preferences, recommending content based on similarities with other users, resulting in personalized and relevant suggestions that improve overall user satisfaction.",
        "B": "Collaborative filtering has no impact on user development as it relies on generic recommendations and fails to consider individual user preferences or diverse content interests.",
        "C": "Collaborative filtering is a valuable technique which struggles to recommend diverse content to users with unique preferences, limiting its effectiveness in certain scenarios and potentially leading to content homogeneity."
    },
    "A",
    {
        "A": "Correct! Collaborative filtering analyzes user behavior and preferences to provide personalized and relevant content recommendations based on similarities with other users, enhancing overall user satisfaction.",
        "B": "Incorrect because collaborative filtering is designed to provide personalized recommendations by considering similarities with other users, and it is not limited to generic suggestions. It takes into account individual user preferences and contributes significantly to user experience improvement.",
        "C": "Partially correct because this answer acknowledges the effectiveness of collaborative filtering but highlights potential limitations, such as struggling with recommending diverse content to users with unique preferences. While collaborative filtering may face challenges in certain scenarios, advancements in recommendation systems continually address these limitations, making it a valuable tool in user development."
    },

)
question_11 = MultipleChoiceQuestion(
    "How does Long Short-Term Memory (LSTM), a type of recurrent neural network, address the challenge of modeling temporal dependencies in financial data for improved forecasting accuracy?",
    {
        "A": "LSTMs excel in modeling temporal dependencies by incorporating a memory mechanism that selectively retains relevant information over extended sequences, allowing for more accurate and effective forecasting in financial data.",
        "B": "LSTMs are adept at capturing short to medium-term temporal dependencies, they encounter challenges in handling extremely long-term dependencies within financial data, potentially impacting their forecasting accuracy over extended timeframes.",
        "C": "LSTMs are irrelevant in addressing temporal dependencies in financial data, as they lack the capacity to adapt to sequential patterns and make accurate predictions in dynamic financial markets."
    },
    "A",
    {
        "A": "Correct! LSTMs excel in modeling temporal dependencies by selectively retaining relevant information over extended sequences, contributing to more accurate and effective forecasting in financial data.",
        "B": "Partially correct because the answer acknowledges LSTMs' strength in capturing short to medium-term temporal dependencies but introduces the idea that LSTMs may struggle with extremely long-term dependencies. While this is a consideration, LSTMs are still valuable for forecasting within appropriate timeframes and can be optimized for long-term dependencies with careful design and tuning.",
        "C": "Incorrect because the statement incorrectly dismisses the relevance of LSTMs in addressing temporal dependencies in financial data. LSTMs are specifically designed to excel in sequential data tasks, making them well-suited for modeling temporal dependencies and forecasting trends in dynamic financial markets."
    },

)
question_12 = MultipleChoiceQuestion(
    "In algorithmic trading, how does the application of reinforcement learning strike a balance between exploring new trading strategies and exploiting known profitable actions?",
    {
        "A": "Reinforcement learning in algorithmic trading strikes a balance by utilizing exploration-exploitation techniques. Initially, the algorithm explores various strategies to discover profitable actions.",
        "B": "Reinforcement learning aims to balance exploration and exploitation, challenges may arise in accurately determining the optimal transition point.",
        "C": "Reinforcement learning in algorithmic trading solely relies on exploiting known profitable actions, disregarding the need for continuous exploration."
    },
    "A",
    {
        "A": "Correct! Reinforcement learning in algorithmic trading incorporates exploration-exploitation techniques, initially exploring various strategies to discover profitable actions.",
        "B": "Partially correct because the answer correctly acknowledges the balance sought by reinforcement learning but introduces the challenge of determining the optimal transition point. While this is a consideration, it might not be as pronounced in well-designed reinforcement learning models. The partial correctness lies in recognizing a potential challenge in practice.",
        "C": "Incorrect because the statement incorrectly suggests that reinforcement learning solely relies on exploiting known profitable actions. In reality, reinforcement learning incorporates both exploration and exploitation phases. During exploration, the algorithm seeks new strategies, and during exploitation, it capitalizes on known profitable actions. This combination allows for continuous adaptation and improvement in trading strategies."
    },

)
questions = [
    question_1,
    question_2,
    question_3,
    question_4,
    question_5,
    question_6,
    question_7,
    question_8,
    question_9,
    question_10,
    question_11,
    question_12
]


class QuizModeHandler(BaseHandler):
    def __init__(self):
        super().__init__()

    def handle(self) -> GameState:

        # Display each question one by one
        for index, question in enumerate(questions, start=1):
            print(f"Question {index}:")
            display_question(question)

        # Calculate and display the total score after the test
        total_score = sum(question.points for question in questions)
        print(f"Total score: {total_score}/{len(questions)}")

        print(f"{'-'*100}")

        return GameState.GREETING

    def get_user_input(self, prompt) -> str:
        return ""
