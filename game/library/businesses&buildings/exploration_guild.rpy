init -6 python:
    # Temporary I'll Put Exploration code here:
    def launch_exploration_run(team, area):
        # Making sure that the team can explore the area.
        # Ask if player wants to send the team exploring:
        # I think this needs to be moved somewhere... it's a good fit for the class:
        if not renpy.call_screen("yesno_prompt",
                                 message="Are you sure that you wish to send %s exploring?" % team.name,
                                 yes_action=Return(True),
                                 no_action=Return(False)):
            return
        
        # I think that the game should be rigged in such a way that this is impossible:
        # for char in team:
            # if char.action == "Exploring":
                # renpy.show_screen("message_screen", "Team Member: %s is already on exploration run!" % char.name)
                # return
        
        for char in team:
            char.action = "Exploring" # We effectively remove char from the game so this is prolly ok.
            char.set_flag("loc_backup", char.location)
            if char in hero.team:
                hero.team.remove(char)
                
            # TODO: Remove char from every possible team setup in any of the buildings?
            for t in fg.teams:
                if t != team:
                    for char in team:
                        for c in t:
                            if c == char:
                                t.remove(char)
    
    class ExplorationTracker(Job):
        # Added inheritance for Job so we can use the required methods,
        """The class that stores data for an exploration job.
        
        *Not really a Job, it stores data and doesn't write any reports to ND. **Maybe it should create ND report once the run is done!
        Adapted from old FG, not sure what we can keep here..."""
        def __init__(self, team, area, guild):
            """Creates a new ExplorationJob.
            
            team = The team that is exploring.
            area = The area that is being explored.
            """
            
            # We do this because this data needs to be tracked separately and area object can only be updated once team has returned.
            # There is a good chance that some of these data must be updated in real time.
            # TODO: Keep this confined to copy of an area? Feels weird and useless to copy all of these properties.
            self.area = deepcopy(area)
            self.team = team
            self.guild = guild # Guild this tracker was initiated from...
            
            self.mobs = self.area.mobs
            self.risk = self.area.risk or 50 # TODO: Remove 50 after testing and interface adjustments.
            self.cash_limit = self.area.cash_limit
            self.items_limit = self.area.items_limit
            self.hazard = self.area.hazard
            
            # Is this it? We should have area items???
            self.items = list(item.id for item in items.values() if "Exploration" in item.locations and item.price < self.items_limit)
            
            # Shit we found!
            self.found_items = []
            self.cash = []
            
            # Traveling to and from + Status flags:
            self.distance = self.area.travel_time * 25 # We may be setting this directly in the future. Distance in KM as units. 25 is what we expect the team to be able to travel in a day. This may be offset through traits and stats/skills.
            # We assume that it's never right outside of the freaking city walls, so we do this:
            if not self.distance:
                self.distance = randint(4, 10)
                
            self.traveled = 0 # Distance traveled in "KM"...
            
            self.arrived = False # Set to True upon arrival to the location.
            self.finished_exploring = False # Set to True after exploration is finished.
            
            # Exploration:
            self.points = 0 # Combined exploration points from the whole team. Replaces AP.
            self.effectiveness = 0 # How well the team can perform any given exploration task.
            self.travel_points = 0 # travel point we use during traveling to offset ep sorrectly.
            
            self.state = "traveling to" # Instead of a bunch of properties, we'll use just the state as string and set it accordingly.
            self.captured_chars = list()
            self.found_items = list()
            self.cash = list()
            
            self.day = 1 # Day since start.
            self.total_days = 0 # Total days, travel times excluded!
            self.days = self.area.days # Days team is expected to be exploring (without travel times)!
            self.days_in_camp = 0 # Simple counter for the amount of days team is spending at camp. This is set back to 0 when team recovers inside of the camping method.
            
            # TODO: Stats here need to be personal for each of the team members.
            self.unlocks = dict()
            for key in self.area.unlocks:
                self.unlocks[key] = 0
            
            self.flag_red = False
            self.flag_green = False
            self.stats = dict(attack=0,
                                     defence=0,
                                     agility=0,
                                     magic=0,
                                     exp=0)
            
            self.logs = list() # List of all log object we create for this exploration run.
            
            # And we got to make copies of chars stat dicts so we can show changes in ND after the exploration run is complete!
            self.init_stats = dict()
            for i in self.team:
                self.init_stats[i] = i.stats.stats.copy()
            
            # fg.exploring.append(self) # TODO: Add to the proper list! Maybe not here but in fg gui.
            renpy.show_screen("message_screen", "Team %s was sent out on %d days exploration run!" % (team.name, area.days))
            # jump("fg_management")
            
        def log(self, txt, name="", nd_log=True, ui_log=False):
            obj = ExLog(name, txt, nd_log, ui_log)
            self.logs.append(obj)
            return obj
            
        def build_nd_report(self):
            # Build one major report for next day!
            txt = [] # Not sure if this is required... we can add log objects and build reports from them in realtime instead of replicating data we already have.
            event_type = "jobreport"
            
            # Build an image combo for the report:
            img = Fixed(xysize=(820, 705))
            img.add(Transform(self.area.img, size=(820, 705)))
            vp = vp_or_fixed(self.team, ["fighting"], {"exclude": ["sex"], "resize": (150, 150)}, xmax=820)
            img.add(Transform(vp, align=(.5, .9)))
            
            # We need to create major report for nd to keep track of progress:
            for log in self.logs:
                if log.nd_log:
                    txt.append("\n".join(log.txt))
            
            
            evt = NDEvent(type=event_type,
                                      img=img,
                                      txt=txt,
                                      char=self.team[0],
                                      team=self.team,
                                      charmod={},
                                      loc=self.guild.instance,
                                      locmod={},
                                      green_flag=self.flag_green,
                                      red_flag=self.flag_red)
            NextDayEvents.append(evt)
            
    class ExLog(Action):
        """Stores resulting text and data for SE.
        
        Also functions as a screen action for future buttons. Maybe...
        """
        def __init__(self, name="", txt="", nd_log=True, ui_log=False):
            """
            nd_log: Printed in next day report upon arrival.
            ui_log: Only reports worth of ui interface in FG.
            """
            self.name = name # Name of the event, to be used as a name of a button in gui. (maybe...)
            self.nd_log = nd_log
            self.txt = [] # I figure we use list to store text.
            if txt:
                self.txt.append(txt)
            self.battle_log = [] # Used to log the event.
            self.battle_won = False
            self.found_items = []
            
        def add(self, text, newline=True):
            # Adds a text to the log.
            self.txt.append(text)
            
        def __call__(self):
            renpy.show_screen("...") # Whatever the pop-up screen with info in gui is gonna be.
            
        def is_sensitive(self):
            # Check if the button has an action.
            return self.battle_log or self.found_items
            
    
    class ExplorationGuild(TaskBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 70, "Bricks": 50, "Glass": 5}
        COST = 10000
        ID = "ExplorationGuild"
        IMG = "content/gfx/bg/buildings/Chorrol_Fighters_Guild.png"
        def __init__(self, name="Exploration Guild", instance=None, desc="Travel to exotic places, meet new monsters and people... and take their shit!", img="content/gfx/bg/buildings/Chorrol_Fighters_Guild.png", build_effort=0, materials=None, in_slots=0, cost=0, **kwargs):
            super(ExplorationGuild, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            
            # Global Values that have effects on the whole business.
            self.teams = list() # List to hold all the teams formed in this guild. We should add at least one team or the guild will be useless...
            self.explorers = list() # List to hold all the (active) exploring trackers.

            self.teams.append(Team("Avengers", free=1))
            if config.debug:
                for i in range(5):
                    self.teams.append(Team(str(i), free=1))
                    
            self.workable = True
            self.focus_team = None
            self.team_to_launch_index = 0
            self.capture_chars = False # Do we capture chars during exploration in this building. # Move to Areas?
            
        # Teams control methods:
        def teams_to_launch(self):
            # Returns a list of teams that can be launched on an exploration run.
            # Must have at least one member and NOT already running exploration!
            return [t for t in self.teams_for_setup() if t]
            
        def prev_team_to_launch(self):
            teams = self.teams_to_launch()
            index = self.team_to_launch_index
            
            index = (index-1) % len(teams)
            
            self.team_to_launch_index = index
            self.focus_team = teams[index]
        
        def next_team_to_launch(self):
            teams = self.teams_to_launch()
            index = self.team_to_launch_index
            
            index = (index+1) % len(teams)
            
            self.team_to_launch_index = index
            self.focus_team = teams[index]
            
        def exploring_teams(self):
            # Teams that are busy with exploration runs.
            return [tracker.team for tracker in self.explorers]
        
        def teams_for_setup(self):
            # Teams avalible for setup in order to set them on exploration runs.
            return [t for t in self.teams if t not in self.exploring_teams()]
            
        # SimPy methods:
        def business_control(self):
            """SimPy business controller.
            """
            for tracker in self.explorers:
                self.env.process(self.exploration_controller(tracker))
                
            while 1:
                yield self.env.timeout(100)
                
        def launch_team(self, area, _team=None):
            # Moves the team to appropriate list, removes from main one and makes sure everything is setup right from there on out:
            team = self.focus_team if not _team else _team
            # self.teams.remove(team) # We prolly do not do this?
            
            tracker = ExplorationTracker(team, area, self)
            self.explorers.append(tracker)
            
            if not _team:
                self.focus_team = None
                self.team_to_launch_index = 0
            
        def exploration_controller(self, tracker):
            # Controls the exploration by setting up proper simpy processes.
            
            # Convert AP to exploration points:
            self.convert_AP(tracker)
            
            # Log the day:
            temp = "{color=[green]}Day: %d{/color} | {color=[green]}%s{/color} is exploring %s!\n"%(tracker.day, tracker.team.name, tracker.area.name)
            if tracker.day != 1:
                temp = "\n" + temp
            tracker.log(temp)
            
            # Set the state to traveling back if we're done:
            if tracker.day > tracker.days:
                tracker.state = "traveling back"
                
            while self.env.now < 99:
                if tracker.state == "traveling to":
                    yield self.env.process(self.travel_to(tracker))
                elif tracker.state == "exploring":
                    yield self.env.process(self.explore(tracker))
                elif tracker.state == "camping":
                    yield self.env.process(self.camping(tracker))
                elif tracker.state == "traveling back":
                    result = yield self.env.process(self.travel_back(tracker))
                    if result == "back2guild":
                        tracker.build_nd_report() # Build the ND report!
                        self.env.exit() # We're done...
                        
            # if config.debug:
                # tracker.log("Debug: The day has come to an end for {}.".format(tracker.team.name))
            self.overnight(tracker)
            tracker.day += 1
            
        def travel_to(self, tracker):
            # Env func that handles the travel to routine.
            
            # Figure out how far we can travel in steps of 5 DU:
            # Understanding here is that any team can travel 25 KM per day on average. This can be offset by traits and stats in the future.
            # tacker.tp = int(round(tracker.points / 20.0))
            travel_points = int(round(tracker.points / 20.0)) # local variable just might do the trick...
            
            if not tracker.traveled:
                temp = "{} is on route to {}!".format(tracker.team.name, tracker.area.id)
                tracker.log(temp)
            
            while 1:
                yield self.env.timeout(5) # We travel...
                
                tracker.points -= tracker.travel_points
                tracker.traveled += 1.25
                
                # Team arrived:
                if tracker.traveled <= tracker.distance:
                    temp = "{} arrived to {}!".format(tracker.team.name, tracker.area.id)
                    if tracker.day > 0:
                        temp = temp + " It took {} {} to get there.".format(tracker.day, plural("day", tracker.day))
                    tracker.log(temp, name="Arrival")
                    tracker.state = "exploring"
                    tracker.traveled = 0 # Reset for traveling back.
                    self.env.exit("arrived")
                
                if self.env.now >= 99: # We couldn't make it there before the days end...
                    temp = "{} spent the entire day on route to {}! ".format(tracker.team.name, tracker.area.id)
                    tracker.log(temp)
                    self.env.exit("not_arrived")
                
        def travel_back(self, tracker):
            # Env func that handles the travel to routine.
            
            # Figure out how far we can travel in 5 du:
            # Understanding here is that any team can travel 25 KM per day on average. This can be offset by traits and stats in the future.
            # tacker.tp = int(round(tracker.points / 20.0))
            travel_points = int(round(tracker.points / 20.0)) # local variable just might do the trick...
            
            if not tracker.traveled:
                temp = "{} is traveling back home!".format(tracker.team.name)
                tracker.log(temp)
            
            while 1:
                yield self.env.timeout(5) # We travel...
                
                tracker.points -= tracker.travel_points
                tracker.traveled += 1.25
                
                # Team arrived:
                if tracker.traveled <= tracker.distance:
                    temp = "{} came back to the guild!".format(tracker.team.name)
                    tracker.log(temp, name="Return")
                    # tracker.state = "exploring"
                    # tracker.traveled = 0 # Reset for traveling back.
                    self.env.exit("back2guild")
                
                if self.evn.now >= 99: # We couldn't make it there before the days end...
                    temp = "{} spent the entire day traveling back to the guild from {}! ".format(tracker.team.name, tracker.area.id)
                    tracker.log(temp)
                    self.env.exit("on the way back")
                    
        def camping(self, tracker):
            """Camping will allow restoration of health/mp/agility and so on. Might be forced on low health.
            """
            team = tracker.team
            area = tracker.area
            auto_equip_counter = 0 # We don't want to run over autoequip on every iteration, two times is enough.
            
            if not tracker.days_in_camp:
                temp = "{} setup a camp to get some rest and recover!".format(team.name)
                tracker.log(temp)
                
            while 1:
                yield self.env.timeout(5) # We camp...
                
                # Base stats:
                for c in team:
                    c.health += randint(8, 12)
                    c.mp += randint(8, 12)
                    c.vitality += randint(20, 50)
                    
                # Apply items:
                if auto_equip_counter < 2:
                    inv = list(c.inventory for c in team)
                    for explorer in team:
                        l = list()
                        if explorer.health <= explorer.get_max("health")*.8:
                            l.extend(explorer.auto_equip(["health"], source=inv))
                        if explorer.vitality <= explorer.get_max("vitality")*.8:
                            l.extend(explorer.auto_equip(["vitality"], source=inv))
                        if explorer.mp <= explorer.get_max("mp")*.8:
                            l.extend(explorer.auto_equip(["mp"], source=inv))
                        if l:
                            temp = "%s used: {color=[lawngreen]}%s %s{/color} to recover!\n" % (explorer.nickname, ", ".join(l), plural("item", len(l)))
                            self.log(temp)
                    auto_equip_counter += 1
                    
                for c in team:
                    if c.health <= c.get_max("health")*.9:
                        break
                    if c.mp <= c.get_max("mp")*.9:
                        break
                    if c.vitality <= c.get_max("vitality")*.8:
                        break
                else:
                    tracker.days_in_camp = 0
                    temp = "{} are now ready for more action in {}! ".format(team.name, area.id)
                    tracker.log(temp)
                    tracker.state = "exploring"
                    self.env.exit("restored after camping")
                    
                if self.env.now >= 99:
                    tracker.days_in_camp += 1
                    # if config.debug:
                        # tracker.log("Debug: Still Camping!")
                    self.env.exit("still camping")
                    
                # if not stop:
                    # for member in self.team:
                        # if member.health <= (member.get_max("health") / 100.0 * (100 - self.risk)) or member.health < 15:
                            # temp = "{color=[blue]}Your party falls back to base due to risk factors!{/color}"
                            # tracker.log(temp)
                    
        def overnight(self, tracker):
            # overnight: More effective heal. Spend the night resting.
            # Do we run this? This prolly doesn't need to be a simpy process... or maybe schedual this to run at 99.
            
            team = tracker.team
            
            if tracker.state == "exploring":
                temp = "{} are done with exploring for the day and will now rest and recover! ".format(tracker.team.name)
                tracker.log(temp)
            elif tracker.state == "camping":
                temp = "{} cozied up in their camp for the night! ".format(tracker.team.name)
                tracker.log(temp)
                
            for c in team:
                c.health += randint(30, 40)
                c.mp += randint(30, 40)
                c.vitality += randint(100, 120)
        
        def explore(self, tracker):
            """SimPy process that handles the exploration itself.
            
            Idea is to keep as much of this logic as possible and adapt it to work with SimPy...
            """
            items = list()
            area = tracker.area
            team = tracker.team
            fought_mobs = 0
            encountered_opfor = 0
            cash = 0
            
            # Points (ability) Convertion:
            for char in team:
                # Set their exploration capabilities as temp flag:
                tracker.effectiveness += int(round(1 + char.agility*.1) + char.get_skill("exploration")) # Effectiveness? How do we calculate?
            
            #Day 1 Risk 1 = 0.213, D 15 R 1 = 0.287, D 1 R 50 = 0.623, D 15 R 50 = 0.938, D 1 R 100 = 1.05, D 15 R 100 = 1.75
            risk_a_day_multiplicator = 50 # int(round(((.2 + (area.risk*.008))*(1 + tracker.day*(.025*(1+area.risk/100))))*.05)) # For now, I'll just devide the damn thing by 20 (*.05)...
            
            while 1:
                yield self.env.timeout(5) # We'll go with 5 du per one iteration of "exploration loop".
                
                # Hazzard:
                if area.hazard:
                    temp = "{color=[yellow]}Hazardous area!{/color} The team has been effected."
                    tracker.log(temp)
                    for char in team:
                        for stat, value in area.hazard:
                            # value, because we calculated effects on daily base in the past...
                            var = max(1, int(round(value*.05)))
                            char.mod_stat(stat, -var) # TODO: Change to log + direct application.
                            
                # This code and comment are both odd...
                # We may have area items draw two times. Investigate later:
                if tracker.items and dice(area.risk*.02 + tracker.day*.15):
                    item = choice(tracker.items)
                    temp = "{color=[lawngreen]}Found an item %s!{/color}"%item
                    tracker.log(temp, "Found Item", ui_log=True)
                    items.append(item)
                
                # Second round of items for those specifically specified for this area:
                for i in area.items:
                    if dice((area.items[i]*risk_a_day_multiplicator)): # TODO: Needs to be adjusted to SimPy (lower the probability!)
                        temp = "{color=[lawngreen]}Found an item %s!{/color}"%i
                        tracker.log(temp, "Found Item", ui_log=True)
                        items.append(i)
                        break
                
                if dice(area.risk*.05 + tracker.day*2*.05):
                    if not tracker.day:
                        raise Exception("tracker.day == 0!")
                    cash += 100 # randint(int(tracker.cash_limit/50*tracker.day*.05), int(tracker.cash_limit/15*tracker.day*.05))
                
                #  =================================================>>>
                # Girls capture (We break off exploration run in case of success):
                # if tracker.capture_chars:
                    # for g in area.girls:
                        # if g in chars and dice(area.girls[g] + tracker.day*0.1) and g.location == "se":
                            # tracker.captured_girl = None # chars[g] # TODO: Properly create the rchar...
                            # self.env.exit("captured char")
                            
                        # TODO: g in rchars looks like broken code! This also need to be updated and reviewed.
                        # elif g in rchars and dice(area.girls[g] + self.day*0.1):
                            # # new_random_girl = build_rc()
                            # self.captured_girl = build_rc()
                            # self.env.exit("captured rchar")
                
                if not fought_mobs:
                    
                    mob = None
                    
                    for key in tracker.mobs:
                        encounter_chance = True # Condition here:
                        if encounter_chance:
                            enemies = choice(tracker.mobs[key][2]) # Amount if mobs on opfor team!
                            mob = key
                            temp = "\n{} were attacked by ".format(team.name)
                            temp = temp + "%d %s!" % (enemies, plural(mob, enemies))
                            log = tracker.log(temp, "Combat!", ui_log=True)
                            break
                            
                    if mob:
                        fought_mobs = 1
                        result = self.combat_mobs(tracker, mob, enemies, log)
                        if result == "defeat":
                            tracker.state = "camping"
                            self.env.exit()
                        
                        
                # This basically means that team spent the day exploring and ready to go to rest.
                if self.env.now >= 99:
                    if items and cash:
                        tracker.log("The team has found: %s %s" % (", ".join(items), plural("item", len(items))))
                        tracker.found_items.extend(items)
                        tracker.log(" and {color=[gold]}%d Gold{/color} in loot!" % cash)
                        tracker.cash.append(cash)
                    
                    if cash and not items:
                        tracker.log("The team has found: {color=[gold]}%d Gold{/color} in loot." % cash)
                        tracker.cash.append(cash)
                    
                    if items and not cash:
                        tracker.log("The team has found: %s %s" % (", ".join(items), plural("item", len(items))))
                        tracker.found_items.extend(items)
                    
                    if not items and not cash:
                        tracker.log("Your team has not found anything of interest...")
                    self.env.exit()
                
                # self.stats["agility"] += randrange(2)
                # self.stats["exp"] += randint(5, int(max(15, self.risk/4)))
                
                # TODO: This should be a part of camping method.
                # inv = list(g.inventory for g in self.team)
                # for g in self.team:
                    # l = list()
                    # if g.health < 75:
                        # l.extend(g.auto_equip(["health"], source=inv))
                    # if g.vitality < 100:
                        # l.extend(g.auto_equip(["vitality"], source=inv))
                    # if g.mp < 30:
                        # l.extend(g.auto_equip(["mp"], source=inv))
                    # if l:
                        # self.txt.append("\n%s used: {color=[blue]}%s %s{/color} to recover!\n" % (g.nickname, ", ".join(l), plural("item", len(l))))
                
                # if not stop:
                    # for member in self.team:
                        # if member.health <= (member.get_max("health") / 100.0 * (100 - self.risk)) or member.health < 15:
                            # temp = "{color=[blue]}Your party falls back to base due to risk factors!{/color}"
                            # tracker.log(temp)
                            
            
        def combat_mobs(self, tracker, mob, opfor_team_size, log):
            # log is the exlog object we add be reports to!
            # Do we really need to pass team size to this method instead of figuring everything out here?
            
            team = tracker.team
            # area = tracker.area
            opfor = Team(name="Enemy Team", max_size=opfor_team_size)
            
            # Get a level we'll set the mobs to:
            level = tracker.mobs[mob][0]
            minl = max(1, level-3)
            maxl = level+3+tracker.day
            level = randint(minl, maxl)
            
            # raise Exception(mob, tracker.area.mobs)
            for i in xrange(opfor_team_size):
                temp = build_mob(id=mob, level=level)
                temp.controller = BE_AI(temp)
                opfor.add(temp)
                
            for i in team:
                i.controller = BE_AI(i)
            
            # Logical battle scenario:
            battle = BE_Core(logical=1)
            store.battle = battle # Making battle global... I need to make sure this is not needed.
            battle.teams.append(team)
            battle.teams.append(opfor)
            battle.start_battle()
            
            # Add the battle report to log!:
            log.battle_log = reversed(battle.combat_log)
            
            for i in team:
                i.controller = "player"
            
            if battle.winner == team:
                log.battle_won = True
                for member in team:
                    member.attack += randrange(3)
                    member.defence + randrange(3)
                    member.agility += randrange(3)
                    member.magic += randrange(3)
                    member.exp += level*10 # Adjust for levels? ! TODO:
                    
                # Death needs to be handled based off risk factor: TODO:
                # self.txt.append("\n{color=[red]}%s has died during this skirmish!{/color}\n" % member.name)

                temp = "{color=[lawngreen]}Your team won!!{/color}\n"
                log.add(temp)
                return "victory"
                
            else: # Defeat here...
                # self.stats["attack"] += randrange(2)
                # self.stats["defence"] += randrange(2)
                # self.stats["agility"] += randrange(2)
                # self.stats["magic"] += randrange(2)
                # self.stats["exp"] += mob_power/15
                
                temp = "{color=[red]}Your team got their asses kicked!!{/color}\n"
                log.add(temp)
                return "defeat"
                
        
        def convert_AP(self, tracker):
            # Convert teams AP to Job points:
            # The idea here is that teammates will help each other to carry out any task and act as a unit, so we don't bother tracking individual AP.
            team = tracker.team
            AP = 0
            for m in team:
                AP + m.AP
            tracker.points = AP * 100
            
