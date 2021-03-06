init python:
    """
    These are used to track current location of any actor and some other object in the game.
    Assumption we make here is that no actor can be at two places at once.
    """

init -20 python:
    # Core Logic:
    def change_location(actor, loc):
        """
        All actors have (or should have) a location property.
        This functions attempts to remove them from their present location and put them in a new one.
        """
        # should probably move to character class, so this can be done in PytGroup.change_location()
        if isinstance(actor, PytGroup):
            if loc == ".home":
                for c in actor.lst:
                    change_location(c, c.home)
            else:
                for c in actor.lst:
                    change_location(c, loc)
            return

        if isinstance(actor.location, basestring):
            devlog.warn("%s has a string location: %s"%(actor.name, actor.location)) # TODO: why do we care about string location? it means they are tied to specific location, and it works properly
        elif actor.location and hasattr(actor.location, "remove"):
            try:
                actor.location.remove(actor)
            except KeyError, e:
                devlog.warn("%s is not in %s (but has it as its location)"%(actor.name, str(actor.location)))

        actor.location = loc
        if isinstance(loc, Location):
            loc.add(actor)

    def set_location(actor, loc):
        """
        This plainly forces a location on an actor.
        """
        actor.location = loc
        if isinstance(loc, Location):
            loc.add(actor)


    class Location(_object):
        """
        Usually a place or a building.
        This simply holds references to actors that are present @ the location.
        If a location is not a member of this class, it is desirable for it to have a similar setup or to be added to change_location() function manually.
        """
        def __init__(self, id=None):
            if id is None:
                self.id = self.__class__
            else:
                self.id = id
            self.actors = set()

        def __str__(self):
            if hasattr(self, "name"):
                return str(self.name)
            else:
                return str(self.id)

        def add(self, actor):
            self.actors.add(actor)

        def remove(self, actor):
            self.actors.remove(actor)


    class CityLoc(Location):
        """This used to be 'city' string.
        They will partake in interactions.
        """
        def __init__(self):
            super(CityLoc, self).__init__(id="City")


    class HabitableLocation(Location):
        """Location where actors can live and modifier for health and items recovery.
        Other Habitable locations can be buildings which mimic this functionality or may inherit from it in the future.
        """
        def __init__(self, id="Livable Location", daily_modifier=.1):
            super(HabitableLocation, self).__init__(id=id)

            self._habitable = True
            self.daily_modifier = daily_modifier

        @property
        def habitabe(self):
            # Property as this is used in building to the same purpose,
            # we may need to
            return self._habitable


    class Streets(HabitableLocation):
        """
        Dummy location for actors that have no place to live...
        """
        def __init__(self):
            super(Streets, self).__init__(id="Streets", daily_modifier=-.1)


    class Apartments(Location):
        """
        Another Dummy Location, this one is used for free characters that have a place to live of their own.
        This maybe replaced later by actual apartments for every character.
        """
        def __init__(self):
            super(Apartments, self).__init__()
            self.id = "City Apartment"
