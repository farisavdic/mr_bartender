# Mr. Bartender
This is the code behind the Django webserver that was the backbone for my team's project for the 2023 [Advisor](https://www.ce.cit.tum.de/lsr/lehre/advisor/ "TUM: Advisor") competition of the Technical University of Munich.
## The project
Our task was to build an "intelligent kitchen assistant". To avoid restrictions regarding temperature limits we decided on a cocktail machine since it did not require any heating parts.
To distinguish ourselves from the competition, we came up with a novel concept for the machine: it should not only make the drinks, but also replace a human bartender throughout the entire experience. 
That's why the entire functionality revolved around a webserver, that could be used to order the drinks from one's smartphone. The twist was what happened when the customer puts their empty cup into the machine.
It starts preparing the drink without the user having to do anything! 
## How it works
The magic starts when the user arrives at the event where Mr. Bartender is deployed. Upon arrival the user receives a cup and registers it at a designated station. The station generates a QR-Code, which takes the user to the Mr. Bartender web interface.
Here, the user can select a drink, customize it and once they are happy with their order they simply press send. In the background, their order get's encoded and put into a SQLite database together with the RFID-Tag on the user's cup. This was passed to the website via the QR-Code the user scanned.
When arriving at the machine, the user places his cup onto a platform, underneath which a RFID scanner is placed. THE RFID-Tag from the cup is read and the machine sends an HTTP-request to the webserver. It checks whether there is an order placed for that cup and returns the previously encoded string in his HTTP-response.
After receiving this string, the machine starts preparing the drink, by moving the platform, which is part of a 2D-rail system, to the designated spaces. Here, each part of the encoded string corresponds to a position on the grid. Once all the required stations were visited the platform returns to its starting position, where the user can retreive their drink.
## Limitations
Since this was developed for a university competition, time was a scarce resource. The implementation was rushed and corners were cut, which is why I definitely missed some edge cases and have not implemented any proper error handling. 
As I don't see any real-life application for this project beyond the competition, I will not continue development on it. If you can make any use of it, feel free to do so! I would love to hear about it.
