from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize the SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def map_sentiment_to_mood(score):
    if score >= 0:
        return "Happy"
    elif score >= -0.5:
        return "Sad"
    elif score >= -0.7:
        return "Angry"
    else:
        return "Angry"

mood_to_yoga = {"Angry":[  # Angry
        {"pose": "Child's Pose", "image": "https://www.theyogacollective.com/wp-content/uploads/2019/10/4143473057707883372_IMG_8546-2-1200x800.jpg"},
        {"pose": "Cat-Cow", "image": "https://yogajala.com/wp-content/uploads/2022/03/cat-cow-pose-page.jpg"},
        {"pose": "Breathing exercises", "image": "https://static.wixstatic.com/media/8d7021_84de0fae57914ea990a6581b73efef40~mv2.png/v1/fill/w_925,h_1233,al_c,q_90,enc_auto/8d7021_84de0fae57914ea990a6581b73efef40~mv2.png"},
        {"pose": "Seated Forward Fold", "image": "https://omstars.com/blog/wp-content/uploads/2022/01/Paschimottanasana-Seated-Forward-Fold-scaled.jpg"},
        {"pose": "Puppy Pose", "image": "https://www.doyou.com/wp-content/uploads/2021/01/How-To-Do-Extended-Puppy-Pose.jpg"},
        {"pose": "Supine Twist", "image": "https://i.ytimg.com/vi/mNdJti7ZwKI/maxresdefault.jpg"},
        {"pose": "Reclined Bound Angle Pose", "image": "https://www.yogicwayoflife.com/wp-content/uploads/2017/01/Supta_Baddha_Konasana_Bound_Angle_Reclined_Pose_Yoga_Asana.jpg"},
        {"pose": "Thread the Needle Pose", "image": "https://d5sbbf6usl3xq.cloudfront.net/thread_the_needle_pose_flow__urdhva_mukha_pasasana_flow_yoga.png"},
        {"pose": "Happy Baby Pose", "image": "https://georgewatts.org/wp-content/uploads/2011/08/Happy-Baby-Variation.jpg"},
        {"pose": "Standing Forward Bend", "image": "https://static.vecteezy.com/system/resources/thumbnails/014/728/084/small/standing-forward-bend-yoga-pose-young-woman-practicing-yoga-exercise-woman-workout-fitness-aerobic-and-exercises-vector.jpg"},
        {"pose": "Garland Pose", "image": "https://beyogi.com/wp-content/uploads/2015/03/Garland-Pose-Malasana-1024x683.png"},
        {"pose": "Sphinx Pose", "image": "https://manflowyoga.com/wp-content/uploads/2023/12/Sphinx-Pose-for-Beginners-and-Men1.jpg"}
    ]
    ,
    "Happy": [
        {"pose": "Warrior Pose", "image": "https://srisrischoolofyoga.org/na/wp-content/uploads/2023/01/warrior-pose-three-variations-1-2-3.jpg"},
        {"pose": "Tree Pose", "image": "https://static.vecteezy.com/system/resources/thumbnails/004/224/332/small/woman-doing-tree-pose-free-vector.jpg"},
        {"pose": "Bridge Pose", "image": "https://thumbs.dreamstime.com/z/variation-bridge-pose-sporty-beautiful-young-woman-practicing-yoga-doing-standing-urdhva-dhanurasana-upward-bow-chakrasana-66275045.jpg"},
        {"pose": "Extended Triangle Pose", "image": "https://www.verywellfit.com/thmb/PFiy_-8S6S1kdV5wTdL1gVXFUqQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/trianglepose-5c5b4f3346e0fb0001105d35.jpg"},
        {"pose": "Half Moon Pose", "image": "https://cdn.yogajournal.com/wp-content/uploads/2007/08/Half-Moon-Pose_Andrew-Clark_2400x1350.jpeg"},
        {"pose": "Chair Pose", "image": "https://www.theyogacollective.com/wp-content/uploads/2019/10/Chair-Pose-2-for-Pose-Page-1200x800.jpeg"},
        {"pose": "Standing Backbend", "image": "https://c8.alamy.com/comp/2DBG2KT/beautiful-sporty-fit-woman-practices-sivananmda-yoga-asana-anuvittasana-standing-back-bend-pose-2DBG2KT.jpg"},
        {"pose": "Revolved Side Angle Pose", "image": "https://i.pinimg.com/736x/63/50/71/6350716418b5398eb1fc9af43b149a4d.jpg"},
        {"pose": "Upward Salute Pose", "image": "https://www.huggermugger.com/wp-content/uploads/2017/10/urdva-hastasana-copy.jpg"},
        {"pose": "Dancer Pose", "image": "https://cdn.yogajournal.com/wp-content/uploads/2007/08/Dancer-Pose_Andrew-Clark_2400x1350.jpeg"},
        {"pose": "Wide-Legged Forward Bend", "image": "https://images.squarespace-cdn.com/content/v1/5d31ed671abe780001b2964d/3691c960-b23d-4181-83db-47d5ebef0676/NR_StretchandDeStress-12.jpg"}
    ],
    "Sad": [ 
        {"pose": "Legs-Up-The-Wall", "image": "https://post.healthline.com/wp-content/uploads/2021/05/legs-leg-wall-yoga-1296x728-header.jpg"},
        {"pose": "Upward Facing Dog", "image": "https://cdn-aolkg.nitrocdn.com/JEsNUzsMoDdLqhSXkopLhNFWnBniacqf/assets/images/optimized/rev-78567b4/www.yoganatomy.com/wp-content/uploads/2011/11/up-dog-squeeze-h.jpg"},
        {"pose": "Camel Pose", "image": "https://www.rishikulyogshalarishikesh.com/blog/wp-content/uploads/2023/12/camel-pose-img-3-1024x683.jpg"},
        {"pose": "Cobra Pose", "image": "https://www.yogafortimesofchange.com/wp-content/uploads/2015/10/Cobra.jpg"},
        {"pose": "Butterfly Pose", "image": "https://res.cloudinary.com/jerrick/image/upload/v1724238561/66c5cae117ed8f001d4dc79b.jpg"},
        {"pose": "Fish Pose", "image": "https://i.ndtvimg.com/i/2016-05/matsyasana_625x350_51462949432.jpg"},
        {"pose": "Low Lunge Pose", "image": "https://yogajala.com/wp-content/uploads/2022/09/low-lunge.jpg"},
        {"pose": "Supported Bridge Pose", "image": "https://i.pinimg.com/474x/46/a8/34/46a8348b76614a9cc77e854543c44ab0.jpg"},
        {"pose": "Cow Face Pose", "image": "https://cdn.prod.website-files.com/670a59845f0989763e175227/670a59845f0989763e17601e_Verywell-10-3567220-CowFace-783-598b736c68e1a2001182604e%20(1).jpg"},
        {"pose": "Hero Pose", "image": "https://static.wixstatic.com/media/4f41ec_9d99e8cbf4e745a19a5f58a30c50f791~mv2.png/v1/fill/w_1200,h_630,al_c/4f41ec_9d99e8cbf4e745a19a5f58a30c50f791~mv2.png"},
        {"pose": "Lotus Pose", "image": "https://omstars.com/blog/wp-content/uploads/2021/12/ig-feed-pose-breakdown-2021-Padmasana.png"},
        {"pose": "Extended Puppy Pose", "image": "https://www.doyou.com/wp-content/uploads/2021/01/How-To-Do-Extended-Puppy-Pose.jpg"}
    ]
}

@app.route('/recommend', methods=['POST'])
def recommend_yoga():
    data = request.json
    review = data.get('review', '')
    sentiment = sia.polarity_scores(review)
    score = sentiment['compound']
    predicted_mood = map_sentiment_to_mood(score)
    yoga_poses = mood_to_yoga.get(predicted_mood, [])
    recommended_yoga = random.sample(yoga_poses, min(len(yoga_poses), 4))
    return jsonify({"mood": predicted_mood, "yoga_poses": recommended_yoga})

if __name__ == '__main__':
    app.run(debug=True)
