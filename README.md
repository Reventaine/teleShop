# teleShop

Simple bot for videogameshop, written for learning purposes in Python and postgreSQL (work in progress).
To use the bot as seller in convinient way you`ll probably need postgres.
Enter Token of your Telegram bot and DB info into config.py and run main.py. 
Admin functions (such as add entries to catalog) avaible witch /admin3517 command.
Logic of the bot: 1) Buyer navigate through catalog - products info goes from "teleShop" table;
                  2) Then add some product in cart - product info goes to temporary "cart" table;
                  3) Goes to cart submenu - order details takes from temporary "cart" table - checks and proceeds to confirming order;
                  4) After confirming order details and buyer contact info (telegram UserID and email) goes to seller telegram chat/email. 
