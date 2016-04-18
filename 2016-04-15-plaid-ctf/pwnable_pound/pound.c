#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/*** HELPER FUNCTIONS ***/


const int N = 1024; // General buffer size

int get_number() {
    int k;
    char buffer[N];
    if (fgets (buffer, N, stdin) == NULL) {
        printf("Failed to read number\n");
        exit(-69);
    }
    sscanf(buffer, "%d\n", &k);

    return k;
}


const int l1_len = L1;
const int l2_len = L2;



#define STATE_SIZE_LEN 512

struct global_s {
    int s1_citizens[l1_len];
    int s2_citizens[l2_len];
    char s1_name[STATE_SIZE_LEN]; // Name of state 1
    char s2_name[STATE_SIZE_LEN]; // Name of state 2
    char *announcement;
    int announcement_length;
    int secret;
} global;


#define PSTATE(X) \
    do { \
        printf("State %s\n", global.s##X##_name);\
        int i=-1, length = sizeof(global.s##X##_citizens)/sizeof(int);\
        while (++i < length) {\
            printf("Citizen %d: $%d\n", i, global.s##X##_citizens[i]);\
        }\
    } while (0)


// Print citizen information of states
void print_states () {
    if (global.announcement != NULL) {
        printf("PSA: %s\n", global.announcement);
    }

    printf("\nState of the world!\n");

    // Macros are beutiful aren't they...
    PSTATE(1);
    printf("\n-----------------------\n");
    PSTATE(2);
}


#define SET_STATE(X, V) \
    do { \
        int i=-1, length = sizeof(global.s##X##_citizens)/sizeof(int);\
        while (++i < length) {\
            global.s##X##_citizens[i] = V;\
        }\
    } while (0)

// Print citizen information of states
void init_states(int k) {
    printf("\nInitializing all states to %d.\n", k);

    // Macros are beutiful aren't they...
    SET_STATE(1, k);
    SET_STATE(2, k);
}
#define _STR(x) #x
#define STR(x) _STR(x)

void propagate_forward(int k) {
    // Somewhere total_length will be used :), with some buffer or heap
    int length_diff = L2 - L1;
	printf("L's: %d %d\n", L1, L2);
	printf("L1: %s\n",STR(L1));
	printf("L2: %s\n",STR(L2));
	printf("L's: %d and %d\n", L1, L2);
	printf("calculated diff=%d\n", L2-L1);
	printf("actual diff=%d\n", (L2)-(L1));
    int i,j;
    
    for (i=0; i < L1-1; i++) {
        // At random, swap money to keep circulation of money 
        if (rand() % 2) {
            int tmp = global.s1_citizens[i];
            global.s1_citizens[i] = global.s2_citizens[i];
            global.s2_citizens[i] = tmp;
        } 

        // Propagate forward s1
        if (global.s1_citizens[i] >= k) {
            global.s1_citizens[i] -= k;
            global.s1_citizens[i+1] += k;

            // If we reach a bankrupt person, 
            // give him the money
            if (global.s1_citizens[i+1] == k) {
                return;
            }
        }

        // Propagate forward s2
        if (global.s2_citizens[i] >= k) {
            global.s2_citizens[i] -= k;
            global.s2_citizens[i+1] += k;

            // If we reach a bankrupt person, 
            // give him the money
            if (global.s2_citizens[i+1] == k) {
                return;
            }
        }
    }
	printf("Final i=%d\n",i);

    for (j=0; j < length_diff; j++) {
        // Propagate forward s2
        if (global.s2_citizens[i+j] >= k) {
            global.s2_citizens[i+j] -= k;
            global.s2_citizens[i+j+1] += k;

            printf("%d:0x%x\n", i+j+1,global.s2_citizens[i+j+1]);
            // If we reach a bankrupt person, 
            // give him the money
            if (global.s2_citizens[i+j+1] == k) {
                return;
            }
        }
    }

}


void propagate_backward(int k) {
    // Somewhere total_length will be used :), with some buffer or heap
    int length_diff = L2 - L1;
    int i,j;

    for (i=0; i < L1 - 1; i++) {
        // At random, swap money to keep circulation of money 
        if (rand() % 2) {
            int tmp = global.s1_citizens[i];
            global.s1_citizens[i] = global.s2_citizens[i];
            global.s2_citizens[i] = tmp;
        } 

        // Propagate forward s1
        if (global.s1_citizens[i+1] >= k) {
            global.s1_citizens[i+1] -= k;
            global.s1_citizens[i] += k;
            
            // If we reach a bankrupt person,
            // give him the money
            if (global.s1_citizens[i] == k) {
                return;
            }
        }

        // Propagate forward s2
        if (global.s2_citizens[i+1] >= k) {
            global.s2_citizens[i+1] -= k;
            global.s2_citizens[i] += k;

            // If we reach a bankrupt person,
            // give him the money
            if (global.s2_citizens[i] == k) {
                return;
            }
        }
    }

    for (j=0; j < length_diff; j++) {
        // Propagate forward s2
        if (global.s2_citizens[i+j+1] >= k) {
            global.s2_citizens[i+j+1] -= k;
            global.s2_citizens[i+j] += k;
            
            printf("%d:0x%x\n", i+j+1,global.s2_citizens[i+j+1]);
            // If we reach a bankrupt person,
            // give him the money
            if (global.s2_citizens[i+j] == k) {
                return;
            }

        }
    }
}


// Welcome Message
void greeting() {
    printf("Welcome to the Trump gold sharing simulator!\n");
    printf("The simulator tries to simulate gold transfering between two "
           "states. \n");
    printf("Enter the name of the first state:");
    if (fgets (global.s1_name, STATE_SIZE_LEN, stdin) == NULL) {
        printf("Failed to read name\n");
        exit(-69);
    }
    global.s1_name[strcspn(global.s1_name, "\n")] = 0;


    printf("Enter the name of the second state:");
    if (fgets (global.s2_name, STATE_SIZE_LEN, stdin) == NULL) {
        printf("Failed to read name\n");
        exit(-69);
    }
    global.s2_name[strcspn(global.s1_name, "\n")] = 0;
}

void init_states_wrap () {
    printf("Enter the amount to set the states in: ");

    int k = get_number();

    if (k < 0) {
        printf("ERR: Negative Number\n");
        return;
    }

    init_states(k);
}

typedef enum {
    FORWARD,
    BACKWARD
} direction_t;

void propagate_wrap (direction_t d) {
    printf("Enter the amount to propagate: ");
    int k = get_number();

    if (k < 0) {
        printf("ERR: Negative Number\n");
        return;
    }
    
    switch(d) {
        case FORWARD: propagate_forward(k); break;
        case BACKWARD: propagate_backward(k); break;
        default:
            printf("ERR: Invalid Direction\n"); 
    }
}


void remove_announcement () {
    free(global.announcement);
    global.announcement = NULL;
    global.announcement_length = 0;
}


#define ANNOUNCEMENT_MAX_LEN 1024
void create_announcement () {
    int len;


    printf("Enter the length of your announcement: ");
    len = get_number();

    if (len <= 0 || len > 1024) {
        printf("ERR: Invalid Length\n");
        return;
    }

    if (global.announcement_length < len) {

        // Use new buffer
        remove_announcement ();
        global.announcement = malloc (len);

        //printf("Malloced %p\n", global.announcement);
        if (global.announcement == NULL) {
            printf("ERR: Failed to allocate announcement\n");
            return;
        }
        global.announcement_length = len;
    }

    // Re-use available buffer
    if (fgets (global.announcement, len, stdin) == NULL) {
        printf("Failed to read announcement\n");
        exit(-69);
    }
    global.announcement[strcspn(global.announcement, "\n")] = 0;

}
void menu() {
    // print stuff here
    int choice;
    while (1) {
        printf("Menu:\n"\
               "0. Print state \n"
               "1. Initialize state \n"
               "2. Simulate Propagate Forward \n"
               "3. Simulate Propagate Backward \n"
               "4. Create Announcement \n"
               "5. Remove Announcement \n"
               "6. Quit \n"
               "\n"
              );
        
        printf("Enter Your Choice: ");
        choice = get_number();

        switch(choice) {
            case 0: print_states(); break;
            case 1: init_states_wrap(); break;
            case 2: propagate_wrap(FORWARD); break;
            case 3: propagate_wrap(BACKWARD); break;
            case 4: create_announcement(); break;
            case 5: remove_announcement(); break;
            case 6: exit(0);       break;
            default: 
                printf("Invalid Option!\n");
        }
        /*
        int i;
        printf("OUTPUT S1:\n");
        for (i=0; i<512; i++) printf("%c", global.s1_name[i]);
        printf("END S1:\n");

        printf("OUTPUT S2:\n");
        for (i=0; i<512; i++) printf("%c", global.s2_name[i]);
        printf("END S2:\n");
        */

    }

    return;
}

int main (){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    // First state must be smaller
    if (!(sizeof(global.s2_citizens) >= sizeof(global.s1_citizens))) {
        return -1;
    }

    global.announcement = NULL;
    global.announcement_length = 0;
    greeting();
    menu();
    return 0;

    /*
    printf("OUTPUT S1:\n");
    for (i=0; i<512; i++) printf("%c", global.s1_name[i]);
    printf("END S1:\n");

    printf("OUTPUT S2:\n");
    for (i=0; i<512; i++) printf("%c", global.s2_name[i]);
    printf("END S2:\n");
    */
}

