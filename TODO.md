# ToDO
- Implement rules as Byte code in a Virtual Machine
    - This will allow the rules to be far less dangerous, though we shouldn't lose the ability to form complex logic.

    -As well, this will pretty much require rules be made through a GUI. I think users would prefer this

    - Add properties for the attributes in the base classes (and their handlers) so that I don't have to rely on other code to check values. This should help pave the way for the rules (which should be implemented as byte code in a VM if I really want to do this right)

- Make a Client GUI

    - Should be able to visualise, in some way:
        - The player list
            - Have some way to see who just played, so the player has a feel for how the game is progressing (perhaps by highlighting the last player
        - The cards in the player's hand
        - The top card on the Pile
            - More than just the top card (the top three?) would be nice for player's who were not following the game closely
        - The Deck
            - Nothing fancy, though a nice design couldn't hurt
        - Player chat, with the ability to send messages to players
            - "Whispering" could be an interesting feature
                - Perhaps also allow a way to easily implement a "No whispering" rule?

    - Fix the server connection prompt

    - Add proper Error handling, such as not being able to connect to a server or when someone is disconnected
