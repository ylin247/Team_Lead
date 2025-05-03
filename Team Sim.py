import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# A simple OpenAI LLM wrapper
class OpenAILLM:
    def __init__(self, model="gpt-4"):
        self.model = model

    def generate(self, messages, temperature=0.5):
        try:
            # Use the openai.chat.completions.create API
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,  # Added temperature parameter
                max_tokens=200 # increased max tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in OpenAILLM.generate: {e}")
            return None

# Define Agent class
class Agent:
    def __init__(self, role, goal, backstory, llm):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = llm

    def generate_response(self, conversation_history, temperature=0.5):
        """
        Generates a response based on the conversation history.

        Args:
            conversation_history (list): A list of messages representing the conversation so far.
            temperature (float, optional): The temperature for the OpenAI API call. Defaults to 0.5.

        Returns:
            str: The agent's response, or None on error.
        """
        # Construct the messages list, including the system message and conversation history
        messages = [
            {"role": "system", "content": self.backstory},
        ] + conversation_history
        
        response = self.llm.generate(messages, temperature)
        return response

    def __repr__(self):
        return f"{self.role}: {self.goal}"

# Define agents with more detailed backstories and goals
lead_designer = Agent(
    role='Lead Designer',
    goal='Ensure all members complete their tasks, approve sketch designs and CAD models, and guide the team to create a functional and aesthetically pleasing alarm clock.',
    backstory='You are a seasoned lead designer with a keen eye for detail and a passion for innovation. You value collaboration and clear communication. You are highly extraverted and agreeable, but also assertive when necessary to keep the project on track. You have a strong understanding of both the artistic and technical aspects of product design.',
    llm=OpenAILLM()
)

cad_designer = Agent(
    role='CAD Designer',
    goal='Create accurate and detailed digital models for the alarm clock using CAD software, ensuring they meet the design specifications and are suitable for manufacturing.',
    backstory='You are a highly skilled CAD designer with years of experience in creating 3D models for various products. You are proficient in multiple CAD software packages and have a strong understanding of engineering principles. You are detail-oriented, precise, and enjoy the challenge of translating design concepts into virtual prototypes. You are highly extraverted and agreeable, and enjoy collaborating with other designers.',
    llm=OpenAILLM()
)

hardware_engineer = Agent(
    role='Hardware Engineer',
    goal='Design the electronic hardware components of the alarm clock, including the circuitry, power supply, display, and user interface, ensuring they fit within the CAD model and meet the functional requirements.',
    backstory='You are a highly experienced hardware engineer specializing in embedded systems and circuit design. You have a deep understanding of electronic components and their applications. You are analytical, methodical, and enjoy solving complex technical challenges. You are high in extraversion and agreeableness, and communicate technical information clearly.',
    llm=OpenAILLM()
)

presenter = Agent(
    role='Presenter',
    goal='Effectively communicate the design progress and key features of the alarm clock to the client, gather feedback, and ensure that the final product meets the client’s needs and expectations.  You are also responsible for managing client expectations and addressing any concerns.',
    backstory='You are a skilled communicator and presenter with a background in marketing and client relations. You have a knack for building rapport with clients and understanding their needs. You are outgoing, enthusiastic, and passionate about the products you represent. You are very extroverted and agreeable, and excel at bridging the gap between the design team and the client.',
    llm=OpenAILLM()
)

prototype_developer = Agent(
    role='Prototype Developer',
    goal='Build a functional physical prototype of the alarm clock based on the approved CAD models and hardware designs, ensuring it meets the design specifications and is suitable for testing and evaluation.',
    backstory='You are a highly skilled prototype developer with expertise in various fabrication techniques and materials. You have a hands-on approach and enjoy the challenge of bringing designs to life. You are resourceful, creative, and adept at problem-solving. You are highly extraverted and agreeable, and enjoy working with your hands.',
    llm=OpenAILLM()
)

industrial_engineer = Agent(
    role='Industrial Engineer',
    goal='Create initial sketch designs for the alarm clock, considering both aesthetics and functionality, and present them to the lead designer for approval.  Focus on generating a variety of design options.',
    backstory='You are a long-time industrial engineer with a proven track record of creating successful designs for a wide range of products. You have a strong understanding of design principles, manufacturing processes, and user needs. You are creative, innovative, and enjoy brainstorming new ideas. You are highly extraverted and agreeable, and enjoy collaborating with other designers in the early stages of the design process.',
    llm=OpenAILLM()
)

client = Agent(
    role='Client',
    goal='Clearly communicate your needs and preferences for the alarm clock to the design team, provide feedback on their designs, and ensure that the final product meets your requirements for functionality, aesthetics, and usability. You want an alarm clock that is both stylish and easy to use.',
    backstory='You are a busy professional who values both style and functionality. You have a clear idea of what you want in an alarm clock: it should be modern, aesthetically pleasing, easy to use, and reliable. You are willing to provide constructive feedback to the design team to ensure that the final product meets your needs. You are not part of the design team, but the client the team is designing for.',
    llm=OpenAILLM()
)

# Define a function for the simulated conversation with user influence
def simulate_conversation(agents, initial_prompt, rounds=5, temperature=0.5):
    """
    Simulates a conversation with user input after each round.

    Args:
        agents (list): A list of Agent objects participating in the conversation.
        initial_prompt (str): The initial prompt to start the conversation.
        rounds (int, optional): The number of rounds in the conversation. Defaults to 5.
        temperature (float, optional): The temperature for the OpenAI API calls. Defaults to 0.5.

    Returns:
        list: A list of dictionaries, where each dictionary contains the agent's role and their response.
    """
    conversation_history = []  # Changed to a list of messages
    responses = []
    
    # Add the initial prompt as the first message in the conversation history
    conversation_history.append({"role": "user", "content": initial_prompt})

    for i in range(rounds):
        for agent in agents:
            # Generate the response for the agent based on the conversation history
            agent_response = agent.generate_response(conversation_history, temperature)
            
            if agent_response is None:
                print(f"\n{agent.role} failed to generate a response.")
                continue  # Skip to the next agent
            
            # Append the agent's response to the conversation history
            conversation_history.append({"role": "assistant", "content": agent_response})
            
            # Store the agent's response
            responses.append({
                "agent": agent.role,
                "response": agent_response
            })
            
            # Print each agent's response for tracking the conversation
            print(f"\n{agent.role} says:\n{agent_response}")
        
        # Prompt the user to steer the conversation
        user_input = input("\nEnter a new prompt to steer the conversation (or press Enter to continue): ")
        if user_input.strip():
            conversation_history.append({"role": "user", "content": user_input.strip()})

    return responses

# Create a list of agents
agents = [
    lead_designer,
    cad_designer,
    hardware_engineer,
    presenter,
    prototype_developer,
    industrial_engineer,
    client
]

# Starting prompt for the conversation
initial_prompt = "The team of designers and the client are having a discussion about designing a new alarm clock. Each agent will contribute their opinion and ideas."

# Simulate a conversation with 5 rounds
conversation_log = simulate_conversation(agents, initial_prompt, rounds=5, temperature=0.7) 
