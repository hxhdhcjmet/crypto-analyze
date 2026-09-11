#include <stdio.h>
#include <stdint.h>
#include <omp.h>


#define STATES 17576
#define TEST 30000000
#define LEN 6


#define THREADS 8


unsigned char table[26][STATES];


int rotor[3][26];
int invrotor[3][26];
int reflector[26];
int K1[26];



static inline unsigned char encrypt_once(
        int state,
        int x
)
{

    int fast = state % 26;
    int mid  = (state / 26)%26;
    int slow = state / 676;


    int y;


    x=K1[x];


    y=(x+fast)%26;
    x=rotor[0][y];
    x=(x-fast+26)%26;


    y=(x+mid)%26;
    x=rotor[1][y];
    x=(x-mid+26)%26;


    y=(x+slow)%26;
    x=rotor[2][y];
    x=(x-slow+26)%26;



    x=reflector[x];


    y=(x+slow)%26;
    x=invrotor[2][y];
    x=(x-slow+26)%26;


    y=(x+mid)%26;
    x=invrotor[1][y];
    x=(x-mid+26)%26;


    y=(x+fast)%26;
    x=invrotor[0][y];
    x=(x-fast+26)%26;


    return K1[x];

}



void build_table()
{

#pragma omp parallel for
    for(int s=0;s<STATES;s++)
    {

        for(int c=0;c<26;c++)
        {

            table[c][s]
                =encrypt_once(s,c);

        }

    }

}





int main()
{

    int S[26]={
        21,18,6,3,4,5,2,7,
        8,9,10,11,13,12,23,
        15,16,17,1,19,20,0,
        22,14,24,25
    };


    int QUICK[26]={
        7,19,3,22,11,25,14,1,
        16,23,8,20,5,17,12,9,
        24,6,15,2,18,21,4,13,
        10,0
    };


    int MID[26]={
        0,10,4,2,8,1,18,20,
        22,19,13,6,17,5,9,3,
        24,14,12,25,21,11,7,16,
        15,23
    };


    int SLOW[26]={
        0,23,5,12,18,3,21,9,
        14,1,17,6,24,11,20,4,
        15,8,22,7,19,13,2,16,
        10,25
    };


    int T[26]={
        5,3,7,1,8,0,9,2,
        4,6,12,14,10,15,11,
        13,18,20,16,21,17,19,
        24,25,22,23
    };



    for(int i=0;i<26;i++)
    {

        rotor[0][i]=QUICK[i];
        rotor[1][i]=MID[i];
        rotor[2][i]=SLOW[i];

        reflector[i]=T[i];

        K1[i]=S[i];

    }



    for(int r=0;r<3;r++)
    {
        for(int i=0;i<26;i++)
        {
            invrotor[r][rotor[r][i]]=i;
        }
    }



    printf("building table...\n");

    build_table();



    omp_set_num_threads(THREADS);



    double start=omp_get_wtime();



    uint64_t total=0;



#pragma omp parallel
{

    uint64_t sum=0;


#pragma omp for
    for(int i=0;i<TEST;i++)
    {

        unsigned int state=i%STATES;


        int x0=i%26;
        int x1=(i+1)%26;
        int x2=(i+2)%26;
        int x3=(i+3)%26;
        int x4=(i+4)%26;
        int x5=(i+5)%26;



        sum+=table[x0][state++];

        if(state==STATES)
            state=0;


        sum+=table[x1][state++];

        if(state==STATES)
            state=0;


        sum+=table[x2][state++];

        if(state==STATES)
            state=0;


        sum+=table[x3][state++];

        if(state==STATES)
            state=0;


        sum+=table[x4][state++];

        if(state==STATES)
            state=0;


        sum+=table[x5][state++];

    }


#pragma omp atomic
    total+=sum;

}



double end=omp_get_wtime();



double t=end-start;



printf(
"time %.6f s\n",
t
);



printf(
"encrypt %.2f M/s\n",
TEST/t/1000000
);



printf(
"char %.2f M/s\n",
TEST*LEN/t/1000000
);



printf(
"sum=%llu\n",
total
);



printf(
"threads=%d\n",
omp_get_max_threads()
);


}