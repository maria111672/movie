from flask import Flask, render_template, jsonify, request
import json
import os
import requests

TMDB_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YzRkYjQzZmJmNGM0M2YzNzJiMGJjNmE3ODkzNjE0MiIsIm5iZiI6MTc4ODUxMjk2OC40NTUwMDAyLCJzdWIiOiI2YTlhOGFjOGRmNDU5OGRmNWMxZjkyMWMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.TKbxWmGIPEHFR-D_dkul6unjRNMl082m7OEmCYv0vQI"

app = Flask(__name__)

MOVIES = [
   
    {
        "id": 26,
        "title": "Obsession",
        "year": 2026,
        "rating": 7.8,
        "category": "Horror",
        "poster": "/static/images/obession.jpeg",
        "description": "A hopeless romantic makes a wish that his crush will fall in love with him, but the wish leads to a sinister consequence.",
        "director": "Curry Barker",
        "cast": ["Michael Johnston", "Inde Navarrette", "Cooper Tomlinson"],
        "duration": "109 min"
    },

    {
        "id": 27,
        "title": "Minions & Monsters",
        "year": 2026,
        "rating": 6.4,
        "category": "Animation",
        "poster": "/static/images/minions.jpeg",
        "description": "The Minions become involved in a wild adventure involving monsters and filmmaking.",
        "director": "Pierre Coffin",
        "cast": ["Pierre Coffin", "Trey Parker", "Allison Janney"],
        "duration": "90 min"
    },

    {
        "id": 28,
        "title": "Evil Dead Burn",
        "year": 2026,
        "rating": 6.3,
        "category": "Horror",
        "poster": "/static/images/evil.jpeg",
        "description": "A woman seeks comfort with her in-laws after losing her husband, but discovers a terrifying supernatural threat.",
        "director": "Sébastien Vanicek",
        "cast": ["Souheila Yacoub", "Tandi Wright", "Hunter Doohan"],
        "duration": "110 min"
    },

    {
        "id": 29,
        "title": "Backrooms",
        "year": 2026,
        "rating": 6.8,
        "category": "Thriller",
        "poster": "/static/images/backrooms.jpg",
        "description": "A mysterious dimension beyond reality becomes the setting for a dangerous rescue mission.",
        "director": "Kane Parsons",
        "cast": ["Chiwetel Ejiofor", "Renate Reinsve", "Mark Duplass"],
        "duration": "110 min"
    },

    {
        "id": 30,
        "title": "Scary Movie",
        "year": 2026,
        "rating": 4.8,
        "category": "Comedy",
        "poster": "/static/images/scarymovie.webp",
        "description": "A group of characters find themselves caught in a chaotic adventure filled with killers, monsters and supernatural events.",
        "director": "Michael Tiddes",
        "cast": ["Marlon Wayans", "Shawn Wayans", "Anna Faris"],
        "duration": "95 min"
    },

    {
        "id": 31,
        "title": "Disclosure Day",
        "year": 2026,
        "rating": 6.4,
        "category": "Thriller",
        "poster": "/static/images/disclosure.jpg",
        "description": "A mysterious discovery raises questions about humanity's place in the universe.",
        "director": "Steven Spielberg",
        "cast": ["Emily Blunt", "Josh O'Connor", "Colin Firth"],
        "duration": "145 min"
    },

    {
        "id": 32,
        "title": "Michael",
        "year": 2026,
        "rating": 7.4,
        "category": "Drama",
        "poster": "/static/images/michael.jpg",
        "description": "A biographical drama following Michael Jackson's early life, rise to fame and development as a performer.",
        "director": "Antoine Fuqua",
        "cast": ["Jaafar Jackson", "Nia Long", "Colman Domingo"],
        "duration": "127 min"
    },

    {
        "id": 33,
        "title": "Toy Story 5",
        "year": 2026,
        "rating": 7.4,
        "category": "Animation",
        "poster": "/static/images/toystory.jpg",
        "description": "Woody, Buzz and the other toys face a new challenge as modern technology changes the way children play.",
        "director": "Andrew Stanton",
        "cast": ["Tom Hanks", "Tim Allen", "Joan Cusack"],
        "duration": "102 min"
    },
    
    

    {
        "id": 34,
        "title": "Nuremberg",
        "year": 2025,
        "rating": 7.3,
        "category": "Drama",
        "poster": "/static/images/nuremberg.jpg",
        "description": "A historical courtroom drama centered on the aftermath of World War II and the Nuremberg trials.",
        "director": "James Vanderbilt",
        "cast": ["Rami Malek", "Russell Crowe", "Michael Shannon"],
        "duration": "148 min"
    },
    
    {
        "id": 2,
        "title": "Inception",
        "year": 2010,
        "rating": 8.8,
        "category": "Sci-Fi",
        "poster": "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg",
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "director": "Christopher Nolan",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
        "duration": "148 min"
    },
    
    {
        "id": 3,
        "title": "The Shawshank Redemption",
        "year": 1994,
        "rating": 9.3,
        "category": "Drama",
        "poster": "/static/images/shaw.jpg",
        "description": "Over the course of several years, two convicts form a friendship, seeking consolation and redemption through basic compassion.",
        "director": "Frank Darabont",
        "cast": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
        "duration": "142 min"
    },
    
    {
        "id": 4, 
        "title": "Pulp Fiction",
        "year": 1994,
        "rating": 8.9,
        "category": "Crime",
        "poster": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
        "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "director": "Quentin Tarantino",
        "cast": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
        "duration": "154 min"
    },
    
    {
        "id": 5,
        "title": "Forrest Gump",
        "year": 1994,
        "rating": 8.8,
        "category": "Drama",
        "poster": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
        "description": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
        "director": "Robert Zemeckis",
        "cast": ["Tom Hanks", "Robin Wright", "Gary Sinise"],
        "duration": "142 min"
    },
    
    {
        "id": 6,
        "title": "The Matrix",
        "year": 1999,
        "rating": 8.7,
        "category": "Sci-Fi",
        "poster": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
        "description": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.",
        "director": "Lana Wachowski, Lilly Wachowski",
        "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
        "duration": "136 min"
    },
        
    {
        "id": 7,
        "title": "Interstellar",
        "year": 2014,
        "rating": 8.6,
        "category": "Sci-Fi",
        "poster": "/static/images/inter.jpeg",
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "director": "Christopher Nolan",
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
        "duration": "169 min"
    },
        
    {
        "id": 8,
        "title": "The Godfather",
        "year": 1972,
        "rating": 9.2,
        "category": "Crime",
        "poster": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
        "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant youngest son.",
        "director": "Francis Ford Coppola",
        "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
        "duration": "175 min"
    },
    
    {
        "id": 9,
        "title": "Fight Club",
        "year": 1999,
        "rating": 8.8,
        "category": "Drama",
        "poster": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "description": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.",
        "director": "David Fincher",
        "cast": ["Brad Pitt", "Edward Norton", "Helena Bonham Carter"],
        "duration": "139 min"
    },
    
    {
        "id": 10,
        "title": "Gladiator",
        "year": 2000,
        "rating": 8.5,
        "category": "Action",
        "poster": "/static/images/glad.jpg",
        "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "director": "Ridley Scott",
        "cast": ["Russell Crowe", "Joaquin Phoenix", "Connie Nielsen"],
        "duration": "155 min"
    },
    
    {
        "id": 11,
        "title": "The Silence of the Lambs",
        "year": 1991,
        "rating": 8.6,
        "category": "Thriller",
        "poster": "/static/images/lambs.jpg",
        "description": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.",
        "director": "Jonathan Demme",
        "cast": ["Jodie Foster", "Anthony Hopkins", "Lawrence A. Bonney"],
        "duration": "118 min"
    },
    
    {
        "id": 12,
        "title": "Saving Private Ryan",
        "year": 1998,
        "rating": 8.6,
        "category": "War",
        "poster": "/static/images/pri.jpeg",
        "description": "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.",
        "director": "Steven Spielberg",
        "cast": ["Tom Hanks", "Matt Damon", "Tom Sizemore"],
        "duration": "169 min"
    },

    {
        "id": 13,
        "title": "The Lord of the Rings: The Fellowship of the Ring",
        "year": 2001,
        "rating": 8.8,
        "category": "Fantasy",
        "poster": "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
        "description": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
        "director": "Peter Jackson",
        "cast": ["Elijah Wood", "Ian McKellen", "Orlando Bloom"],
        "duration": "178 min"
    },

    {
        "id": 14,
        "title": "Titanic",
        "year": 1997,
        "rating": 7.9,
        "category": "Romance",
        "poster": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
        "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        "director": "James Cameron",
        "cast": ["Leonardo DiCaprio", "Kate Winslet", "Billy Zane"],
        "duration": "194 min"
    },
    
    {
        "id": 15,
        "title": "Schindler's List",
        "year": 1993,
        "rating": 9.0,
        "category": "Drama",
        "poster": "https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg",
        "description": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.",
        "director": "Steven Spielberg",
        "cast": ["Liam Neeson", "Ben Kingsley", "Ralph Fiennes"],
        "duration": "195 min"
    },
    
    {
        "id": 16,
        "title": "Jurassic Park",
        "year": 1993,
        "rating": 8.2,
        "category": "Sci-Fi",
        "poster": "/static/images/jur.jpg",
        "description": "A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the park's cloned dinosaurs to run loose.",
        "director": "Steven Spielberg",
        "cast": ["Sam Neill", "Laura Dern", "Jeff Goldblum"],
        "duration": "127 min"
    },
    
    {
        "id": 17,
        "title": "The Departed",
        "year": 2006,
        "rating": 8.5,
        "category": "Crime",
        "poster": "/static/images/Dep.jpg",
        "description": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.",
        "director": "Martin Scorsese",
        "cast": ["Leonardo DiCaprio", "Matt Damon", "Jack Nicholson"],
        "duration": "151 min"
    },
    
    {
        "id": 18,
        "title": "Avengers: Endgame",
        "year": 2019,
        "rating": 8.4,
        "category": "Action",
        "poster": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "description": "After the devastating events of Infinity War, the remaining Avengers assemble once more to reverse Thanos' actions and restore balance to the universe.",
        "director": "Anthony Russo, Joe Russo",
        "cast": ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo"],
        "duration": "181 min"
    },
    
    {
        "id": 19,
        "title": "Parasite",
        "year": 2019,
        "rating": 8.5,
        "category": "Thriller",
        "poster": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "director": "Bong Joon-ho",
        "cast": ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"],
        "duration": "132 min"
    },

    {
        "id": 20,
        "title": "The Lion King",
        "year": 1994,
        "rating": 8.5,
        "category": "Animation",
        "poster": "https://image.tmdb.org/t/p/w500/sKCr78MXSLixwmZ8DyJLrpMsd15.jpg",
        "description": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.",
        "director": "Roger Allers, Rob Minkoff",
        "cast": ["Matthew Broderick", "Jeremy Irons", "James Earl Jones"],
        "duration": "88 min"
    },
    
    {
        "id": 21,
        "title": "Dune",
        "year": 2021,
        "rating": 8.0,
        "category": "Sci-Fi",
        "poster": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
        "description": "Paul Atreides must travel to the most dangerous planet in the universe to ensure the future of his family and his people.",
        "director": "Denis Villeneuve",
        "cast": ["Timothée Chalamet", "Rebecca Ferguson", "Oscar Isaac"],
        "duration": "155 min"
    },
    
    {
        "id": 22,
        "title": "The Conjuring",
        "year": 2013,
        "rating": 7.5,
        "category": "Horror",
        "poster": "/static/images/con.jpg",
        "description": "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.",
        "director": "James Wan",
        "cast": ["Patrick Wilson", "Vera Farmiga", "Lili Taylor"],
        "duration": "112 min"
    },
    
    {
        "id": 1,
        "title": "The Dark Knight",
        "year": 2008,
        "rating": 9.0,
        "category": "Action",
        "poster": "/static/images/dark.jpg",
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "duration": "152 min"
    },
         
    
    {
        "id": 23,
        "title": "Spirited Away",
        "year": 2001,
        "rating": 8.6,
        "category": "Animation",
        "poster": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg",
        "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits.",
        "director": "Hayao Miyazaki",
        "cast": ["Rumi Hiiragi", "Miyu Irino", "Mari Natsuki"],
        "duration": "125 min"
    },
    
    {
        "id": 24,
        "title": "The Prestige",
        "year": 2006,
        "rating": 8.5,
        "category": "Thriller",
        "poster": "https://image.tmdb.org/t/p/w500/bdN3gXuIZYaJP7ftKK2sU0nPtEA.jpg",
        "description": "After a tragic accident, two stage magicians in 1890s London engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other.",
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Hugh Jackman", "Scarlett Johansson"],
        "duration": "130 min"
    },
    
    {
        "id": 25,
        "title": "Snowpiercer",
        "year": 2013,
        "rating": 6.9,
        "category": "Sci-Fi",
        "poster": "/static/images/snow.jpg",
        "description": "a post-apocalyptic story about the last humans on Earth who survive aboard a giant, perpetually moving train circling a frozen planet.",
        "director": " Bong Joon-ho",
        "cast": ["Jennifer Connelly", "Daveed Diggs"],
        "duration" : "126 min",
        "video": "/static/videos/snowpiercer.mp4"
    },   
    
    {
        "id": 35,
        "title": "The Mandalorian and Grogu",
        "year": 2026,
        "rating": 6.8,
        "category": "Action",
        "poster": "/static/images/grogu.jpg",
        "description": "The Mandalorian and Grogu embark on another adventure across the galaxy while facing new dangers.",
        "director": "Jon Favreau",
        "cast": ["Pedro Pascal", "Jeremy Allen White", "Sigourney Weaver"],
        "duration": "132 min"
    }
    
]

