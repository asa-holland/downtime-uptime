import random

def d_roll(dice_size):
	return random.randint(1,dice_size)


def round_down(dice_rolled):
	if '.5' in str(dice_rolled):
		dice_rolled -= 0.5
	return int(dice_rolled)
	
def ability_score_to_bonus(ability):
	return round_down((ability - 10)/2)



def format_coins(wealth_value):
	try:
	    float(wealth_value)		
	except:
		return 'Error! Coin format not float'
	wealth_value = str(format(wealth_value,'.2f'))
	
	gold = wealth_value.split('.')[0]
	silver = wealth_value.split('.')[1][0]
	copper = wealth_value.split('.')[1][1]
	coin_amounts = []
	for coin in ((gold, ' gp'), (silver, ' sp'), (copper, ' cp')):
		if int(coin[0]) > 0:
			coin_amounts.append(str(coin[0]) +  coin[1])
	if coin_amounts == []:
		return ('0 gp')
	else:
		return (', ').join(coin_amounts)




class item:
	def __init__(self, item_name, use_function):
		self.item_name = item_name
		self.use_function = use_function
	
	def use(self):
		self.use_function

class skill:
	def __init__(self, skill_name, ability_score, is_proficient, misc_bonus):
		self.skill_name = skill_name
		self.is_proficient = is_proficient
		self.misc_bonus = misc_bonus
		self.ability_score = ability_score
	
	def get_is_proficient(self):
		return self.is_proficient
	def get_misc_bonus(self):
		return self.misc_bonus
	
	def get_ability_bonus(self):
		return ability_score_to_bonus(self.ability_score)
	
	
	
	def get_skill_name(self):
		return self.skill_name
	
	def get_total_bonus(self):
		total_bonus = self.get_ability_bonus() + self.get_misc_bonus()
		if self.is_proficient:
			total_bonus += proficiency_bonus
		return total_bonus
	
	def roll(self):
		roll_result = d_roll(20) + self.get_total_bonus()
		return roll_result
		

class Player_Character():
	def __init__(self,downtime,coins,unsp_low=0,unsp_mid=0,unsp_up=0,unsp_hos=0, unsp_cur_counter = 0):
		self.available_days = downtime
		self.available_wealth = coins
		
		self.unsp_up = unsp_up
		self.unsp_mid = unsp_mid
		self.unsp_low = unsp_low
		self.unsp_cur_counter = unsp_cur_counter
		self.unsp_total = unsp_up + unsp_mid + unsp_low
		self.unsp_hos = unsp_hos
		
		self.cha_ability_score = d_roll(6) + d_roll(6) + d_roll(6)
		self.cha_bonus = ability_score_to_bonus(self.cha_ability_score)

		self.unsp_max = max(1, 1+self.cha_bonus)
	
	def update(self):
		self.unsp_total = self.unsp_up + self.unsp_mid + self.unsp_low
	
	def get_dt_stats(self):
		return f'{self.available_days} downtime days and {self.available_wealth} remaining.'
	
	def get_cur_uns_cons(self):
		statement = (', ').join([str(i[0]) + ' ' + i[1] + ' class' for i in ((self.unsp_up, 'upper'), (pc.unsp_mid, 'middle'), (self.unsp_low, 'lower')) if i[0] != 0])
		if statement == '':
			statement = '0'
		self.unsp_total
		return statement

proficiency_bonus = 2




pc = Player_Character(500,1000)	
pc.get_dt_stats()

print('\nABILITIES')
print(f'Charisma: {pc.cha_ability_score} ({pc.cha_bonus})')

skill_deception = skill('Deception', pc.cha_ability_score, True, 0)

skill_persuasion = skill('Persuasion', pc.cha_ability_score, False, 0)

print('\nSKILL MODIFIERS')
for skill in (skill_deception, skill_persuasion):
	title = skill.get_skill_name()
	adj_value = skill.get_total_bonus()
	print(f'{title}: {adj_value}')

print('\nITEMS')
shiny = format_coins(pc.available_wealth)
print(f'Coins: {shiny}')
disguise_kit_count = 3
print(f'Disguise Kits: {disguise_kit_count}')

print('\nDOWNTIME')
print(f'Downtime days: {pc.available_days}')



	
def func_disguise_kit():
	if disguise_kit_count >= 1:
		disguise_kit_count -= 1
		print ('You use a disguise kit to improve your Deception.')
		skill_deception.roll()
	else:
		print ('You don\'t have any disguise kits.')

disguise_kit = item('Disguise Kit', func_disguise_kit)
		
disguise_kit.use()


nobility_access = False
sufficient_contacts = False
deception_passed = False
background = 'Urchin'


