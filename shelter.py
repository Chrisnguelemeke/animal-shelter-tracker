"""
Animal Shelter Tracker - Version 1
A console program that helps a small shelter keep track of the
dogs, cats, and birds in its care.
"""

from datetime import date


# ---------------------------------------------------------------
# Animal superclass
# ---------------------------------------------------------------
class Animal:
    """Holds the data and behavior every shelter animal shares."""

    def __init__(self, name, age, intake_date=None):
        self.name = name
        self.age = age
        # Use today's date if no intake date is given
        self.intake_date = intake_date if intake_date else date.today()
        self.is_adopted = False

    def make_sound(self):
        return "..."

    def mark_adopted(self):
        self.is_adopted = True

    def get_type(self):
        return self.__class__.__name__

    def extra_info(self):
        """Subclasses override this to show their own details."""
        return ""

    def __str__(self):
        status = "Adopted" if self.is_adopted else "Available"
        text = (f"{self.get_type():<5} | {self.name:<10} | Age {self.age:<3} | "
                f"Intake {self.intake_date} | {status}")
        extra = self.extra_info()
        if extra:
            text += f" | {extra}"
        return text


# ---------------------------------------------------------------
# Subclasses
# ---------------------------------------------------------------
class Dog(Animal):
    def __init__(self, name, age, breed, house_trained, intake_date=None):
        super().__init__(name, age, intake_date)
        self.breed = breed
        self.house_trained = house_trained

    def make_sound(self):
        return "Woof!"

    def extra_info(self):
        trained = "Yes" if self.house_trained else "No"
        return f"Breed: {self.breed}, House-trained: {trained}"


class Cat(Animal):
    def __init__(self, name, age, breed, declawed, intake_date=None):
        super().__init__(name, age, intake_date)
        self.breed = breed
        self.declawed = declawed

    def make_sound(self):
        return "Meow!"

    def extra_info(self):
        declawed = "Yes" if self.declawed else "No"
        return f"Breed: {self.breed}, Declawed: {declawed}"


class Bird(Animal):
    def __init__(self, name, age, species, can_fly, intake_date=None):
        super().__init__(name, age, intake_date)
        self.species = species
        self.can_fly = can_fly

    def make_sound(self):
        return "Tweet!"

    def extra_info(self):
        flies = "Yes" if self.can_fly else "No"
        return f"Species: {self.species}, Can fly: {flies}"


# ---------------------------------------------------------------
# Shelter manager class (aggregation - holds Animal objects)
# ---------------------------------------------------------------
class Shelter:
    def __init__(self, name):
        self.name = name
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"{animal.name} the {animal.get_type().lower()} was added.")

    def find_by_name(self, name):
        """Case-insensitive search. Returns the animal or None."""
        for animal in self.animals:
            if animal.name.lower() == name.lower():
                return animal
        return None

    def adopt_animal(self, name):
        animal = self.find_by_name(name)
        if animal is None:
            print(f"No animal named '{name}' was found.")
        elif animal.is_adopted:
            print(f"{animal.name} has already been adopted.")
        else:
            animal.mark_adopted()
            print(f"{animal.name} has been adopted! {animal.make_sound()}")

    def remove_animal(self, name):
        # Find first, then remove, so we never change the list mid-loop
        animal = self.find_by_name(name)
        if animal is None:
            print(f"No animal named '{name}' was found.")
        else:
            self.animals.remove(animal)
            print(f"{animal.name} was removed from the shelter records.")

    def list_available(self):
        return [a for a in self.animals if not a.is_adopted]

    def list_adopted(self):
        return [a for a in self.animals if a.is_adopted]


# ---------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------
def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter something.")


def get_age(prompt):
    while True:
        try:
            age = int(input(prompt))
            if age >= 0:
                return age
            print("Age can't be negative.")
        except ValueError:
            print("Please enter a whole number.")


def get_yes_no(prompt):
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y or n.")


def print_list(title, animals):
    print(f"\n--- {title} ({len(animals)}) ---")
    if not animals:
        print("None.")
    for animal in animals:
        print(animal)


# ---------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------
def add_intake(shelter):
    print("\nWhat kind of animal?  1) Dog  2) Cat  3) Bird")
    choice = input("Choose 1-3: ").strip()
    if choice not in ("1", "2", "3"):
        print("Invalid choice.")
        return

    name = get_text("Name: ")
    if shelter.find_by_name(name):
        print(f"There is already an animal named {name}. Please use a different name.")
        return
    age = get_age("Age (years): ")

    if choice == "1":
        breed = get_text("Breed: ")
        trained = get_yes_no("House-trained?")
        shelter.add_animal(Dog(name, age, breed, trained))
    elif choice == "2":
        breed = get_text("Breed: ")
        declawed = get_yes_no("Declawed?")
        shelter.add_animal(Cat(name, age, breed, declawed))
    else:
        species = get_text("Species: ")
        can_fly = get_yes_no("Can it fly?")
        shelter.add_animal(Bird(name, age, species, can_fly))


def search(shelter):
    name = get_text("Enter the name to search for: ")
    animal = shelter.find_by_name(name)
    if animal:
        print(animal)
        print(f"{animal.name} says: {animal.make_sound()}")
    else:
        print(f"No animal named '{name}' was found.")


def main():
    shelter = Shelter("Happy Paws Shelter")

    while True:
        print(f"\n===== {shelter.name} =====")
        print("1) Add an animal")
        print("2) Adopt an animal")
        print("3) Remove an animal")
        print("4) Search by name")
        print("5) List available animals")
        print("6) List adopted animals")
        print("7) Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_intake(shelter)
        elif choice == "2":
            shelter.adopt_animal(get_text("Name of animal to adopt: "))
        elif choice == "3":
            shelter.remove_animal(get_text("Name of animal to remove: "))
        elif choice == "4":
            search(shelter)
        elif choice == "5":
            print_list("Available Animals", shelter.list_available())
        elif choice == "6":
            print_list("Adopted Animals", shelter.list_adopted())
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 7.")


if __name__ == "__main__":
    main()
