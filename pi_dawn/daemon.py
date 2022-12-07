import signal
import datetime
import threading
import time

from pi_dawn import app
from pi_dawn import comm
from pi_dawn.graphics import Geometry, Sunrise
from pi_dawn import model
from pi_dawn import Wire
from pi_dawn import Screen

def shutdown(signum, frame):
    comm.send_message(app, comm.StopMessage())


def clear_screen(led_screen):
    surface = led_screen.make_surface()
    surface.draw(Geometry.Fill((0, 0, 0)))
    led_screen.draw_surface(surface)


def configure_surface(state, surface, sunrise_alarm):
    if state.light_on:
        surface.draw(Geometry.Fill((255, 255, 255)))
    else:
        if state.active_alarm == -1:
            surface.draw(Geometry.Fill((0, 0, 0)))
        else:
            sunrise_alarm.draw(surface, state.alarm_pos)
    
    return surface


def reschedule_alarms(alarms):
    dirty = False
    cutoff = datetime.datetime.now() - datetime.timedelta(seconds=app.config['ALARM_POST_DURATION'])
    for alarm in alarms:
        if alarm.next_alarm is not None and alarm.next_alarm < cutoff:
            dirty = True
            if not alarm.repeat:
                alarm.enabled = False
            alarm.schedule_next_alarm()
    if dirty:
        model.db.session.commit()


def find_active_alarm(alarms):
    now = datetime.datetime.now()
    for alarm in alarms:
        alarm_time = alarm.next_alarm
        if alarm_time is None:
            continue
        diff = (now - alarm_time).total_seconds()
        if diff < 0 and -diff < app.config['ALARM_PRE_DURATION']:
            return alarm, diff / app.config['ALARM_PRE_DURATION']
        elif diff > 0 and diff < app.config['ALARM_POST_DURATION']:
            return alarm, diff / app.config['ALARM_POST_DURATION']
    return None, 0

def set_alarm_pos(state, alarms):
    active_alarm, alarm_pos = find_active_alarm(alarms)
    if active_alarm is None:
        state.active_alarm = -1
        state.alarm_pos = 0
    else:
        state.active_alarm = active_alarm.id
        state.alarm_pos = alarm_pos


class StoppeableThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.stopRequested = False
        self.stopped = False
        self.threadLock = threading.Lock() # Using the lock to block until stopped

    def run(self):
        try:
            self.threadLock.acquire()
            while not self.stopRequested:
                self.execute()
        except Exception as e:
            raise e
        finally:
            self.stopped = True
            self.threadLock.release()
    
    def execute(self):
        pass

    def onStop(self):
        pass
    
    # Blocks until threadLock is released
    def stop(self):
        if not self.stopped:
            self.stopRequested = True
            self.onStop()
            self.wait()

    def wait(self):
        if self.stopped:
            return

        self.threadLock.acquire()
        self.threadLock.release()

class Redraw (StoppeableThread):
    def __init__(self, state, led_screen):
        StoppeableThread.__init__(self)

        self.state = state
        self.led_screen = led_screen
        self.sunrise_alarm = Sunrise(led_screen)

    def execute(self):
        with app.app_context():
            surface = self.led_screen.make_surface()
            configure_surface(self.state, surface, self.sunrise_alarm)
            self.led_screen.draw_surface(surface)
    
    # Blocks until threadLock is released
    def onStop(self):
        self.led_screen.reset()


class Schedule (StoppeableThread):
    def __init__(self, state):
        StoppeableThread.__init__(self)

        with app.app_context():
            self.state = state
            self.alarms = model.Alarm.query.order_by(model.Alarm.time).all()

    def execute(self):
        with app.app_context():
            set_alarm_pos(self.state, self.alarms)
            reschedule_alarms(self.alarms)
            comm.set_state(app, self.state)

    def reload(self):
        with app.app_context():
            model.db.session.rollback()
            self.alarms = model.Alarm.query.order_by(model.Alarm.time).all()


def main():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    state = comm.State()
    led_screen = Screen.Screen(hardware=Wire.wired)

    redrawThread = Redraw( state, led_screen )
    scheduleThread = Schedule( state )
    redrawThread.start()
    scheduleThread.start()

    while True:
        msg = comm.receive_message(app, timeout=None)
        led_screen.reset()
        if isinstance(msg, comm.StopMessage):
            break
        elif isinstance(msg, comm.SetLightStateMessage):
            state.light_on = msg.on
        elif isinstance(msg, comm.ReloadAlarmsMessage):
            scheduleThread.reload()

    redrawThread.stop()
    scheduleThread.stop()
    clear_screen(led_screen)
