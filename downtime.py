# DownTime Tracking Tool
import random

# Choose a LifeStyle Expense
available_wealth = 10
available_days = 30

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


def dt_number_days(activity_text):
	days_not_inputted = True
	while days_not_inputted:
		number_DT_days = input(f'\n\nHow many downtime days will you spend {activity_text}? ')
		try:
			str(int(number_DT_days))
			days_not_inputted = False
			return number_DT_days
		except:
			print('Error! Number of days is an integer.')
			return 0

number_DT_days = 0	
# dictionary keys follow this format: Downtime Activity: (Requirements), (Additional Lifestyle Options)

def dta_crafting(total_wealth, total_days):
	print('Downtime: Crafting')
	days_crafting = dt_number_days('Crafting')
	
	item_to_craft = input('What item are you crafting? ')
	value_of_item = input('Cost of item? ')
	tools_required = input('Which tools required? ')
	location_required = input('Any location required? ')
	number_workers = input('How many characters are working on the item? ')
	total_materials_cost = int(value_of_item) / 2
	crafting_effort = int(days_crafting) * int(number_workers)
	step_materials_cost = 2.5*int(days_crafting)
	crafting_percentage_complete = round((crafting_effort/step_materials_cost) *100)
	step_materials_cost_formatted = format_coins(step_materials_cost)
	crafting_statement = f'Spending {days_crafting} days crafting the {item_to_craft} will bring the item to {crafting_percentage_complete}% completion and cost you {step_materials_cost_formatted} in raw materials.\n'
	return f'Crafting for {total_days} days spending {total_wealth}!'

def dta_profession(total_wealth, total_days):
    return f'Profession for {total_days} days spending {total_wealth}!'

dispatch = {
    '1': dta_crafting,
    '2': dta_profession,
}

def process_input(command, total_wealth, total_days):
	if command in dispatch.keys():
		print(dispatch[command](total_wealth, total_days))
	else:
		print('Invalid entry.')


process_input(input('Which activity? '), available_wealth, available_days)

downtime_activities = {

# Building a Stronghold
#    'Build a Stronghold': (('plot of land'),(),()),

# Carousing

# Crafting Non-Magical Item
    'Crafting': (
    ('Proficiency: Artisan Tools'),
    (('Modest - Crafting', 0), ('Comfortable - Crafting', 1)),
    #dta_crafting(),
    ),
# Crafting a Magic Item 

# Gaining Reknown

# Practicing a Profession
    'Profession': (
    ('Proficiency: Profession'),
    (('Modest - Profession', 0), ('Comfortable - Profession (Req: Organization, Guild, or Temple', 0), ('Wealthy - Profession (Req: Performance)', 0))
    ),

# Performing a Sacred Rite

# Recuperating
#    'Recuperating': ((),(),),

# Researching

# Running a Business

# Selling Magic Items

# Sowing Rumors

# Training to Gain Levels
#    'Training (Levels)': ((),(),),
    
# Training Language
#    'Training (Language)': ((),(),),
    
# Training Skill
#    'Training (Skill)': ((),(),)
}






downtime_options = [activity_type for activity_type in downtime_activities]

#numbered_options = [f'{activity_number}) {activity_type}' for activity_number,activity_type in enumerate(downtime_options, 1)]

# numbered_options = [f'{activity_number}) {activity_type}' for activity_number,activity_type in enumerate(downtime_options, 1)]


lifestyle_events = (
		    ('Wretched', ((), ('violent wretch', 'hungry wretch', 'diseased wretch'),())),
			('Squalid', ((),('exiled person', 'disturbed person', 'diseased person'),())),
			('Poor', ((),('unskilled laborer', 'costermongerer', 'peddler', 'thief', 'mercenary'),())),
			('Modest', ((),('soldier', 'laborer', 'student', 'priest', 'hedge wizard'),())),
			('Comfortable', ((),('merchant', 'military officer', 'skilled tradesperson'),())),
			('Wealthy', ((),('highly succeasful merchant', 'favored servant of royalty', 'owner of several small businesses'),())),
			('Aristocratic', ((),('politician', 'guild leader', 'high priest', 'noble'),())),
	)

def get_lifestyle_adjustments(given_lifestyle):
	# ls: (), (associates), ()
	for item in lifestyle_events:
		if given_lifestyle == item[0]:
			random_interaction = random.choice(item[1][1])
	if random.randint(1,10) == 2:
		lifestyle_statement = f'Due to your {given_lifestyle} lifestyle, you have an encounter with a {random_interaction}.'
	else:
		lifestyle_statement = ''
	return lifestyle_statement

	
print ('Welcome to DATA: the Downtime Activity Tracking App!\n')
	
# manual set	
character_lifestyle = 'Wealthy'

for n in range(0,5):
	print( get_lifestyle_adjustments(character_lifestyle))


# Initiate application and list activities
def select_downtime_activity():
	
	current_formatted_wealth = format_coins(available_wealth)
	print (f'Current funds: {current_formatted_wealth}\nDowntime Days Remaining: {available_days}\n')
	
	DT_location_unselected = True
	while DT_location_unselected:
		downtime_location = input('\n\nAre you spending self-sufficient downtime? (Y/N) ')		
		
		if downtime_location == 'Y' or downtime_location == 'y':
			lifestyle_options = {
			'Self-Sufficiency: no activities': 0,
			'Poor Self-Sufficiency (Req: Profession)': 0,
			'Comfortable Self-Sufficiency (Req: Survival)': 0
			}
			DT_location_unselected = False
		elif downtime_location == 'N' or downtime_location == 'n':
			lifestyle_options = {
			'Wretched': 0,
			'Squalid': 0.1,
			'Poor': 0.2,
			'Modest': 1,
			'Comfortable': 2,
			'Wealthy': 4,
			'Aristocratic': 10
			}
			DT_location_unselected = False
		else:
			print ('Enter Y for yes or N for no.')
			
	print('\n\nYour Lifestyle Options (Price per Day)')
	for lifestyle_option, lifestyle_worth in lifestyle_options.items():
		print (lifestyle_option + ': ' + format_coins(lifestyle_worth))
		
		
	print('\n\nYour Downtime Activity Options:')
	numbered_options = enumerate(downtime_activities, 1)
	for number_option, (downtime_activity, down_act_details) in enumerate(downtime_activities.items(),1):
		print(number_option, downtime_activity)
#	[print(activity_number,'-',downtime_activity) for activity_number, downtime_activity in numbered_options]
	input_unselected = True
	while input_unselected:
	    selected_activity = input('\nEnter the number of the activity you want to pursue:  ')
	    try:
	    	selected_activity_number = int(selected_activity)
	    	selection_statement = f'You chose {selected_activity_number}: what next?'
	    	print (selection_statement)
	    	for option in numbered_options:
	    		if selected_activity_number == option:
	    			print("&&&")
	    	if selected_activity_number in numbered_options:
	    		#activity_name for activity_na
	    		print ('found it!')
	    		input_unselected = False
	    	else:
	    		print ('Select an existing activity.')
	    except TypeError:
	    	print ('A type error occured. Select an activity by entering an option number.')
	    except ValueError:
	    	print ('Select an activity by entering an option number.')
	    	
select_downtime_activity()

# dta_crafting(number_DT_days)

