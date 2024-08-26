# Star Track
Track who stars your repository 👀

<p align="center">
  <img alt="llama_track" src="https://github.com/kingjulio8238/startrack/blob/main/assets/llama-track.png?raw=true">
</p>

## Quickstart 🏁
[Demo](https://www.loom.com/share/7027cd1849694349b1114d6f79904e9a?sid=224f5b20-14b0-4f89-9ba6-3604c08befa2)

### Clone Star Track 

```bash
git clone https://github.com/kingjulio8238/startrack.git
cd startrack
```

### Install python dependencies: 
```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Setup necessary API keys and local variables
```bash
cp .env_local .env
vim .env_local

# You will need to provide
MULTION_API_KEY = '...'
# You can get it here: https://app.multion.ai/api-keys
# Read the MultiOn docs: https://docs.multion.ai

# Depending on your use case, you may also need other API keys
```

### Track your stars 
```bash
python main.py https://github.com/kingjulio8238/startrack --with-linkedin

# See help for more options and use cases
python main.py --help
# usage: main.py [-h] [--max-stargazers MAX_STARGAZERS] [-li] [-aops] [-mem0] [-kg] repo_url
# 
# Scrape GitHub and LinkedIn data for repository stargazers.
# 
# positional arguments:
#   repo_url              URL of the GitHub repository to scrape
# 
# options:
#   -h, --help            show this help message and exit
#   --max-stargazers MAX_STARGAZERS
#                         Maximum number of stargazers to scrape
#   -aops, --with-agentops
#                         Use Agentops for tracking and reporting agents' actions
#   -li, --with-linkedin  Scrape LinkedIn profiles
#   -mem0, --with-mem0    Option to include memory usage for scraping
#   -kg, --with-neo4j-kg  Option to use Neo4j knowledge graph. Requires --with-mem0
```

### Visualize stargazers 
```bash
python dataviz.py
```

### List CSV files with stargazers and preview the most recent ones 
```bash
ls data/*
ls -t data/* | tail -1 | xargs less
```

## Architecture 
<p align="center">
  <img alt="star_track_architecture" src="https://github.com/kingjulio8238/startrack/blob/main/assets/architecture-final.png?raw=true">
</p>

## Future features  
- Detailed scraping
- More than 1 page of stars 
- API integration 
- Improve graph connections 
- Advanced visualizations

<p align="center">
  <img alt="coming_soon" src="https://github.com/kingjulio8238/startrack/blob/main/assets/coming-soon.png?raw=true">
</p>


Go contribute 🫡🚢

## Initial contributors 
[Julian Saks](https://www.linkedin.com/in/juliansaks/), [Teo Feliu](http://linkedin.com/in/teofeliu), [Jeremiasz Jaworski](https://www.linkedin.com/in/jeremiasz-j), [Mark Bain](https://www.linkedin.com/in/markmbain/)
