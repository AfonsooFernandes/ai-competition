# Artificial Intelligence | Informatics Engineering [@IPVC/ESTG](https://www.ipvc.pt/estg/)  #
Teachers: [Luís Teófilo](mailto:luisteofilo@estg.ipvc.pt) and [Jorge Ribeiro](mailto:jribeiro@estg.ipvc.pt) 
___
### Introduction ###

The base code to create games and run agent competitions in Python, using a Docker environment

### How can I set up my environment? ###

* Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Build the Docker image by running the following command in the project's root folder:
```
docker-compose build
```

### How can I create my own player? ###

You simply need to pick one of the available games (or create your own) and add your player class to the players folder 
of that game. If the class inherits from the base player class for that game it will be automatically detected!
Please check below how to include the player in a simulation.

### How do I run a competition? ###

After building the Docker image, you can run a competition by running the following command
```
docker compose run --rm ai-competition <flags>
```

### Game Simulation Tool Documentation ###
 
This section provides details on how to use the flags. The tool supports several flags that allow users to configure the simulation.

## Flags

### --game
- **Description**: Specifies the type of game to simulate.
- **Usage**: `--game <GAME_TYPE>`
- **Required**: Yes
- **Example**: `--game hlpoker` or `--game connect4`

### --seat-permutation
- **Description**: Indicates if seats should be permuted during the simulation. This means that each iteration will have 2 games where players will take different seats in the table. 
- **Usage**: `--seat-permutation`
- **Required**: No (default is `True`)
- **Example**: `--seat-permutation` (to enable) or `--no-seat-permutation` (to disable)

### --num-iterations
- **Description**: Sets the number of iterations for each game in the simulation.
- **Usage**: `--num-iterations <NUMBER>`
- **Required**: No (default is `10000`)
- **Example**: `--num-iterations 10`

### --player
- **Description**: Adds a player to the simulation. Requires a name and a type. Must be specified at least twice.
- **Usage**: `--player <NAME> <NAME_PLAYER_CLASS>`
- **Required**: Yes (at least two players)
- **Example**: `--player "Luís" HumanHLPokerPlayer --player "GPT" RandomHLPokerPlayer`
- **Note**: The types of players available depend on the game. The types will be read directly from the players folder in the game.

## Examples
- Running a Limit Holdem Poker game against the random player  
```
docker compose run ai-competition --num-iterations 1 --game hlpoker --player "Luís" HumanHLPokerPlayer --player "Random" RandomHLPokerPlayer
```
- Running a Limit Holdem Poker tournament between all computer players
```
docker compose run ai-competition --game hlpoker --player "Random" RandomHLPokerPlayer --player "Call" AlwaysCallHLPokerPlayer --player "Raise" AlwaysRaiseHLPokerPlayer --player "Fold" AlwaysFoldHLPokerPlayer
```
