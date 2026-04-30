# Physics & Domain Concepts

This project simulates a real-world problem: **Space Debris Collision Avoidance**.

Since the dawn of the space age, humanity has left thousands of dead satellites, spent rocket stages, and shards of metal orbiting the Earth. These objects travel at roughly 17,000 miles per hour. If a tiny piece of debris hits an active satellite, it can destroy it entirely.

As a satellite operator, your job is to keep your satellite safe while managing limited fuel and keeping your satellite in its correct orbit.

## The Threat: A "Conjunction"
In orbital mechanics, a **Conjunction** is an event where two objects are predicted to pass dangerously close to each other. In our code, this is called a `ConjunctionEvent`.

Because radars on Earth aren't perfect, we never know *exactly* where the debris is. We only have probability clouds. Therefore, every conjunction has key metrics:
1. **Collision Probability (Pc):** The percentage chance (from 0.0 to 1.0) that the objects will actually hit each other.
2. **Time to Closest Approach (TCA):** How many "steps" or "turns" until the debris zips past the satellite. 
3. **Miss Distance:** Our best guess at how far away the debris will be at the TCA.
4. **Uncertainty:** How blurry or bad our radar data is. High uncertainty means the true danger could be much higher or lower than we think.

## The Actions: How to Survive
To survive a conjunction, the Agent can choose to take actions.

### 1. Maneuvers (Firing the Thrusters)
The satellite can fire its thrusters to push itself out of the way. Space is 3D, so we can push in three directions:
* **Radial Maneuver:** Pushing "up" away from Earth, or "down" toward Earth. (Changes altitude).
* **Along-Track Maneuver:** Pushing "forward" to speed up, or "backward" to slow down.
* **Normal Maneuver:** Pushing "left" or "right" out of the standard orbital plane.

**The Catch:** Maneuvering costs **Fuel**. Fuel is limited. If you run out of fuel, you can't dodge the next piece of debris. Furthermore, maneuvering causes **Mission Offsets**. Your satellite is supposed to be pointing at a specific city or taking photos of a specific ocean. If you drift too far from your assigned orbit, your mission fails!

### 2. Requesting a Tracking Update
Sometimes the `Uncertainty` is so high you don't know if you should waste fuel to dodge. The agent can use the `REQUEST_TRACKING_UPDATE` action. 
* This tells ground radars to focus on the debris to get a better picture. 
* It reduces uncertainty, which might reveal the debris is actually safely missing you!
* **The Catch:** Tracking updates cost a small amount of fuel (for repositioning antennas) and you have a limited `tracking_budget`. 

### 3. Do Nothing (`NOOP`)
If the risk is low, or the debris is far away, the best action is often to do nothing, save fuel, and stay on mission.

## Abstraction: Making it an RL Game
Real orbital mechanics require heavy calculus and solving differential equations. This project **abstracts** those physics into simple math so an AI can learn it easily.
* Instead of calculating physics trajectories, `simulator.py` simply assigns an "effectiveness" score to each direction. For example, if a piece of debris is coming from above, a `RADIAL_MANEUVER` might have a high effectiveness (0.9), meaning it drastically reduces the probability of a collision, while a `NORMAL_MANEUVER` might have low effectiveness (0.1).
* Instead of continuous real-time, the game is broken down into discrete "Steps" (turns).

Your goal as the AI is to find the perfect balance: Dodge the debris, keep your fuel high, and stay close to your mission orbit!