# TODO remove an fix
impersonation = 16
print (f'Attempt to impersonate a noble: {impersonation}')



if impersonation > 15:
	deception_passed = True
	print ('You\'re able to deceive your way into the higher circle and pose as a noble from far away.')

if background == 'Noble' or sufficient_contacts or deception_passed:
	nobility_access == True
	print('You have access to upper-class society. You can Carouse at the upper-class level.\n')
		
	
carousing_levels = (
	['lower', 10, pc.unsp_low, ['criminal', 'mercenary', 'town guard', 'farmer', 'laborer', 'soldier'], False],
	['middle', 50, pc.unsp_mid, ['merchant', 'spellcaster', 'guild member', 'town official'], False],
	['upper', 250, pc.unsp_up, ['noble', 'noble\'s servant'], False],
	)

contacts = []

def pick_one(to_select_from):
	size = len(to_select_from)
	
	return to_select_from[random.randrange(0,size)]

names = [
'Dobbin', 'Wennfield', 'Rachel', 'Sibdon'
]

races = ['human', 'dwarf', 'elf', 'gnome']

positions_lower = ['criminal', 'mercenary', 'town guard', 'farmer', 'laborer', 'soldier']

positions_middle = ['merchant', 'spellcaster', 'guild member', 'town official']

positions_upper = ['noble', 'noble\'s servant']

connections = ['Family', 'Collaborator']

dispositions = ['hostile', 'unfriendly', 'indifferent', 'friendly', 'loyal']




def add_carousing_contact(character, disposition, tier, counter):
	
	if character.unsp_cur_counter > 0:
		character.unsp_cur_counter -= 1
		new_contact = contact('Carousing Contact', pick_one(names), pick_one(races), tier, disposition)
	else:
		print('You have no unspecified contacts.')

class contact:
	def __init__ (self, connection, name, race, position, disposition):
		self.name = name
		self.race = race
		self.connection = connection
		self.disposition = disposition
		self.position = position
		
	def details(self):
		return f'{self.connection} - {self.name}: {self.race} {self.position}, {self.disposition}'


	
def carousing_complications():
	def carouse_pickpocket():
		stolen = d_roll(10) * 5
		if pc.available_wealth > stolen:
			pc.available_wealth -= stolen
			print(f'A pickpocket lifts {stolen} gp from you!')
		else:
			pc.available_wealth = 0
			print('A pickpocket lifts all your coins from you!')

# TODO: determine scar

	def carouse_brawl():
		part_a = 'A tavern brawl leaves you with a new scar!'
		part_b = ''
		if d_roll(2) == 1:
			part_b = 'Your rival is to blame.'
		print((' ').join((part_a, part_b)))

# TODO: detemine crime

	def carouse_fuzzy():
		print('You have fuzzy memories of doing something very, very illegal but you can\'t remember exactly what.')

# TODO: determine behavior

	def carouse_tavern():
		part_a = 'You have been banned from a tavern after some obnoxious behavior.'
		part_b = ''
		if d_roll(2) == 1:
			part_b = 'Your rival is to blame.'
		print((' ').join((part_a, part_b)))

# TODO: determine quest

	def carouse_quest():
		print('After a few drinks you swore in the town square to pursue a dangerous quest.')

# TODO: add married person	
	def carouse_married():
		print('Surprise! You\'re married.')

	def carouse_streak():
		print('Streaking naked through the streets seemed like a good idea at the time.')

