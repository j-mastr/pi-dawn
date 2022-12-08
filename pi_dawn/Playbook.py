import attr

from .graphics.Color import Color
from .graphics.Geometry import Fill, Gradient
from .graphics.Surface import Surface
from .graphics.Transition import Blend
from pi_dawn.play.Screenwriter import Screenwriter
from pi_dawn import app

Sunrise = (Screenwriter()
    .start_from(Gradient([
        Gradient.Stop(0.0, Color(0, 0, 0)),
        Gradient.Stop(1.0, Color(0, 0, 0)),
    ]))
    .transition(Blend(), duration=0.33)
    .to(Gradient([
        Gradient.Stop(0.0, Color(51, 0, 105)),
        Gradient.Stop(0.75, Color(51, 0, 105)),
        Gradient.Stop(1.0, Color(255, 0, 0)),
    ]))
    .then(Blend(), duration=0.33)
    .frame(Gradient([
        Gradient.Stop(0.0, Color(127, 0, 0)),
        Gradient.Stop(0.5, Color(127, 0, 0)),
        Gradient.Stop(1.0, Color(255, 255, 0)),
    ]))
    .transition(Blend(), duration=0.33)
    .frame(Fill(Color(255, 255, 255)))
    .duration(app.config['ALARM_PRE_DURATION'])
    .write()
    )
