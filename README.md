# CYOA
Python program that can parse json/yaml "story" files for a choose your own adventure

## Required packages
`yaml` and/or `json`. Install using `pip`

## Usage
Use the helper functions `loadYamlStoryFile(filepath)` or `loadJsonStoryFile(filepath)` to read a file into a python object.
Then you can use `parseStory(storyDict)` to run the story.

## Story elements
Each story element should be an object in a dictionary, identified by its string key. 
There are currently 3 types of elements: `question`, `dialogue` and `ask_var`.

The element with the string key `"start"` will be used as the beginning of the story.
Any elements that end up going (with `goto`) to the element with key `""` will end the story.

`question` elements should define a string `ask`, a list of strings `answers`, and a list of strings `goto`.
When the element is run, it will ask the question from `ask`.
Then it will continue asking for a response till an answer from `answers` is given by the user.
It will then use the index of that answer in `answers` as an index in `goto` for the next element to run.
<details>
    <summary>Example (json)</summary>

```json
{
  "q": {
    "type": "question",
    "ask": "Do you want 1 or 2?",
    "answers": ["1", "2"],
    "goto": ["answer_one", "answer_two"]
  }
}
```
</details>
<details>
    <summary>Example (yaml)</summary>

```yaml
q: 
  type: question
  ask: Do you want 1 or 2?
  answers: 
  # quotation marks here are just to escape the numbers being literal
  - '1' 
  - '2'
  goto: 
  - answer_one
  - answer_two
```
</details>

`dialogue` elements should define a string `text`, a number `delay` and a string `goto`.
When the element is run, it will say the text in `text`. Then it will wait `delay` seconds, then use `goto` as the next element to run.
<details>
    <summary>Example (json)</summary>

```json
{
  "d": {
    "type": "dialogue",
    "text": "This message takes 5 seconds",
    "delay": 5,
    "goto": "after_d"
  }
}
```
</details>
<details>
    <summary>Example (yaml)</summary>

```yaml
d: 
  type: dialogue
  text: This message takes 5 seconds
  delay: 5
  goto: after_d
```
</details>

`ask_var` elements should define a string `key`, a string `ask`, and a string `goto`.
When the element is run, it will ask the text in `ask` and put the response into a variable as `key`.
These variables can be accessed along the story (in dialogue `text` and question `ask` strings) by using `${<key>}`. 
If they haven't been defined yet when an element is run, it will simple leave it as "\${<key>}".
<details>
    <summary>Example (json)</summary>

```json
{
  "a": {
    "type": "ask_var",
    "key": "name",
    "ask": "What is your name?",
    "goto": "d"
  },
  "d": {
    "type": "dialogue",
    "text": "Hello, ${name}",
    "delay": 3,
    "goto": ""
  }
}
```
</details>
<details>
    <summary>Example (yaml)</summary>

```yaml
a:
  type: ask_var
  key: name
  ask: What is your name?
  goto: d
d:
  type: dialogue
  text: Hello, ${name}
  delay: 3
  goto: ""
```
</details>

