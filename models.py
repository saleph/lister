import datetime
from django.db import models
from django.contrib.auth.models import User


class Reader(models.Model):
    """
    The model of a reader.


    Attributes:
        name: name of the reader

        want_lection, wants_psalm, wants_believers_pray: boolean value describing
            a reader's relation towards the type of lection.

        speech_number: number of occurrences in readers table;
            used to sort.

        owner: foreign key; tells which user add the reader
    """
    name = models.CharField(max_length=50)
    wants_lection = models.BooleanField(default=False)
    wants_psalm = models.BooleanField(default=False)
    wants_believers_pray = models.BooleanField(default=False)
    speech_number = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User)

    def __str__(self) -> str:
        return self.name

    def reset_speech_number(self):
        """
        Resets speech number: if it was >1, speech number = 1
        else speech number = 0.

        Method used after new reader's addition.
        """
        if self.speech_number > 0:
            self.speech_number = 1
        else:
            self.speech_number = 0

    def at_least_one_wants_is_true(self) -> bool:
        """
        Returns True if at least one of the wants is True.
        Else returns False.
        """
        if (self.wants_lection or
                self.wants_psalm or
                self.wants_believers_pray):
            return True
        else:
            return False


class Day(models.Model):
    """
    The model of a day.
    The reason why user's foreign key occurs here and not in
    Mess model is the case when in the same day two different
    users have different is_second_lection value (because of
    e.g. patron saint day).


    Attributes:
        date: date of the day

        is_second_lection: a boolean value describes if this
            day has a second lection

        owner: user's foreign key
    """
    date = models.DateField('date', default=datetime.date.today())
    second_lection_exist = models.BooleanField(default=True)
    owner = models.ForeignKey(User)

    def __str__(self):
        return str(self.date)


class Mess(models.Model):
    """
    The model of a mess.
    It contains date, time and names of readers assigned
    to lection type.


    Attributes:
        day: Day's foreign key

        hour: time field, stores hour of the mess

        first_lection, second_lection, psalm, believers_pray:
            stores Reader's foreign key - simply who will read
            the lection
    """
    day = models.ForeignKey(Day)
    hour = models.TimeField('hour', default=datetime.time(9, 0))
    first_lection = models.ForeignKey(Reader, related_name='first_lection_users')

    # NOTICE! If day.is_second_lection == False
    # second_lection has to be '---'
    second_lection = models.ForeignKey(Reader, related_name='second_lection_users')
    psalm = models.ForeignKey(Reader, related_name='psalm_users')
    believers_pray = models.ForeignKey(Reader, related_name='believers_pray_users')

    class Meta:
        verbose_name_plural = 'messes'

    def __str__(self):
        return '{date} {hour}'.format(date=self.day.date, hour=self.hour)
