
# create environment
python3 -m venv venv
source venv/bin/activate

# run api
pip install -r requirements.txt  
uvicorn main:app --reload 

# run ui
streamlit run interface/ui.py


# ######### ADDING NEW MODEL #########
add agent property :  utils > agent_list.json
add llm api key    :  .env 


