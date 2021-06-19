# Leetcode-Bot

## A discord bot for programming guilds to keep track on their coding stats.

> !lc register <username>
> !lc register
> !lc post <leetcode_url>
> !lc post <leetcode question id>
> !lc stats
> !lc posts
> !lc self-stats

## TO DO

- [*] User should be able to register themselves, they can provide a username or bot picks it from their discord username
- [] User can post a question from leetcode using question id or url, parse the url and bot sends the question as message
- [] Only moderators should be able to post questions, keep a check for this
- [] Writing a script to scrape the leetcode for question
- [] Users can react to the moderator's leetcode question post
  - [] attempt - A user can opt to attempt the question
  - [] completed - Once the user completes the question, user can react to the message as completed
  - [] help - If user is stuck with a question user can opt for help which will notify the moderators
  
- [] Add reaction events to the bot to check reactions for post to keep track of the updates
- [] Stats page which will keep track of all the registered users' attempted and submitted questions
- [] UI for the table
- [] Get all the posted questions and stats of how many users solved and how many didn't
- [] Get self stats of the user
- [] **NEXT RELEASE** Automatically scrape leetcode website if user has actually submitted the question
- [] **NEXT RELEASE** Map each user to his/her/their leetcode account
