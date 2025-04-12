
import openai

import time

from helper import get_env, file_helper, agent_get_func_helper
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents import Tool
from langchain.agents import create_react_agent
from langchain.memory import ConversationBufferMemory

from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
) 

# GET API KEY
DEEPSEEK_API_KEY= get_env.retreive_value( "DEEPSEEK_API_KEY")
MISTRAL_API_KEY = get_env.retreive_value( "MISTRAL_API_KEY")
OPENAI_API_KEY  = get_env.retreive_value( "OPENAI_API_KEY")
openai.api_key  = OPENAI_API_KEY

AGENT_MODEL     =  get_env.retreive_value( "AGENT_MODEL_MISTRAL")

ACTIONPLAN_VECTOR = "vector_db"

 
POPERTY_PATH = get_env.retreive_value( "PROPERTY_PATH")
POPERTY = file_helper.read_json( POPERTY_PATH ) 

template_str     = POPERTY.get("template_str")
tool_description = POPERTY.get("tool_description")

def agent_executor( payload ):
    
    age        = payload.age
    gene_fault = payload.gene_fault
    category   = payload.category
    patient_question = payload.patient_question
    
    
    start_time = time.time()
    
    # GET CHAT MODEL v
    chat_model = agent_get_func_helper.get_chat_model("mistral") 
    
    
    # SYSTEM
    system_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["context"],
            template=template_str,
        )
    )

    # HUMAN
    human_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["question"],
            template="{question}",
        )
    )

    # COMBIME MESSAGE
    messages = [system_prompt, human_prompt]

    # SET UP PROMPT TEMPLATE
    prompt_template = ChatPromptTemplate( input_variables=["context", "question"], 
                                          messages=messages, )
    vectordb = Chroma(
            persist_directory=ACTIONPLAN_VECTOR,
            embedding_function=OpenAIEmbeddings(),
    )

    retriever = vectordb.as_retriever(search_type="similarity", 
                                      search_kwargs={"k": 20})

    vector_chain = (
            {"context": retriever, "question":  RunnablePassthrough() }
            | prompt_template
            | chat_model
            | StrOutputParser()
    )

    tools = [
        Tool(
            name="ActionPlan",
            func=vector_chain.invoke,
            description= tool_description,
        ),
      
    ]

    # agent_prompt = hub.pull("hwchase17/openai-functions-agent") # DOWNLOAD PREBUILD PROMPT
    agent_prompt = hub.pull("hwchase17/react-chat") # Use react chat prompt that works with any llm.

    # Create Agent
    agent = create_react_agent(chat_model, tools, agent_prompt)

    # Create Agent Executor
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True) # memory to remember past conversations
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory = memory)

    # # Example Usage
    # question = "I am 30 years old and have a BRCA2 gene fault. What are the risks of developing cancer?"
    
    context = " I am at age " + str( age ) + " and I have " + gene_fault + " gene fault. " + "My question is about " + category + "."
    question = context + " " + patient_question
    
    print ( "question : ", question )
    
    response = agent_executor.invoke({"input": question})
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    result = { 
               "output": response.get("output", "No answer found"),
               "explanation": response.get("explanation", "No explanation found"),
               "intermediate_steps" : response.get("intermediate_steps", "No intermediate steps found"),
               "elapsed_time": f"{elapsed_time:.2f}",  # Format to 2 decimal places
            }

    return result

