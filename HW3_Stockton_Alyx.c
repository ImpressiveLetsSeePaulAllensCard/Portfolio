#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUM_CHILD_THREADS 9

// structure for passing data to a thread
typedef struct {
    int topRow;
    int bottomRow;
    int leftColumn;
    int rightColumn;
} parameters;

// Global matrix, the one we'll use to do our analysis
int matrix[9][9];

// 9 element validity arrays, set value to 1 if corresponding row/column/grid is valid
int columnValidity[9] = {0};
int rowValidity[9] = {0};
int subGridValidity[9] = {0};

int overallValidity = 1; //boolean flag for overall validity of the sudoku puzzle, set to 1 if all elements in prior array are 1


//Function for checking columns
void *ValidColumn(void* param) {
    parameters *params = (parameters*) param;
    int topRow = params->topRow;
    int bottomRow = params->bottomRow;
    int leftColumn = params->leftColumn;
    int rightColumn = params->rightColumn;
    int flag[9] = {0};

    for (int i = topRow; i <= bottomRow; i++) { //topRow = 0, bottomRow = 8
        for (int j = leftColumn; j <= rightColumn; j++) { // leftColumn = i, rightColumn = i
            int num = matrix[i][j];
            if (num < 1 || num > 9 || flag[num - 1] == 1) {
                // Invalid condition found 
                columnValidity[leftColumn] = 0;  // Set array element to 0 and exit
                pthread_exit(NULL);
            } else {
                flag[num - 1] = 1;
            }
        }
    }
    columnValidity[leftColumn] = 1;  // Use leftColumn as index for value, current thread has finished its job once reaching here
    pthread_exit(NULL);
}

//Function to check the rows
void *ValidRow(void *param){
    parameters *params = (parameters*) param;
    int topRow = params->topRow;
    int bottomRow = params->bottomRow;
    int leftColumn = params->leftColumn;
    int rightColumn = params->rightColumn;

    int flag[9] = {0};

    for (int i = leftColumn; i <= rightColumn; i++) {
        for (int j = topRow; j <= bottomRow; j++) {
            int num = matrix[j][i];
            if (num < 1 || num > 9 || flag[num - 1] == 1) {
                rowValidity[leftColumn] = 0;  
                pthread_exit(NULL);
            } else {
                flag[num - 1] = 1;
            }
        }
    }
    rowValidity[topRow] = 1;
    pthread_exit(NULL);

}

void *ValidGrid(void *param){
    parameters *params = (parameters *)param;
    int topRow = params->topRow;
    int bottomRow = params->bottomRow;
    int leftColumn = params->leftColumn;
    int rightColumn = params->rightColumn;

    int flag[9] = {0};

    int subgridIndex = topRow + (leftColumn / 3); // Calculate subgrid index will traverse the matrix left to right

    for (int i = topRow; i <= bottomRow; i++) {
        for (int j = leftColumn; j <= rightColumn; j++) {
            int num = matrix[i][j];
            if (num < 1 || num > 9 || flag[num - 1] == 1) {
                // Invalid condition found in this subgrid
                subGridValidity[subgridIndex] = 0;
                pthread_exit(NULL);
            } else {
                flag[num - 1] = 1;
            }
        }
    }
    subGridValidity[subgridIndex] = 1;
    pthread_exit(NULL);


}

