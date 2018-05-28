#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_LIST_SZ 256

int main(void)
{
    double unit = 156.25e-6; // convert the time tagger scale of the time tagger to us
    double responseT = 1.12; // time for AOM to respond to the pulse [us] 
    // Slot6 (2x200MHz): 1.12us
    double initT = 0 + responseT; // time to start data acquisition [us]
    double endT = 1000 + responseT; // time to start data acquisition [us]

    int order;
    char *tList = malloc (MAX_LIST_SZ);
    int timeList[25]; // Array to store the pump time list
    int listLen = 0;
    char fileNum[10];
    char outDirNum[5];
    char outDirName[10];
    int num;
    int i, j;
    printf("Pump time list (comma separated values) ");
    // scanf("%99[^n]",tList);
    fgets(tList, MAX_LIST_SZ, stdin);
    printf("Repeat number? ");
    scanf("%d", &num);
    printf("Measurement order?   1. Time scan -> Repeat   2. Repeat -> Time Scan\n");
    scanf("%d", &order);
    // printf("%s\n",tList);

    // Make comma separated values into array
    char *pt;
    pt = strtok (tList,",");
    while(pt != NULL) {
        int a = atoi(pt);
        timeList[listLen] = a;
        listLen++;
        pt = strtok(NULL, ",");
    }
    printf("Number of pump times: %d\n",listLen);

//    static const char filename[] = "tags.txt";
    static const char filename[] = "../tags.txt";
    FILE *file = fopen(filename, "r");
    sprintf(outDirNum, "%03d", num);
    strcpy(outDirName,"../rpn");
    strcat(outDirName,outDirNum);

    mkdir(outDirName);
    char fileList[listLen][25];
    FILE** files = malloc(sizeof(FILE*) * listLen);
    for (i=0; i<listLen; i++) {
        sprintf(fileNum, "%03d", timeList[i]);
        strcpy(fileList[i],outDirName);
//        strcat(fileList[i], "\\release_");
        strcat(fileList[i], "\\pump_");
        strcat(fileList[i], fileNum);
        strcat(fileList[i], "us.txt");
//        strcat(fileList[i], "ms.txt");
        printf("%s\n",fileList[i]);
        files[i] = fopen(fileList[i], "w");
    }
    free(tList);

    double refT = 0;
    double timeSum[listLen];
    int pulseNum = 0;
    int photonNum[listLen];
    for (j=0; j<listLen; j++) { timeSum[j]=0.0; photonNum[j]=0; }
    
    i = 0; j = 0;

    if (file != NULL )
    {
        char line[BUFSIZ];
        while ( fgets(line, sizeof line, file) != NULL )
        {
            int ch;
            double t;
            sscanf(line, "%d\t%lf", &ch, &t);
            if (order == 1) {
                if (ch == 2) {
                    refT = t;  pulseNum += 1;
                    j++;  if (j==listLen+1) { j=1; }
                }
                else if (ch == 1) {
                    t = unit*(t-refT);
                    if ((t>initT) & (t<endT)) {
                        if(pulseNum > 0) { fprintf(files[j-1], "%.4f\n", t-responseT); }
                        photonNum[j-1] += 1; timeSum[j-1] += (t-responseT);            
                        if(t < responseT) { printf("Detected before time 0.\n"); }
                    }
                }
            }
            else if (order == 2) {
                if (ch == 2) {
                    refT = t;  pulseNum += 1;
                    i++;  if (i==num+1) { i=1; j++; }
                }
                else if (ch == 1) {
                    t = unit*(t-refT);
                    if ((t>initT) & (t<endT)) {
                        if(pulseNum > 0) { fprintf(files[j], "%.4f\n", t-responseT); }
                        photonNum[j] += 1; timeSum[j] += (t-responseT);            
                        if(t < responseT) { printf("Detected before time 0.\n"); }
                    }
                }
            }
        }

        if(pulseNum == (listLen * num)) { printf("Data OK!\n"); }
        else { printf("Problem found!\n"); }

        FILE *sfile = fopen("output\\summary.txt", "w");
        for (j=0; j<listLen; j++) {
            fprintf(sfile,"Pump **%d us**\n", timeList[j]);
            fprintf(sfile,"Pulse number: %d\n",num);
            fprintf(sfile,"Photon number: %d\n",photonNum[j]);
            fprintf(sfile,"%.4f photons per pulse\n",(double)photonNum[j]/num);
            fprintf(sfile,"Average time: %.4f us\n\n",(double)timeSum[j]/photonNum[j]);
            fclose(files[j]);
        }
        // printf("Pulse number: %d\n",pulseNum);
        // printf("Photon number: %d\n",photonNum);
        // printf("%.4f photons per pulse\n",(double)photonNum/pulseNum);
        // printf("Average time: %.4f us\n",(double)timeSum/photonNum);
    }
    // for (i=0; i<listLen; i++) { fclose(files[i]); }
    fclose(file);
    free(files);
}
