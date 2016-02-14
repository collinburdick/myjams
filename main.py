import os, soundcloud, urllib, string, zipfile

from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, static_url_path='')
app.SECRET_KEY = os.urandom(24)
app.debug = True
app.config['soundcloud_id'] = '71cb4b050d554c977dfa40be99dda7ba'
app.config['soundcloud_secret'] = '93e3223e55ae98ee3350be6f6d90e2b1'

@app.route("/")
def index():
    return "<form action='/soundcloudDownloader' method='post'><input type='email' name='username' placeholder='Soundcloud Email'><br><input type='password' name='password' placeholder='Soundcloud Password'><br><input type='number' name='numberoffavs' value='1' placeholder='Number of Favorites (max 200)'><br><input type='submit' value='Download Your Latest Soundcloud Jamz'></form>"
 
@app.route('/<path:filename>')
def download_file(fname):
    return send_from_directory('', fname, as_attachment=True)
	
@app.route("/soundcloudDownloader", methods=['POST'])
def soundcloudDownloader(): 
	print "in the downloader"
	if request.method == 'POST':
		print "valid"
		app.config['soundcloud_username'] = request.form['username']
		app.config['soundcloud_password'] = request.form['password']
		numberOfFavs = request.form['numberoffavs']
		soundcloud_login_info = soundcloud.Client(client_id=app.config['soundcloud_id'], client_secret=app.config['soundcloud_secret'], username=app.config['soundcloud_username'], password=app.config['soundcloud_password'])
		my_soundcloud_id = soundcloud_login_info.get('/me').id
		my_soundcloud_favorites = soundcloud_login_info.get('/users/' + str(my_soundcloud_id) + '/favorites?limit=' + numberOfFavs + '?linked_partitioning=1')
		count=-1
		favorites_length = my_soundcloud_favorites[1].obj
		zfile = zipfile.ZipFile('MySoundcloudFavorites.zip', 'w')
		for fav_num in my_soundcloud_favorites:
			count += 1
			try: 
				fav = my_soundcloud_favorites[count].obj
				artist = fav['user']['username']
				title = fav['title']
				fav_stream_url = fav['stream_url']
				stream_url = soundcloud_login_info.get(fav_stream_url, allow_redirects=False).location
				filename = artist + " - " + title + ".mp3"
				filename = string.replace(filename, '<', " ")
				filename = string.replace(filename, '>', " ")
				filename = string.replace(filename, ':', " ")
				filename = string.replace(filename, '"', " ")
				filename = string.replace(filename, '/', " ")
				filename = string.replace(filename, '\\', " ")
				filename = string.replace(filename, '|', " ")
				filename = string.replace(filename, '?', " ")
				filename = string.replace(filename, '*', " ")
				print "Working on " + filename
				savedSCfile = urllib.URLopener()
				savedSCfile.retrieve(stream_url, filename)
				zfile.write(filename)
				os.remove(filename)
			except:
				continue
	else:
		print "invalid"
		return "form not posted"
	zfile.close()
	return download_file('MySoundcloudFavorites.zip')

#@app.route('/', methods=['GET', 'POST'])
#def index():
#	return render_template('index.html')
#
#@app.post('/', methods=['GET', 'POST'])
#def soundcloudDownloader():

if __name__ == '__main__':
	app.run(port=5000, host='127.0.0.1')
