# Discord Lore Bot

#### Video Demo:  https://youtu.be/himrocH5toU

### Description:
Say hello to Lore Bot, your ultimate companion for TTRPG servers! Lore Bot is designed to assist new and seasoned players by providing quick, comprehensive answers to fandom lore questions. It seamlessly integrates into your Discord server, ensuring everyone has access to the rich histories, characters, and worlds that make your campaigns extraordinary. With real-time web scraping, advanced natural language processing, and cutting-edge AI summarization, LoreBot brings the essence of your favorite fandoms right to your fingertips.

Some of the technologies used for this project include: 
    - Python: The backbone of Lore Bot, providing robust and efficient scripting capabilities.
    - Discord.py: Powers the bot's seamless integration and interaction within Discord.
    - BeautifulSoup: Scrapes the web for up-to-date lore and information from various fandom websites.
    - SpaCy: Utilizes natural language processing to clean and format the scraped data.
    - OpenAI API: Leverages GPT-4o-mini for advanced text summarization and contextual understanding.
    - YAML: Manages and organizes fandom URLs and cache data for efficient access.
    - Requests: Handles HTTP requests to fetch data from the web.

For this project, I have created three Python files that handle running the bot, the Discord logic need to integrate the bot into a server as well as give it command functionality, and the logic the bot uses in order to take a website, scrape it, and generate a short and digestible response for the user regarding their respective fandom inquiry. Aditionally, I created a .env file that has been ignored by Git in order to maintain the Discord token and the OpenAI token secure. 

1. main.py
    This file contains only a few lines of code pertaining to simply just running the bot. At the top of the file the following have been imported: a bot.py file, the load_dotenv functionality from the dotenv library, and the os library. load_dotenv together with os load the Discord token from the .env file found in the project in order to give the bot access to Discord functionalities.

2. bot.py
    This file contains the programming logic that sets up the bot for Discord integration. At the top of the file the Discord library, the commands functionality from the discord.ext library, the lore data  dictionary initialized in responses.py and the process question function from the responses.py file have been imported so that the bot can process the question here, the bot.py file. In this file, intents have been set to the default setting and have been set as True in order to allow for user messages to go through by using the assigned bot command so that the bot can proceed to analyze it. Afterwards, the bot command has been initialized with a line of code that utilizes the .Bot method on the 'commands' object. The first parameter of the .Bot method assigns the prefix for the command as '!' and the second parameter assigns the intents as intents. 
    
    A bot event has been initiated followed by an async function that has been defined, allowing a programmer to check if the bot has succesfully logged into their desired Discord server by printing a message in the terminal as: "We have logged in as Lore Bot#1215". Below that line, a bot command name assignment has been initiated, assigning the command name 'ask'. 
    
    Finally, another async function called ask has been defined that allows the bot to process the question the user asks in Discord. This function contains three parameters: ctx (which stands for context and), is an intance of 'discord.ext.commands.Context' passed automatically by the Discord.py library when a command is invoked and contains information about the invocation context such as the message that triggered the command, the channel it was triggered in, the author of the message, the guild (server) in which the command was used, and the methods to send messages as well as interact with Discord; the * (astericks) parameter is there to indicate that the question parameter is a keyword-only argument; within the response variable is stored the answer that the lore bot has generated calling the process_question function, found in the responses.py logic, which contains the question and lore_data parameters; finally the await keyword is used due to ctx.send being an async function,needing some time to wait for it to complete. The ctx.send method is used to send a message back to the channel where the command was invoked.

