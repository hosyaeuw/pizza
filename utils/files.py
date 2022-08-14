from app import app


def get_img_url(filename):
    return f"/{app.config['MEDIA_FOLDER']}/{filename}"