int main(int argc, char *argv[]) {
    
    pthread_t tidColumns[NUM_CHILD_THREADS]; // Array for column thread IDs
    pthread_t tidRows[NUM_CHILD_THREADS];    // Array for row thread IDs
    pthread_t tidGrids[NUM_CHILD_THREADS]; //Array for grid IDS


    // Pointer file variable and file opening
    FILE *file;
    file = fopen("matrix.txt", "r");

    if (file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    //Convert the contents of our file to a 2D array called matrix
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            fscanf(file, "%d", &matrix[i][j]);
        }
    }

    fclose(file);

    //pthread attributes
    pthread_attr_t attr;
    pthread_attr_init(&attr);

    parameters thrParam[NUM_CHILD_THREADS]; // Array to store thread parameters

    //First create and initialize attributes for the column checking threads
    for (int i = 0; i < NUM_CHILD_THREADS; i++) {
        thrParam[i].topRow = 0;  // Adjust topRow, bottomRow, leftColumn, and rightColumn as needed
        thrParam[i].bottomRow = 8;
        thrParam[i].leftColumn = i;
        thrParam[i].rightColumn = i;
        pthread_create(&tidColumns[i], &attr, ValidColumn, &(thrParam[i]));
    }

    // Wait for all column threads to finish
    for (int i = 0; i < NUM_CHILD_THREADS; i++) {
        pthread_join(tidColumns[i], NULL);
    }
    
    //Now do the same for rows:
    for (int i = 0; i < NUM_CHILD_THREADS;i++){
        thrParam[i].topRow = i;
        thrParam[i].bottomRow = i;
        thrParam[i].leftColumn = 0;
        thrParam[i].rightColumn = 8;
        pthread_create(&tidRows[i], &attr, ValidRow, &(thrParam[i]));
    }
    
    for (int i = 0; i < NUM_CHILD_THREADS; i++) {
        pthread_join(tidRows[i], NULL);
    }

    //Finally, do the same for the subgrids:
    for (int i = 0; i < NUM_CHILD_THREADS; i++) {
        //Calculations into variables to determine how to divide our matrix and our starting points
        int topRow = (i / 3) * 3;
        int bottomRow = topRow + 2;
        int leftColumn = (i % 3) * 3;
        int rightColumn = leftColumn + 2;

        thrParam[i].topRow = topRow;
        thrParam[i].bottomRow = bottomRow;
        thrParam[i].leftColumn = leftColumn;
        thrParam[i].rightColumn = rightColumn;

        pthread_create(&tidGrids[i], &attr, ValidGrid, &(thrParam[i]));
    }

    for (int i = 0; i < NUM_CHILD_THREADS; i++) {
        pthread_join(tidGrids[i], NULL);
    }


    
    //Print validity results for rows, columns and grids
    for (int i = 0; i < NUM_CHILD_THREADS; i++) {
       pthread_t thread_id = tidColumns[i];
        if (columnValidity[i] == 1) {
            printf("I am thread %d (ID: %lx), Column %d is valid! (Top row: %d, Bottom Row: %d, LeftCol: %d, RightCol: %d)\n", i, thread_id, i,0,8,i,i);
        } else {
            printf("I am thread %d (ID: %lx), Column %d is not valid! (Top row: %d, Bottom Row: %d, LeftCol: %d, RightCol: %d)\n", i, thread_id, i,0,8,i,i);
          }
    }
    
    printf("\n");

    //Now add another for loop to check the validity for rows
     for (int i = 0; i< NUM_CHILD_THREADS;i++){
        pthread_t thread_id = tidRows[i];
        if (rowValidity[i] == 1) {
            printf("I am thread %d (ID: %lx), Row %d is valid! (Top row: %d, Bottom Row: %d, LeftCol: %d, RightCol: %d)\n", i + 9, thread_id, i,i,i,0,8);
    }  else {
            printf("I am thread %d (ID: %lx), Row %d is invalid! (Top row: %d, Bottom Row: %d, LeftCol: %d, RightCol: %d)\n", i + 9, thread_id, i,i,i,0,8);
       }

    }
    printf("\n");

    //Finally check grids
    for (int i = 0; i < NUM_CHILD_THREADS; i++) {
        pthread_t thread_id = tidGrids[i];
        int rowCalc = (i / 3) * 3;
        int colCalc = (i % 3) * 3;
        if (subGridValidity[i] == 1) {
            printf("I am thread %d (ID: %lx), Subgrid %d is valid! (Top row: %d, Bottom Row: %d, LeftCol: %d, RightCol: %d)\n",
               i + 18, thread_id, i, rowCalc, rowCalc + 2, colCalc, colCalc + 2);
      } else {
        printf("I am thread %d (ID: %lx), Subgrid %d is invalid! (Top row: %d, Bottom Row: %d, LeftCol: %d, RightCol: %d)\n",
               i + 18, thread_id, i, rowCalc, rowCalc + 2, colCalc, colCalc + 2);
        }
    }

    printf("\n");

    //Now check all of the boolean arrays. If a single element is not 1, immediately set the flag to false, otherwise our puzzle is valid
    for (int i = 0; i < NUM_CHILD_THREADS; i++){
        if (columnValidity[i] != 1 || rowValidity[i] != 1 || subGridValidity[i] != 1){
            overallValidity = 0;
            break;
        }
    }

    if (overallValidity){
        printf("The sudoku puzzle is valid!");
    } else{
        printf("The sudoku puzzle is not valid!");

    }
    
    
    printf("\n");
    return 0;
}

