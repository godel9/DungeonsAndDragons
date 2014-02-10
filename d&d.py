#Weapon:
#	Proficiency: Simple, Martial, Exotic
#	Encumberance: Light, One-Handed, Two-Handed, Ranged
#	Affinity: Race Associated (if applicable)
#	Price:
#	Damage:
#	Critical:
#	DamageType: B,P,S,etc. (can use multiple to stack)
#	Special:

#Unit:
#Name	[CR]
#[XP]
#Race Classes...
#Lineage (ex. Medium Humanoid (elf, human))
#Init
#Senses
#DEFENSE
#	AC: Reg, touch, flat-footed (armor modifier, dex)
#	HP: actual (hd)
#	Fort, Reflex & Will: Bonuses (ex. x2 vs. enchantments)
#	Immunities (if any)
#OFFENSE
#	Speed
#	Melee:
#		Weapons w/ damage ...
#	Ranged:
#		Weapons w/ damage ...
#	Special Attacks:
#		...
#	[Tactics]
#STATISTICS
#	STR, DEX, CON, INT, WIS, CHA
#	Base Attack Bonus
#	Combat Maneuver Bonus
#	Combat Maneuver Defense
#	Feats...
#	Skills...
#	Languages...
#	SQ...
#	Combat Gear...



#Feats:
#Acrobatic: {
#	required: {},
#	gives: {
#		skill: {
#			Acrobatics: 2,
#			Fly: 2
#		}


import random
from numpy.random import binomial
import re
import itertools
random.seed()

class Struct:
	def __init__(self, **kargs):
		self.__dict__.update(kargs)

def dict_clone(d):
	tmp = {}
	for key,val in d.iteritems():
		tmp[key] = val
	return tmp

def d(a,b):
	return sum([random.randint(1,b) for i in xrange(a)])

def randomChoice(points, L):
	tmp = {}
	tot = len(L)
	random.shuffle(L)
	for i,rank in zip(L,binomial(points,1/float(tot),tot).tolist()):
		if points > 0 and rank > 0:
			tmp[i] = rank
			points -= rank
	if points > 0:
		if L[0] not in tmp:
			tmp[L[0]] = 0
		tmp[L[0]] += points
	return tmp		

def genAbility():
	tmp = [d(1,6) for count in range(4)]
	tmp.remove(min(tmp))
	return sum(tmp)

def modifier(ability):
	return int((ability - 10)/2)

def compound(dice,mul):
	a,b = tuple(dice.split('d'))
	if a == '':
		return str(mul) + dice
	return '%id%i' % (mul*int(a),b)

roll_regex = re.compile(r'([0-9]+\*)?([0-9]+)d([0-9]+)(\+[0-9]+|-[0-9]+)?')
def roll(die):
	tmp = roll_regex.match(die)
	mul = 1
	if tmp.group(1):
		mul = int(tmp.group(1)[:-1])
	a = int(tmp.group(2))
	b = int(tmp.group(3))
	plus = 0
	if tmp.group(4):
		plus = int(tmp.group(3))
	return mul*d(a,b) + plus

crit_regex = re.compile(r'([0-9]+-[0-9]+/)?x([0-9]+)')
def crit(stat,roll):
	tmp = crit_regex.match(stat)
	low = 20
	high = 20
	if tmp.group(1):
		low,high = tmp.group(1)[:-1].split('-')
		low,high = (int(low),int(high))
	mul = tmp.group(2)
	if roll in range(low,high):
		return int(mul)
	return 1



TinyWeaponDamage = {
	'1d3': '1d1',
	'1d4': '1d2',
	'1d6': '1d3',
	'1d8': '1d4',
	'1d10': '1d6',
	'1d12': '1d8',
	'2d4': '1d4',
	'2d6': '1d8',
	'2d8': '1d10',
	'2d10': '2d6'
}
LargeWeaponDamage = {
	'1d3': '1d3',
	'1d4': '1d4',
	'1d6': '1d6',
	'1d8': '1d8',
	'1d10': '2d6',
	'1d12': '2d8',
	'2d4': '3d6',
	'2d6': '2d6',
	'2d8': '3d8',
	'2d10': '4d8'
}
SizeModifierTable = {
	'Colossal': -8,
	'Gargantuan': -4,
	'Huge': -2,
	'Large': -1,
	'Medium': 0,
	'Small': 1,
	'Tiny': 2,
	'Diminutive': 4,
	'Fine': 8,
}
SizesList = ['Fine','Diminutive','Tiny','Small','Medium','Large','Huge','Gargantuan','Colossal']
SkillAbility = {
	'Acrobatics': 'DEX',
	'Appraise': 'INT',
	'Bluff': 'CHA',
	'Climb': 'STR',
	'Craft': 'INT',
	'Diplomacy': 'CHA',
	'DisableDevice': 'DEX',
	'Disguise': 'CHA',
	'EscapeArtist': 'DEX',
	'Fly': 'DEX',
	'HandleAnimal': 'CHA',
	'Heal': 'WIS',
	'Intimidate': 'CHA',
	'KnowledgeArcana': 'INT',
	'KnowledgeDungeoneering': 'INT',
	'KnowledgeEngineering': 'INT',
	'KnowledgeGeography': 'INT',
	'KnowledgeHistory': 'INT',
	'KnowledgeLocal': 'INT',
	'KnowledgeNature': 'INT',
	'KnowledgeNobility': 'INT',
	'KnowledgePlanes': 'INT',
	'KnowledgeReligion': 'INT',
	'Linguistics': 'INT',
	'Perception': 'WIS',
	'Perform': 'CHA',
	'Profession': 'WIS',
	'Ride': 'DEX',
	'SenseMotive': 'WIS',
	'SleightOfHand': 'DEX',
	'Spellcraft': 'INT',
	'Stealth': 'DEX',
	'Survival': 'WIS',
	'Swim': 'STR',
	'UseMagicDevice': 'CHA'
}
SkillArmorCheck = ['Acrobatics','Climb','DisableDevice','EscapeArtist','Fly','Ride','SleightOfHand','Stealth','Swim']
#Race:
#	AbilityModifier <Dict>
#	Effects <List>
#	Speed <Int>
#	Size <Int>

