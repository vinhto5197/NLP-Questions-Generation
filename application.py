from flask import Flask, redirect, url_for, render_template, request, flash
import backend

# start app
application = Flask(__name__)
application.secret_key = "secret"
application.url_map.strict_slashes = False


@application.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        num_q = request.form["num_questions"]
        txt_doc = request.form["text"]
        valid_num_ques = num_q.isnumeric()
        valid_txt = len(txt_doc) > 0

        if not valid_num_ques:
            flash("Number of questions must be a number", "error")
            return render_template("home.html", num_q=num_q, txt_doc=txt_doc)
        elif not valid_txt:
            flash("Text must not be empty", "error")
            return render_template("home.html", num_q=num_q, txt_doc=txt_doc)
        else:
            return redirect(url_for("results", num_q=num_q, txt_doc=txt_doc))
    else:
        txt_doc = request.args.get("txt_doc", "")
        num_q = request.args.get("num_q", "")
        return render_template("home.html", num_q=num_q, txt_doc=txt_doc)


@application.route("/redirect/<sample>", methods=["POST", "GET"])
def redir(sample):
    file_name = sample + ".txt"
    with open("texts/" + file_name) as f:
        txt = f.read()
    return redirect(url_for("home", txt_doc=txt))


@application.route("/results")
def results():
    num_q = request.args.get("num_q", "")
    txt_doc = request.args.get("txt_doc", "")
    questions = backend.gen(num_q, txt_doc)
    return render_template("results.html", questions=questions, txt_doc=txt_doc)


@application.route("/known_issues")
def known_issues():
    return render_template("issues.html")


@application.route("/wiki_scraping")
def wiki_scraping():
    return render_template("wiki.html")


# call app
if __name__ == "__main__":
    application.run(debug=True)
