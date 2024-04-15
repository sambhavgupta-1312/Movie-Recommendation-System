import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import requests
import gzip
import shutil

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20230415/pngtree-website-technology-line-dark-background-image_2344719.jpg");
background-size: cover;
# opacity:0.9;
}

[data-testid="stHeader"]{
background-color: rgba(0,0,0,0);
}

[ data-testid="baseButton-header"]{
color: rgb(174,255,0);
}

[data-testid="baseButton-headerNoPadding"]{
color: rgb(174,255,0);
}

.st-emotion-cache-1wbqy5l e17vllj40 {    #the deploy button
font-weight: 1000;
}

[ data-testid="stDeployButton"]{
font-size: 20px;
}

[id="welcome-to-our-movie-recommender-system"],[id="explore-our-streamlit-web-app"]{
color:rgb(189 199 255);
}

[data-testid="stMarkdownContainer"]{
color:rgb(255 241 137);
font-size: 19px;
}

[id="movie-recommendation-system"]{
color:rgb(216 216 216);
}

[data-testid="baseButton-secondary"]{
background-color:rgb(108 80 216);
}

[data-testid="stText"]{
color:rgb(255,255,255);
font-size:14px;
font-weight: 700;
}

[class="stTextLabelWrapper st-emotion-cache-y4bq5x ewgb6651"]{
width: 99px;
}

[id="contact-me"]{
color:rgb(167 176 231);
}

[data-testid="stSidebar"]{
background-color:rgb(93 120 184);
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

movies=pickle.load(open('movies.pkl','rb'))

# with gzip.open('similarity.pkl.gz.gz', 'rb') as f_in:
#     with open('similarity.pkl.gz', 'wb') as f_out:
#         shutil.copyfileobj(f_in, f_out)

with gzip.open('similarity.pkl.gz', 'rb') as f_in:
    with open('similarity.pkl', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
        
similarity=pickle.load(open('similarity.pkl','rb'))

def get_image(id):
    url='https://api.themoviedb.org/3/movie/{}?api_key=2af841ab954eb08e433756d3f577db89'.format(id)
    response=requests.get(url)                         
    data=response.json()
    poster_path=data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
    

def recommend(movie):
    index=movies[movies['title'] == movie].index[0]
    distances=similarity[index]
    movie_list=sorted(enumerate(distances),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movie_names=[]
    recommended_movie_posters=[]
    for i in movie_list:
        recommended_movie_names.append(movies.iloc[i[0]].title)
        movie_id=movies.iloc[i[0]].id
        recommended_movie_posters.append(get_image(movie_id))

    return recommended_movie_names,recommended_movie_posters

with st.sidebar:
    selected=option_menu('Movie Recommendation System',
                         ['Home page',
                          'Movie Recommender',
                          'Contact Me'],
                          icons=['house-check-fill','film','person-lines-fill'],   #from bootstrap icons
                          default_index=0)
    
st.sidebar.header("Project Creator")
st.sidebar.info(
    "This Recommender System is created by [Sambhav Gupta](https://www.linkedin.com/in/sambhav-gupta-504975244/). Fill in the contact details to connect and grow together."
)

if selected == 'Home page':
    st.header('Welcome to our Movie Recommender System')
    st.write("This web application, powered by Streamlit, helps you explore movie recommendations tailored to your preferences.")

    st.header("Explore Our Streamlit Web App")
    st.write("Our web application features the following key sections:")

    st.write("Home Page")
    st.write("The landing page introduces you to our Movie Recommender System. It's your gateway to discovering great movies.")
    st.write("Movie Recommender System")
    st.write(" Here, you can enter a movie title or select one from the dropdown menu. Upon clicking 'Show Recommendations', you'll get a list of similar movies.")
    st.write("Contact Us")
    st.write("This section enables you to provide contact details to reach out to the developer or project owner.")

elif selected == 'Contact Me':
    st.header('Contact Me')
    st.write("Please fill the form given below to connect with the project creator")

    my_name = st.text_input("Your Name")
    my_email = st.text_input("Your Email")
    my_text = st.text_area("Your Thoughts", height=150)

    # Submit button
    if st.button("Submit"):
        if my_name.strip() == "" or my_email.strip() == "" or my_text.strip() == "":
            st.warning("Please fill all the fields.")
        else:
            send_email_to = 'samgpt1312@gmail.com'
            st.success("Your contact details have been shared successfully! The owner will reach you out shortly")

elif selected == 'Movie Recommender':
    st.title('Movie Recommendation System')
    movie_list = movies['title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown menu", movie_list)

    if st.button('Show Recommendations', key='show_recommendations'):
        recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])