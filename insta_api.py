import instaloader
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_cookies_from_txt(file_path):
    """Function to parse cookies from cookies.txt"""
    cookies = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '\t' in line:
                parts = line.strip().split('\t')
                if len(parts) >= 7:
                    cookies[parts[5]] = parts[6]
    return cookies

def download_instagram_post(url, cookies):
    loader = instaloader.Instaloader(save_metadata=False)

    # Create a custom session and add the cookies
    session = requests.Session()
    session.cookies.update(cookies)

    # Set the session for instaloader context
    loader.context._session = session

    try:
        post_shortcode = url.split("/p/")[1].split("/")[0]
        post = instaloader.Post.from_shortcode(loader.context, post_shortcode)

        # Get all image URLs (for carousel posts)
        image_urls = [node.url for node in post.get_images()]
        return image_urls
    except Exception as e:
        print(f"[✘] Failed to download post: {e}")
        return None

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    cookies = get_cookies_from_txt('cookies.txt')  # Provide the path to your cookies.txt

    if not cookies:
        return jsonify({"error": "No cookies provided"}), 400

    image_urls = download_instagram_post(url, cookies)

    if image_urls:
        return jsonify({
            "message": "[✔] Images downloaded successfully!",
            "download_links": image_urls
        })
    else:
        return jsonify({"error": "Failed to download the post images"}), 400

if __name__ == '__main__':
    app.run(debug=True)
