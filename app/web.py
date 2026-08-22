from flask import Flask, render_template, request
from agent import SupportAgent


app = Flask(__name__)

agent = SupportAgent()


@app.route("/", methods=["GET", "POST"])
def home():

    answer = None
    sources = []
    question = ""

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        ).strip()

        if question:

            result = agent.answer(
                question,
                session_id="web-user"
            )

            answer = result.get(
                "response",
                ""
            )

            sources = result.get(
                "sources",
                []
            )

    return render_template(
        "index.html",
        answer=answer,
        sources=sources,
        question=question,
    )


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )