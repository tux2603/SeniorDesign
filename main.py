import cv2
from flask import Flask, make_response, render_template, request, redirect, url_for
from LineFollowing.LineFollowing import LineFollower

app = Flask(__name__)

order_queue = []    

@app.route('/')
def index():
    return 'Hello, World! Welcome to the Bartender Bot'


@app.route('/admin')
def admin():
    if request.args.get('clear_queue') == '1':
        order_queue.clear()
        return redirect(url_for('admin'))
    return render_template('admin/adminPage.html', order_queue=order_queue)


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


@app.route('/customer/order', methods=['GET', 'POST'])
def customer_order():
    if request.method == 'POST':
        drink = request.form.get('drink')
        station = request.form.get('station')
        order_queue.append((drink, station))
        return render_template('customer/order_placed.html', drink=drink, station=station, queue_position=len(order_queue))
    else:
        # get the station from the URL
        station = request.args.get('station')
        return render_template('customer/customerPage.html', station=station)


if __name__ == '__main__':
    line_follower = LineFollower(show_debug_window=True)
    app.run(host='localhost', port=8080, debug=True)

    line_follower.stop()
    