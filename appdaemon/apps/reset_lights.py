import appdaemon.plugins.hass.hassapi as hass
import datetime

class ResetLights(hass.Hass):
  groups = ['living_room_lights', 'kitchen_lights', 'bedroom_lights']

  def initialize(self):
    time = datetime.time(13, 00, 0)
    self.run_daily(self.run_daily_callback, time)

  def run_daily_callback(self, kwargs):
    self.log('daily callback fired')
    self.on_lights = []

    self.turn_on_lights()

    self.run_in(self.turn_off_lights, 30)

  # turn on the lights to 100%, recording which were already turned on
  def turn_on_lights(self):
    self.log('lights about to turn on')
    for group_name in ResetLights.groups:
      group = self.entities.group[group_name]
      for light in group.attributes.entity_id:
        if self.get_state(light) == 'on':
          self.on_lights.append(light)
        self.turn_on(light, brightness_pct=100)
    self.log('lights on')

  # turn off the lights that were not on previously
  def turn_off_lights(self, kwargs):
    self.log('lights about to turn off')
    for group_name in ResetLights.groups:
      group = self.entities.group[group_name]
      for light in group.attributes.entity_id:
        if light not in self.on_lights:
          self.turn_off(light)
    self.log('lights off')
