from psychopy import visual, core, event, gui, data
import random
import pandas as pd
import os 

def esc_space():
    global key
    key = event.waitKeys(keyList = ['space','escape'])
    if key[0] == 'escape':
        core.quit()
    else:
        pass

# Intro dialog
dialog = gui.Dlg(title = "visuospatial task")
dialog.addField("anonymous mail:") 
dialog.addField("age:")
dialog.addField("gender:", choices = ["female", "male", "other"])
dialog.addField("time since sex:")
dialog.addField("consent:", choices = ["yes", "no"])
dialog.show()

#Dialogue quo
if dialog.OK:
    id = dialog.data[0]
    age = dialog.data[1]
    gender = dialog.data[2]
    time_since = dialog.data[3]
    consent = dialog.data[4]
    if consent == "yes":
        print("Consent given, continuing experiment.")
    else:
        print("Consent not given, quitting experiment.")
        core.quit()
else:
    core.quit()

# Making sure there is a logfile directory
if not os.path.exists("logfiles_vst"):
    os.makedirs("logfiles_vst")

# set up log file
date = data.getDateStr()
stopwatch = core.Clock()
logfile = pd.DataFrame(columns = ["ID","age","gender","time_since","number_of_shapes","accuacy", "reaction_time",])
filename = "logfiles/logfile_{}.csv".format(id, date)

# Create a window
win = visual.Window(size=(800, 600), fullscr=True, allowGUI=True, color='black')
mouse = event.Mouse(win=win)
shape_stimuli = []
participant_response = []
stim_positions = []
correct_response = []
margin_of_error = 0.2  

#text stimuli to be defined
intro_txt = visual.TextStim(win, text = "Welcome Rune! In this experiment you will be shown some white figures on the screen for 5 seconds. Your job is to remember the individual positions of the shown shapes after the screen goes blank and then click on them. You'll get two trial runs with feedback before starting Good luck! Press space to start your trial runs")
click_msg = visual.TextStim(win, text="", pos=[0, -0.5], height=0.1)
end_msg = visual.TextStim(win, text ="This task is done - thank you for now")
yes_msg = visual.TextStim(win, text ="Good job!")
no_msg = visual.TextStim(win, text ="Not quite")
ready_msg = visual.TextStim(win, text ="All good? When pressing space the experiment will start. There'll be 6 trials in total and they get harder as we move forward. You will not be given feedback after keypress. Good luck! Press space to start")

# Set up stimuli
target_positions = [(-0.5, 0.5), (0.5, 0.5), (-0.5, -0.5), (0.5, -0.5),(0,0),(0,0.5),(0,-0.5),(-0.5,0),(0.5,0)]
shapes = ['triangle', 'square', 'circle', 'cross','rhombus']  # Geometric shapes

intro_txt.draw()
win.flip()
esc_space()

##Make trial Run##
for trial_run in range(2):
    random.shuffle(shapes)
    random.shuffle(target_positions)
    trial_shapes = random.sample(shapes, 3)
    trial_target_positions = random.sample(target_positions, 3)
    
    shape_stimuli.clear() #clear the shape_stimuli appended in shown earlier trials
    for shape, loc in zip(trial_shapes, trial_target_positions): #to the shape stimuli variable, append each shape with a position
        if shape == 'triangle':
            shape_stimuli.append(visual.Polygon(win, edges=3, radius=0.1, pos=loc))
        elif shape == 'square':
            shape_stimuli.append(visual.Rect(win, width= 0.15, height= 0.15, pos=loc, fillColor='white'))
        elif shape == 'circle':
            shape_stimuli.append(visual.Circle(win, radius=0.1, pos=loc))
        elif shape == 'cross':
            shape_stimuli.append(visual.TextStim(win, text='+', pos=loc, height=0.35))
        elif shape == 'rhombus':
            shape_stimuli.append(visual.Polygon(win, edges=4, radius=0.1, pos=loc))
        
    for shape_stim in shape_stimuli: #draw the shapes in their designated position
        shape_stim.draw()
    win.flip() #show the shapes
    core.wait(5) #wait for 5 seconds
    win.flip()
    for idx, shape_stim in enumerate(shape_stimuli): #connect the shape stim with the name of the shape
        stim_position = shape_stim.pos #get the position of each shape
        stim_positions.append(stim_position)
        click_msg.text = "Click at the position of the {}!".format(trial_shapes[idx]) #tell participant what shape to press on
        click_msg.draw() #show participant the text
        win.flip()
    
    
        mouse.clickReset()  # Reset the mouse click status
        while not any(mouse.getPressed()):  # Wait for a mouse click
            pass
    
        response_pos = mouse.getPos()  # Get the position of the mouse click
        # get the differnece for the x and y coordinates for the mouse click and actual position of the shape
        x_diff = abs(response_pos[0] - trial_target_positions[idx][0])
        y_diff = abs(response_pos[1] - trial_target_positions[idx][1])

        if x_diff <= margin_of_error and y_diff <= margin_of_error:
            yes_msg.draw()
            win.flip()
            core.wait(1)
        else:
            no_msg.draw()
            win.flip()
            core.wait(1)
        core.wait(0.3)
    

