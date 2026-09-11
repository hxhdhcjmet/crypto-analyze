#include <stdio.h>
#include <stdlib.h>
#include <time.h>


#define ALPHA 26


typedef struct{

    int rotor[3][26];

    int reflector[26];

    int offset[3];

    int count;

} Enigma;



void setRotor(
        Enigma *e,
        int K2[3]
)
{
    for(int i=0;i<3;i++)
        e->offset[i]=K2[i];

    e->count=0;
}



void updateRotor(Enigma *e)
{
    e->count++;

    e->offset[0]++;

    if(e->offset[0]==26)
    {
        e->offset[0]=0;

        e->offset[1]++;

        if(e->offset[1]==26)
        {
            e->offset[1]=0;

            e->offset[2]++;

            if(e->offset[2]==26)
                e->offset[2]=0;
        }
    }
}



/*
    正向经过转子

    Python:
    Rotor_right.index(Rotor_left[m])

    这里提前求逆表
*/
int passRotorForward(
        Enigma *e,
        int r,
        int x
)
{

    int in=(x+e->offset[r])%26;

    int out=e->rotor[r][in];

    return (out-e->offset[r]+26)%26;

}


/*
    反向
*/
int passRotorBackward(
        Enigma *e,
        int r,
        int x
)
{

    int target=(x+e->offset[r])%26;


    for(int i=0;i<26;i++)
    {
        if(e->rotor[r][i]==target)
        {
            return (i-e->offset[r]+26)%26;
        }
    }


    return -1;
}



int encrypt_char(
        Enigma *e,
        int m,
        int K1[26]
)
{

    // 插线板
    m=K1[m];


    // 正向
    for(int i=0;i<3;i++)
        m=passRotorForward(e,i,m);


    // 反射
    m=e->reflector[m];


    // 反向
    for(int i=2;i>=0;i--)
        m=passRotorBackward(e,i,m);


    // 插线板
    m=K1[m];


    updateRotor(e);


    return m;
}



void encrypt(
        Enigma *e,
        char *plain,
        char *cipher,
        int K1[26]
)
{

    int i=0;

    while(plain[i])
    {

        int x=plain[i]-'A';

        cipher[i]=encrypt_char(
                e,
                x,
                K1
        )+'A';


        i++;
    }

    cipher[i]=0;
}




void init(
        Enigma *e,
        int QUICK[26],
        int MID[26],
        int SLOW[26],
        int T[26]
)
{

    for(int i=0;i<26;i++)
    {
        e->rotor[0][i]=QUICK[i];
        e->rotor[1][i]=MID[i];
        e->rotor[2][i]=SLOW[i];

        e->reflector[i]=T[i];
    }


    for(int i=0;i<3;i++)
        e->offset[i]=0;

}



char randomChar()
{
    return 'A'+rand()%26;
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


    int K2[3]={8,9,10};



    Enigma e;


    init(
        &e,
        QUICK,
        MID,
        SLOW,
        T
    );


    setRotor(&e,K2);



    srand(202698);


    char plain[7];
    char cipher[7];


    clock_t start=clock();


    int n=1000000;


    for(int i=0;i<n;i++)
    {

        for(int j=0;j<6;j++)
            plain[j]=randomChar();

        plain[6]=0;


        encrypt(
            &e,
            plain,
            cipher,
            S
        );

    }


    clock_t end=clock();



    printf(
        "%d encrypt cost %.4f s\n",
        n,
        (double)(end-start)/CLOCKS_PER_SEC
    );


    printf(
        "speed %.1f encrypt/s\n",
        n/
        ((double)(end-start)/CLOCKS_PER_SEC)
    );

}