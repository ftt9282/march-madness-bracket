# march-madness-bracket
Generate a March Madness Bracket based on data and probability found on 538. The generated 'march_madness_bracket.csv' bracket will appear once the program is finished running. 

Data for teams, seeding, and win probability were found at:
https://projects.fivethirtyeight.com/2021-march-madness-predictions/

While the CSV does show updated probability round by round, for this project I'm only utilizing data available to me prior to the start of the tournament (or else it wouldn't be a proper prediction).

They do not disclose their exact formula, but [538 is open with how they update each team's probability when they move on to the next round](https://fivethirtyeight.com/methodology/how-our-march-madness-predictions-work-2/). Needless to say... if I were to attempt to implement this I don't know if I would have finished by the time the tournament started. I instead needed to implement a way to simulate a round where the provided percentage outcomes didn't actually add up to 100%.

The methodology I ended up using was pretty simple. Imagine that Gonzaga and Oklahoma facing off to see who moves into the Sweet Sixteen. The Zags have a 73.37% chance of making it to that round, while Oklahoma was predicted as having only a 10.23% chance. For each team I generate a random float, and a team will move on if they are the only one to win that round. I consider it a tie if both teams win/lose and generate another set of floats.

This is far from perfect and someone smarter than me could most likely find a much better way to do this. Admittedly the results come out a [little bit chalky](https://www.sportingcharts.com/dictionary/sports-betting/chalk.aspx)

I can't complain too much, however, [since this helped me win my office pool this year!](https://fantasy.espn.com/tournament-challenge-bracket/2021/en/entry?entryID=45620918)
