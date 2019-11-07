import random
import re

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
	wealth_value = str(format(float(wealth_value),'.2f'))
	
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
		self.wis_ability_score = d_roll(6) + d_roll(6) + d_roll(6)
		self.wis_bonus = ability_score_to_bonus(self.wis_ability_score)

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
	
def gam_dc():
	return d_roll(10) + d_roll(10) + 5
			
	
proficiency_bonus = 2




pc = Player_Character(500,1000)	
pc.get_dt_stats()

print('\nABILITIES')
print(f'Charisma: {pc.cha_ability_score} ({pc.cha_bonus})\nWisdom: {pc.wis_ability_score} ({pc.wis_bonus})')

skill_deception = skill('Deception', pc.cha_ability_score, True, 0)

skill_persuasion = skill('Persuasion', pc.cha_ability_score, False, 0)

skill_insight = skill('Insight', pc.wis_ability_score, True, 0)

skill_intimidation = skill('Intimidation', pc.cha_ability_score, False, 0)



print('\nSKILL MODIFIERS')
for skill in (skill_deception, skill_persuasion, skill_insight, skill_intimidation):
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


def roll_vs_dc(roll, dc):
	return 'Success!' if roll > dc else 'Failure!'
	

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

def gambling_complications():
	if d_roll(10) == 1:
		part_b = ''
		if d_roll(2) == 1:
			part_a = random.choice([])
			if d_roll(2) == 1:
				part_b = 'A rival is to blame.'
		else:
			part_a = random.choice([])
		return (' ').join([part_a, part_b])

def dta_gambling():
	welcome_statement = 'You are about to spend a workweek gambling! Games of chance are a way to make a fortune... or lose one. Each five-day workweek you can gamble with a minimum of 10gp up to a maximum of 1000gp.\n'
	print(welcome_statement)
	
	gambling_prep = True
	while gambling_prep:
		initial_bet = input('How much are you willing to wager during the week? ')
		
		try:
			ini_bet = float(initial_bet)
		except:
			print('Value error! Coins must be numerical.')
		pattern = '[0-9]*(.[0-9]*)?'
		if re.search(pattern, initial_bet) is False:
			print('Enter an amount of coins between 10 and 1000gp.')
		elif ini_bet < 10 or ini_bet > 1000:
			print('Wagered sums must be between 10 and 1000gp.')
		else:
			for_bet = format_coins(initial_bet)
			print(f'Over the course of the week, you bet {for_bet}.')
			gambling_prep = False
		suc_count = fail_count = 0
		for skill in [skill_deception, skill_insight, skill_intimidation]:
			s_name = skill.get_skill_name()
			s_dc = gam_dc()
			s_roll = skill.roll()
			result = roll_vs_dc(s_roll, s_dc)
			print(f'{s_name}: {s_roll} vs DC {s_dc}... {result}!')
			if result[0] == 'S':
				suc_count += 1
		# print(f'Successes: {suc_count}, Failures: {fail_count}')
		ret_val_dict = {
			3: (1, 2),
			2: (1, 1.5),
			1: (1, 0.5),
			0: (1.5, 0)}
		for k,v in ret_val_dict.items():
			if k == suc_count:
				cost = ini_bet * v[0]
				ret_val = ini_bet * v[1]
		if ret_val > cost:
			profit = -cost + ret_val
			daily = format_coins(profit / 5)
			sentence = f'You spend {format_coins(cost)}, and win {format_coins(ret_val)}! (net profit: +{format_coins(profit)})'
		else:
			loss = cost -  ret_val
			daily = format_coins(loss / 5)
			sentence = f'You spend {format_coins(cost)}, and win {format_coins(ret_val)}! (net loss: -{format_coins(loss)})'
		print (sentence)
			
dta_gambling()
dta_gambling()



# successes: cost, return
