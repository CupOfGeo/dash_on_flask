# Ghost Rhymes

Ghost Rhymes is website that uses AI models trained on music lyrics to create new lyrics.


This website is built with flask and plotly dash.
It is currently deployed on heroku www.ghostrhymes.com.


# Functionality
- Test out the generation of the Rapper model which was trained on 600 songs by Eminem, J. Cole, Kendrick Lamar, and Drake.

- There is also a Cowboy model that's trained on 60 songs. It is awful but is used for deployment and pipeline testing

- Strip payment processing.
- User dashboard
- Dataset creation. Turn any spotify playlist into a dataset that will be used to train your model.
- Fine tune your model to improve its results keep it current and prevent data drift.
  - Allows you to pick which output you like to be added to the dataset for better performance.
    
- Login and Oauth Sign in with Google.  
    - Would like to add sign in with twitter.
    - Thinking about only letting users sign in with google.
    

# Tech

### Frontend 
- Flask and Dash are great python libraries for building websites and dashboards.
- Bootstrap styling 
### Backend
- This site is deployed on heroku from this git repo but will eventually be moved to google in a docker container.
- Postgres database that saves user information.
### Data
- Google cloud run for the api Spotify2Genius which turns your playlist into a dataset
- Google storage buckets which holds your dataset and models
- Being able to save new data to your dataset to better model performance. 
### Models
- GPT-Neo by Eleuther.ai's 1.3 Billion parameter model is what's used for the Rapper AI. I can also use the 2.7B.
  - I plan on adding the option to use Eleuther.ai's GPT-J which is a 6B parameter model trained on googles TPUv3
- Google Kubernetes engine where the models are deployed to my gpu cluster.
    - Currently, only 1 node with 2 K80 gpus that can scale to 2.
    - Only using spot instances right now for price would like to create a combination of spot and dedicated node pools
- Google Compute Engine for training. Models are trained on a V100 card and are tuned depending on the type and size of the dataset.

