import smbus
import time

######################################
#
# Class for controlling PT2314 via i2c 
# 4-channel input audo processor
#
# Ronald Diaz ronald@ronalddiaz.net
#
class PT2314:
  def __init__(self):
    try:
      # open Linux device /dev/i2c-0
      self.i2c = smbus.SMBus(1)
    except:
      pass
    self.i2cAddress = 0x44    
    self.volume = 0x20   # volume = minimum
    self.attenuationL = 0# (-x -> x ? )
    self.attenuationR = 0# (-x -> x ? )
    self.mute = False    # mute on
    self.loudness = True # loudness on
    self.channel = 0     # channel 0 selected [ 0 > 3 ]
    self.bass = 0x0F     # bass = 0
    self.treble = 0x0F   # treble = 0    
    self._updateAll()    # Initialise all 
    
  # High Level Commands

  def setVolume(self, volume):
    self.volume = volume
    self._updateVolume()
    
  def muteOn(self):
    self.mute = True
    self._updateAttenuation()    

  def muteOff(self):
    self.mute = False
    self._updateAttenuation()

  def selectChannel(self, ch):
    self.channel = ch
    self._updateAudioSwitch()
  
  def loudnessOn(self):
    self.loudness = True
    self._updateAudioSwitch()
    
  def loudnessOff(self):
    self.loudness = False
    self._updateAudioSwitch()
    
  def setAttenuation(self, l, r):
    self.attenuationL = l
    self.attenuationR = r
    self._updateAttenuation()
    
  def setBass(self, bass):
    self.bass = bass
    self._updateBass()

  def setTreble(self, treble):
    self.treble = treble
    self._updateTreble()

  # Low Level Commands

  def _updateVolume(self):
    self._sendByte(self.volume)
    
  def _updateAttenuation(self):
    if self.mute == True:
      self._sendByte(0xDF)      
      self._sendByte(0xFF)
    else:
      self._sendByte(0xC0 | self.attenuationL)
      self._sendByte(0xE0 | self.attenuationR)
    
  def _updateAudioSwitch(self):           
    audioByte = 0x58          # Audio Switch Byte 
    if self.loudness == True: # Loudness
      audioByte |= 0x00
    else:
      audioByte |= 0x04    
    audioByte |= self.channel # Select Channel
    self._sendByte(audioByte) # Send Byte

  def _updateBass(self):
    self._sendByte(0x60 | self.bass)

  def _updateTreble(self):
    self._sendByte(0x70 | self.bass)
    
  def _updateAll(self):    
    self._updateVolume()
    self._updateAttenuation()
    self._updateAudioSwitch()
    self._updateBass()
    self._updateTreble()
    
  def _sendByte(self, b):
    print "data: %x" % b
    try:
      self.i2c.write_byte(self.i2cAddress, b) # send data via i2c    
    except:
      #print "exception"
      pass