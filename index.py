from flask import Flask, request, render_template

app = Flask(__name__)


# Showing HTML ON THE WEB THORUGH FLASK - py framwork for making web apps
@app.route('/', methods=['GET'])
def index():
    # Just render the form page
    return render_template('index.html')

# Handle the POST method
@app.route('/reportcard' , methods =['POST'] )
def reportcard():
    return f''                #Response of LLM

if __name__ == '__main__':
    app.run(debug=True)
