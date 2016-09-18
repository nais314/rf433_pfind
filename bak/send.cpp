#include <cstdlib>
#include <cstdio>
#include <cstdint> // uint8_t
#include <iostream>


#include <wiringPi.h>
#include <vector>

#include <fstream>
#include <string>

using namespace std;



int main(int argc, char *argv[]) {
    int PIN = atoi(argv[1]);
    int Plen = atoi(argv[2]);
    string in_filename = argv[3];
    
    if(!PIN) {PIN = 21; };
    if(!Plen) {Plen = 100; };
    //if(in_filename == "") { in_filename = "0441-1-off_n.csv"; };
    
    if (wiringPiSetupGpio () == -1) return 1;
    
    pinMode(PIN, OUTPUT);
    
    //.........................
    
    vector<uint8_t> vec;
    ifstream file ( in_filename ); // declare file stream: http://www.cplusplus.com/reference/iostream/ifstream/
    string value;
    unsigned int numread = 0;
    while ( file.good() )
    {
         getline ( file, value, ',' ); // read a string until next comma: http://www.cplusplus.com/reference/string/getline/
         //cout  << string( value, 0, value.length()-2 ) << ','; // display value removing the first and the last character from it
         vec.push_back( (stoi(value) == 0)? 1 : stoi(value) );
         numread += 1;
    };
    
    cout  << "\n\n";
    
    uint8_t raw_rf_code[numread];
    for(unsigned int i = 0; i < numread; i++){
        raw_rf_code[i] = vec[i];
        cout << to_string( raw_rf_code[i] ) << ',';
    };
      
    cout  << "\n\n";

    
    
    digitalWrite(PIN, LOW);
    digitalWrite(PIN, HIGH);    delayMicroseconds( Plen * 19 );
    digitalWrite(PIN, LOW);   
    //........
    //for(short rep = 0; rep < 4; rep++)
        //for (int ii = Plen; ii < Plen + 30; ii+=5 ){
        for (int ii = Plen; ii <= Plen + 50; ii+=10 ){
            //cout << to_string(ii) << '\n';
            for(unsigned int i = 0; i < numread; i++){
                digitalWrite(PIN, HIGH);
                delayMicroseconds( ii * (raw_rf_code[i] ) );
                i++;
                digitalWrite(PIN, LOW);
                delayMicroseconds( ii * (raw_rf_code[i] ) );
                
            };
        };
    digitalWrite(PIN, LOW);
    digitalWrite(PIN, HIGH);    delayMicroseconds( Plen * 19 );
    digitalWrite(PIN, LOW); 
 
 
    //_________________________
 /*   
    cout << "send from list \n";
    
    uint code2[] = {
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        3,1,
        1,4,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        1,4,
        1,4,
        1,43,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        3,1,
        1,4,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        1,4,
        1,4,
        1,43,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        1,9,
        1,4,
        1,4,
        3,1,
        3,1,
        3,1,
        1,4,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,6,
        1,4,
        1,43,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        3,1,
        1,4,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        1,4,
        1,4,
        1,43,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        3,1,
        1,4,
        3,1,
        1,4,
        1,4,
        1,4,
        1,4,
        3,1,
        3,1,
        1,4,
        1,4,
        1,43
        };
        
        for (int ii = 80; ii <= 150; ii+=10 ){
            cout << to_string(ii) << '\n';
            for(unsigned int i = 0; i < 100; i++){
                digitalWrite(PIN, HIGH);
                delayMicroseconds( ii * (code2[i] ) );
                i++;
                digitalWrite(PIN, LOW);
                delayMicroseconds( ii * (code2[i] ) );
                
            };
        };
    digitalWrite(PIN, LOW);
    
    
    //.........................
    
    unsigned int code = 0;
    unsigned int repeat = 0;
    
    for(unsigned int i = 0; i < vec.size(); i++){
        if (vec[i] > 40 && vec[i] < 60 ){
            repeat++;
            if (repeat > 1) break;
            continue;
            }
        
        if (repeat == 1)
        if (vec[i] < 2){
            code = code << 1;
        }else{
            code += 1;
            code = code << 1;   
        }
    };
    
    cout << to_string(code) << '\n';
    //....................
    
    
    code = 0;
    repeat = 0;
    for(unsigned int i = 0; i < vec.size(); i++){
        if (vec[i] > 40 && vec[i] < 60 ){
            repeat++;
            if (repeat > 1) break;
            continue;
            }
        
        if (repeat == 1){
            if (vec[i] < 2 && vec[i+1] > 2){
                code += 1;
                code = code << 1;
            }else{
                code = code << 1;   
            }
        i++;}
    };
    
    cout << to_string(code) << '\n';    
    
cout << "-= THE END =-\n";
* 
*/
}//END
