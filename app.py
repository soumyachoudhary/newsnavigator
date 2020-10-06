from flask import Flask, render_template, request
import model
from model import get_headlines

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    url = request.form['url']
    predict = model.predict(url)
    value = predict[1]
    clickbait = predict[2]
    text = predict[3]
    article_title = predict[0]
    model.update(value)
    model.update(clickbait)
    return render_template('results.html', 
                          value = value, 
                          clickbait = clickbait,
                          text = text,
                          article_title=article_title,
                          url=url)
  else:
    return render_template('index.html')


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/feed')
def feed():
  headlines = get_headlines()
  return render_template('feed.html',
                          headlines = headlines)


@app.route('/trends')
def trends():
  return render_template('trends.html', 
                        num_fake = model.get_data("FAKE"), 
                        num_real = model.get_data("REAL"), 
                        num_clickbait = model.get_data("CLICKBAIT"), num_notclickbait = model.get_data("NOT CLICKBAIT"))
 
if __name__ == "__main__": 
  app.run() 
