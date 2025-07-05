from Swarm.sim import Agent
from prompts import calendar_agent_prompt, main_agent_prompt
from calendar_tools import list_calendar_list, list_calendar_events, create_calendar_list, insert_calendar_event

MODEL= 'gpt-4o-mini'

def transfer_to_main():
    return main_agent

def transfer_to_calendar():
    return calendar_agent

main_agent = Agent(
    name='Main Agent',
    model=MODEL,
    instructions=main_agent_prompt, 
    functions=[transfer_to_calendar]
)

calendar_agent = Agent(
    name='Google Calendar Agent',
    model=MODEL,
    instructions=calendar_agent_prompt,
    functions=[transfer_to_main]
)

calendar_agent.functions.extend([list_calendar_list, list_calendar_events, insert_calendar_event, create_calendar_list])
