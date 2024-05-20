# run.py
import os
from app import app

if __name__ == '__main__':
    app.config['SECRECT_KEY'] = 'blog_platform_587'
    app.run(debug=True)
