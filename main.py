import os
import json
import session
from dotenv import find_dotenv, load_dotenv
from google.cloud import dialogflowcx_v3

load_dotenv(find_dotenv())
PROJECT = os.environ["PROJECT"]
LOCATION = os.environ["LOCATION"]
AGENT_ID = os.environ["AGENT_ID"]
SESSION_ID = session.generate_session_id()

def format_response(response):
    result = {}
    link = set()
    
    rich_content = response.query_result.response_messages
    for item in rich_content:
        if item.text:
            result["answer"] = item.text.text[0]
        elif item.payload:
            for citation in rich_content[1].payload['richContent'][0][0].items():
                if str(type(citation))=="<class 'tuple'>":
                    if citation[0] == "citations":
                        value = citation[1]
                        for item in value:
                            for i in item:
                                if str(i) == "actionLink":
                                    value = item[i].split("#")[0]
                                    link.add(value)
                    result['link'] = list(link)
                else:
                    print(type(citation))
    return result

def sample_detect_intent(query, language_code="en"):
    client = dialogflowcx_v3.SessionsClient()

    query_input = dialogflowcx_v3.QueryInput()
    query_input.text.text = query
    query_input.language_code = language_code

    request = dialogflowcx_v3.DetectIntentRequest(
        session = f"projects/{PROJECT}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{SESSION_ID}",
        query_input=query_input,
    )

    # Make the request
    response = client.detect_intent(request=request)
    # print(response)
    response = format_response(response)

    return response

if __name__=="__main__":
    # query = "how many vacation leaves are there for employee"
    # query = "how to get vacation leave"
    # query = "how to apply leave with link?"
    # query = "what is Annual work from home days are allocated?"
    # query = "what is the Work from Home Request Process"
    # query = "Give me some reason to apply WFH"
    # query = "what is the purpose information policy?"
    # query = "how to manage asset, to maintain the information policy?"
    query = "what is the role of management to secure the client data?"

    # query = "tell me about information policy"
    # query = "what is dress-code policy"
    # query = "what is CNN"
    response  = sample_detect_intent(query)
    print(query)
    print(json.dumps(response, indent=4))