FAVORITES = set()

CATEGORIES = sorted(set(m["category"] for m in MOVIES))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/movies")
def api_movies():
    query = request.args.get("q", "").lower()

    category = request.args.get("category", "")
    sort = request.args.get("sort", "")

    results = MOVIES[:]

    if query:
        results = [ 
            m for m in results
            if query in m["title"].lower()
            or query in m["description"].lower()
            or query in m["director"].lower()
            or any(query in c.lower() for c in m["cast"])
        ]

    if category:
        results = [m for m in results if m["category"] == category]

    if sort == "rating_desc":
        results.sort(key=lambda m: m["rating"], reverse=True)
    elif sort == "rating_asc":
        results.sort(key=lambda m: m["rating"])
    elif sort == "year_desc":
        results.sort(key=lambda m: m["year"], reverse=True)
    elif sort == "year_asc":
        results.sort(key=lambda m: m["year"])
    elif sort == "title":
        results.sort(key=lambda m: m["title"])

    return jsonify(results)

@app.route("/api/tmdb-search")
def tmdb_search():
    query = request.args.get("q", "")

    url = "https://api.themoviedb.org/3/search/movie"

    headers = {
        "Authorization": f"Bearer {TMDB_TOKEN}"
    }

    params = {
        "query": query
    }

    response = requests.get(url, headers=headers, params=params)

    return jsonify(response.json())


@app.route("/api/movies/<int:movie_id>")
def api_movie_detail(movie_id):
    movie = next((m for m in MOVIES if m["id"] == movie_id), None)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    data = dict(movie)
    data["favorited"] = movie["id"] in FAVORITES
    return jsonify(data)


@app.route("/api/categories")
def api_categories():
    return jsonify(CATEGORIES)


@app.route("/api/favorites", methods=["GET"])
def api_favorites():
    favs = [m for m in MOVIES if m["id"] in FAVORITES]
    return jsonify(favs)


@app.route("/api/favorites/<int:movie_id>", methods=["POST"])
def api_toggle_favorite(movie_id):
    if movie_id in FAVORITES:
        FAVORITES.remove(movie_id)
        return jsonify({"favorited": False})
    else:
        FAVORITES.add(movie_id)
        return jsonify({"favorited": True})


@app.route("/api/stats")
def api_stats():
    return jsonify({
        "total_movies": len(MOVIES),
        "total_categories": len(CATEGORIES),
        "avg_rating": round(sum(m["rating"] for m in MOVIES) / len(MOVIES), 1),
        "total_favorites": len(FAVORITES),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
