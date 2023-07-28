from time import sleep
from flask import Flask, request, jsonify
from getInfoAboutGraphs import get_info_about_graphs
from yelp_sentiment_analysis import get_plot
from flask_cors import CORS
from returnobj import returnObj

app = Flask(__name__)
CORS(app, resources={r"/getGraph/*": {"origins": "http://localhost:3000"}})


@app.route("/", methods=["GET"])
def basicGet():
    return "Hello to the World"


@app.route("/getGraph", methods=["GET"])
def get_graph():
    status_code = 418

    firstUrl = request.args.get("url1")
    secondUrl = request.args.get("url2")
    print("firstUrl", firstUrl)
    print("secondUrl", secondUrl)

    # Sleep is for testing
    sleep(5)
    print("data returned")
    return {"data": returnObj}

    try:
        base64Url1, graphPointsUrl1 = get_plot(firstUrl)
        base64Url2, graphPointsUrl2 = get_plot(secondUrl)
        status_code = 200
        print("graphPointsUrl1", graphPointsUrl2)
        print("graphPointsUrl1", graphPointsUrl2)

        response = {
            "data": {
                "url": firstUrl,
                "url1GraphImage": base64Url1,
                "url2GraphImage": base64Url2,
                "gptBlurb": get_info_about_graphs(graphPointsUrl1, graphPointsUrl2),
            }
        }

    except Exception as e:
        print("There was an error", e)
        status_code = 500

        response = {"data": {"url": firstUrl, "graph": "There was an error"}}

    return response, status_code


if __name__ == "__main__":
    app.run(debug=True)
