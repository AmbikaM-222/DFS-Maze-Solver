//maze.c

#include <stdio.h>
#include <stdlib.h>
#include "maze.h"

/*Ambika Mohapatra
*This program employs a depth-first search (DFS) algorithm to navigate and solve a 
*maze. We have utilized allocation and deallocation techniques along with maze 
*visualization. We define the recursive conditions to traverse in the up, down, left, right
*directions in order to find the shortest path from the Start (S) to End(E) while avoiding 
*maze walls and staying within defined maze bounds.
*/

/*
 * createMaze -- Creates and fills a maze structure from the given file
 * INPUTS:       fileName - character array containing the name of the maze file
 * OUTPUTS:      None 
 * RETURN:       A filled maze structure that represents the contents of the input file
 * SIDE EFFECTS: None
 */
maze_t * createMaze(char * fileName)
{
  int num_rows, num_cols, row_index, col_index, k, l;
  FILE* file = fopen(fileName, "r"); // Open the input file for reading

  fscanf(file, "%d", &num_cols);   
  fscanf(file, "%d", &num_rows);  // Read the width (num_cols) and height (num_rows)


  maze_t* maze = (maze_t*) malloc(sizeof(maze_t)); // Allocate memory for the maze structure
  maze->cells = calloc(num_rows, sizeof(char*)); // Allocate memory for each row's character array pointers (num_rows)

  for (k = 0; k < num_rows; k++) {
    maze->cells[k] = calloc(num_cols, sizeof(char)); // Allocate memory for each row's character array of size num_cols
  }

  maze->width = num_cols; // Set the maze's width to num_cols
  maze->height = num_rows; // Set the maze's height to num_rows

  char buffer[num_rows][num_cols+2]; // Create a buffer for input, num_cols + 2 to accommodate space and newline characters

  for (l = 0; l < num_rows; l++) {
    fgets(buffer[l], num_cols+2, file); // Read one row of characters from each input line and store it in the buffer
  }

  for (row_index = 0; row_index < num_rows; row_index++) { // Loop through rows and columns to save maze cells
    for (col_index = 0; col_index < num_cols; col_index++) {
      maze->cells[row_index][col_index] = buffer[row_index][col_index];
      if (buffer[row_index][col_index] == 'S') { // Check if the cell contains the start/end point and update the start row and column if found
        maze->startRow = row_index;
        maze->startColumn = col_index;
      }
      if (buffer[row_index][col_index] == 'E') { // Check if the cell contains the end point and update the end row and column if found
        maze->endRow = row_index;
        maze->endColumn = col_index;
      }
    }
  }
  return maze;
}

/*
 * destroyMaze -- Frees all memory associated with the maze structure, including the structure itself
 * INPUTS:        maze -- pointer to maze structure that contains all necessary information 
 * OUTPUTS:       None
 * RETURN:        None
 * SIDE EFFECTS:  All memory that has been allocated for the maze is freed
 */
void destroyMaze(maze_t * maze)
{
  for(int x = 0; x < maze->height; x++){
    free(maze->cells[x]); // free the memory of each cell iterating through all maze rows
  }
  
  free(maze->cells); // free memory from the array of maze cells
  free(maze); // free the whole maze structure 
}

/*
 * printMaze --  Prints out the maze in a human readable format (should look like examples)
 * INPUTS:       maze -- pointer to maze structure that contains all necessary information 
 *               width -- width of the maze
 *               height -- height of the maze
 * OUTPUTS:      None
 * RETURN:       None
 * SIDE EFFECTS: Prints the maze to the console
 */
void printMaze(maze_t * maze) {
    	for (int i = 0; i < maze->height; i++) {
		for (int j = 0; j < maze->width; j++) {
			printf("%c", maze->cells[i][j]);
		}
		printf("\n");
	}
}


/*
 * solveMazeManhattanDFS -- recursively solves the maze using depth first search,
 * INPUTS:               maze -- pointer to maze structure with all necessary maze information
 *                       col -- the column of the cell currently bringing visited within the maze
 *                       row -- the row of the cell currently being visited within the maze
 * OUTPUTS:              None
 * RETURNS:              0 if the maze is unsolvable, 1 if it is solved
 * SIDE EFFECTS:         Marks maze cells as visited or part of the solution path
 */ 
int solveMazeDFS(maze_t * maze, int col, int row) {
	
	if (row < 0 || col < 0 || row >= maze->height || col >= maze->width) {
		return 0;
	}
	//We need the base case first for when the maze reaches the end location
	//Since we've edited the value of start, we need to reset it to 'S'
	if (maze->cells[row][col] == 'E') {
		maze->cells[maze->startRow][maze->startColumn] = 'S';
		return 1;
	}

	if (maze->cells[row][col] != ' ' && maze->cells[row][col] != 'S') {
		return 0;
	}

	//We also need to make sure that if we return to the start value, we don't
	//replace the S value with a *, elsewise, we fill the space with *
	if (maze->cells[row][col] != 'S') {
		maze->cells[row][col] = '*';
	}

	//For cases where we return to S, we need to make sure the
	//solve function doesn't treat S as a potential, valid spot to move, and any branches
	//that loop around S cannot be marked as part of the final solution

	maze->cells[maze->startRow][maze->startColumn] = '*';

	//We need to now test movements up, down, left, and right while also
	//checking whether or not the coordinates fall within bounds and if
	//the cell is an empty, valid cell

	//Down movements
	if (solveMazeDFS(maze, col, row+1)) {
		return 1;	
		}

	//Up movements
	if (solveMazeDFS(maze, col, row-1)) {
		return 1;
		}

	//Right movements
	if (solveMazeDFS(maze, col+1, row)) {
		return 1;
		}

	//Left movements
	if (solveMazeDFS(maze, col-1, row)) {
		return 1;
		}


	maze->cells[row][col] = '~';
	return 0;
}
