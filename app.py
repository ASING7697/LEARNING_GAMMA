from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_file, url_for
import yt_dlp

app = Flask(__name__)
app.secret_key = "change-me"

BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        output_format = request.form.get("format", "").strip()

        if not url:
            flash("Please provide a URL to download.")
            return redirect(url_for("index"))

        ydl_opts = {
            "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
            "format": output_format or "best",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        file_path = Path(filename)
        if not file_path.exists():
            flash("Download finished but the file could not be found.")
            return redirect(url_for("index"))

        return send_file(file_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
