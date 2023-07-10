from flask import render_template

def handle_error(e):
    # 处理错误的逻辑
    return render_template('error.html', error=e), 404