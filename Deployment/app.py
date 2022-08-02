from flask import Flask,render_template,request
import pandas
import numpy as np
import pickle

popular = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score= pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular['Book-Title'].values),
                           author = list(popular['Book-Author'].values),
                           image = list(popular['Image-URL-M'].values),
                           votes = list(popular['Num of Ratings'].values),
                           rating = list(popular['avg of Ratings'].values),)

@app.route('/Recommend')
def recommend_ui():
    return render_template('Recommend.html')

@app.route('/Recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_books:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('Recommend.html',data=data)

if __name__ == "__main__":
    app.run(debug=True)