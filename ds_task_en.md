You need to design a service for intents search in an incoming sentence. The application should be a web service wrapped in a docker container.

Request:

{ "data":"Hi! My name is George, I work as an engineer, I want to fly to Mars at 12:30." }

Answer:

{ "response": [ "name":"George", "destination":"mars", "work":"engineer", "time":"12:30", ] }

You can use anything (duckling and etc ..) except for ready-made services.
