from flask import Flask, Response, render_template, session, request, jsonify

app = Flask(__name__)
app.secret_key = open('private/secret.txt').read()

flags = {
	'fake1': {
		'price': 125,
		'coupons': ['fL@__g'],
		'data': 'fake1{this_is_a_fake_flag}'
	},
	'fake2': {
		'price': 290,
		'coupons': ['fL@__g'],
		'data': 'fake2{this_is_a_fake_flag}'
	},
	'asis': {
		'price': 110,
		'coupons': [],
		'data': open('private/flag.txt').read()
	}
}

@app.route('/')
def main():
	if session.get('credit') == None:
		session['credit'] = 0
		session['coupons'] = []
	return render_template('index.html', credit = session['credit'])
	#return 'Hello World!<br>Your Credit is {}<br>Used Coupons is {}'.format(session.get('credit'), session.get('coupons'))

@app.route('/image')
def resouce():
	image_name = request.args.get('name')
	if '/' in image_name or '..' in image_name or 'private' in image_name:
		return 'Access Denied'
	return Response(open(image_name).read(), mimetype='image/png')

@app.route('/pay', methods=['POST'])
def pay():
	data = request.get_json()
	card = data['card']
	coupon = data['coupon']
	if coupon.replace('=','') in session.get('coupons'):
		return jsonify({'result': 'the coupon is already used'})
	for flag in card:
		if flag['count'] <= 0:
			return jsonify({'result':'item count must be greater than zero'})
	discount = 0
	for flag in card:
                if coupon.decode('base64').strip() in flags[flag['name']]['coupons']:
			discount += flag['count'] * flags[flag['name']]['price']
	credit = session.get('credit') + discount
	for flag in card:
		credit -= flag['count'] * flags[flag['name']]['price']
	if credit < 0:
		result = {'result': 'your credit not enough'}
	else:
		result = {'result': 'pay success'}
		result_data = []
		for flag in card:
			result_data.append({'flag': flag['name'], 'data': flags[flag['name']]['data']})
		result['data'] = result_data
		session['credit'] = credit
		session['coupons'].append(coupon.replace('=',''))
	return jsonify(result)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
