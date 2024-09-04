# Bench Money NBA

**Bench Money NBA** is a tool that calculates the amount of money spent by an NBA organization on players sitting on the bench per game. It provides a visual representation of how much money is allocated to inactive players in comparison to active players on the court.

## Features

- **Team Comparisons:** See which team is spending more money on inactive players during a game.
- **Top Bench Players:** Displays the top three highest-paid bench players for each team.
- **Interactive Graphs:** Generates visual representations of team spending.
- **API Integration:** Uses the NBA API to retrieve game data and Beautiful Soup for web scraping player salaries.
- **Social Media Integration:** Posts generated images to Twitter using the Twitter API.

## Technologies Used

- **Python**
  - pandas
  - matplotlib
  - PIL (Python Imaging Library)
  - cairosvg
  - tweepy
  - requests
  - Beautiful Soup
  - MongoDB
  - Matplotlib
- **APIs**
  - NBA API
  - Twitter API
  - MongoDB
- **Frontend**
  - React
  - Chakra UI
  - TypeScript

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/twelckle/Bench_Money_NBA.git
   cd Bench_Money_NBA
   
2.	Install dependencies
3. Set up your MongoDB database and update the connection details in your project. The link can be found in the nbaAPI.py file.
4. Get your API keys for the Twitter APIs, and add them to the twitter.py file.
   
## Usage

1. Fetch NBA game data and player salaries using the NBA API and web scraping scripts.
2. Generate visual representations of team spending on bench players.
3. Post the generated images to Twitter by running the script.


## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- NBA API for providing game data.
- Beautiful Soup for web scraping.
- Twitter API for posting game summaries.

