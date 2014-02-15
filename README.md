#Mao
[Mao](http://en.wikipedia.org/wiki/Mao_%28card_game%29) is a card game, usually played amongst teenagers, where the rules are dynamic. Usually only one player (known as the Grand Chairman) knows the rules and is entrusted to enforce them fairly and consistently. Because this is a demanding job, especially when they also act as a player in the game, in this adaption of the game the computer handles the rules. This way, all the players can participate as clueless players.

##Rules
Unlike most adaptations of the card game, which hard-code the most widely known rules and call it a day, rules are constructed from functions in Python modules. Each function is not a rule, a rule is made up of the functions and control statements at runtime. Each function requires at least one parameter, `server`, which represents the entire Server object. Other parameters can be given, which could influence how a function works. Though passing the entire Server gives rules a lot of power, this is balanced by both the availability of the source code and the fact that these functions should be written by the Server owner only. If a player is to make a rule, he uses these functions to construct the rule. This last part has not been implemented yet, as I have yet to find a safe way to do this.

For each rule that is activated, the code runs in a separate thread, so rules can wait on different events or even go in infinite loops (though you should really put in pauses or the server could become overloaded)

The `trigger` that activate the rule (which can be a phrase or a card) is determined when the rule is imported into the server. It is not part of the rule's code at all. If a trigger is not specified, the rule's code is executed each time the current player ends his turn, but before the next player's turn starts.

Here is an example:

```python
def no_special_order(server):
    server.player_handler.order = 1
```
If this rule has no trigger, then the order will always be one (So the only way for other rules to edit the order is to manually call `next_player`).


If the `trigger` is a card, then the rule activate when the card is **successfully** placed down by the current player. I.e: it is that player's turn and that card is now the top card on the pile. Because of this, when the rule's code activate, <u>it is no longer that player's turn</u>. It is now the next player's turn. 

Here is an example:

```python
def reverse_order(server):
    server.player_handler.order = -server.player_handler.order
    server.player_handler.next_player()
    server.player_handler.next_player()
```
This rule flips the order around. This rule works differently, depending on whether the trigger is a card or a phrase. If it is a phrase, it reverses the order and then immediately skips the next player (according to the new order). If it is a card, then the order is reversed **after** it is the next player's turn, so the next two `next_player` calls make it appear that the order change happened before the player who played the trigger card's turn ended.

A rule's code can also have parameters other than `server`, but they *should* be optional (`*args, **kargs`). If they are not optional


##Server Setup and Configuration
To start a server, just run and interactive session on Server.py (`python -i Server.py`). One word of warning: make sure you call `shutdown()` **before** you exit the prompt, or you'll have to kill the process manually.

The 'options.cfg' file contains options to control server options, such as the default amount of cards that a player receives when they are punished.

The server actually reads this information at runtime, so it can be edited while the server is running, without having to restart it each time.
