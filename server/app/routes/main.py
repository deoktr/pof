from flask import Blueprint, send_from_directory

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return send_from_directory("html", "index.html")


@main_bp.get("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon.png")


@main_bp.get("/robots.txt")
def robots():
    return """User-agent: *
Allow: /
"""
