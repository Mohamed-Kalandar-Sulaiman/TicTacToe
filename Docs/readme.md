

### Flow
1. Login/ SignUp Page
[UI/landingpage]

2. Home Page
    [UI/home]
    [UI/leaderboard]
    
    >> Display username profile pic
    > Enter Arena
    > leaderBoard

3. Arena/lobby
    >> Queued in RedisStream waiting for match
    Just an intermediary state

4. Arena/game/<gameId>
    > Layout
    > In background connect to WS
    * Exchange game states
    * Make moves
    * Resign or Claim victory
    * Timeout checks
    * Send and Recive messages


REST Endpoints:
arena/join-a-game
areana/game/<gameId>

WS Endpoints:
game/<gameId>

~ Format
* action - [UPDATE, RESIGN , CLAIM_VICTORY, MESSAGE]
* 