from django.db import models
from random import choice, randint, shuffle



class Board(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя доски (комнаты)')
    rows = models.IntegerField(default=10)
    cols = models.IntegerField(default=10)
    # ships = models.IntegerField(default=4)

    def new_ship(self, orientation, start_loc, size):
        (start_x, start_y) = start_loc
        locations = []
        if orientation == 'horizontal':
            if start_x + size > self.rows:
                return None
        for x in range(0, size):
            locations.append((start_x+x,start_y))
        if orientation == 'vertical':
            if start_y + size > self.cols:
                return None
            for y in range(0, size):
                locations.append((start_x, start_y+y))
        ship = Ship.objects.create(board=self)
        for (x,y) in locations:
            location = Location.objects.create(row=x, col=y, board=self)
            ship.location.add(location)
        ship.save()
        return ship

    def build_ships(self, amount=4 ,min_ship_size=1, max_ship_size=4):
        size = randint(min_ship_size, max_ship_size)
        orientation = 'horizontal' if randint(0, 1) == 0 else 'vertical'
        locations_tried = []
        while (len(locations_tried) < (self.cols * self.rows)):
            x = randint(1, self.rows)
            y = randint(1, self.cols)
            if (x, y) in locations_tried:
                continue
            else:
                locations_tried.append((x,y))
            ship = self.new_ship(orientation, (x, y), size)
            return ship
        return None



    def get_location(self, size, orientation):
        locations = []
        if orientation == 'horizontal':
            for r in range(self.rows):
                for c in range(self.cols - size + 1):
                    if not Location.objects.filter(row=r, col=c, board=self).exists():
                        locations.append({'row': r, 'col': c})
        elif orientation == 'vertical':
                for c in range(self.cols):
                    for r in range(self.rows - size + 1):
                        if not Location.objects.filter(row=r, col=c, board=self).exists():
                            locations.append({'row': r, 'col': c})
        return locations

class Location(models.Model):
    row = models.IntegerField()
    col = models.IntegerField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.row} x {self.col}'

class Ship(models.Model):
    location = models.ManyToManyField(Location)
    # opts - vertical/horizontal
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def check_for_hit(self, coordinates):
        (row, col) = coordinates
        for location in self.location.all():
            if row == location.row and col == location.col:
                return True
        return False

    def tulpe_locations(self):
        locations = []
        for location in self.location.all():
            locations.append((location.row, location.col))
        return locations

