class Customer:
	def __init__(self, name: str):
		self.name = name
		self.id = None
		self.borrowed = 0
		self.returned = 0