#show stuff in 6 trials
ready_msg.draw()
win.flip()
esc_space()
for trial in range(6):
    random.shuffle(shapes)
    random.shuffle(target_positions)
    if trial == 0: #first trial only show 2 shapes
        trial_shapes = random.sample(shapes, 2)
        trial_target_positions = random.sample(target_positions, 2)
    elif trial == 1 or trial == 2: #now 3 shapes for trial 2 and 3
        trial_shapes = random.sample(shapes, 3)
        trial_target_positions = random.sample(target_positions, 3)
    elif trial == 3 or trial == 4: #now 4 shapes for trial 4 and 5
        trial_shapes = random.sample(shapes, 4)
        trial_target_positions = random.sample(target_positions, 4)
    elif trial == 5: #in the 6th trial show 5 shapes
        trial_shapes = random.sample(shapes, 5)
        trial_target_positions = random.sample(target_positions, 5)


    shape_stimuli.clear() #clear the shape_stimuli appended in shown earlier trials
    for shape, loc in zip(trial_shapes, trial_target_positions): #to the shape stimuli variable, append each shape with a position
        if shape == 'triangle':
            shape_stimuli.append(visual.Polygon(win, edges=3, radius=0.1, pos=loc))
        elif shape == 'square':
            shape_stimuli.append(visual.Rect(win, width= 0.15, height= 0.15, pos=loc, fillColor='white'))
        elif shape == 'circle':
            shape_stimuli.append(visual.Circle(win, radius=0.1, pos=loc))
        elif shape == 'cross':
            shape_stimuli.append(visual.TextStim(win, text='+', pos=loc, height=0.35))
        elif shape == 'rhombus':
            shape_stimuli.append(visual.Polygon(win, edges=4, radius=0.1, pos=loc))

    
    for shape_stim in shape_stimuli: #draw the shapes in their designated position
        shape_stim.draw()
    win.flip() #show the shapes
    core.wait(5) #wait for 5 seconds
    
    win.flip()
    correct_response.clear() #clear number of correct responses in ealier trials
    stopwatch.reset() #reset clock
    for idx, shape_stim in enumerate(shape_stimuli): #connect the shape stim with the name of the shape
        stim_position = shape_stim.pos #get the position of each shape
        stim_positions.append(stim_position)
        click_msg.text = "Click at the position of the {}!".format(trial_shapes[idx]) #tell participant what shape to press on
        click_msg.draw() #show participant the text
        win.flip()
    
    
        mouse.clickReset()  # Reset the mouse click status
        while not any(mouse.getPressed()):  # Wait for a mouse click
            pass
        
        response_pos = mouse.getPos()  # Get the position of the mouse click
        # get the differnece for the x and y coordinates for the mouse click and actual position of the shape
        x_diff = abs(response_pos[0] - trial_target_positions[idx][0])
        y_diff = abs(response_pos[1] - trial_target_positions[idx][1])

        if x_diff <= margin_of_error and y_diff <= margin_of_error:
            correct_response.append('True') #if the clicked position is within the margin of error the response is correct
        else:
            pass
    
        participant_response.append((trial_shapes[idx], idx, response_pos))
        core.wait(0.3)
        
    reaction_time = stopwatch.getTime() #get reaction time
    logfile = logfile.append( {'ID': id,
    'age': age,
    'gender': gender,
    'time_since': time_since,
    'number_of_shapes': len(shape_stimuli),
    'accuacy': len(correct_response),
    'reaction_time': reaction_time}, ignore_index = True)
end_msg.draw()
win.flip()
core.wait(3)
win.close()

#Createing a unique file name
logfile_name = 'logfiles_vst/logfile_{}_{}.csv'.format(id, date)
#Save the data frame as a csv file
logfile.to_csv(logfile_name)

core.quit()