# Nextbike Wrapped
I have made this app because I love Nextbike and wanted to show my skills.

### Backend:
Besides providing some quite simple summaries, it's approximating real mileage, assuming that user has always chosen the shortest paths. Shortest distances is calculated via Google Distance Matrix API and data is stored in Neo4j graph database, to minimize amount of paid requests. Algorithm is meant to be both time efficient (could be better) and money saving (cannot precalculate all distances for all cities). Google developer API key is also necesary to generate minimap with rides drawn via Google Static Maps API. Finally, each summary is saved in Mongo database to allow users sharing theirs' summaries.

### Frontend:
TypeScript + Angular, simple two views app. I'm not huge UX/UI designer, so it is what it is.

### Deployment:
I doubt anyone will try to run it locally, but in order to run app and api, you need to fill .env for API and also pass a /etc/secrets file during docker build in order to change destination API URL adress in environment.ts file. Docker compose is also prepared and working.