#Class:
#	AbilityPriority <List>
#	Effects <List> ???
#	SkillRank <Int>
#	ClassSkills <List>

#Effects:
def interpret(unit,query):
	return query

def applyTemplate(template,unit):
	for key,val in template.iteritems():
		tmp = unit.__dict__
		if ':' in key:
			path, cmd = tuple(key.split(':'))
			path = path.split('.')
		else:
			path = key.split('.')
			cmd = ''
		for x in path[:-1]:
			tmp = tmp[x]
		q = interpret(unit,val)
		if cmd == '' or cmd == 'set':
			tmp[path[-1]] = q
		elif cmd == 'inc':
			tmp[path[-1]] += q
		elif cmd == 'ext':
			tmp[path[-1]].extend(q)
		else:
			raise Exception

class Unit:
	def __init__(self, Name, Level, Race, Class, Base={}):
		self.Name = Name
		self.Level = Level
		self.Race = Race
		self.Class = Class
		self.Size= Race.Size
		self.Speed = Race.Speed
		
		self.SaveEffects = []
		self.DefenseEffects = []
		self.AttackEffects = []
		self.GeneralEffects = []
		
		try:
			self.NaturalArmor = Race.NaturalArmor
		except Exception:
			self.NaturalArmor = 0
		if 'Ability' in Base:
			self.Ability = dict_clone(Base['Ability'])
		else:
			abilities = sorted([genAbility() for count in range(6)])
			abilities.reverse()
			self.Ability = dict_clone(dict(zip(Class.AbilityPriority,abilities)))
		#Apply Racial Bonuses
		for attribute,bonus in Race.AbilityModifier.iteritems():
			self.Ability[attribute] += bonus
		if 'Skill' in Base:
			self.Skill = dict_clone(Base['Skill'])
		else:
			skillPoints = Level*(Class.SkillRank + modifier(self.Ability['INT']))
			self.Skill = randomChoice(skillPoints,Class.ClassSkills)
		if 'Equipment' in Base:
			self.Armor = None
			self.Shield = None
			if 'Armor' in Base['Equipment']:
				self.Armor = Base['Equipment']['Armor']
			if 'Shield' in Base['Equipment']:
				self.Shield = Base['Equipment']['Shield']
			self.Melee = Base['Equipment']['Melee']
			self.Ranged = Base['Equipment']['Ranged']	
		else:
			self.Gold = roll(Class.StartingWealth)
			self.Armor = None
			self.Shield = None
			self.Melee = []
			self.Ranged = []
		
	def addWeapon(self,base):
		tmp = Struct()
		tmp.Proficiency = base.Proficiency
		tmp.Encumberance = base.Encumberance
		tmp.Weight = base.Weight
		tmp.Price = base.Price
		tmp.DamageType = base.DamageType
		tmp.Critical = base.Critical
		tmp.Special = base.Special
		tmp.Name = base.Name
		try:
			tmp.Affinity = base.Affinity
		except Exception:
			pass
		if self.Size == 'Medium':
			tmp.Damage = base.DamageMedium
			tmp.Size = self.Size
		elif self.Size == 'Small':
			tmp.Damage = base.DamageSmall
			tmp.Size = self.Size
		elif self.Size in ['Colossal', 'Gargantuan', 'Huge', 'Large']:
			if base.DamageMedium in LargeWeaponDamage:
				tmp.Damage = LargeWeaponDamage[base.DamageMedium]
				tmp.Size = 'Large'
			else:
				tmp.Damage = base.DamageMedium
				tmp.Size = 'Medium'
		elif self.Size in ['Tiny', 'Diminutive', 'Fine']:
			if base.DamageMedium in TinyWeaponDamage:
				tmp.Damage = TinyWeaponDamage[base.DamageMedium]
				tmp.Size = 'Tiny'
			else:
				tmp.Damage = base.DamageSmall
				tmp.Size = 'Small'
		else:
			raise Exception
		if tmp.Encumberance == 'Ranged':
			self.Ranged.append(tmp)
		else:
			self.Melee.append(tmp)

	def getFortSave(self):
		return int(self.Class.Fort[self.Level-1]) + modifier(self.Ability['CON'])

	def getRefSave(self):
		return int(self.Class.Ref[self.Level-1]) + modifier(self.Ability['DEX'])

	def getWillSave(self):
		return int(self.Class.Will[self.Level-1]) + modifier(self.Ability['WIS'])

	def getHP(self):
		return compound(self.Class.HD,self.Level) + '+' + str(modifier(self.Ability['CON']))

	def getAttackBonus(self,weapon):
		BaseAttackBonus = self.Class.BaseAttackBonus[self.Level-1].replace('+','').split('/')
		tmp = SizeModifierTable[self.Size]
		if weapon.Encumberance != "Ranged":
			tmp += modifier(self.Ability['STR'])
		else:
			tmp += modifier(self.Ability['DEX'])
		if not self.isProficient(weapon):
			tmp -= 4
		if self.Race.Size != weapon.Size:
			self_index = SizesList.index(self.Race.Size)
			weapon_index = SizesList.index(weapon.Size)
			tmp -= 2*abs(self_index - weapon_index)
		return '/'.join(map(lambda x: '+' + str(int(x)+tmp), BaseAttackBonus))

	def isProficient(self,weapon):
		if weapon.Proficiency in self.Class.WeaponProficiency:
			return True
		try:
			return (weapon.Affinity == self.Race.Name) or (self.Race.Name in weapon.Affinity)
		except Exception:
			return False

	def getArmorClass(self,FlatFoot=False):
		tmp = 10 + self.NaturalArmor
		if self.Armor:
			tmp += self.Armor.Bonus
		if self.Shield:
			tmp += self.Shield.Bonus
		if not FlatFoot:
			tmp += modifier(self.Ability['DEX'])
		return tmp

	def getSkill(self,skill):
		return self.Skill[skill] + modifier(self.Ability[SkillAbility[skill]])

	def toString(self):
		tmp =  'Name: %s\n' % self.Name
		tmp += 'Level %i %s %s\n' % (self.Level,self.Race.Name,self.Class.Name)
		tmp += 'DEFENSE:\n'
		tmp += '\tAC: %i, flat-footed %i\n' % (self.getArmorClass(),self.getArmorClass(FlatFoot=True))
		tmp += '\tHP: %s\n' % self.getHP()
		tmp += '\tFort +%i, Ref +%i, Will +%i\n' % (self.getFortSave(),self.getRefSave(),self.getWillSave())
		tmp += 'OFFENSE:\n'
		tmp += '\tSpeed: %i\n' % self.Speed
		tmp += '\tMelee: '
		if len(self.Melee) == 0:
			tmp += '<None>'
		else:
			tmp += '\n\t\t'.join(['%s %s (%s, %s)' % (w.Name, self.getAttackBonus(w), w.Damage, w.Critical) for w in self.Melee])
		tmp += '\n\tRanged: '
		if len(self.Ranged) == 0:
			tmp += '<None>'
		else:
			tmp += '\n\t\t'.join(['%s +%i (%s, %s)' % (w.Name, self.getAttackBonus(w), w.Damage, w.Critical) for w in self.Ranged])
		tmp += '\nSTATISTICS:\n'
		tmp += '\t'+', '.join([a + ' ' + str(b) for (a,b) in self.Ability.iteritems()]) + '\n'
		tmp += '\tBase Attack Bonus: %s\n' % self.Class.BaseAttackBonus[self.Level-1]
		tmp += '\tSkills:\n'
		for skill in self.Skill.keys():
			tmp += '\t\t%s +%i\n' % (skill,self.getSkill(skill))
		return tmp

if __name__ == '__main__':
	import json
	def loadData(filename):
		jsonData = json.loads(open(filename,'r').read())
		tmp = {}
		for key,value in jsonData.iteritems():
			value['Name'] = key
			tmp[key] = Struct(**value)
		return tmp
	def submitData(data, filename):
		with open(filename,'w') as f:
			tmp = {}
			for key,value in data.iteritems():
				tmp[key] = value.__dict__
			f.write(json.dumps(tmp,indent=4,separators=(',',': ')))
	Classes = loadData('classes.json')
	Races = loadData('races.json')
	Weapons = loadData('weapons.json')


	drow = Races['Drow']
	ranger = Classes['Ranger']
	my_unit = Unit("Tyler", 3, drow, ranger)
	my_unit.addWeapon(Weapons['Glaive'])
	#for a in ['STR', 'DEX', 'CON', 'INT', 'CAR', 'WIS']:
	#	print a,my_unit.getAbility(a)
	#for a in my_unit.Skill:
	#	print a,my_unit.Skill[a]
	print my_unit.toString()
	#print my_unit.__dict__
	
	#applyTemplate({'Ability.STR:inc': 2},my_unit)
	#print my_unit.toString()






