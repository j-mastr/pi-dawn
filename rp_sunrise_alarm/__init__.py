import os

import flask
import requests

from rp_sunrise_alarm import model
from rp_sunrise_alarm import comm

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


class VueFlask(flask.Flask):
    @property
    def static_folder(self):
        if self.debug:
            return None
        else:
            return os.path.join(ROOT_PATH, 'static')


def create_app():
    app = VueFlask(__name__,
                   static_folder=None,
                   template_folder=os.path.join(ROOT_PATH, 'frontend'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/alarms.db'.format(app.instance_path)
    app.config['REDIS_QUEUE_KEY'] = 'rp_sunrise_alarm_alarm_queue'
    app.config['REDIS_STATE_KEY'] = 'rp_sunrise_alarm_state'
    app.config['ALARM_PRE_DURATION'] = 60 * 30
    app.config['ALARM_POST_DURATION'] = 60 * 30

    model.db.init_app(app)
    model.db.app = app

    return app

app = create_app()


@app.route('/api/1.0/alarm', methods=['GET'])
def get_alarms():
    alarms = model.Alarm.query.all()
    return flask.jsonify([alarm.to_dict() for alarm in alarms])


@app.route('/api/1.0/alarm', methods=['POST'])
def add_alarm():
    alarm = model.Alarm()
    alarm.update_from_dict(flask.request.json)
    alarm.schedule_next_alarm()
    model.db.session.add(alarm)
    model.db.session.commit()
    comm.send_message(app, comm.ReloadAlarmsMessage())
    return flask.jsonify(alarm.to_dict())


@app.route('/api/1.0/alarm/<int:id>', methods=['GET'])
def get_alarm(id):
    alarm = model.Alarm.query.filter(model.Alarm.id == id).first()
    if alarm is None:
        flask.abort(404)
    return flask.jsonify(alarm.to_dict())


@app.route('/api/1.0/alarm/<int:id>', methods=['PATCH'])
def update_alarm(id):
    alarm = model.Alarm.query.filter(model.Alarm.id == id).first()
    if alarm is None:
        flask.abort(404)
    alarm.update_from_dict(flask.request.json)
    alarm.schedule_next_alarm()
    model.db.session.add(alarm)
    model.db.session.commit()
    comm.send_message(app, comm.ReloadAlarmsMessage())
    return flask.jsonify(alarm.to_dict())


@app.route('/api/1.0/alarm/<int:id>', methods=['DELETE'])
def delete_alarm(id):
    alarm = model.Alarm.query.filter(model.Alarm.id == id).first()
    if alarm is None:
        flask.abort(404)
    model.db.session.delete(alarm)
    model.db.session.commit()
    comm.send_message(app, comm.ReloadAlarmsMessage())
    return '', 204

@app.route('/api/1.0/light', methods = ['GET'])
def get_light():
    state = comm.get_state(app)
    return flask.jsonify({'on': state.light_on})


@app.route('/api/1.0/light', methods = ['PATCH'])
def patch_light():
    state = comm.get_state(app)
    new_light_on = bool(flask.request.json.get('on'))
    if new_light_on != state.light_on:
        comm.send_message(app, comm.SetLightStateMessage(on=new_light_on))
    return flask.jsonify({'on': new_light_on})


@app.route('/api', defaults={'path': ''})
@app.route('/api/<path:path>')
def api_four_oh_four(path):
    flask.abort(404)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        rq = requests.get('http://localhost:8080/{}'.format(path))
        return flask.Response(rq.content, mimetype=rq.headers['Content-Type'])
    return flask.render_template("index.html")


@app.cli.command()
def initdb():
    if not os.path.exists(app.instance_path):
        os.mkdir(app.instance_path)
    model.db.create_all()
