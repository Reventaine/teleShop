# teleShop

Simple bot for videogameshop, written for learning purposes in Python and postgreSQL (work in progress).<br/>
To use the bot as seller in convinient way you`ll probably need postgres.<br/>
Enter Token of your Telegram bot and DB info into config.py and run main.py. <br/>
Admin functions (such as add entries to catalog) avaible witch /admin3517 command.<br/>
Logic of the bot: 1) Buyer navigate through catalog - products info goes from "teleShop" table;<br/>
                  2) Then add some product in cart - product info goes to temporary "cart" table;<br/>
                  3) Goes to cart submenu - order details takes from temporary "cart" table - checks and proceeds to confirming order;<br/>
                  4) After confirming order details and buyer contact info (telegram UserID and email) goes to seller telegram chat/email. <br/>
