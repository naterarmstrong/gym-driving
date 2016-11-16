from car import Car
import numpy as np

class Environment:
    """
    Coordinates updates to participants
    in environment. Interactions should
    be done through simulator wrapper class.
    """

    def __init__(self, screen_size, num_cpu_cars=2):
        #TODO: Randomize car locations
        self.main_car = Car(screen_size[0]/2, screen_size[1]/2)
        self.vehicles = [Car(screen_size[0]/2, screen_size[1]/2) for _ in range(num_cpu_cars)]
        self.terrain = []

    def step(self):
        """
        Updates environment by one timestep.
        :return: None
        """
        self.main_car.step()
        for vehicle in self.vehicles:
            vehicle.step()

    def get_state(self):
        """
        Returns current state, corresponding
        to locations of all cars.
        :return: dict
            'main_car': Position of main car.
            'other_cars': Position of other cars.
        """
        state_dict = {}
        state_dict['main_car'] = self.main_car.get_state()
        state_dict['other_cars'] = [vehicle.get_state() for vehicle in self.vehicles]
        state_dict['car_collisions'] = [self.main_car.collide_rect(car) for car in self.vehicles]
        state_dict['num_car_collisions'] = sum(state_dict['car_collisions'])
        state_dict['terrain_collisions'] = [self.main_car.collide_rect(terrain) for terrain in self.terrain]        
        done = False
        return state_dict, done

    def take_action(self, action):
        """
        Takes input action, updates environment.
        :param action: dict
            Input action.
        :return: array
            Reward.
        """
        self.main_car.take_action(action)
        self.step()
        state_dict, done = self.get_state()
        reward = -state_dict['num_car_collisions']
        return state_dict, reward, done
