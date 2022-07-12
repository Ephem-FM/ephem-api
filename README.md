# ephem api
external api to schedule texts via twilio based on user's preferences

Utilized FastAPI to create an endpoint that accepts POST requests and constructs a preferences object including user's number.  The 'playlists' table is transformed into Pandas DataFrame, grouped by show, then the mean for each audio characteristic we care about--valence, artist popularity, danceability, energy--are retrieved.  

A 'composite score' based on how closely aligned a user's preferences are with the means of a given show is then created for each show, and the three closest fits are transformed into scheduled texts to the user via the Twilio API.  There's also some work done to ensure that the start time of the show is normalized into UTC time and that the datetime for when it'll be scheduled is more than 15 minutes into the future and less than one week into the future as these are the current constraints of the Twilio Scheduled Texts API (currently in public beta).  

Lastly, a user also gets an introductory text as a little treat.