# TODO: title, rival
	def carouse_title():
		title_the_carouser = random.choice(['Puddle-Drinker', 'Bench-Slayer'])
		part_a = f'You discover that everyone is calling you \'{title_the_carouser}\', and no one will say why.'
		part_b = ''
		if d_roll(2) == 1:
			part_b = 'Your rival is to blame.'
		print((' ').join((part_a, part_b)))
	
	def carouse_additional(amount):
		if pc.available_wealth > amount:
			pc.available_wealth -= amount
			print(f'You spend an additional {amount}gp trying to impress people.')
		else:
			debt = amount - pc.available_wealth
			pc.available_wealth = 0
			print(f'You spend all your coin trying to impress people, and additionally rack up a debt of {debt} to a creditor.')
			debt_active = True
			print('You can pay back your debt by:\n   1) Working for your creditor. (1 downtime day per gold coin of debt)\n   2) Selling some of your possesions.\n   3) Using two middle class contacts or an upper class contact to clear your debt.\n   Or... 4) You can refuse to pay, causing your creditor to be hostile to you.\n   Or... 5) You can use an alternative solution to clear your debt.')
			while debt_active:
				debt_free = input('How will you pay back your debt? ')
				if debt_free == '1':
					if pc.available_days > debt:
						pc.available_days -= debt
						debt_active = False
					else:
						debt -= pc.available_days
						print(f'You spend {pc.available_days} days working for your creditor, but still have an existing debt.')
						pc.available_days = 0
				elif debt_free == '2':
					print(f'You sell {debt} gp worth of your possessions to pay off your debt.')
					debt_active = False
				elif debt_free == '3':
					if pc.unsp_up >= 1 and pc.unsp_mid < 1:
						pc.unsp_up -= 1
						print('You use an upper class contact to smooth things over with your creditor.')
						debt_active = False
					elif pc.unsp_up < 1 and pc.unsp_mid >= 2:
						print('You use two middle class contacts to smooth things over with your creditor.')
						debt_active = False
						pc.unsp_mid -= 2
					elif pc.unsp_up < 1 and pc.unsp_mid < 2:
						print ('You don\'t have enough contacts to clear your debt.')
					elif pc.unsp_up >=1 and pc.unsp_mid >=2:
						print('You can call upon the favor of...\n   1) 1 upper class contact\n2) 2 middle class contacts')
						contact_opt = input('Which contact class would you like to cash in your favor from? ')
						if contact_up == '1':
							print('You call in a favor from an upper class contact to clear your debt.')
							debt_active = False
						elif contact_up == '2':
							print('You call in a favor from two middle class contacts to clear your debt.')
							debt_active = False
						else:
							print('You must enter one of the numbered options.')
							
				elif debt_free == '4':
					print()
					new_contact = contact ('Carousing Creditor', pick_one(names), pick_one(races), pick_one(positions_upper), 'Hostile')
					print(new_contact.details())
					debt_active = False
				elif debt_free == '5':
					print('You use an alternative solution to clear your debt.')
					debt_active = False
				else:
					print('You must address your debt by selecting one of the numbered options above.')
	
	def carouse_additional_100():
		carouse_additional(100)
		
	def carouse_additional_500():
		carouse_additional(500)
		
	def carouse_guild():
		part_a = 'You accidentally insulted a guild master, and only a public apology will let you do business with the guild again.'
		part_b = ''
		if d_roll(2) == 1:
			part_b = 'Your rival is to blame.'
		print((' ').join((part_a, part_b)))
	
	# TODo : gods and guilds
	def carouse_quest_mid():
		q_location = random.choice([
		random.choice(['thieves', 'blacksmithing', 'tailor\'s']) + ' guild', ' temple to ' + random.choice(['Auril', 'Helm'])])		
		print( f'You swore to undertake a quest for the local {q_location}.')
	
	def carouse_drunken():
		print('You made a drunken toast that scandalized the locals.')
		
	# todo: add events
	def carouse_event():
		event = random.choice(['festival', 'play'])
		print(f'You have been recruited to help with a local {event}.')
	def carouse_romantic ():
		parta = 'A particularly obnoxious person has taken an intense romantic interest in you.'
		partb = ''
		if d_roll(2) == 1:
			partb = 'Your rival is involved.'
		print( (' ').join([parta, partb]) )
		
	def carouse_gaffe():
		print('A social gaffe has made you the talk of the town.')
		
	def carouse_joust():
		parta = 'You have been challenged to a joust by a knight.'
		partb = ''
		if d_roll(2) == 1:
			partb = 'Your rival is to blame.'
			print( (' ').join([parta, partb]) )
		
	def carouse_spellcaster():
		print('You made a foe out of a local spellcaster.')
	
	def carouse_family():
		print('A pushy noble family wants to marry off one of their scions to you.')
	
	def carouse_tripped():
		print('You tripped and fell during a dance, and people can\'t stop talking about it.')
	
	def carouse_boring():
		print('A boring noble insists you visit each day and listen to long, tedious theories of magic.')
	
	def carouse_foe():
		part_a = 'You have made a foe out of a local noble.'
		part_b = ''
		if d_roll(2) == 1:
			part_b = 'Your rival is to blame.'
		print((' ').join((part_a, part_b)))
	
	def carouse_debts():
		print('You have agreed to take on a noble\'s debts.')
	
	def carouse_rumors():
		parta = 'You have become the target of a variety of embarassing rumors.'
		partb = ''
		if d_roll(2) == 1:
			partb = 'Your rival is involved.'
		print( (' ').join([parta, partb]) )
	
	
	
	def carouse_():
		print('not finished')
	
	complication_low = (
	(carouse_pickpocket),
	(carouse_brawl),
	(carouse_fuzzy),
	(carouse_tavern),
	(carouse_quest),
	(carouse_married),
	(carouse_streak),
	(carouse_title),)
	
	complication_mid = (
	(carouse_additional_100),
	(carouse_guild),	
	(carouse_quest_mid),
	(carouse_event),	
	(carouse_drunken),
	(carouse_romantic),
	(carouse_gaffe),
	(carouse_spellcaster))
	
	complication_up = (
	(carouse_family),
	(carouse_tripped),
	(carouse_boring),
	(carouse_foe),
	(carouse_rumors),
	(carouse_additional_500),
	(carouse_debts),
	(carouse_joust))	

