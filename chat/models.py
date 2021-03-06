from django.db import models
from random import randint


class Board(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя доски (комнаты)')
    rows = models.IntegerField(default=10)
    cols = models.IntegerField(default=10)

    def new_ship(self, orientation, start_loc, size):
        (start_x, start_y) = start_loc
        locations = []
        if orientation == 'horizontal':
            if start_x + size > self.rows:
                return None
            for x in range(0, size):
                x = start_x+x
                y = start_y
                r = [x-1, x, x+1]
                c = [y-1, y, y+1]
                if Location.objects.filter(
                    board=self, row__in=r, col__in=c
                ).exists():
                    return f'The location {start_x+x}x{start_y} is busy'
                locations.append((start_x+x,start_y))
        if orientation == 'vertical':
            if start_y + size > self.cols:
                return None
            for y in range(0, size):
                x = start_x
                y = start_y+y
                r = [x-1, x, x+1]
                c = [y-1, y, y+1]
                if Location.objects.filter(
                        board=self, row__in=r, col__in=c
                ).exists():
                    return f'The location {start_x}x{start_y} is busy'
                locations.append((start_x, start_y+y))
        ship = Ship.objects.create(board=self)
        for (x,y) in locations:
            location = Location.objects.create(row=x, col=y, board=self)
            ship.location.add(location)
        ship.save()
        return ship

    def full_board(self):
        """Get board with marked busy places."""
        board = [[0] * self.rows for _ in range(self.cols)]
        for x in range(0, self.rows):
            for y in range(0, self.cols):
                if Location.objects.filter(board=self, col=x, row=y).exists():
                    board[x][y-1] = '1'
        return board

    def build_ships(self,min_ship_size=1, max_ship_size=4):
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
            if not ship:
                continue
            return ship
        return None

    def check_for_hit(self, location):
        ships = Ship.objects.all().filter(board=self)
        for ship in ships:
            if ship.check_for_hit(location):
                return ship
        return None

    def shot(self, location):
        (x, y) = location
        ship = Ship.objects.filter(
            location__row=x, location__col=y, board=self
        ).first()
        if ship:
            ship.location.filter(row=x, col=y).delete()
            if not ship.location.exists():
                ship.delete()
                return 'Killed'
            return 'Hit'
        return 'Loose'


class Location(models.Model):
    row = models.IntegerField()
    col = models.IntegerField()
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE,
        related_name='locations'
    )


class Ship(models.Model):
    location = models.ManyToManyField(Location, related_name='ship')
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE,
        related_name='ship'
    )

    def __str__(self):
        return f'Ship id {self.id}'

    def tulpe_locations(self):
        locations = []
        for location in self.location.all():
            locations.append((location.row, location.col))
        return locations
