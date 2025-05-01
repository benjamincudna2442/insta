from flask import Flask, request, jsonify
import instaloader
import os

app = Flask(__name__)

# Function to download Instagram post using Instaloader
def download_instagram_post(url, cookies):
    loader = instaloader.Instaloader(dirname_pattern='downloads', save_metadata=False)
    loader.context.session.cookies.update(cookies)
    
    try:
        post_shortcode = url.split("/p/")[1].split("/")[0]
        post = instaloader.Post.from_shortcode(loader.context, post_shortcode)
        loader.download_post(post, target="insta_post")
        return f"Downloaded: {post_shortcode}", None
    except Exception as e:
        return None, f"Failed to download post: {e}"

# Route to handle the download request
@app.route('/download', methods=['GET'])
def handle_download():
    url = request.args.get('url')
    cookies = request.cookies.get('cookie')  # Assuming cookie is passed from client-side
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    if not cookies:
        return jsonify({'error': 'No cookies provided'}), 400
    
    # Try downloading the Instagram post
    message, error = download_instagram_post(url, cookies)
    
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify({'message': message}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
