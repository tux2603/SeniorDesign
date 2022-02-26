import cv2
from flask import Flask, make_response, render_template
from LineFollowing.LineFollowing import LineFollower

app = Flask(__name__)

    

@app.route('/')
def index():
    return 'Hello, World! Welcome to the Bartender Bot'


@app.route('/admin')
def admin():
    return render_template('admin/adminPage.html')


@app.route('/admin/line_follower')
def line_follower():
    if line_follower.latency >= 5000:
        status = 'is broken'
    elif line_follower.latency >= 1000:
        status = 'is slow'
    elif not line_follower.is_line_acquired:
        status = 'does not see the line'
    elif line_follower.steering == -1:
        status = 'needs to turn left'
    elif line_follower.steering == 0:
        status = 'needs to go straight'
    elif line_follower.steering == 1:
        status = 'needs to turn right'
    else:
        status = 'is broken'

    return render_template('admin/line_follower.html', status=status)


@app.route('/admin/line_follower/image')
def line_follower_image():
    image = line_follower.frame
    response = make_response(image.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route('/customer/order')
def customer_order():
    return render_template('Customer/customerPage.html')


if __name__ == '__main__':
    line_follower = LineFollower(show_debug_window=True)
    app.run(host='localhost', port=8080, debug=False)

    line_follower.stop()
    