3. responses.py
    This file contains the logic that the bot uses to to process the question, scrape for information, and generate an output message to the user asking the question. First, at the top of the file the following libraries have been imported: bs4 from BeautifulSoup, dotenv from load_dotenv, requests, spacy, os, yaml, re, and openai. 

    A SpaCy model has been initiated with English functionality in order to perform natural language processing on the webscrapped data retrieved from the fandom url page. The decision to use the SpaCy library over others out there was due to the following reasons: SpaCy is optimized for performance, meaning it can handle large-scale, real-time requirements for this Discord bot to work efficiently; it has a user-friendly API where implementation and maintanance of NLP tasks are easier; it possess state of the art features for NLP such as entity recognition that enhances the bot's functionality; it has high-quality pre-trained models, allowing for advanced NLP implementations without the need of extensive model training; and its extendable architecture makes it possible to integrate the library with other libraries and frameworks which permits the project to evolve with future NLP advancements. 

    The OpenAI key is then loaded into the file so that the bot can access it in order to use the openai library.

    The first function declared, named load_urls, accepts a parameter that is the path to the url stored in the fandoms_urls.yaml file. This function opens the file as file in read mode and returns a parsed data as a dictionary with the safe_load method, only loading simple, safe data types such as integers, floats, strings, lists, and dictionaries. This method, unlike the default load method, prevents the execution of arbitrary code and the loading of potentially dangerous objects, which can be a security risk. 

    The second funtion that is declared, named scrape_lore, takes in a parameter that is the url to the page of any particular fandom so long as it is found in the fandom_urls.yaml file. A variable called response uses the requests.get method on the url. After that, a variable called soup uses the BeautifulSoup function that takes in the content found in the response variable as the first argument and specifies the parser to use, in this case the html parser, as the second argument. The code proceeds to use the newly created soup object in order to find all the paragraphs by identifying all the 'p' tags in the HTML. The line lore_text = '\n'.join([para.text for para in paragraphs]) creates a single string by extracting the text from each paragraph in the paragraphs list and joining them with newline characters. This results in a string where each paragraph's text is on a new line. The return lore_text statement then returns this concatenated string as the function's output.

    The third function declared in the file, named clean_text, takes in a parameter named text. This function uses the regex (regular expressions) module in order to replace a patern in a string with a specified string replacement. In the first line that utilizes re.sub replaces all consecutive whitespace characters (spaces, tabs, newlines, etc.) in the text with a single space. This helps in normalizing the whitespace in the text. In the second line that uses re.sub it replaces all consecutive newlines in the text with a single newline. This helps in reducing multiple consecutive newlines to a single newline, ensuring that the text is not excessively spaced out vertically.

    In the fourth function declared in this file, named format_text, it takes a parameter named text as well. The 'paragraph' variable stores the operation made on the text parameter by using the .split() method, which splits 'text' into substrings wherever it finds a double newline character '/n/n'. In the formatted text variable, the .join() method is used to concatenate all the elements in the paragraphs list into a single string, with each element separated by double newline characters ('\n\n'). This ensures that the resulting formatted_text has paragraphs separated by double newlines, maintaining the paragraph structure. This function then returns the formatted text. 

    The fifth function is then declared, taking in a parameter called text. Aptly named openai_summarize, this function takes care of the logic necessary to use the OpenAI API. The 'client.chat.completions.create' is a method from API's client that creates a new chat-based completion. This method then takes in a number of arguments. The first is the model, which in this case the project uses the GPT 4o-mini model. Second, the messages variable stores a list of messages that set up the context for the completion which includes a system message and a user message. Third, the max tokens variable limits the message completion to 150 tokens. Finally, the temperature variable controls the creativity of the response. In this case it is set to 0.8, (the closer it is to or up to 1, the more random the outputs) so that it may the AI generates a more random output. After the response variable, the summary variable uses the response object returned by the API call and accesses the first choice of in the list of generated completions by using: response.choices[0]. It then uses .message.content to extract the content of the message from the first choice. The function concludes by returning the summary. 

    The sixth function, named cache_lore_data takes in two parameters: fandom_url, a dictionary containing the different fandom names as keys and their corresponding URLs as values, and a cache path which is directed at a file named 'lore_cache.yaml'. The first conditional checks whether the cache file specified by 'cache_path' exists. If it does, it opens the file in 'r' mode. The lore_data variable stores the read and parsed YAML content from the file by using the following line: yaml.safe_load(cache_file), converting it later into a Python dictionary. If the cache file doesn't exist, an empty dictionary named 'lore_data' is intialized. With the use of a for loop, each item is iterated over in the 'fandom_urls' dictionary. For each fandom and its corresposning URL, if the fandom is not already in the cache, the 'scrape_lore(url)' function is called to scrape the lore from the URL anf then add that result into the lore_data dictionary. The updated lore_data dictionary is written back on the cache file in YAML format using this line of code: 'yaml.safe_dump'. The funtion then returns the lore_data dictionary. 

    On the 80th line, the URLs are loaded by using the load_urls function and on the 81th line, the cache_lore_data function is used and takes the dictionary of fandom URLs, checks for an existing cache, scrapes any missing lore data, updates the cache file, and returns the updated cache data.

    Finally the final function in this file, named process_question, takes in two parameters: a question and lore data. In this function, the user's question is made case insensitive by using the .lower() method on the question object. In order for the lore bot to determine which topic it is asked about it uses a for loop that evaluates what the keyword in the question is. The for loop works as a follows: for a keyword found in the lore data dictionary, if the keyword is in the question it accesses the value associated with the keyword in the dictionary and retrieves the raw lore content for the specified keyword. It then proceeds to clean up the text by using the previously established clean_text function on the raw text variable and formats the cleaned text with the use of the format_text function. Finally, the summmarize_text function is used to generate a summarized answer for the question asked by using the openai_summarize function on the formatted text variable, returning the  summarized text. The lore bot also handles the event in where it doesn't recognize a keyword in a question by returning a message stating it doesn't know about a topic yet, politely prompting the user to ask it about something else instead. 

### Installation
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/yourusername/discord-lore-bot.git
   cd discord-lore-bot

2. Create a virtual environment
    python -m venv lore-bot
    source lore-bot/bin/activate  
    #On Windows use `lore-bot\Scripts\activate`

3. Install dependancies
    pip install -r requirements.txt

4. Set up a virtual environment
    Create a .env file in the project root and add your Discord token and OpenAI API key
    Example:
    DISCORD_TOKEN=your_discord_token_here
    OPENAI_API_KEY=your_openai_api_key_here

5. Run the bot 
    Run the bot by using python main.py in the terminal


### Usage

1. Starting the Bot:
    Once the bot is running, invite it to your Discord server using the OAuth2 URL provided in the Discord Developer Portal.

2. Using Commands:
    !ask <question>: Ask LoreBot any lore-related question.
    Example: !ask Tell me about dragons in DnD.

3. Adding Fandoms:
    Update the fandom_urls.yaml file with new fandom URLs to expand the bot's knowledge base.

### Configuration
    fandom_urls.yaml: Manage URLs of different fandoms for the bot to scrape and provide lore information.
    
    Example:
        #fandom_name:
        #description: "Brief description of the fandom"
        url: "http://example.com/fandom-lore-page"
    
    Ensure you have your DISCORD_TOKEN and OPENAI_API_KEY set up in the .env file.


### Contributing

    I welcome contributions! 
    
    To contribute:

    Fork the repository.
    Create a new branch: git checkout -b feature-branch-name
    Make your changes and commit them: git commit -m 'Add some feature'
    Push to the branch: git push origin feature-branch-name
    Open a pull request.


Thank you sooooo much for using the Lore Bot. If you have any questions or concerns, please open an issue on GitHub or contact the project maintainer. 