from flask import Flask, render_template, request, jsonify

from agent import SupportAgent


app = Flask(
    __name__,
    template_folder="../templates"
)


agent = SupportAgent()


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    data = request.get_json()

    if not data:

        return jsonify({
            "response": "Please enter a question.",
            "sources": []
        })

    message = data.get(
        "message",
        ""
    ).strip()

    if not message:

        return jsonify({
            "response": "Please enter a question.",
            "sources": []
        })

    try:

        result = agent.answer(
            message,
            session_id="web-session"
        )

        return jsonify(result)

    except Exception as error:

        print("ERROR:", error)

        return jsonify({
            "response": (
                "Sorry, something went wrong "
                "while processing your request."
            ),
            "sources": []
        }), 500


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )