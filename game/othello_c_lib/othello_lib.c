#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 8
#define EMPTY_CELL 0
const int DIRECTIONS[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};

bool validMove(int board[SIZE][SIZE], int row, int col, int player) {
    if(board[row][col] != EMPTY_CELL)
        return false;


    int opponent = 1 + player % 2;

    for(int i = 0; i < 8; i++) {
        int dx = DIRECTIONS[i][0];
        int dy = DIRECTIONS[i][1];
        int nx = row + dx;
        int ny = col + dy;

        if(nx >= 0 && nx < SIZE && ny >= 0 && ny < SIZE && board[nx][ny] == opponent) {
            while(nx >= 0 && nx < SIZE && ny >= 0 && ny < SIZE && board[nx][ny] != EMPTY_CELL) {
                nx += dx;
                ny += dy;
                if(nx >= 0 && nx < SIZE && ny >= 0 && ny < SIZE && board[nx][ny] == player)
                    return true;
            }
        }
    }

    return false;
}

void applyMove(int board[SIZE][SIZE], int row, int col, int player) {
    board[row][col] = player;

    int opponent = 1 + player % 2;

    for (int i = 0; i < 8; i++) {
        int dx = DIRECTIONS[i][0];
        int dy = DIRECTIONS[i][1];

        int nx = row + dx;
        int ny = col + dy;

        int to_flip[SIZE * SIZE][2];
        int num_flips = 0;

        if (0 <= nx && nx < SIZE && 0 <= ny && ny < SIZE && board[nx][ny] == opponent) {
            while (0 <= nx && nx < SIZE && 0 <= ny && ny < SIZE && board[nx][ny] == opponent) {
                to_flip[num_flips][0] = nx;
                to_flip[num_flips][1] = ny;
                num_flips++;
                nx += dx;
                ny += dy;
            }

            if (!(0 <= nx && nx < SIZE && 0 <= ny && ny < SIZE && board[nx][ny] == player)) {
                num_flips = 0;
            }
        }

        for (int j = 0; j < num_flips; j++) {
            board[to_flip[j][0]][to_flip[j][1]] = player;
        }
    }
}

void freeArray(int **array, int row, int col) {
    for (int i = 0; i < row; i++) {
        free(array[i]);
    }
    array = NULL;
    free(array);
}
