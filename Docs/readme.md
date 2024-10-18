

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


### **REST Endpoints:**
1. arena/lobby
2. arena/game/<gameId>



### **WS Endpoints:**
game/<gameId>
Only for delta changes

~ Format
* action - [UPDATE_GAME_STATE, RESIGN
 , CLAIM_VICTORY, MESSAGE]
* 

### User Flow
1. User Logins
    > /home login button
2. User clicks on ENTER ARENA 
    > api/v1/arena/lobby is invoked
    > User is autheticated and put on queue for matchmaking
    > gameId is returned as reponse
3. User is redirected