from flask import Flask
from flask import send_from_directory
from flask import request
from flask import jsonify
from flask import redirect
from twitter import Twitter
from instoosh import Instoosh
from sentiment_analyzer import classifyTweets
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import os
import instoosh
import re

# Flask configuration
app = Flask(__name__)
app.debug = True
app.root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static/dist/'))
twit = Twitter() 
ins = Instoosh()
'''
Example usage:

	tweets = twit.get_twitter_data('iphone', 'today' or 'lastweek') - get tweets for a given keyword
	tweets = twit.traslate_tweets(tweets) - replace emojis to constant words
	tweets = twit.process_tweets(tweets)	- preprocessing tweets before creating the feature_vectors 
	twit.map_to_vectores(twits) - map all tweets to feature_vectores
'''

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
   
@app.route('/')
def index():
	return redirect('index.html')

@app.route('/<path:path>', methods=['GET'])
@crossdomain(origin='*')
def hello(path):
	return send_from_directory(app.root, path)

@app.route("/rate", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def rate_place():
	'''
		rate() return rating on a specific place
		example:
			/rate??place=some_value
	'''
	place = request.args.get('place')
	tweets = twit.get_twitter_data(place, 'today')
	tweets = twit.traslate_tweets(tweets)
	tweets = twit.process_tweets(tweets)
	vecs = twit.map_to_vectores(tweets)
	return jsonify(place=place, rating=classifyTweets(vecs))

@app.route("/photos", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_photos():
	'''
		example:
			/photos?name=some_value&geo=123,123
	'''
	place = request.args.get('place')
	geo = request.args.get('geo')
	geo = tuple(re.split(' *, *', geo))
	posts, photos = ins.get_posts(place, geo)
	return jsonify(place=place, posts=posts, photos=photos)


if __name__ == "__main__":
	app.run(threaded=True, port=3000, host='0.0.0.0')
