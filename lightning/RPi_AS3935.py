import time

class RPi_AS3935:
	#Developed by  Phil Fenstermacher. Revised by Hiroshi Ishikawa.
	def __init__(self, address, bus=1):
		self.address = address
		import smbus
		self.i2cbus = smbus.SMBus(bus)

	def calibrate(self, tun_cap=None):
		time.sleep(0.08)
		self.read_data()
		if tun_cap is not None:
			if tun_cap < 0x10 and tun_cap > -1:
				self.set_byte(0x08, (self.registers[0x08] & 0xF0) | tun_cap)				
				time.sleep(0.002)
			else:
				raise Exception("Value of TUN_CAP must be between 0 and 15")
		self.set_byte(0x3D, 0x96)#CALIB_RCO
		time.sleep(0.002)
		self.read_data() 
		self.set_byte(0x08, self.registers[0x08] | 0x20)
		time.sleep(0.002)
		self.read_data() 
		self.set_byte(0x08, self.registers[0x08] & 0xDF)
		time.sleep(0.002)

	def reset(self):
		self.set_byte(0x3C, 0x96)

	def get_interrupt(self):
		self.read_data()
		return self.registers[0x03] & 0x0F

	def get_distance(self):
		self.read_data()
		return self.registers[0x07] & 0x3F

	def get_energy(self):
		self.read_data()
		return ((self.registers[0x06] & 0x1F) * 65536)+ (self.registers[0x05] * 256)+ (self.registers[0x04])

	def get_noise_floor(self):
		self.read_data()
		return (self.registers[0x01] & 0x70) >> 4

	def set_noise_floor(self, noisefloor):
		self.read_data()
		noisefloor = (noisefloor & 0x07) << 4
		write_data = (self.registers[0x01] & 0x8F) + noisefloor
		self.set_byte(0x01, write_data)

	def lower_noise_floor(self, min_noise=0):
		floor = self.get_noise_floor()
		if floor > min_noise:
			floor = floor - 1
			self.set_noise_floor(floor)
		return floor

	def raise_noise_floor(self, max_noise=7):
		floor = self.get_noise_floor()
		if floor < max_noise:
			floor = floor + 1
			self.set_noise_floor(floor)
		return floor

	def get_min_strikes(self):
		self.read_data()
		value = (self.registers[0x02] >> 4) & 0x03
		if value == 0:
			return 1
		elif value == 1:
			return 5
		elif value == 2:
			return 9
		elif value == 3:
			return 16

	def set_min_strikes(self, minstrikes):
		if minstrikes == 1:
			minstrikes = 0
		elif minstrikes == 5:
			minstrikes = 1
		elif minstrikes == 9:
			minstrikes = 2
		elif minstrikes == 16:
			minstrikes = 3
		else:
			raise Exception("Value must be 1, 5, 9, or 16")

		self.read_data()
		minstrikes = (minstrikes & 0x03) << 4
		write_data = (self.registers[0x02] & 0xCF) + minstrikes
		self.set_byte(0x02, write_data)

	def get_indoors(self):
		self.read_data()
		if self.registers[0x00] & 0x10 == 0x10:#pending
			return True
		else:
			return False

	def set_indoors(self, indoors):
		self.read_data()
		if indoors:
			write_value = (self.registers[0x00] & 0xC1) | (0b10010 << 1) #
		else:
			write_value = (self.registers[0x00] & 0xC1) | (0b01110 << 1) #
		self.set_byte(0x00, write_value)

	def set_mask_disturber(self, mask_dist):
		self.read_data()
		if mask_dist:
			write_value = self.registers[0x03] | 0x20
		else:
			write_value = self.registers[0x03] & 0xDF
		self.set_byte(0x03, write_value)

	def get_mask_disturber(self):
		self.read_data()
		if self.registers[0x03] & 0x20 == 0x20:
			return True
		else:
			return False

	def set_byte(self, register, value):
		self.i2cbus.write_byte_data(self.address, register, value)

	def read_data(self):
		self.registers = self.i2cbus.read_i2c_block_data(self.address, 0x00)

	def set_disp_lco(self, display):
		self.read_data()
		if display:
			self.set_byte(0x08, (self.registers[0x08] | 0x80))
		else:
			self.set_byte(0x08, (self.registers[0x08] & 0x7F))
		time.sleep(0.002)
