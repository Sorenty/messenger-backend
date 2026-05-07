from flask import Blueprint, request, jsonify, g, current_app
from werkzeug.utils import secure_filename
from pathlib import Path
from ..models.post import Post
from ..utils.db import db

posts_bp = Blueprint("posts", __name__)
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@posts_bp.route("", methods=["GET"])
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([{
        "id": p.id,
        "text": p.text,
        "file_name": p.file_name,
        "file_path": p.file_path,
        "file_type": p.file_type,
        "created_at": p.created_at.isoformat(),
        "author_id": p.author_id,
    } for p in posts]), 200

@posts_bp.route("", methods=["POST"])
def create_post():
    if not g.current_user:
        return jsonify({"error": "unauthorized"}), 401

    text = request.form.get("text", "").strip()
    file = request.files.get("file")

    if not text and not file:
        return jsonify({"error": "text or file is required"}), 400

    file_name = file_path = file_type = None

    if file and file.filename:
        file_name = secure_filename(file.filename)
        file_path = str(UPLOAD_DIR / file_name)
        file.save(file_path)
        file_type = file.mimetype

    post = Post(
        author_id=g.current_user.id,
        text=text or "",
        file_name=file_name,
        file_path=file_path,
        file_type=file_type,
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "post created"}), 201