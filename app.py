from flask import Flask, render_template, request, flash, send_from_directory
import backend
import os

# start app
app = Flask(__name__)
app.secret_key = "secret"
app.url_map.strict_slashes = False


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        num_q = request.form["num_questions"]
        txt_doc = request.form["text"]
        valid_num_ques = num_q.isnumeric() and 1 <= int(num_q)
        valid_txt = len(txt_doc) > 0

        if not valid_num_ques:
            flash("Number of questions must be a positive number", "error")
            return render_template("home.html", num_q=num_q, txt_doc=txt_doc)
        elif not valid_txt:
            flash("Text must not be empty", "error")
            return render_template("home.html", num_q=num_q, txt_doc=txt_doc)
        else:
            questions = backend.gen(num_q, txt_doc)
            return render_template("results.html", questions=questions, txt_doc=txt_doc)
    else:
        txt_doc = request.args.get("txt_doc", "")
        num_q = request.args.get("num_q", "")
        return render_template("home.html", num_q=num_q, txt_doc=txt_doc)


@app.route("/<name>", methods=["POST", "GET"])
def sample(name):
    if request.method == "POST":
        num_q = request.form["num_questions"]
        txt_doc = request.form["text"]
        valid_num_ques = num_q.isnumeric() and 1 <= int(num_q)
        valid_txt = len(txt_doc) > 0

        if not valid_num_ques:
            flash("Number of questions must be a positive number", "error")
            return render_template("sample.html", num_q=num_q, txt_doc=txt_doc)
        elif int(num_q) > 10:
            flash("Please request fewer than 10 questions.", "error")
            return render_template("sample.html", num_q=num_q, txt_doc=txt_doc)
        elif not valid_txt:
            flash("Text must not be empty", "error")
            return render_template("sample.html", num_q=num_q, txt_doc=txt_doc)
        else:
            questions = backend.gen(num_q, txt_doc)
            return render_template("results.html", questions=questions, txt_doc=txt_doc)
    else:
        d = {"TigerWoods": "Tiger Woods", "XSXS": "Xbox Series X and Series S", "Python": "Python", "Dog": "Dog"}
        file_name = name + ".txt"
        with open("texts/" + file_name) as f:
            txt_doc = f.read()
        return render_template("sample.html", name=d[name], txt_doc=txt_doc)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico", mimetype="image/vnd.microsoft.icon")


@app.route("/known_issues")
def known_issues():
    return render_template("issues.html")


@app.route("/wiki_scraping")
def wiki_scraping():
    return render_template("wiki.html")


# call app
if __name__ == "__main__":
    app.run(debug=True)
