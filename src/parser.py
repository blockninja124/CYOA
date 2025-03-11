import time
import yaml
from yaml.scanner import ScannerError
import json
from json import JSONDecodeError
import re

class ParseStoryError(Exception):
    pass

story_variables = {}

def parseText(text):
    global story_variables
    return re.sub(r'\$\{(\w+)\}', lambda m: story_variables.get(m.group(1), m.group(0)), text)
    
def parseNode(nodeJson):
    try:
        if nodeJson["type"] == "question":
                        
            while True:
                answer = input(parseText(nodeJson["ask"]))
                
                for index, possible_answer in enumerate(nodeJson["answers"]):
                    if answer.lower() == possible_answer.lower():
                        # technically, the user always has to hit this return statement
                        return nodeJson["goto"][index]
                print("Invalid response. Please enter "+", ".join(nodeJson["answers"]))

        if nodeJson["type"] == "dialogue":
            print(parseText(nodeJson["text"]))
            
            if "delay" in nodeJson:    
                time.sleep(nodeJson["delay"])
            
            return nodeJson["goto"]
        
        if nodeJson["type"] == "set_var":
            story_variables[nodeJson["key"]] = nodeJson["value"]
            return nodeJson["goto"]
        
        if nodeJson["type"] == "ask_var":
            answer = input(parseText(nodeJson["ask"]))
            story_variables[nodeJson["key"]] = answer
            return nodeJson["goto"]

    except KeyError as e:
        raise ParseStoryError("Expected key '"+e.args[0]+"' wasn't found in node")


def parseStory(storyJson):
    next_node = "start"
    
    while True:
        try:
            next_node = parseNode(storyJson[next_node])
            
            # Leave loop if "goto": ""
            if next_node == "":
                break
            
        except ParseStoryError as e: 
            raise ParseStoryError("Error while parsing node '" + next_node + "': " + e.args[0])
        
        except KeyError as e:
            raise ParseStoryError("Node '"+e.args[0]+"' wasn't found in story")
        
def loadJsonStoryFile(filepath):
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
            
    except JSONDecodeError:
        raise ParseStoryError("File '"+filepath+"' isn't a valid JSON file")
    
    except FileNotFoundError:
        raise ParseStoryError("File '"+filepath+"' doesn't exist")
    
    else:
        return data
    
def loadYamlStoryFile(filepath):
    try:
        with open(filepath, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise ParseStoryError("File '"+filepath+"' doesn't exist")
    except ScannerError:
        raise ParseStoryError("File '"+filepath+"' isn't a valid YAML file")
    
parseStory(loadYamlStoryFile("story.yaml"))