# TODO: change to 10			
	if d_roll(1) == 1:
		for level in carousing_levels:
			if level[4] == True:
				comp_options = [pair[1] for pair in (('upper', complication_up), ('middle', complication_mid), ('lower', complication_low)) if pair[0] == level[0]][0]
				break
		curr_comp = comp_options[d_roll(8)-1]
		curr_comp()
	
		
def dta_carousing():
	# Resources
	days_cost = 5
	pc.available_days -= days_cost		
	carouse_selected = False
	position_levels = (positions_lower, positions_middle, positions_upper)
	counter_levels = (pc.unsp_low, pc.unsp_mid, pc.unsp_up)
	while not carouse_selected:
		carouse_class_selection = input('\nWhich social level would you like to carouse at? ')
		if carouse_class_selection in ('1','2','3'):
			current_carouse_class = position_levels[int(carouse_class_selection)-1]
			car_cost = carousing_levels [int(carouse_class_selection)-1][1]
			class_choice = carousing_levels[int(carouse_class_selection)-1][0]
			if pc.available_wealth >= car_cost:
				car_cost = carousing_levels [int(carouse_class_selection)-1][1]
				class_choice = carousing_levels[int(carouse_class_selection)-1][0]
				pc.available_wealth -= car_cost
				funds_cost = format_coins(car_cost)
				print(f'You spend {funds_cost} on five days of revelry with the {class_choice} class.')
				pc.unsp_cur_counterr = counter_levels [int(carouse_class_selection)-1] 
				carousing_levels[int(carouse_class_selection)-1][4] = True
				carouse_selected = True
				carousing_score = skill_persuasion.roll()
				print(f'Persuasian (Cha) roll... {carousing_score}!')
				carousing_contact_results = ((-99,6,'You make one new hostile contact.', 0, 1),(6,11,'You have made no new contacts.', 0, 0),(11,16,'You have made one new friendly contact.', 1, 0),(16,21, 'You have made two new friendly contacts.', 2, 0),(21,99, 'You have made three new friendly contacts.', 3, 0))
				for set in carousing_contact_results:
					if carousing_score in range (set[0],set[1]):
						print(set[2])
						for i in range(0, set[3]):
							if pc.unsp_total < pc.unsp_max:
								for item in carousing_levels:
									if item[4] == True:
										if item[0] == 'lower':
											pc.unsp_low += 1
										elif item[0] == 'middle':
											pc.unsp_mid += 1
										elif item[0] == 'upper':
											pc.unsp_up += 1
											pc.update()
										else:
											print('You made additional friendly contacts, but you can\'t maintain any more due to your Charisma.')
											break
										statement = str(f'Unspecified contact slots in use: ' + str(pc.get_cur_uns_cons()) + f'/{pc.unsp_max}')
										#TODO: print this appropriately
										print(statement)
										for i in range(0, set[4]):
											new_contact = contact ('Carousing Contact', pick_one(names), pick_one(races), pick_one(current_carouse_class), 'Hostile')
											print(new_contact.details())
										carousing_complications()
									carousing_levels [int(carouse_class_selection)-1][4] = False

			else:
				difference = format_coins(car_cost - pc.available_wealth)
				print(f'You need an additional {difference} if you want to carouse with the {class_choice}. Enter a social class for which you have the necessary funds.')
		else:
			print('Enter an integer to choose your selection.')



is_carousing = True

print('You are about to spend one workweek (five days) carousing. Get ready for fine food, strong drink, and socializing!')

print('\nCarousing Options')
for carousing_level in carousing_levels:
	(level, cost) = (carousing_level[0], carousing_level[1])
	if level == 'upper' and not nobility_access:
		print('Nobility access is required to carouse with the upper class.')
		break
	else:
		print(f'{level}-class carousing: {cost}gp/workweek')


while is_carousing:
	if pc.available_days >= 5:
		if pc.available_wealth >= 10:
			dta_carousing()
			print(f'Downtime remaining: {pc.available_days} days')
			print(f'Funds: {pc.available_wealth}')
		else:
			print('You don\'t have enough coin to carouse. You\'ll need to spend your downtime somehow else.')
			is_carousing = False
	else:
		print('You\'ve used all your downtime. Back to adventuring!')
		is_carousing = False


