#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A small docstring for pets database"""

import sqlite3

def main():
    conn = sqlite3.connect("pets.db")
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS person''')
    c.execute('''DROP TABLE IF EXISTS pet''')
    c.execute('''DROP TABLE IF EXISTS person_pet''')
    c.execute('''CREATE TABLE person (
                     id INTEGER PRIMARY KEY,
                     first_name TEXT,
                     last_name TEXT,
                     age INTEGER )
              ''')
    c.execute('''CREATE TABLE pet (
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     breed TEXT,
                     age INTEGER,
                     dead INTEGER );
              ''')
    c.execute('''CREATE TABLE person_pet (
                     person_id INTEGER,
                     pet_id INTEGER );
              ''')
    c.execute('''INSERT INTO person
                     (id, first_name, last_name, age)
                 VALUES
                     (1, "James", "Smith", 41),
                     (2, "Diana", "Greene", 23),
                     (3, "Sara", "White", 27),
                     (4, "William", "Gibson", 23)
              ''')
    c.execute('''INSERT INTO pet
                     (id, name, breed, age, dead)
                 VALUES
                     (1, "Rusty", "Dalmation", 4, 1),
                     (2, "Bella", "Alaskan Malamute", 3, 0),
                     (3, "Max", "Cocker Spaniel", 1, 0),
                     (4, "Rocky", "Beagle", 7, 0),
                     (5, "Rufus", "Cocker Spaniel", 1, 0),
                     (6, "Spot", "Bloodhound", 2, 1)
              ''')
    c.execute('''INSERT INTO person_pet
                     (person_id, pet_id)
                 VALUES
                     (1, 1),
                     (1, 2),
                     (2, 3),
                     (2, 4),
                     (3, 5),
                     (4, 6)
              ''')
    conn.commit()

    person_id = 0
    while person_id != -1:
        try:
            person_id = int(raw_input("\nPlease enter an ID number: "))
            c.execute('''SELECT first_name, last_name, age FROM person WHERE
             id = %i''' % person_id)
            person_data = c.fetchone()
            person_name = "%s %s" % (person_data[0], person_data[1])
            person_age = person_data[2]
            print " %s, %i years old" % (person_name, person_age)
            c.execute('''SELECT person.first_name, person.last_name, pet.name,
                          pet.breed, pet.age, pet.dead
                         FROM pet
                         LEFT JOIN person_pet
                         ON pet.id = person_pet.pet_id
                         LEFT JOIN person
                         ON person_pet.person_id = person.id
                         WHERE person.id = %i
                      ''' % person_id)
            pet_list = c.fetchall()
            for pet in pet_list:
                pet_name = pet[2]
                pet_breed = pet[3]
                pet_age = pet[4]
                pet_dead = pet[5]
                if pet_dead == 0:
                    print " %s owns %s, a %s, that is %s" % \
                          (person_name, pet_name, pet_breed, pet_age)
                elif pet_dead == 1:
                    print " %s owned %s, a %s, that was %s" % \
                          (person_name, pet_name, pet_breed, pet_age)
        except ValueError:
            print " Enter only integers."
        except TypeError:
            if person_id == -1:
                conn.close()
                print " Now exiting program."
                exit(-1)
            print " There is no data associated with that ID number."

if __name__ == "__main__":
    main()
