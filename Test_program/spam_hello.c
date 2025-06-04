#include <stdio.h>
#include <unistd.h>

int main() {
    char dog[] = "   / \\__\n  (    @\\___\n  /         O\n /   (_____/\n/_____/   U";
    char cat[] = "  /\\_/\\\n ( o.o )\n  > ^ <";
    char status = 0;
    while(1)
    {
        if(status)
        {
            printf("%s\n Hello Process Manager!\n", dog);
        }
        else
        {
            printf("%s\n Hello Process Manager!\n", cat);
        }
        status = 1 - status;

        // sleep 300ms
        usleep(300000);
    }
}
