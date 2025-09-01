# Unequal Length Mazes – Heuristic Search for Solitaire Games

## Project Description
This project implements and solves a **solitaire game** called **Unequal Length Mazes**.  
The program is capable of:  
- Allowing a **human player** to play the game in **Normal Mode** or **Challenge Mode**.  
- Solving different levels automatically using the **Depth-First Search (DFS)** algorithm.  

The program evaluates the solution based on:  
- Whether the player reaches the goal cell (top-right) after visiting all other cells.  
- Compliance with the game rules (no revisiting cells, no crossing obstacles, segments in different directions not having the same length).  
- Ability to move through all reachable cells without getting blocked. 

The interface shows the evolution of the board, allowing user interaction and optionally providing hints.  

## Authors
- Ana Matilde Ferreira
- Maria Leonor Carvalho

## Requirements and Libraries
- Python 3.x installed on your system

The project requires the following Python libraries:
- tkinter (standard library)
- random (standard library)
- collections (standard library, for deque)
- Pillow (`PIL`)  
  Install with: `pip install pillow`
- tabuleiros.py (local module containing maze layouts)

## How to Run
1. Navigate to the project directory.  
3. Edit line 25 of `unequal_l_m.py` to set the correct path to the image used in the game.  
4. Run the following commands:  
```bash
python unequal_l_m.py
python modo_desafio.py  # Optional, for Challenge Mode

