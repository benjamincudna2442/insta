import instaloader
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_cookies_from_txt(file_path):
    """Function to parse cookies from cookies.txt"""
    cookies = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Look for cookies in the appropriate format
            if '\t' in line:
                parts = line.strip().split('\t')
                if len(parts) >= 7:
                    cookies[parts[5]] = parts[6]  # key and value from the cookies.txt
    return cookies

def download_instagram_post(url, cookies):
    loader = instaloader.Instaloader(dirname_pattern='downloads', save_metadata=False)
    try:
        post_shortcode = url.split("/p/")[1].split("/")[0]
        post = instaloader.Post.from_shortcode(loader.context, post_shortcode)
        # Ensure cookies are used during the download
        loader.context.session.cookies.update(cookies)
        loader.download_post(post, target="insta_post")
        return f"[✔] Downloaded: {post_shortcode}"
    except Exception as e:
        return f"[✘] Failed to download post: {e}"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    cookies = get_cookies_from_txt('cookies.txt')  # Provide the path to your cookies.txt

    if not cookies:
        return jsonify({"error": "No cookies provided"}), 400

    result = download_instagram_post(url, cookies)
    return jsonify({"message": result})


if __name__ == '__main__':
    app.run(debug=True)
